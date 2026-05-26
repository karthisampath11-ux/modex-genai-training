import os
import json
import argparse
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")


def process_text(user_input):

    print("STEP 1: Checking input...")

    # Handle empty input
    if not user_input.strip():
        return {
            "status": "error",
            "message": "Input cannot be empty."
        }

    # Handle very long input
    if len(user_input) > 1000:
        return {
            "status": "error",
            "message": "Input is too long."
        }

    print("STEP 2: Sending request to Gemini...")

    prompt = f"""
    Analyze this text and return valid JSON only.

    Required fields:
    - summary
    - sentiment
    - keywords

    Text:
    {user_input}
    """

    try:
        response = model.generate_content(prompt)

        print("STEP 3: Response received.")

        raw_text = response.text.strip()

        # Remove markdown formatting
        raw_text = raw_text.replace("```json", "")
        raw_text = raw_text.replace("```", "")
        raw_text = raw_text.strip()

        parsed_json = json.loads(raw_text)

        return {
            "status": "success",
            "data": parsed_json
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--text",
        type=str,
        required=True,
        help="Input text"
    )

    args = parser.parse_args()

    result = process_text(args.text)

    print("\nFINAL OUTPUT:\n")

    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()