import os
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini model
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# Image folder
IMAGE_FOLDER = "images"

# Image list
images = [
    "building.jpg",
    "infographic.jpg",
    "ui.jpg",
    "nature.jpg",
    "receipt.jpg"
]

print("\nRUNNING IMAGE DESCRIPTION TESTS...\n")

for image_name in images:

    print("=" * 60)
    print(f"IMAGE: {image_name}")

    image_path = os.path.join(IMAGE_FOLDER, image_name)

    try:
        img = Image.open(image_path)

        prompt = """
        Describe this image in detail.
        Mention:
        - Main objects
        - Scene/environment
        - Text if visible
        - Overall purpose of image
        """

        response = model.generate_content([prompt, img])

        print("\nDESCRIPTION:\n")
        print(response.text)

    except Exception as e:
        print(f"\nERROR: {e}")

print("\nALL IMAGE TESTS COMPLETED")