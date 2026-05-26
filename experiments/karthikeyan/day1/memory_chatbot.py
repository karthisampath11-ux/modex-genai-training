from google import genai
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)

# Store chat history
chat_history = []

print("Memory AI Chatbot Started!")
print("Type 'exit' to stop.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Chat ended.")
        break

    # Add user message
    chat_history.append(f"User: {user_input}")

    # Create full conversation
    full_prompt = "\n".join(chat_history)

    # Send to Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )

    ai_reply = response.text

    # Store AI reply
    chat_history.append(f"AI: {ai_reply}")

    # Print AI response
    print("AI:", ai_reply)
    print()