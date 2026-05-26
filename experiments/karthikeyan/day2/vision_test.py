import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

# Load environment variables from .env
load_dotenv()

# Read Gemini API key from environment
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY not found. Add it to your .env file or environment variables."
    )

# Configure the Google Generative AI SDK
genai.configure(api_key=api_key)

# Load the Gemini model for vision tasks
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# Load the image file
image_path = "office.jpg.png"
try:
    image = Image.open(image_path)
except FileNotFoundError:
    raise RuntimeError(f"Image file not found: {image_path}")

# Prompt variations for the image
prompts = [
    "Describe this image in detail.",
    "List all visible objects in the image.",
    "Write a professional caption for this image."
]

# Run prompts and print the responses
for i, prompt in enumerate(prompts, start=1):
    print("\n" + "=" * 60)
    print(f"PROMPT {i}")
    print("=" * 60)
    print("\nPrompt:")
    print(prompt)

    try:
        response = model.generate_content([prompt, image])
        print("\nResponse:")
        print(response.text)
    except Exception as err:
        print("\nError generating response:")
        print(err)
        break
