import json
import os

from dotenv import load_dotenv
import google.generativeai as genai


def main():
    # Load environment variables
    load_dotenv()

    # Get API key
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("Error: GEMINI_API_KEY not found")
        return

    # Configure Gemini
    genai.configure(api_key=api_key)

    # Load model
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    # More realistic input text
    user_text = """
    Priya Sharma is a 32-year-old Data Scientist from Chennai.
    She works at Infosys and has 7 years of experience.
    Her skills include Python, Machine Learning, SQL, and Power BI.
    """

    # Advanced extraction prompt
    prompt = f"""
You are an AI data extraction system.

Extract information from the text and return ONLY valid JSON.

Rules:
- No markdown
- No explanation
- No extra text
- Output must be parseable JSON

Required JSON format:

{{
    "name": "",
    "age": 0,
    "city": "",
    "profession": "",
    "company": "",
    "experience_years": 0,
    "skills": []
}}

Text:
{user_text}
"""

    try:
        # Generate response
        response = model.generate_content(prompt)

        # Extract raw text
        raw_text = response.text.strip()

        # Cleanup if needed
        raw_text = raw_text.replace("```json", "")
        raw_text = raw_text.replace("```", "")
        raw_text = raw_text.strip()

        # Print raw response
        print("\n================ RAW GEMINI RESPONSE ================\n")
        print(raw_text)

        # Parse JSON
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