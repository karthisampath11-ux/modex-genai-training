from google import genai
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Create client
client = genai.Client(api_key=api_key)

# Different prompts
prompts = {
    "Factual": "What is Artificial Intelligence?",
    
    "Creative": "Write a short futuristic story about AI in 3 lines.",
    
    "Summarization": "Summarize this: Artificial Intelligence is a technology that enables machines to learn, reason, and solve problems like humans."
}

# Run prompts
for style, prompt in prompts.items():
    print("\n" + "="*50)
    print(f"{style} Prompt")
    print("="*50)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    print(response.text)