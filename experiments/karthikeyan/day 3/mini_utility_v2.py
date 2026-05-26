import argparse
import json
import os

from dotenv import load_dotenv
import google.generativeai as genai


def setup_gemini():
    """Load API key and configure Gemini."""

    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found.")

    genai.configure(api_key=api_key)


def process_text(user_text):
    """Send text to Gemini and return structured output."""

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    Analyze this text and return:
    1. summary
    2. sentiment
    3. keywords list

    Text:
    {user_text}

    Return JSON only.
    """

    response = model.generate_content(prompt)

    raw_text = response.text.strip()

    raw_text = raw_text.replace("```json", "")
    raw_text = raw_text.replace("```", "")

    return json.loads(raw_text)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--text",
        required=True,
        help="Input text"
    )

    args = parser.parse_args()

    try:

        print("STEP 1: Setting up Gemini...")
        setup_gemini()

        print("STEP 2: Processing text...")
        result = process_text(args.text)

        final_output = {
            "status": "success",
            "data": result
        }

        print("\nFINAL OUTPUT:\n")
        print(json.dumps(final_output, indent=4))

    except Exception as error:

        error_output = {
            "status": "error",
            "message": str(error)
        }

        print(json.dumps(error_output, indent=4))


if __name__ == "__main__":
    main()