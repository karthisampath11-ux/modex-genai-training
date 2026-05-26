import os
import argparse
from dotenv import load_dotenv
import google.generativeai as genai

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# --------------------------------------------------
# Configure Gemini
# --------------------------------------------------

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

# --------------------------------------------------
# Parse command-line arguments
# --------------------------------------------------

parser = argparse.ArgumentParser(
    description="Chained Gemini Utility"
)

parser.add_argument(
    "--text",
    required=True,
    help="Input article or paragraph"
)

args = parser.parse_args()

input_text = args.text

# --------------------------------------------------
# Gemini Call 1 → Generate Summary
# --------------------------------------------------

print("STEP 1: Generating summary...\n")

summary_prompt = f"""
Summarize the following text in 2-3 sentences.

Text:
{input_text}
"""

summary_response = model.generate_content(summary_prompt)

summary = summary_response.text.strip()

print("SUMMARY GENERATED:\n")
print(summary)

# --------------------------------------------------
# Gemini Call 2 → Generate Questions
# --------------------------------------------------

print("\nSTEP 2: Generating analytical questions...\n")

question_prompt = f"""
Based on the following summary,
generate 5 important analytical questions.

Summary:
{summary}
"""

question_response = model.generate_content(question_prompt)

questions = question_response.text.strip()

# --------------------------------------------------
# Final Output
# --------------------------------------------------

print("\nFINAL OUTPUT")
print("=" * 60)

print("\nINPUT TEXT:\n")
print(input_text)

print("\nSUMMARY:\n")
print(summary)

print("\nKEY QUESTIONS:\n")
print(questions)