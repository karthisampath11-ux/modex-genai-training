import google.generativeai as genai
from dotenv import load_dotenv
import os
import time
import json

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

# -----------------------------------
# SAMPLE DATA
# -----------------------------------

samples = [
    """
    Product: Wireless Mouse
    Price: $25
    Category: Electronics
    Rating: 4.5 stars
    """,

    """
    Product: Running Shoes
    Price: $80
    Category: Footwear
    Rating: 4.2 stars
    """,

    """
    Product: Coffee Maker
    Price: $120
    Category: Home Appliances
    Rating: 4.7 stars
    """
]

# -----------------------------------
# BASIC PROMPT
# -----------------------------------

def basic_extraction(text):

    prompt = f"""
Extract the following information from the text:

- Product
- Price
- Category
- Rating

Return the result in JSON format.

TEXT:
{text}
"""

    response = safe_generate(prompt)
    return response.text.strip()


# -----------------------------------
# FEW SHOT PROMPT
# -----------------------------------

def few_shot_extraction(text):

    prompt = f"""
Example:

TEXT:
Product: Laptop
Price: $900
Category: Electronics
Rating: 4.8 stars

OUTPUT:
{{
    "product": "Laptop",
    "price": "$900",
    "category": "Electronics",
    "rating": "4.8 stars"
}}

Now extract information from this text:

TEXT:
{text}

OUTPUT:
"""

    response = safe_generate(prompt)
    return response.text.strip()


# -----------------------------------
# RETRY + BACKOFF
# -----------------------------------

def safe_generate(prompt):

    retries = 5

    for attempt in range(retries):

        try:
            response = model.generate_content(prompt)
            return response

        except Exception as e:

            print("\nRATE LIMIT HIT")

            wait_time = (attempt + 1) * 15

            print(f"Waiting {wait_time} seconds...\n")

            time.sleep(wait_time)

    raise Exception("API failed after retries")


# -----------------------------------
# RUN TESTS
# -----------------------------------

print("\nRUNNING EXTRACTION TESTS...\n")

for i, sample in enumerate(samples):

    print("=" * 60)
    print(f"SAMPLE {i+1}")

    print("\nINPUT:")
    print(sample)

    print("\nBASIC EXTRACTION:\n")
    basic_result = basic_extraction(sample)
    print(basic_result)

    time.sleep(20)

    print("\nFEW SHOT EXTRACTION:\n")
    few_shot_result = few_shot_extraction(sample)
    print(few_shot_result)

    print("\n")

    # Delay to avoid RPM limits
    time.sleep(25)
