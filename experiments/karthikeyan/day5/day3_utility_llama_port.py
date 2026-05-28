"""day3_utility_llama_port.py

Port of Day 3 Gemini utility to Groq (llama-3.1-8b-instant).

Features:
- Uses `groq` SDK and `dotenv` for credentials
- Preserves prompt-chaining workflow
- Argparse command-line interface
- JSON structured output saved to file
- Logging and error handling
- Latency and token usage measurement per chain step

Usage:
    python day3_utility_llama_port.py --prompt "Explain X" --output result.json

"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from groq import Groq


logger = logging.getLogger("day3_port")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


@dataclass
class StepResult:
    name: str
    prompt: str
    response: str
    latency_ms: float
    tokens: Optional[int]


def load_api_key() -> str:
    load_dotenv()
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise EnvironmentError("GROQ_API_KEY must be set in .env")
    return key


def create_groq_client(api_key: str) -> Groq:
    return Groq(api_key=api_key)


def call_groq_chat(groq_client: Groq, prompt: str, model: str = "llama-3.1-8b-instant", **kwargs) -> Dict[str, Any]:
    """Call Groq chat completions and return parsed info.

    Returns a dict with keys: text, latency_ms, tokens (if available), raw
    """
    start = time.perf_counter()
    try:
        response = groq_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs,
        )
    except Exception:
        logger.exception("Groq API call failed")
        raise
    latency = (time.perf_counter() - start) * 1000.0

    # Try to extract text and token usage in a robust way
    text = ""
    tokens: Optional[int] = None

    try:
        # support both attribute-style and dict-style responses
        if hasattr(response, "choices") and response.choices:
            choice = response.choices[0]
            # message content
            msg = getattr(choice, "message", None) or choice.get("message") if isinstance(choice, dict) else None
            if msg:
                text = getattr(msg, "content", None) or msg.get("content", "")
            else:
                # older/net-newer response shapes
                text = getattr(choice, "text", None) or choice.get("text", "")
        elif isinstance(response, dict) and response.get("choices"):
            text = response["choices"][0].get("message", {}).get("content", response["choices"][0].get("text", ""))

        # token usage
        if hasattr(response, "usage"):
            usage = getattr(response, "usage")
            tokens = getattr(usage, "total_tokens", None) or usage.get("total_tokens") if isinstance(usage, dict) else None
        elif isinstance(response, dict) and response.get("usage"):
            tokens = response["usage"].get("total_tokens")
    except Exception:
        logger.debug("Failed to parse response structure for text/usage", exc_info=True)

    return {"text": (text or "").strip(), "latency_ms": latency, "tokens": tokens, "raw": response}


def default_chain() -> List[Dict[str, Any]]:
    """Return a default prompt chain definition.

    Each chain step is a dict with keys: name, template
    The template may include `{input}` to be filled with previous step output.
    """
    return [
        {
            "name": "clarify",
            "template": (
                "You are an assistant. Restate the user's input clearly and identify the goal in one sentence.\n\n"
                "User input: {input}"
            ),
        },
        {
            "name": "expand",
            "template": (
                "Expand the clarified goal into a detailed explanation with examples and next steps.\n\n"
                "Clarified: {input}"
            ),
        },
        {
            "name": "extract_json",
            "template": (
                "Extract key facts and structure the result as JSON. Use keys: summary, actions, key_points.\n\n"
                "Text: {input}"
            ),
        },
    ]


def run_chain(groq_client: Groq, chain: List[Dict[str, Any]], initial_input: str, model: str, max_tokens: int) -> List[StepResult]:
    results: List[StepResult] = []
    current_input = initial_input

    for step in chain:
        name = step.get("name", "step")
        template = step.get("template", "{input}")
        prompt = template.format(input=current_input)

        logger.info("Running step '%s'", name)

        try:
            resp = call_groq_chat(groq_client, prompt, model=model, max_tokens=max_tokens, temperature=0)
        except Exception as exc:
            logger.error("Step '%s' failed: %s", name, exc)
            raise

        text = resp.get("text", "")
        latency = resp.get("latency_ms", 0.0)
        tokens = resp.get("tokens")

        # Print required info
        print(f"Step: {name}")
        print(f"Response: {text}\n")
        print(f"Latency: {latency:.2f} ms")
        print(f"Tokens: {tokens if tokens is not None else 'N/A'}")
        print("-" * 60)

        results.append(StepResult(name=name, prompt=prompt, response=text, latency_ms=latency, tokens=tokens))

        # For chaining, set next input to the response text
        current_input = text

    return results


def save_json(output_path: Path, payload: Dict[str, Any]) -> None:
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info("Saved structured result to %s", output_path)


def build_structured_result(prompt: str, chain_results: List[StepResult], start_time: float, end_time: float) -> Dict[str, Any]:
    return {
        "input_prompt": prompt,
        "started_at": start_time,
        "finished_at": end_time,
        "duration_ms": (end_time - start_time) * 1000.0,
        "steps": [asdict(s) for s in chain_results],
    }


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Day 3 utility ported to Groq Llama")
    # accept --text as an alias to be compatible with previous runs
    p.add_argument("--prompt", "--text", dest="prompt", type=str, help="Input prompt or text to process", required=True)
    p.add_argument("--output", type=str, help="JSON output file", default="day3_result.json")
    p.add_argument("--model", type=str, help="Groq model to use", default="llama-3.1-8b-instant")
    p.add_argument("--max-tokens", type=int, help="max tokens per step", default=512)
    p.add_argument("--verbose", action="store_true", help="Enable debug logging")
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    try:
        api_key = load_api_key()
        groq_client = create_groq_client(api_key)
    except Exception as exc:
        logger.error("Failed to load Groq API key: %s", exc)
        return 2

    chain = default_chain()

    start_time = time.time()
    try:
        chain_results = run_chain(groq_client, chain, args.prompt, model=args.model, max_tokens=args.max_tokens)
    except Exception as exc:
        logger.error("Chain execution failed: %s", exc)
        return 3
    end_time = time.time()

    structured = build_structured_result(args.prompt, chain_results, start_time, end_time)

    try:
        save_json(Path(args.output), structured)
    except Exception:
        logger.exception("Failed to save JSON output")
        return 4

    # Pretty-print summary
    print("\nFinal structured result saved to:", args.output)
    print(json.dumps(structured, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    sys.exit(main())
