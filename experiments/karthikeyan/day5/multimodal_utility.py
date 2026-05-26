import os
import sys
import json
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai

# UTF-8 Fix
sys.stdout.reconfigure(encoding='utf-8')

# Load API key
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini model
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# Image path
IMAGE_PATH = "images/ui.jpg"

print("\nMULTIMODAL UTILITY PROJECT")
print("=" * 60)

try:

    # Open image
    img = Image.open(IMAGE_PATH)

    # --------------------------------------------------
    # STEP 1 — IMAGE DESCRIPTION
    # --------------------------------------------------

    print("\nSTEP 1: IMAGE DESCRIPTION\n")

    description_prompt = """
    Describe this image in detail.
    Mention:
    - Main content
    - Visual elements
    - Purpose
    """

    description_response = model.generate_content(
        [description_prompt, img]
    )

    description = description_response.text

    print(description)

    # --------------------------------------------------
    # STEP 2 — OCR TEXT EXTRACTION
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("\nSTEP 2: OCR TEXT EXTRACTION\n")

    ocr_prompt = """
    Extract all visible text from this image.
    """

    ocr_response = model.generate_content(
        [ocr_prompt, img]
    )

    extracted_text = ocr_response.text

    print(extracted_text)

    # --------------------------------------------------
    # STEP 3 — STRUCTURED JSON EXTRACTION
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("\nSTEP 3: STRUCTURED DATA\n")

    structure_prompt = """
    Analyze this image.

    Return ONLY valid JSON:

    {
        "application_name": "",
        "main_sections": [],
        "important_metrics": [],
        "purpose": "",
        "ui_type": ""
    }
    """

    structure_response = model.generate_content(
        [structure_prompt, img]
    )

    cleaned = structure_response.text.strip()
    cleaned = cleaned.replace("```json", "")
    cleaned = cleaned.replace("```", "")

    try:
        parsed_json = json.loads(cleaned)

        formatted_json = json.dumps(
            parsed_json,
            indent=4
        )

        print(formatted_json)

    except Exception:
        formatted_json = cleaned
        print(cleaned)

    # --------------------------------------------------
    # STEP 4 — INSIGHT GENERATION
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("\nSTEP 4: BUSINESS INSIGHTS\n")

    insight_prompt = """
    Analyze this dashboard and provide:
    - Key business insights
    - Trends
    - Possible recommendations
    """

    insight_response = model.generate_content(
        [insight_prompt, img]
    )

    insights = insight_response.text

    print(insights)

    # --------------------------------------------------
    # STEP 5 — SAVE REPORT
    # --------------------------------------------------

    report = f"""
MULTIMODAL UTILITY REPORT
============================================================

STEP 1 — DESCRIPTION
--------------------
{description}

============================================================

STEP 2 — OCR TEXT
--------------------
{extracted_text}

============================================================

STEP 3 — STRUCTURED JSON
--------------------
{formatted_json}

============================================================

STEP 4 — INSIGHTS
--------------------
{insights}
"""

    with open(
        "multimodal_report.txt",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(report)

    print("\n" + "=" * 60)
    print("\nREPORT SAVED: multimodal_report.txt")

except Exception as e:
    print(f"\nERROR: {e}")