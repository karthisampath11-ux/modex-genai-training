import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from groq import Groq


# .env file in same folder as this script
ROOT_ENV_PATH = Path(".env")

# Output JSON file
DEFAULT_OUTPUT_PATH = Path(__file__).resolve().parent / "day3_utility_result.json"

# Groq Model
MODEL_NAME = "llama-3.1-8b-instant"


def configure_logging(debug: bool = False) -> None:
    """Configure logging settings."""
    level = logging.DEBUG if debug else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def load_api_key() -> str:
    """Load GROQ_API_KEY from .env file."""

    load_dotenv(dotenv_path=ROOT_ENV_PATH)

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        logging.error("GROQ_API_KEY not found in .env")
        raise ValueError("GROQ_API_KEY must be set in .env")

    return api_key


def create_groq_client(api_key: str) -> Groq:
    """Create Groq client."""
    return Groq(api_key=api_key)


def measure_latency(func):
    """Decorator to measure API latency."""

    def wrapper(*args, **kwargs):
        start = time.perf_counter()

        result = func(*args, **kwargs)

        latency_ms = (time.perf_counter() - start) * 1000

        return result, latency_ms

    return wrapper


@measure_latency
def send_groq_prompt(client: Groq, prompt: str) -> Dict[str, Any]:
    """Send prompt to Groq."""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        max_tokens=400,
        temperature=0,
    )

    if not response.choices:
        raise ValueError("No response choices returned from Groq.")

    content = response.choices[0].message.content.strip()

    usage = response.usage

    input_tokens = getattr(usage, "prompt_tokens", 0)
    output_tokens = getattr(usage, "completion_tokens", 0)
    total_tokens = getattr(usage, "total_tokens", 0)

    return {
        "text": content,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
    }


def build_chain_steps(user_input: str) -> List[Dict[str, str]]:
    """Create prompt chain workflow."""

    return [
        {
            "name": "Intent Extraction",
            "prompt": (
                "Extract the main intent from the user input "
                "and summarize it in one concise sentence.\n\n"
                f"User Input:\n{user_input}"
            ),
        },
        {
            "name": "Response Drafting",
            "prompt": (
                "Using the extracted intent below, write a clear "
                "professional response in two short paragraphs.\n\n"
                "Extracted Intent:\n{previous_response}"
            ),
        },
        {
            "name": "Structured Packaging",
            "prompt": (
                "Convert the following into valid JSON.\n"
                "Return ONLY JSON.\n\n"
                "Original Input:\n{original_input}\n\n"
                "Objective:\n{objective}\n\n"
                "Draft Response:\n{draft_response}"
            ),
        },
    ]


def run_chain(client: Groq, user_input: str) -> Dict[str, Any]:
    """Run prompt chain."""

    chain_steps = build_chain_steps(user_input)

    results = []

    intent_response = ""
    draft_response = ""

    for index, step in enumerate(chain_steps, start=1):

        if step["name"] == "Intent Extraction":

            prompt_text = step["prompt"]

        elif step["name"] == "Response Drafting":

            prompt_text = step["prompt"].format(
                previous_response=intent_response
            )

        else:

            prompt_text = step["prompt"].format(
                original_input=user_input,
                objective=intent_response,
                draft_response=draft_response,
            )

        logging.info("Running Step %d: %s", index, step["name"])

        response_payload, latency_ms = send_groq_prompt(
            client,
            prompt_text
        )

        response_text = response_payload["text"]

        if step["name"] == "Intent Extraction":
            intent_response = response_text

        elif step["name"] == "Response Drafting":
            draft_response = response_text

        step_result = {
            "step": step["name"],
            "prompt": prompt_text,
            "response": response_text,
            "latency_ms": round(latency_ms, 2),
            "input_tokens": response_payload["input_tokens"],
            "output_tokens": response_payload["output_tokens"],
            "total_tokens": response_payload["total_tokens"],
        }

        logging.info(
            "Step completed: %s | Latency: %.2f ms",
            step["name"],
            latency_ms,
        )

        logging.info("Response:\n%s", response_text)

        results.append(step_result)

    final_payload = {
        "input": user_input,
        "created_at": datetime.now().isoformat(),
        "model": MODEL_NAME,
        "chain": results,
        "summary": {
            "total_latency_ms": round(
                sum(step["latency_ms"] for step in results),
                2,
            ),
            "average_latency_ms": round(
                sum(step["latency_ms"] for step in results) / len(results),
                2,
            ),
            "total_tokens": sum(
                step["total_tokens"] for step in results
            ),
        },
    }

    return final_payload


def save_json(output_path: Path, payload: Dict[str, Any]) -> None:
    """Save result to JSON file."""

    output_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    logging.info("Saved JSON result to %s", output_path)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse CLI arguments."""

    parser = argparse.ArgumentParser(
        description="Groq Prompt Chaining Utility"
    )

    parser.add_argument(
        "--input",
        type=str,
        help="Input text",
    )

    parser.add_argument(
        "--input-file",
        type=Path,
        help="Path to text file",
    )

    parser.add_argument(
        "--output-file",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Output JSON file",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    return parser.parse_args(argv)


def read_input(args: argparse.Namespace) -> str:
    """Read input from CLI or file."""

    if args.input:
        return args.input.strip()

    if args.input_file:

        if not args.input_file.exists():
            raise FileNotFoundError(
                f"Input file not found: {args.input_file}"
            )

        return args.input_file.read_text(
            encoding="utf-8"
        ).strip()

    raise ValueError(
        "Provide either --input or --input-file"
    )


def main(argv: Optional[List[str]] = None) -> int:
    """Main function."""

    args = parse_args(argv)

    configure_logging(args.debug)

    try:
        user_input = read_input(args)

        api_key = load_api_key()

        client = create_groq_client(api_key)

        final_result = run_chain(client, user_input)

        save_json(args.output_file, final_result)

        print(
            f"\nSaved structured result to:\n{args.output_file}"
        )

        return 0

    except Exception as exc:

        logging.error("Execution failed: %s", exc)

        return 1


if __name__ == "__main__":
    sys.exit(main())