import os
import time
import json
from dotenv import load_dotenv

import google.generativeai as genai
from groq import Groq


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

if not gemini_key or not groq_key:
    raise ValueError("GEMINI_API_KEY or GROQ_API_KEY missing in .env")


# --------------------------------------------------
# CONFIGURE CLIENTS
# --------------------------------------------------

genai.configure(api_key=gemini_key)

groq_client = Groq(
    api_key=groq_key
)


# --------------------------------------------------
# GEMINI FUNCTION
# --------------------------------------------------

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


# --------------------------------------------------
# GROQ FUNCTION
# --------------------------------------------------

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
        temperature=0
    )

    end_time = time.perf_counter()

    latency_ms = (end_time - start_time) * 1000

    return {
        "text": response.choices[0].message.content,
        "latency_ms": latency_ms
    }


# --------------------------------------------------
# EVALUATION PROMPTS
# --------------------------------------------------

evaluation_prompts = {
    "FACTUAL": "What is the capital of France? Answer in one sentence.",

    "SUMMARIZATION":
    """
    Summarize this paragraph in 2 sentences:

    Artificial Intelligence is transforming industries by automating tasks,
    improving efficiency, and enabling data-driven decision making.
    AI systems are used in healthcare, finance, education,
    transportation, and many other fields.
    """,

    "EMAIL WRITING":
    """
    Write a professional leave request email for taking 2 days leave
    due to personal reasons.
    """,

    "JSON EXTRACTION":
    """
    Extract the following information into JSON format:

    Name: John Doe
    Age: 28
    City: New York
    Profession: Software Engineer
    """,

    "REASONING":
    """
    A farmer has 17 sheep. All but 9 die.
    How many sheep are left?
    """
}


# --------------------------------------------------
# EVALUATION FUNCTION
# --------------------------------------------------

def evaluate_models():

    results = []

    for category, prompt in evaluation_prompts.items():

        print("\n" + "=" * 70)
        print(f"Running category: {category}")
        print("=" * 70)

        # Gemini
        gemini_result = ask_gemini(prompt)

        # Groq
        groq_result = ask_groq(prompt)

        result = {
            "category": category,

            "gemini_response": gemini_result["text"],
            "gemini_latency_ms": round(
                gemini_result["latency_ms"], 2
            ),

            "groq_response": groq_result["text"],
            "groq_latency_ms": round(
                groq_result["latency_ms"], 2
            )
        }

        results.append(result)

        print("\nGEMINI RESPONSE:")
        print(gemini_result["text"])

        print("\nGemini Latency:")
        print(f"{gemini_result['latency_ms']:.2f} ms")

        print("\nGROQ RESPONSE:")
        print(groq_result["text"])

        print("\nGroq Latency:")
        print(f"{groq_result['latency_ms']:.2f} ms")

    return results


# --------------------------------------------------
# SAVE RESULTS
# --------------------------------------------------

def save_results(results):

    with open("evaluation_results.txt", "w", encoding="utf-8") as f:

        for item in results:

            f.write("=" * 70 + "\n")
            f.write(f"CATEGORY: {item['category']}\n")
            f.write("=" * 70 + "\n\n")

            f.write("GEMINI RESPONSE:\n")
            f.write(item["gemini_response"] + "\n\n")

            f.write(
                f"Gemini Latency: "
                f"{item['gemini_latency_ms']} ms\n\n"
            )

            f.write("GROQ RESPONSE:\n")
            f.write(item["groq_response"] + "\n\n")

            f.write(
                f"Groq Latency: "
                f"{item['groq_latency_ms']} ms\n\n"
            )

    with open("evaluation_results.json", "w", encoding="utf-8") as jf:
        json.dump(results, jf, indent=4)

    print("\nResults saved successfully.")


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    print("\nMULTI-MODEL EVALUATION REPORT")
    print("=" * 70)

    results = evaluate_models()

    save_results(results)

    print("\nEvaluation completed successfully.")


if __name__ == "__main__":
    main()


