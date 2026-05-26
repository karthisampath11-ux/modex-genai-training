from google import genai
from dotenv import load_dotenv
from PIL import Image
import os

# Load API key from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)

# Open image
image = Image.open("test.py.jpg")

# Send image + prompt
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        "Describe this image clearly.",
        image
    ]
)

# Print AI response
print("\nAI Response:\n")
print(response.text)