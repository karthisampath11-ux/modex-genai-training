from google import genai
from dotenv import load_dotenv
import os

# Load env
load_dotenv()

# API key
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)

print("Streaming Chatbot Started!")
print("Type 'exit' to stop.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Chat ended.")
        break

    print("AI: ", end="")

    # Stream response
    response = client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=user_input
    )

    for chunk in response:
        print(chunk.text, end="")

    print("\n")