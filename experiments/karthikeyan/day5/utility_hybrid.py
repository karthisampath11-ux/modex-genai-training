import os
import time
import argparse
from typing import Dict, Any, List, Tuple

from dotenv import load_dotenv
from groq import Groq

try:
    import google.generativeai as genai
except ImportError:
    genai = None

# In-memory cache for model calls.
CACHE: Dict[Tuple[str, str, int], Dict[str, Any]] = {}


def load_api_keys() -> Dict[str, str]:
    """Load Gemini and Groq API keys from .env."""
    load_dotenv()
    gemini_key = os.getenv("GEMINI_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")

    if not gemini_key:
        raise ValueError("GEMINI_API_KEY is missing in .env")
    if not groq_key:
        raise ValueError("GROQ_API_KEY is missing in .env")

    return {"gemini": gemini_key, "groq": groq_key}


def create_clients(api_keys: Dict[str, str]) -> Groq:
    """Initialize both SDK clients."""
    if genai is None:
        raise ImportError(
            "google.generativeai is required for Gemini support"
        )

    genai.configure(api_key=api_keys["gemini"])
    groq_client = Groq(api_key=api_keys["groq"])
    return groq_client


def ask_gemini(model: str, prompt: str, max_tokens: int = 500) -> Dict[str, Any]:
    """Call Gemini and return a normalized result dictionary."""
    start = time.perf_counter()
    try:
        gemini_model = genai.GenerativeModel(model)
        response = gemini_model.generate_content(
            prompt=prompt,
            max_output_tokens=max_tokens,
        )
        latency_ms = (time.perf_counter() - start) * 1000
        return {
            "model": model,
            "prompt": prompt,
            "response": getattr(response, "text", "").strip(),
            "latency_ms": latency_ms,
            "error": "",
            "cached": False,
        }
    except Exception as error:
        latency_ms = (time.perf_counter() - start) * 1000
        return {
            "model": model,
            "prompt": prompt,
            "response": "",
            "latency_ms": latency_ms,
            "error": str(error),
            "cached": False,
        }


def ask_groq(model: str, prompt: str, max_tokens: int = 500, groq_client: Groq = None) -> Dict[str, Any]:
    """Call Groq Llama and return a normalized result dictionary."""
    start = time.perf_counter()
    try:
        response = groq_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0,
        )
        latency_ms = (time.perf_counter() - start) * 1000
        return {
            "model": model,
            "prompt": prompt,
            "response": response.choices[0].message.content.strip(),
            "latency_ms": latency_ms,
            "error": "",
            "cached": False,
        }
    except Exception as error:
        latency_ms = (time.perf_counter() - start) * 1000
        return {
            "model": model,
            "prompt": prompt,
            "response": "",
            "latency_ms": latency_ms,
            "error": str(error),
            "cached": False,
        }


def ask(
    model: str,
    prompt: str,
    max_tokens: int = 500,
    groq_client: Groq = None,
) -> Dict[str, Any]:
    """Route the call to the correct SDK based on the model prefix."""
    cache_key = (model, prompt, max_tokens)
    if cache_key in CACHE:
        cached_result = CACHE[cache_key].copy()
        cached_result["cached"] = True
        return cached_result

    if model.startswith("gemini-"):
        result = ask_gemini(model, prompt, max_tokens)
    elif model.startswith("llama-"):
        result = ask_groq(model, prompt, max_tokens, groq_client=groq_client)
    else:
        raise ValueError(f"Unsupported model prefix for model: {model}")

    CACHE[cache_key] = result.copy()
    return result


def build_chain(input_text: str) -> List[Dict[str, Any]]:
    """Define chain steps and assign the model explicitly for each."""
    return [
        {
            "name": "summarization",
            "model": "llama-3.1-8b-instant",
            "prompt_template": (
                "Summarize the following text in three sentences:\n\n" "{input_text}"
            ),
            "description": "Summarize the original input.",
        },
        {
            "name": "action_items",
            "model": "gemini-2.5-flash-lite",
            "prompt_template": (
                "Based on the summary below, write a short list of three action items with bullets:\n\n" "{summary}"
            ),
            "description": "Create structured action items from the summary.",
        },
    ]


def run_chain(input_text: str, groq_client: Groq) -> Dict[str, Any]:
    """Execute the hybrid chain and collect timing and call counts."""
    steps = build_chain(input_text)
    results = []
    total_latency = 0.0
    gemini_calls = 0
    groq_calls = 0
    previous_summary = ""

    for step in steps:
        prompt = step["prompt_template"].format(
            input_text=input_text,
            summary=previous_summary,
        )
        result = ask(
            model=step["model"],
            prompt=prompt,
            max_tokens=500,
            groq_client=groq_client,
        )

        if not result.get("cached"):
            if step["model"].startswith("gemini-"):
                gemini_calls += 1
            elif step["model"].startswith("llama-"):
                groq_calls += 1

        results.append({
            "step_name": step["name"],
            "model": step["model"],
            "prompt": prompt,
            "response": result["response"],
            "error": result["error"],
            "latency_ms": result["latency_ms"],
            "cached": result.get("cached", False),
        })

        total_latency += result["latency_ms"]
        if result["response"] and step["name"] == "summarization":
            previous_summary = result["response"]

    return {
        "results": results,
        "total_latency_ms": total_latency,
        "gemini_calls": gemini_calls,
        "groq_calls": groq_calls,
    }


def format_step(step_result: Dict[str, Any]) -> str:
    """Create readable text for a single chain step."""
    lines = [
        f"Step: {step_result['step_name']}",
        f"Model: {step_result['model']}",
        f"Latency: {step_result['latency_ms']:.2f} ms",
        f"Cached: {step_result['cached']}",
    ]
    if step_result["error"]:
        lines.append(f"Error: {step_result['error']}")
    else:
        lines.append("Response:")
        lines.append(step_result["response"])
    return "\n".join(lines)


def main() -> int:
    """Run the hybrid utility from the command line."""
    parser = argparse.ArgumentParser(
        description="Hybrid LLM utility using Gemini and Groq models in a two-step chain."
    )
    parser.add_argument(
        "--text",
        type=str,
        default=(
            "The team needs to align on launch priorities, simplify the onboarding "
            "process, and improve cross-team communication by the end of the month."
        ),
        help="Input text to summarize and generate action items from.",
    )
    args = parser.parse_args()

    try:
        api_keys = load_api_keys()
        groq_client = create_clients(api_keys)

        summary = run_chain(args.text, groq_client)

        for step_result in summary["results"]:
            print("=" * 80)
            print(format_step(step_result))
            print()

        print("=" * 80)
        print(f"Total latency: {summary['total_latency_ms']:.2f} ms")
        print(f"Total Gemini calls: {summary['gemini_calls']}")
        print(f"Total Groq calls: {summary['groq_calls']}")
        print("=" * 80)

        return 0
    except Exception as error:
        print(f"Error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
