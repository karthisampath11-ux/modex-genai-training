import json
import os

from dotenv import load_dotenv
import google.generativeai as genai


# ---------------------------------------------------
# STEP 1: Configure Gemini
# ---------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found.")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")


# ---------------------------------------------------
# STEP 2: Sample Text Inputs
# ---------------------------------------------------

texts = [
    "Artificial Intelligence is improving healthcare.",
    "Python is one of the most popular programming languages.",
    "Cloud computing helps companies scale faster."
]


# ---------------------------------------------------
# STEP 3: Function to Process Text
# ---------------------------------------------------

def process_text(text):

    prompt = f"""
    Analyze the following text and return JSON with:
    - summary
    - sentiment
    - keywords

    Text:
    {text}

    Return JSON only.
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

print("Starting batch processing...\n")

for index, text in enumerate(texts, start=1):

    print(f"Processing Text {index}...")

    try:

        result = process_text(text)

        results.append({
            "input": text,
            "output": result
        })

        print("Completed.\n")

    except Exception as error:

        print(f"Error: {error}\n")


# ---------------------------------------------------
# STEP 5: Final Output
# ---------------------------------------------------

print("=" * 60)
print("FINAL BATCH OUTPUT")
print("=" * 60)

print(json.dumps(results, indent=4))