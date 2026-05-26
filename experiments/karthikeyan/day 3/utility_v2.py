import google.generativeai as genai
import os
import argparse
import json
import time
from dotenv import load_dotenv

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

# -----------------------------
# Configure Gemini API
# -----------------------------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# -----------------------------
# Use Gemini 2.5 Flash
# -----------------------------
model = genai.GenerativeModel("gemini-2.5-flash")

# -----------------------------
# Simple In-Memory Cache
# -----------------------------
cache = {}


# -----------------------------
# Retry Function with Backoff
# -----------------------------
def generate_with_retry(prompt, retries=3, delay=2):

    for attempt in range(retries):

        try:
            response = model.generate_content(prompt)
            return response.text

        except Exception as error:

            print(f"\nAPI Error: {error}")

            if attempt < retries - 1:

                wait_time = delay * (2 ** attempt)

                print(f"Retrying in {wait_time} seconds...\n")

                time.sleep(wait_time)

            else:
                return "ERROR: Failed after multiple retries."


# -----------------------------
# Step 1: Generate Summary
# -----------------------------
def generate_summary(input_text):

    summary_prompt = f"""
Summarize the following text in 3 concise sentences.

Text:
{input_text}
"""

    return generate_with_retry(summary_prompt)


# -----------------------------
# Step 2: Generate Questions
# -----------------------------
def generate_questions(summary_text):

    question_prompt = f"""
Based on the summary below,
generate 5 analytical questions.

Summary:
{summary_text}
"""

    return generate_with_retry(question_prompt)


# -----------------------------
# Main Program
# -----------------------------
def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--text",
        required=True,
        help="Input text for analysis"
    )

    args = parser.parse_args()

    input_text = args.text.strip()

    # -----------------------------
    # Input Validation
    # -----------------------------
    if not input_text:

        print("ERROR: Empty input provided.")
        return

    # -----------------------------
    # FIRST REQUEST
    # -----------------------------
    print("\nFIRST REQUEST\n")

    if input_text in cache:

        print("CACHE HIT: Returning saved result.\n")

        final_output = cache[input_text]

    else:

        print("STEP 1: Generating summary...\n")

        summary = generate_summary(input_text)

        print("SUMMARY GENERATED:\n")
        print(summary)

        print("\nSTEP 2: Generating analytical questions...\n")

        questions = generate_questions(summary)

        final_output = {
            "input": input_text,
            "summary": summary,
            "questions": questions
        }

        # Save result in cache
        cache[input_text] = final_output

    # -----------------------------
    # FINAL OUTPUT
    # -----------------------------
    print("\nFINAL OUTPUT")
    print("=" * 60)

    print(json.dumps(final_output, indent=4))

    # -----------------------------
    # SECOND REQUEST (CACHE TEST)
    # -----------------------------
    print("\nSECOND REQUEST (Same Input)\n")

    if input_text in cache:

        print("CACHE HIT: Returning saved result instantly.\n")

        cached_output = cache[input_text]

        print(json.dumps(cached_output, indent=4))


# -----------------------------
# Run Program
# -----------------------------
if __name__ == "__main__":
    main()