"""
extract_event.py

Extract Event objects from news article text using Gemini JSON mode
and validate the response using the Event Pydantic schema.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import List

from dotenv import load_dotenv
import google.generativeai as genai
from pydantic import ValidationError

from schemas import Event


MODEL_NAME = "gemini-2.5-flash-lite"


def find_dotenv_path() -> Path:
    """Find .env file from current folder or parent folders."""
    current = Path(__file__).resolve()

    for parent in [current.parent, *current.parents]:
        candidate = parent / ".env"

        if candidate.is_file():
            return candidate

    raise FileNotFoundError("Could not find .env file")


def configure_gemini() -> None:
    """Load Gemini API key and configure Gemini client."""
    dotenv_path = find_dotenv_path()

    load_dotenv(dotenv_path=dotenv_path)

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing in .env")

    genai.configure(api_key=api_key)


def extract_event(article_text: str) -> Event:
    """Extract and validate one Event object from article text."""

    prompt = f"""
Extract one event from the news article below.

Return the event with:
- title
- date in YYYY-MM-DD format
- location
- summary_line as one sentence

Article:
{article_text.strip()}
"""

    model = genai.GenerativeModel(
        MODEL_NAME,
        generation_config={
            "response_mime_type": "application/json"
        }
    )

    response = model.generate_content(prompt)

    raw_text = response.text

    try:
        parsed_json = json.loads(raw_text)

        # Gemini sometimes returns a list with one object.
        # Event expects one dictionary/object.
        if isinstance(parsed_json, list):
            if not parsed_json:
                raise ValueError("Gemini returned an empty list")
            parsed_json = parsed_json[0]

        if not isinstance(parsed_json, dict):
            raise TypeError(
                f"Expected JSON object, got {type(parsed_json).__name__}"
            )

    except json.JSONDecodeError as error:
        print("JSON parsing failed.")
        print("Raw response:")
        print(raw_text)
        raise error

    try:
        event = Event(**parsed_json)

    except ValidationError as error:
        print("Pydantic validation failed.")
        print(error)
        raise error

    return event


def load_articles(article_file: Path) -> List[str]:
    """Load articles separated by blank lines."""

    raw_text = article_file.read_text(
        encoding="utf-8"
    ).strip()

    if not raw_text:
        return []

    articles = re.split(
        r"\n\s*\n",
        raw_text
    )

    return [
        article.strip()
        for article in articles
        if article.strip()
    ]


def main() -> None:
    """Run event extraction on all article fixtures."""

    configure_gemini()

    article_file = (
        Path(__file__).resolve().parent
        / "fixtures"
        / "articles.txt"
    )

    articles = load_articles(article_file)

    success_count = 0
    failure_count = 0

    print("EVENT EXTRACTION TEST")
    print("=" * 60)

    for index, article in enumerate(
        articles,
        start=1
    ):
        print(f"\nARTICLE {index}")
        print("-" * 60)

        try:
            event = extract_event(article)

            print(event.model_dump_json(indent=2))

            success_count += 1

        except Exception as error:
            failure_count += 1

            print(f"Failed article {index}: {error}")

    print("\nSUMMARY")
    print("=" * 60)
    print(f"Extracted {success_count} / {len(articles)} events successfully.")
    print(f"Failures: {failure_count}")


if __name__ == "__main__":
    main()

