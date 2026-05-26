import json
import os

from dotenv import load_dotenv
import google.generativeai as genai


def main():
    # Load environment variables from .env
    load_dotenv()

    # Get Gemini API key
    api_key = os.getenv("GEMINI_API_KEY")

    # Check if API key exists
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env file")
        return

    # Configure Gemini API
    genai.configure(api_key=api_key)

    # Create Gemini model
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    # Sample unstructured text
    user_text = (
        "Rahul is a 28-year-old software engineer "
        "from Bangalore who works in AI."
    )

    # Prompt for structured JSON extraction
    prompt = f"""
Extract the following fields from the text below.

Return ONLY valid JSON.

Fields:
- name
- age
- city
- profession

Text:
{user_text}
"""

    try:
        # Generate Gemini response
        response = model.generate_content(prompt)

        # Extract response text
        raw_text = response.text.strip()

        # Remove markdown formatting if Gemini adds it
        raw_text = raw_text.replace("```json", "")
        raw_text = raw_text.replace("```", "")
        raw_text = raw_text.strip()

        # Print raw response
        print("\n================ RAW GEMINI RESPONSE ================\n")
        print(raw_text)

        # Convert JSON string into Python dictionary
        parsed_json = json.loads(raw_text)

        # Print formatted JSON
        print("\n================ PARSED JSON ================\n")
        print(json.dumps(parsed_json, indent=4))

    except json.JSONDecodeError as e:
        print("\nJSON Parsing Error")
        print(e)

    except Exception as e:
        print("\nError occurred")
        print(e)


if __name__ == "__main__":
    main()