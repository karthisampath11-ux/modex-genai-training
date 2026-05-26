import json
import os

from dotenv import load_dotenv
import google.generativeai as genai


def main():
    # Load .env variables
    load_dotenv()

    # Read Gemini API key
    api_key = os.getenv("GEMINI_API_KEY")

    # Check API key
    if not api_key:
        print("Error: GEMINI_API_KEY not found")
        return

    # Configure Gemini
    genai.configure(api_key=api_key)

    # Use lighter Gemini model
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    # Input text
    user_text = (
        "Rahul is a 28-year-old software engineer "
        "from Bangalore who works in AI."
    )

    # Improved prompt
    prompt = f"""
You are a JSON extraction system.

Return ONLY pure valid JSON.

Do NOT:
- add markdown
- add explanation
- add comments
- add extra text

Required format:
{{
    "name": "",
    "age": 0,
    "city": "",
    "profession": ""
}}

Text:
{user_text}
"""

    try:
        # Generate response
        response = model.generate_content(prompt)

        # Extract response text
        raw_text = response.text.strip()

        # Safety cleanup
        raw_text = raw_text.replace("```json", "")
        raw_text = raw_text.replace("```", "")
        raw_text = raw_text.strip()

        # Print raw output
        print("\n================ RAW GEMINI RESPONSE ================\n")
        print(raw_text)

        # Convert JSON text into Python dictionary
        parsed_json = json.loads(raw_text)

        # Pretty print parsed JSON
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