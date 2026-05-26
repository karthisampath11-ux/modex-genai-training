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


# Define the base prompts (same as gemini_three_prompts.py)
base_prompts = [
    {
        "id": 1,
        "type": "Factual",
        "text": "What's the capital of Australia? Answer in one sentence."
    },
    {
        "id": 2,
        "type": "Creative",
        "text": "Write a 4-line poem about debugging code."
    },
    {
        "id": 3,
        "type": "Summarization",
        "text": "Summarize this in exactly 2 sentences:\n\nThe Internet has changed nearly every aspect of modern life, from communication and entertainment to business, education, and healthcare. Originally a research project in the 1960s, it became commercially available in the 1990s and now connects over five billion people. Today it underpins cloud computing, social media, e-commerce, and AI."
    }
]

# Prefix for Variation B (step-by-step reasoning)
reasoning_prefix = "Explain your reasoning step-by-step. Be thorough."


# Process each prompt with both variations
for prompt_data in base_prompts:
    prompt_id = prompt_data["id"]
    prompt_type = prompt_data["type"]
    base_text = prompt_data["text"]
    
    # Variation A: Original prompt
    print("\n" + "=" * 80)
    print(f"[Prompt {prompt_id} - Variation A]")
    print("=" * 80)
    print(f"\nType: {prompt_type}")
    print(f"\nPrompt:\n{base_text}\n")
    print("-" * 80)
    
    response_a = get_response(base_text)
    print(f"Response:\n{response_a}\n")
    
    # Variation B: With step-by-step reasoning prefix
    print("=" * 80)
    print(f"[Prompt {prompt_id} - Variation B]")
    print("=" * 80)
    print(f"\nType: {prompt_type} (with step-by-step reasoning)")
    
    # Combine base prompt with reasoning prefix
    enhanced_prompt = f"{reasoning_prefix}\n\n{base_text}"
    print(f"\nPrompt:\n{enhanced_prompt}\n")
    print("-" * 80)
    
    response_b = get_response(enhanced_prompt)
    print(f"Response:\n{response_b}\n")

print("=" * 80)
print("All prompt variations completed successfully!")
print("=" * 80)
