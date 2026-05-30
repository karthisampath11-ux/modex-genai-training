from __future__ import annotations

import time
from pathlib import Path
from typing import Callable, TypeVar

from pydantic import ValidationError

from extract_event import (
    extract_event,
    configure_gemini,
)

T = TypeVar("T")


def retry_on_validation_failure(
    extractor_func: Callable[[str], T],
    input_text: str,
    max_retries: int = 3,
) -> T:
    """
    Retry extractor when validation fails.
    """

    start_time = time.time()
    last_error = None

    for attempt in range(1, max_retries + 1):

        try:
            result = extractor_func(input_text)

            elapsed = time.time() - start_time

            print(f"Success on attempt {attempt}")
            print(f"Total time: {elapsed:.2f}s")
            print(f"Retries used: {attempt - 1}")

            return result

        except ValidationError as error:
            last_error = error

            print(f"Validation failed on attempt {attempt}")
            print(error)

            if attempt < max_retries:
                print("Retrying...")
                time.sleep(2)

            else:
                print("Maximum retries reached.")

    raise last_error


def load_first_article() -> str:

    article_file = (
        Path(__file__).resolve().parent
        / "fixtures"
        / "articles.txt"
    )

    raw_text = article_file.read_text(
        encoding="utf-8"
    ).strip()

    articles = [
        article.strip()
        for article in raw_text.split("\n\n")
        if article.strip()
    ]

    if not articles:
        raise ValueError(
            "No articles found in fixtures/articles.txt"
        )

    return articles[0]


def main() -> None:

    configure_gemini()

    first_article = load_first_article()

    print("RETRY WRAPPER TEST")
    print("=" * 60)

    print("Running Event extraction with Gemini")
    print("-" * 60)

    event = retry_on_validation_failure(
        extractor_func=extract_event,
        input_text=first_article,
        max_retries=3,
    )

    print("\nFINAL RESULT")
    print("=" * 60)

    print(
        event.model_dump_json(
            indent=2
        )
    )


if __name__ == "__main__":
    main()