from google import genai
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

# Create client
client = genai.Client(api_key=api_key)

# Send request
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say hello in one sentence."
)

# Print response
print("Gemini says:")
print(response.text)