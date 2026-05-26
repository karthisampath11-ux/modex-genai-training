import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash-lite")

article = """
Apple announced a new AI-powered MacBook Pro on May 20, 2026.
The launch event was led by CEO Tim Cook in California.
The laptop includes improved battery life and faster AI processing.
"""

# Prompt Version 2
prompt = f"""
You are a JSON extraction assistant.

Extract:
1. title
2. author
3. date
4. key_facts

Rules:
- Return only JSON
- key_facts must be a list
- No explanation

Article:
{article}
"""

response = model.generate_content(prompt)

raw_text = response.text.strip()

print(raw_text)

cleaned = raw_text.replace("```json", "").replace("```", "").strip()

data = json.loads(cleaned)

print(json.dumps(data, indent=4))