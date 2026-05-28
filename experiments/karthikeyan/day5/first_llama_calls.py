"""
first_llama_calls.py

Day 5 — Groq API Introduction + First Llama Calls

This script:
- Loads GROQ_API_KEY from the root .env file
- Connects to Groq API
- Sends 3 prompts to llama-3.1-8b-instant
- Measures latency
- Tracks token usage
- Prints total tokens and average latency
"""

from groq import Groq
from dotenv import load_dotenv
import os
import time


# Load .env from project root
load_dotenv()


# Create Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_llama(prompt: str):
    """
    Sends a prompt to Groq Llama model
    and returns response + metrics
    """

    start_time = time.perf_counter()

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=400,
        temperature=0
    )

    end_time = time.perf_counter()

    latency_ms = (end_time - start_time) * 1000

    text = response.choices[0].message.content

    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens

    return {
        "text": text,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "latency_ms": latency_ms
    }


def main():

    prompts = [
        (
            "Prompt 1 (Factual)",
            "What is the capital of Australia? Answer in one sentence."
        ),

        (
            "Prompt 2 (Summarization)",
            """Summarize this in exactly 2 sentences:

The Internet has changed nearly every aspect of modern life, from communication and entertainment to business, education, and healthcare. Originally a research project in the 1960s, it became commercially available in the 1990s and now connects over five billion people. Today it underpins cloud computing, social media, e-commerce, and AI."""
        ),

        (
            "Prompt 3 (JSON extraction)",
            """Extract a JSON object with fields {title, author, year} from this text:
'Sapiens by Yuval Noah Harari, published 2011 by Harper.'

Return ONLY valid JSON, no preamble, no markdown fences."""
        )
    ]

    total_input_tokens = 0
    total_output_tokens = 0
    total_latency = 0

    print("FIRST LLAMA CALLS TEST")
    print("=" * 60)

    for label, prompt in prompts:

        print(f"\n{label}")
        print("-" * 60)

        print("\nPROMPT:")
        print(prompt)

        result = ask_llama(prompt)

        print("\nRESPONSE:")
        print(result["text"])

        print("\nMETRICS:")
        print(f"Input Tokens: {result['input_tokens']}")
        print(f"Output Tokens: {result['output_tokens']}")
        print(f"Latency: {result['latency_ms']:.2f} ms")

        total_input_tokens += result["input_tokens"]
        total_output_tokens += result["output_tokens"]
        total_latency += result["latency_ms"]

        print("\n" + "=" * 60)

    average_latency = total_latency / len(prompts)

    print("\nFINAL SUMMARY")
    print("=" * 60)

    print(f"Total Input Tokens: {total_input_tokens}")
    print(f"Total Output Tokens: {total_output_tokens}")
    print(f"Total Tokens: {total_input_tokens + total_output_tokens}")
    print(f"Average Latency: {average_latency:.2f} ms")


if __name__ == "__main__":
    main()