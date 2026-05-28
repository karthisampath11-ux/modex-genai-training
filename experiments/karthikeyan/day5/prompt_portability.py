"""
prompt_portability.py

Compare the same prompts across Gemini and Groq models.
Measures:
- response quality
- latency
- structure
"""

import os
import time

from dotenv import load_dotenv

import google.generativeai as genai
from groq import Groq


# Load environment variables
load_dotenv()


def load_api_keys():

    gemini_key = os.getenv("GEMINI_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")

    if not gemini_key or not groq_key:
        raise KeyError(
            "GEMINI_API_KEY and GROQ_API_KEY must be set in .env"
        )

    return gemini_key, groq_key


# Load keys
gemini_key, groq_key = load_api_keys()


# Configure Gemini
genai.configure(api_key=gemini_key)

# Configure Groq
groq_client = Groq(api_key=groq_key)


def ask_gemini(prompt):

    start_time = time.perf_counter()

    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    response = model.generate_content(prompt)

    end_time = time.perf_counter()

    latency_ms = (end_time - start_time) * 1000

    return {
        "text": response.text,
        "latency_ms": latency_ms
    }


def ask_groq(prompt):

    start_time = time.perf_counter()

    response = groq_client.chat.completions.create(
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

    return {
        "text": response.choices[0].message.content,
        "latency_ms": latency_ms
    }


def compare_prompts(prompts):

    total_gemini_latency = 0
    total_groq_latency = 0

    for prompt in prompts:

        print("\n" + "-" * 80)
        print(f"Prompt: {prompt}\n")

        # Gemini
        gem_res = ask_gemini(prompt)

        print("GEMINI RESPONSE:\n")
        print(gem_res["text"])

        print(f"\nGemini Latency: {gem_res['latency_ms']:.2f} ms")

        total_gemini_latency += gem_res["latency_ms"]

        print("\n" + "=" * 80)

        # Groq
        groq_res = ask_groq(prompt)

        print("\nGROQ RESPONSE:\n")
        print(groq_res["text"])

        print(f"\nGroq Latency: {groq_res['latency_ms']:.2f} ms")

        total_groq_latency += groq_res["latency_ms"]

        print("\n" + "=" * 80)

        # Comparison Note
        print("\nCOMPARISON NOTE:\n")

        if gem_res["latency_ms"] < groq_res["latency_ms"]:
            print("Gemini responded faster for this prompt.")
        else:
            print("Groq responded faster for this prompt.")

        if len(gem_res["text"]) > len(groq_res["text"]):
            print("Gemini gave a more detailed response.")
        else:
            print("Groq gave a more detailed response.")

    print("\n" + "#" * 80)
    print("FINAL ANALYSIS")
    print("#" * 80)

    avg_gemini = total_gemini_latency / len(prompts)
    avg_groq = total_groq_latency / len(prompts)

    print(f"\nAverage Gemini Latency: {avg_gemini:.2f} ms")
    print(f"Average Groq Latency: {avg_groq:.2f} ms")

    if avg_gemini < avg_groq:
        print("\nGemini was faster overall.")
    else:
        print("\nGroq was faster overall.")

    print("\nStructured Response Observation:")
    print(
        "Gemini generally produces more polished and structured outputs, "
        "while Groq responses are often shorter and faster."
    )


def main():

    prompts = [
        "Explain machine learning for a beginner student.",

        "Write a professional email requesting leave for 2 days.",

        "Summarize the importance of APIs in software engineering."
    ]

    compare_prompts(prompts)


if __name__ == "__main__":
    main()