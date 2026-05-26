import json
import os
from datetime import datetime

from dotenv import load_dotenv
import google.generativeai as genai


# ---------------------------------------------------
# STEP 1: Gemini Setup
# ---------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found.")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")


# ---------------------------------------------------
# STEP 2: Input Texts
# ---------------------------------------------------

texts = [
    "Artificial Intelligence is improving healthcare.",
    "Python is widely used in data science.",
    "Cloud platforms help businesses scale quickly."
]


# ---------------------------------------------------
# STEP 3: AI Processing Function
# ---------------------------------------------------

def analyze_text(text):

    prompt = f"""
    Analyze the following text and return JSON with:
    - summary
    - sentiment
    - keywords

    Text:
    {text}

    Return valid JSON only.
    """

    response = model.generate_content(prompt)

    raw_text = response.text.strip()

    raw_text = raw_text.replace("```json", "")
    raw_text = raw_text.replace("```", "")

    return json.loads(raw_text)


# ---------------------------------------------------
# STEP 4: Batch Processing
# ---------------------------------------------------

results = []

print("Starting Batch Processing...\n")

for index, text in enumerate(texts, start=1):

    print(f"Processing Text {index}")

    try:

        result = analyze_text(text)

        results.append({
            "input": text,
            "output": result,
            "processed_at": str(datetime.now())
        })

        print("Completed\n")

    except Exception as error:

        print(f"Error: {error}\n")


# ---------------------------------------------------
# STEP 5: Save Results
# ---------------------------------------------------

output_file = "batch_results.json"

with open(output_file, "w") as file:

    json.dump(results, file, indent=4)


# ---------------------------------------------------
# STEP 6: Final Message
# ---------------------------------------------------

print("=" * 60)
print("Batch Processing Completed")
print(f"Results saved to: {output_file}")
print("=" * 60)