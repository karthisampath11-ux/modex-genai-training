"""
extract_compliance.py

Extract ComplianceCheck objects from inspection paragraphs using Gemini JSON mode,
validate with Pydantic, and run through retry wrapper.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai
from pydantic import ValidationError

from schemas import ComplianceCheck
from retry_wrapper import retry_on_validation_failure


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

    genai.configure(
        api_key=api_key,
        transport="rest"
    )


def normalize_compliance_json(parsed_json: dict) -> dict:
    """Normalize small field-name drift before Pydantic validation."""

    if "evidence" in parsed_json and "evidence_quotes" not in parsed_json:
        parsed_json["evidence_quotes"] = parsed_json.pop("evidence")

    if "verdict" in parsed_json and "status" not in parsed_json:
        parsed_json["status"] = parsed_json.pop("verdict")

    if "result" in parsed_json and "status" not in parsed_json:
        parsed_json["status"] = parsed_json.pop("result")

    if "evidence_quotes" not in parsed_json:
        parsed_json["evidence_quotes"] = []

    if "notes" not in parsed_json:
        parsed_json["notes"] = ""

    return parsed_json


def extract_compliance(paragraph_text: str) -> ComplianceCheck:
    """Extract and validate one ComplianceCheck object from inspection text."""

    prompt = f"""
Extract one compliance check from the paragraph below.

Return JSON with EXACTLY these fields:
- rule_id
- status
- evidence_quotes
- confidence
- notes

Status must be exactly one of:
- compliant
- non_compliant
- insufficient_evidence

Rules:
- Identify rule_id from the paragraph.
- Use rule_id format like NBC-EXIT-001, NBC-FIRE-001, NBC-SPRINKLER-001.
- evidence_quotes must be VERBATIM substrings from the paragraph.
- Do not paraphrase evidence_quotes.
- Use insufficient_evidence only when there is not enough proof.
- Use non_compliant when the paragraph clearly shows a violation.
- confidence must be between 0.0 and 1.0.
- notes can be empty string.

Paragraph:
{paragraph_text.strip()}
"""

    model = genai.GenerativeModel(
        MODEL_NAME,
        generation_config={
            "response_mime_type": "application/json"
        }
    )

    response = model.generate_content(
        prompt,
        request_options={
            "timeout": 60
        }
    )

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

        parsed_json = normalize_compliance_json(parsed_json)

    except json.JSONDecodeError as error:
        print("JSON parsing failed.")
        print("Raw response:")
        print(raw_text)
        raise error

    try:
        compliance_check = ComplianceCheck(**parsed_json)

    except ValidationError as error:
        print("Pydantic validation failed.")
        print("Normalized JSON:")
        print(json.dumps(parsed_json, indent=2))
        print(error)
        raise error

    return compliance_check


def load_inspections(inspection_file: Path) -> list[str]:
    """Load inspections separated by blank lines or ---."""

    raw_text = inspection_file.read_text(
        encoding="utf-8"
    ).strip()

    if not raw_text:
        return []

    inspections = re.split(
        r"\n\s*(?:---)?\s*\n",
        raw_text
    )

    return [
        inspection.strip()
        for inspection in inspections
        if inspection.strip()
    ]


def main() -> None:
    """Run compliance extraction on all inspection fixtures with retry."""

    configure_gemini()

    inspection_file = (
        Path(__file__).resolve().parent
        / "fixtures"
        / "inspections.txt"
    )

    inspections = load_inspections(inspection_file)

    success_count = 0
    failure_count = 0

    print("COMPLIANCE EXTRACTION TEST WITH RETRY")
    print("=" * 60)

    for index, inspection_text in enumerate(
        inspections,
        start=1
    ):
        print(f"\nINSPECTION {index}")
        print("-" * 60)

        try:
            compliance_check = retry_on_validation_failure(
                extractor_func=extract_compliance,
                input_text=inspection_text,
                max_retries=3,
            )

            print(compliance_check.model_dump_json(indent=2))

            success_count += 1

        except Exception as error:
            failure_count += 1

            print(f"Failed inspection {index}: {error}")

    print("\nSUMMARY")
    print("=" * 60)
    print(
        f"Extracted {success_count} / {len(inspections)} compliance checks successfully."
    )
    print(f"Failures: {failure_count}")


if __name__ == "__main__":
    main()