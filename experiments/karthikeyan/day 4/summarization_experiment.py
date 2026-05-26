import google.generativeai as genai
from dotenv import load_dotenv
import os
import time

# -----------------------------------
# LOAD API KEY
# -----------------------------------

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash-lite")

# -----------------------------------
# SAMPLE TEXT
# -----------------------------------

text = """
Artificial Intelligence is rapidly transforming industries through automation,
predictive analytics, customer support systems, and operational efficiency improvements.
Businesses are increasingly adopting AI technologies to reduce costs, improve scalability,
and enhance decision-making processes. However, challenges such as data privacy,
ethical concerns, and workforce adaptation remain important considerations.
"""

# -----------------------------------
# SAFE GENERATE
# -----------------------------------

def safe_generate(prompt):

    retries = 3

    for attempt in range(retries):

        try:
            response = model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:

            wait_time = 20 * (attempt + 1)

            print(f"\nRATE LIMIT HIT — Waiting {wait_time} seconds...\n")

            time.sleep(wait_time)

    return "API FAILED"

# -----------------------------------
# SHORT SUMMARY
# -----------------------------------

short_prompt = f"""
Summarize the following text in exactly 2 sentences.

TEXT:
{text}
"""

# -----------------------------------
# BULLET SUMMARY
# -----------------------------------

bullet_prompt = f"""
Summarize the following text as bullet points.

TEXT:
{text}
"""

# -----------------------------------
# EXECUTIVE SUMMARY
# -----------------------------------

executive_prompt = f"""
Write an executive-level summary for business leaders.

TEXT:
{text}
"""

# -----------------------------------
# TWEET SUMMARY
# -----------------------------------

tweet_prompt = f"""
Summarize the following text in under 280 characters.

TEXT:
{text}
"""

# -----------------------------------
# RUN TESTS
# -----------------------------------

print("\nRUNNING SUMMARIZATION EXPERIMENT\n")

print("=" * 60)
print("ORIGINAL TEXT:\n")
print(text)

# SHORT SUMMARY
print("\nSHORT SUMMARY:\n")

short_result = safe_generate(short_prompt)
print(short_result)

time.sleep(20)

# BULLET SUMMARY
print("\nBULLET SUMMARY:\n")

bullet_result = safe_generate(bullet_prompt)
print(bullet_result)

time.sleep(20)

# EXECUTIVE SUMMARY
print("\nEXECUTIVE SUMMARY:\n")

executive_result = safe_generate(executive_prompt)
print(executive_result)

time.sleep(20)

# TWEET SUMMARY
print("\nTWEET-LENGTH SUMMARY:\n")

tweet_result = safe_generate(tweet_prompt)
print(tweet_result)

print("\nEXPERIMENT COMPLETED")