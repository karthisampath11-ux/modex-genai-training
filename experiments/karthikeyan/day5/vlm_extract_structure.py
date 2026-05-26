import os
import sys
import json
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai

# Fix Unicode issue
sys.stdout.reconfigure(encoding='utf-8')

# Load API key
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini model
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# Images to analyze
image_tasks = [
    {
        "file": "images/receipt.jpg",
        "prompt": """
        Extract receipt information.

        Return ONLY valid JSON in this format:

        {
            "store_name": "",
            "items": [],
            "total_amount": "",
            "payment_method": "",
            "date": ""
        }
        """
    },

    {
        "file": "images/infographic.jpg",
        "prompt": """
        Analyze this infographic.

        Return ONLY valid JSON:

        {
            "title": "",
            "main_topics": [],
            "key_points": []
        }
        """
    },

    {
        "file": "images/ui.jpg",
        "prompt": """
        Analyze this dashboard UI.

        Return ONLY valid JSON:

        {
            "application_name": "",
            "main_sections": [],
            "metrics_visible": [],
            "purpose": ""
        }
        """
    }
]

print("\nRUNNING STRUCTURED EXTRACTION TESTS...\n")

for task in image_tasks:

    print("=" * 60)
    print(f"IMAGE: {task['file']}")

    try:
        img = Image.open(task["file"])

        response = model.generate_content(
            [task["prompt"], img]
        )

        print("\nEXTRACTED STRUCTURE:\n")

        try:
            cleaned_text = response.text.strip()

            cleaned_text = cleaned_text.replace("```json", "")
            cleaned_text = cleaned_text.replace("```", "")

            parsed = json.loads(cleaned_text)

            print(json.dumps(parsed, indent=4))

        except Exception:
            print(response.text)

    except Exception as e:
        print(f"\nERROR: {e}")

print("\nALL STRUCTURED EXTRACTION TESTS COMPLETED")