import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)

# Use lightweight model
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# Base task
task = "Explain Artificial Intelligence in simple terms."

# Prompt Version A
prompt_a = f"""
Answer briefly in 2 sentences.

Task:
{task}
"""

# Prompt Version B
prompt_b = f"""
Explain step-by-step with a real-world example.

Task:
{task}
"""

# Generate Response A
response_a = model.generate_content(prompt_a)

# Generate Response B
response_b = model.generate_content(prompt_b)

# Print Results
print("\n" + "=" * 70)
print("PROMPT A")
print("=" * 70)

print("\nPrompt:")
print(prompt_a)

print("\nResponse:")
print(response_a.text)

print("\n" + "=" * 70)
print("PROMPT B")
print("=" * 70)

print("\nPrompt:")
print(prompt_b)

print("\nResponse:")
print(response_b.text)

# Simple Comparison
print("\n" + "=" * 70)
print("COMPARISON OBSERVATIONS")
print("=" * 70)

print("""
1. Prompt A produced a short concise response.

2. Prompt B produced a detailed explanation with examples.

3. Prompt wording strongly affected:
   - response length
   - detail level
   - explanation style
""")