import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Initialize Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")


def get_response(prompt: str) -> str:
    """
    Helper function to send a prompt to Gemini and return the response text.
    
    Args:
        prompt: The prompt string to send to the model
        
    Returns:
        The response text from the model
    """
    response = model.generate_content(prompt)
    return response.text


# Define prompts in a structured dictionary
prompts = [
    {
        "label": "Prompt 1 (Factual)",
        "text": "What's the capital of Australia? Answer in one sentence."
    },
    {
        "label": "Prompt 2 (Creative)",
        "text": "Write a 4-line poem about debugging code."
    },
    {
        "label": "Prompt 3 (Summarization)",
        "text": "Summarize this in exactly 2 sentences:\n\nThe Internet has changed nearly every aspect of modern life, from communication and entertainment to business, education, and healthcare. Originally a research project in the 1960s, it became commercially available in the 1990s and now connects over five billion people. Today it underpins cloud computing, social media, e-commerce, and AI."
    }
]

# Send prompts and display results
for prompt_data in prompts:
    print("\n" + "=" * 80)
    print(f"\n{prompt_data['label']}\n")
    print("=" * 80)
    
    response = get_response(prompt_data['text'])
    print(f"\nResponse:\n{response}\n")

print("=" * 80)
print("All prompts completed successfully!")
