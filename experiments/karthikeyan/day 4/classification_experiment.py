import google.generativeai as genai
import os
import time
from dotenv import load_dotenv
from google.api_core.exceptions import ResourceExhausted

# -----------------------------------
# LOAD API KEY
# -----------------------------------

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

# -----------------------------------
# DATASET
# -----------------------------------

dataset = [
    ("The movie was amazing and emotional.", "Positive"),
    ("Worst customer service ever.", "Negative"),
    ("The product arrived yesterday.", "Neutral"),
    ("I absolutely loved the performance.", "Positive"),
    ("The app crashes every time I open it.", "Negative"),
]

# -----------------------------------
# SAFE API CALL FUNCTION
# -----------------------------------

def safe_generate(prompt):

    while True:
        try:
            response = model.generate_content(prompt)
            return response.text.strip()

        except ResourceExhausted:
            print("\nRATE LIMIT HIT")
            print("Waiting 60 seconds before retrying...\n")
            time.sleep(60)

        except Exception as e:
            print(f"ERROR: {e}")
            return "Error"

# -----------------------------------
# ZERO SHOT
# -----------------------------------

def zero_shot(text):

    prompt = f"""
Classify the sentiment as:
Positive, Negative, or Neutral.

Text:
{text}

Return ONLY the label.
"""

    return safe_generate(prompt)

# -----------------------------------
# FEW SHOT
# -----------------------------------

def few_shot(text):

    prompt = f"""
Text: I love this product.
Sentiment: Positive

Text: This app is terrible.
Sentiment: Negative

Text: The meeting starts at 5 PM.
Sentiment: Neutral

Now classify:

Text:
{text}

Return ONLY the label.
"""

    return safe_generate(prompt)

# -----------------------------------
# CHAIN OF THOUGHT
# -----------------------------------

def chain_of_thought(text):

    prompt = f"""
Analyze step-by-step.

1. Identify positive words
2. Identify negative words
3. Identify neutral meaning

Then return final sentiment label.

Text:
{text}
"""

    result = safe_generate(prompt)

    if "Positive" in result:
        return "Positive"
    elif "Negative" in result:
        return "Negative"
    else:
        return "Neutral"

# -----------------------------------
# TESTING
# -----------------------------------

zero_correct = 0
few_correct = 0
cot_correct = 0

print("\nRUNNING PROMPT TESTS...\n")

for text, actual in dataset:

    print("=" * 60)
    print(f"TEXT: {text}")
    print(f"ACTUAL: {actual}")

    zero_result = zero_shot(text)
    print(f"ZERO-SHOT: {zero_result}")

    time.sleep(12)

    few_result = few_shot(text)
    print(f"FEW-SHOT: {few_result}")

    time.sleep(12)

    cot_result = chain_of_thought(text)
    print(f"CHAIN-OF-THOUGHT: {cot_result}")

    time.sleep(12)

    if zero_result == actual:
        zero_correct += 1

    if few_result == actual:
        few_correct += 1

    if cot_result == actual:
        cot_correct += 1

# -----------------------------------
# FINAL RESULTS
# -----------------------------------

total = len(dataset)

print("\n" + "=" * 60)
print("FINAL RESULTS")
print("=" * 60)

print(f"Zero-Shot Accuracy: {zero_correct}/{total}")
print(f"Few-Shot Accuracy: {few_correct}/{total}")
print(f"Chain-of-Thought Accuracy: {cot_correct}/{total}")