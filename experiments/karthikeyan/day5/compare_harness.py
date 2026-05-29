import os
import time
import textwrap
from dataclasses import dataclass
from typing import List, Dict

from dotenv import load_dotenv
from groq import Groq

try:
    import google.generativeai as genai
except ImportError:
    genai = None


# --------------------------------------------------
# RESULT MODEL
# --------------------------------------------------

@dataclass
class ModelResult:
    model_name: str
    prompt: str
    response: str
    latency_ms: float
    error: str = ""


# --------------------------------------------------
# LOAD API KEYS
# --------------------------------------------------

def load_api_keys() -> Dict[str, str]:

    load_dotenv()

    gemini_key = os.getenv("GEMINI_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")

    if not gemini_key:
        raise ValueError("GEMINI_API_KEY is missing in .env")

    if not groq_key:
        raise ValueError("GROQ_API_KEY is missing in .env")

    return {
        "gemini": gemini_key,
        "groq": groq_key,
    }


# --------------------------------------------------
# GEMINI SETUP
# --------------------------------------------------

def create_gemini_client(api_key: str):

    if genai is None:
        raise ImportError(
            "google.generativeai package is not installed"
        )

    genai.configure(api_key=api_key)

    return genai


# --------------------------------------------------
# GROQ SETUP
# --------------------------------------------------

def create_groq_client(api_key: str) -> Groq:

    return Groq(api_key=api_key)


# --------------------------------------------------
# GEMINI CALL
# --------------------------------------------------

def ask_gemini(prompt: str) -> ModelResult:

    start_time = time.perf_counter()

    try:

        model = genai.GenerativeModel(
            "gemini-2.5-flash-lite"
        )

        response = model.generate_content(prompt)

        end_time = time.perf_counter()

        latency_ms = (end_time - start_time) * 1000

        return ModelResult(
            model_name="gemini-2.5-flash-lite",
            prompt=prompt,
            response=response.text.strip(),
            latency_ms=latency_ms,
        )

    except Exception as error:

        end_time = time.perf_counter()

        latency_ms = (end_time - start_time) * 1000

        return ModelResult(
            model_name="gemini-2.5-flash-lite",
            prompt=prompt,
            response="",
            latency_ms=latency_ms,
            error=str(error),
        )


# --------------------------------------------------
# GROQ LLAMA CALL
# --------------------------------------------------

def ask_groq(client: Groq, prompt: str) -> ModelResult:

    start_time = time.perf_counter()

    try:

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0
        )

        end_time = time.perf_counter()

        latency_ms = (end_time - start_time) * 1000

        return ModelResult(
            model_name="llama-3.1-8b-instant",
            prompt=prompt,
            response=response.choices[0].message.content.strip(),
            latency_ms=latency_ms,
        )

    except Exception as error:

        end_time = time.perf_counter()

        latency_ms = (end_time - start_time) * 1000

        return ModelResult(
            model_name="llama-3.1-8b-instant",
            prompt=prompt,
            response="",
            latency_ms=latency_ms,
            error=str(error),
        )


# --------------------------------------------------
# PROMPTS
# --------------------------------------------------

def build_prompts() -> List[str]:

    return [

        "Explain artificial intelligence in simple terms.",

        "Summarize why cybersecurity is important for small businesses.",

        "List three ways AI can help doctors and nurses.",

        "Write a short friendly email inviting a team to a brainstorming meeting.",

        "Describe one green technology that helps save energy."
    ]


# --------------------------------------------------
# COMPARE PROMPTS
# --------------------------------------------------

def compare_prompts(
    prompts: List[str],
    gemini_client,
    groq_client
):

    comparisons = []

    for prompt in prompts:

        gemini_result = ask_gemini(prompt)

        groq_result = ask_groq(
            groq_client,
            prompt
        )

        comparisons.append({

            "prompt": prompt,

            "gemini": gemini_result,

            "groq": groq_result
        })

    return comparisons


# --------------------------------------------------
# FORMAT OUTPUT
# --------------------------------------------------

def format_side_by_side(
    comparison,
    width: int = 60
) -> str:

    prompt = comparison["prompt"]

    gemini = comparison["gemini"]

    groq = comparison["groq"]

    separator = " | "

    left_header = (
        "Gemini (gemini-2.5-flash-lite)"
    )

    right_header = (
        "Groq (llama-3.1-8b-instant)"
    )

    left_lines = [

        f"Prompt: {prompt}",

        "",

        left_header,

        f"Latency: {gemini.latency_ms:.2f} ms"
    ]

    right_lines = [

        right_header,

        f"Latency: {groq.latency_ms:.2f} ms"
    ]

    if gemini.error:

        left_lines.append(
            f"Error: {gemini.error}"
        )

    else:

        left_lines.extend(
            textwrap.wrap(
                gemini.response,
                width
            )
        )

    if groq.error:

        right_lines.append(
            f"Error: {groq.error}"
        )

    else:

        right_lines.extend(
            textwrap.wrap(
                groq.response,
                width
            )
        )

    max_lines = max(
        len(left_lines),
        len(right_lines)
    )

    left_lines += [""] * (
        max_lines - len(left_lines)
    )

    right_lines += [""] * (
        max_lines - len(right_lines)
    )

    formatted_lines = [

        "=" * (
            width * 2 + len(separator)
        )
    ]

    formatted_lines.append(
        f"Prompt: {prompt}"
    )

    formatted_lines.append(

        "-" * (
            width * 2 + len(separator)
        )
    )

    for left, right in zip(
        left_lines,
        right_lines
    ):

        formatted_lines.append(

            f"{left.ljust(width)}"
            f"{separator}"
            f"{right.ljust(width)}"
        )

    formatted_lines.append(

        "=" * (
            width * 2 + len(separator)
        )
    )

    return "\n".join(formatted_lines)


# --------------------------------------------------
# SAVE RESULTS
# --------------------------------------------------

def save_results(

    text: str,

    file_name: str = "comparison_results.txt"
):

    with open(
        file_name,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(text)


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    try:

        keys = load_api_keys()

        gemini_client = create_gemini_client(
            keys["gemini"]
        )

        groq_client = create_groq_client(
            keys["groq"]
        )

        prompts = build_prompts()

        comparisons = compare_prompts(
            prompts,
            gemini_client,
            groq_client
        )

        output_lines = []

        for comparison in comparisons:

            output_lines.append(
                format_side_by_side(comparison)
            )

            output_lines.append("\n")

        output_text = "\n".join(
            output_lines
        ).strip()

        print(output_text)

        save_results(output_text)

        print(
            "\nComparison saved to comparison_results.txt"
        )

        return 0

    except Exception as error:

        print(f"Error: {error}")

        return 1


if __name__ == "__main__":

    raise SystemExit(main())