"""
extract_event_llama.py
Extract Event objects using Groq Llama and validate using Pydantic.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from groq import Groq
from pydantic import ValidationError

from schemas import Event


MODEL_NAME = "llama-3.1-8b-instant"


def find_dotenv_path() -> Path:
    current = Path(__file__).resolve()

    for parent in [current.parent, *current.parents]:
        candidate = parent / ".env"
        if candidate.is_file():
            return candidate

    raise FileNotFoundError("Could not find .env file")


def create_groq_client() -> Groq:
    dotenv_path = find_dotenv_path()
    load_dotenv(dotenv_path=dotenv_path)

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing in .env")

    return Groq(api_key=api_key)


def extract_event_llama(article_text: str, client: Groq) -> Event:
    prompt = f"""
Extract event information from the article below.

Return ONLY a JSON object with exactly these fields:
- title
- date
- location
- summary_line

Date must be in YYYY-MM-DD format.
Do not include markdown or explanation.

Article:
{article_text.strip()}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_tokens=500,
        response_format={
            "type": "json_object"
        }
    )

    raw_text = response.choices[0].message.content

    try:
        parsed_json = json.loads(raw_text)

        if isinstance(parsed_json, list):
            parsed_json = parsed_json[0]

    except json.JSONDecodeError as error:
        print("JSON parsing failed.")
        print(raw_text)
        raise error

    try:
        return Event(**parsed_json)

    except ValidationError as error:
        print("Pydantic validation failed.")
        print(json.dumps(parsed_json, indent=2))
        print(error)
        raise error


def load_articles(article_file: Path) -> List[str]:
    raw_text = article_file.read_text(encoding="utf-8").strip()

    if not raw_text:
        return []

    return [
        article.strip()
        for article in re.split(r"\n\s*\n", raw_text)
        if article.strip()
    ]


def main() -> None:
    client = create_groq_client()

    article_file = (
        Path(__file__).resolve().parent
        / "fixtures"
        / "articles.txt"
    )

    articles = load_articles(article_file)

    success_count = 0
    failure_count = 0

    print("LLAMA EVENT EXTRACTION")
    print("=" * 60)

    for index, article in enumerate(articles, start=1):
        print(f"\nARTICLE {index}")
        print("-" * 60)

        try:
            event = extract_event_llama(article, client)
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