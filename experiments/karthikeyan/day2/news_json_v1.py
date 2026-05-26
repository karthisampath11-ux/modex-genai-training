import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash-lite")

# Sample news article
article = """
Apple announced a new AI-powered MacBook Pro on May 20, 2026.
The launch event was led by CEO Tim Cook in California.
The laptop includes improved battery life and faster AI processing.
"""

# Prompt Version 1
prompt = f"""
Extract the following information from this news article as JSON:

- title
- author
- date
- key_facts (as list)

Article:
{article}

Return ONLY valid JSON.
"""

response = model.generate_content(prompt)

raw_text = response.text.strip()

print("=========== RAW RESPONSE ===========")
print(raw_text)

# Parse JSON
cleaned = raw_text.replace("```json", "").replace("```", "").strip()

data = json.loads(cleaned)

print("\n=========== PARSED JSON ===========")
print(json.dumps(data, indent=4))