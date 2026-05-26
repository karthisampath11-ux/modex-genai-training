from google import genai
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# API key
api_key = os.getenv("GEMINI_API_KEY")

# Gemini client
client = genai.Client(api_key=api_key)

# Chat history
chat_history = []

# System personality
system_prompt = """
You are a friendly AI assistant.
You answer shortly and clearly.
You are helpful and polite.
"""

print("Personality AI Chatbot Started!")
print("Type 'exit' to stop.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Chat ended.")
        break

    # Store user message
    chat_history.append(f"User: {user_input}")

    # Combine everything
    full_prompt = system_prompt + "\n" + "\n".join(chat_history)

    # Generate response
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )

    ai_reply = response.text

    # Store AI reply
    chat_history.append(f"AI: {ai_reply}")

    print("AI:", ai_reply)
    print()