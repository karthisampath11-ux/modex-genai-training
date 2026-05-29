import os
import time
from dotenv import load_dotenv
from groq import Groq


# LOAD ENV VARIABLES
load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")

if not groq_key:
    raise ValueError("GROQ_API_KEY missing in .env")


# CREATE CLIENT
client = Groq(
    api_key=groq_key
)


# FUNCTION
def ask_llama(prompt):

    start_time = time.perf_counter()

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    end_time = time.perf_counter()

    latency_ms = (end_time - start_time) * 1000

    return {
        "text": response.choices[0].message.content,
        "latency_ms": latency_ms
    }


# MAIN
def main():

    prompt = "Explain Artificial Intelligence in simple words."

    result = ask_llama(prompt)

    print("\nLLAMA RESPONSE")
    print("=" * 50)

    print(result["text"])

    print("\nLATENCY")
    print("=" * 50)

    print(f"{result['latency_ms']:.2f} ms")


if __name__ == "__main__":
    main()