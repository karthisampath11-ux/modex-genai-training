import os
import sys
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai

# Fix Unicode
sys.stdout.reconfigure(encoding='utf-8')

# Load API key
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini model
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# Load receipt image
image_path = "images/receipt.jpg"

print("\nOCR VS VLM COMPARISON\n")

try:
    img = Image.open(image_path)

    # OCR STYLE PROMPT
    ocr_prompt = """
    Extract ONLY the visible text from this receipt.
    Do not summarize.
    """

    # VLM UNDERSTANDING PROMPT
    vlm_prompt = """
    Analyze this receipt and explain:
    - Store name
    - Purchased items
    - Total amount
    - Type of business
    - Customer insights

    Give a meaningful understanding, not raw OCR.
    """

    print("=" * 60)
    print("OCR STYLE EXTRACTION\n")

    ocr_response = model.generate_content([ocr_prompt, img])

    print(ocr_response.text)

    print("\n" + "=" * 60)
    print("VLM UNDERSTANDING\n")

    vlm_response = model.generate_content([vlm_prompt, img])

    print(vlm_response.text)

except Exception as e:
    print(f"\nERROR: {e}")

print("\nCOMPARISON COMPLETED")