"""
extract_recipe.py

Extract Recipe objects from recipe text using Gemini JSON mode
and validate the response using the Recipe Pydantic schema.
"""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import List

from dotenv import load_dotenv
import google.generativeai as genai
from pydantic import ValidationError

from schemas import Recipe


MODEL_NAME = "gemini-2.5-flash-lite"


def find_dotenv_path() -> Path:
    current = Path(__file__).resolve()

    for parent in [current.parent, *current.parents]:
        candidate = parent / ".env"

        if candidate.is_file():
            return candidate

    raise FileNotFoundError("Could not find .env file")


def configure_gemini() -> None:
    dotenv_path = find_dotenv_path()

    load_dotenv(dotenv_path=dotenv_path)

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing in .env")

    genai.configure(
        api_key=api_key,
        transport="rest"
    )


def normalize_recipe_json(parsed_json: dict) -> dict:
    """
    Fix common field-name drift from model output before Pydantic validation.
    """

    if "recipe_name" in parsed_json and "title" not in parsed_json:
        parsed_json["title"] = parsed_json.pop("recipe_name")

    if "name" in parsed_json and "title" not in parsed_json:
        parsed_json["title"] = parsed_json.pop("name")

    if "ingredients" in parsed_json:
        for ingredient in parsed_json["ingredients"]:

            if "ingredient" in ingredient and "name" not in ingredient:
                ingredient["name"] = ingredient.pop("ingredient")

            if "ingredient_name" in ingredient and "name" not in ingredient:
                ingredient["name"] = ingredient.pop("ingredient_name")

            if "item" in ingredient and "name" not in ingredient:
                ingredient["name"] = ingredient.pop("item")

    return parsed_json


def extract_recipe(recipe_text: str) -> Recipe:
    prompt = f"""
Extract one recipe from the text below.

You must use EXACTLY these top-level JSON field names:
- title
- servings
- ingredients
- steps
- prep_minutes

Each object inside ingredients must use EXACTLY these field names:
- name
- quantity
- unit

Do not use these wrong field names:
- recipe_name
- ingredient
- ingredient_name
- item

Rules:
- quantity must be numeric value, not string
- unit must be one of: g, ml, cups, tsp, tbsp, pieces, oz
- for countable items without explicit unit, use pieces
- if prep time says about 30 minutes or 30-40 minutes, return lower bound as prep_minutes
- steps must be ordered correctly

Recipe:
{recipe_text.strip()}
"""

    model = genai.GenerativeModel(
        MODEL_NAME,
        generation_config={
            "response_mime_type": "application/json"
        }
    )

    start_time = time.perf_counter()

    response = model.generate_content(
        prompt,
        request_options={
            "timeout": 60
        }
    )

    latency_ms = (time.perf_counter() - start_time) * 1000

    raw_text = response.text

    try:
        parsed_json = json.loads(raw_text)

        if isinstance(parsed_json, list):
            if not parsed_json:
                raise ValueError("Gemini returned an empty list")
            parsed_json = parsed_json[0]

        if not isinstance(parsed_json, dict):
            raise TypeError(
                f"Expected JSON object, got {type(parsed_json).__name__}"
            )

        parsed_json = normalize_recipe_json(parsed_json)

    except json.JSONDecodeError as error:
        print("JSON parsing failed.")
        print("Raw response:")
        print(raw_text)
        raise error

    try:
        recipe = Recipe(**parsed_json)

    except ValidationError as error:
        print("Pydantic validation failed.")
        print("Normalized JSON:")
        print(json.dumps(parsed_json, indent=2))
        print(error)
        raise error

    print(f"Latency: {latency_ms:.2f} ms")

    return recipe


def load_recipes(recipe_file: Path) -> List[str]:
    raw_text = recipe_file.read_text(
        encoding="utf-8"
    ).strip()

    if not raw_text:
        return []

    recipes = re.split(
        r"\n\s*\n",
        raw_text
    )

    return [
        recipe.strip()
        for recipe in recipes
        if recipe.strip()
    ]


def main() -> None:
    configure_gemini()

    recipe_file = (
        Path(__file__).resolve().parent
        / "fixtures"
        / "recipes.txt"
    )

    recipes = load_recipes(recipe_file)

    success_count = 0
    failure_count = 0

    print("RECIPE EXTRACTION TEST")
    print("=" * 60)

    for index, recipe_text in enumerate(
        recipes,
        start=1
    ):
        print(f"\nRECIPE {index}")
        print("-" * 60)

        try:
            recipe = extract_recipe(recipe_text)

            print(recipe.model_dump_json(indent=2))

            success_count += 1

        except Exception as error:
            failure_count += 1

            print(f"Failed recipe {index}: {error}")

    print("\nSUMMARY")
    print("=" * 60)
    print(f"Extracted {success_count} / {len(recipes)} recipes successfully.")
    print(f"Failures: {failure_count}")


if __name__ == "__main__":
    main()