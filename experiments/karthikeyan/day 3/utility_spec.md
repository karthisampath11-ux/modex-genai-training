# Utility Design Specification

## Utility Name

Chained Article Insight Generator

---

# 1. What does this utility do?

This utility analyzes an article or text using Gemini 2.5 Flash and performs prompt chaining to generate a summary followed by important follow-up questions for deeper understanding.

---

# 2. Who is the user and what problem does it solve?

## Target Users
- Students
- Researchers
- Developers
- Content readers
- Analysts

## Problem Solved

Long articles can be difficult and time-consuming to understand completely. This utility simplifies understanding by:
1. generating a concise summary
2. creating important analytical questions for further reading

This helps users quickly understand the main topic and explore deeper insights.

---

# 3. Input → Output Examples

## Example 1

### Input
Artificial Intelligence is transforming healthcare through predictive analytics and automation.

### Output
Summary:
AI is improving healthcare using automation and predictive systems.

Questions:
1. How does AI improve diagnosis?
2. What are predictive analytics?
3. What are the risks of AI in healthcare?

---

## Example 2

### Input
Cloud computing enables companies to scale infrastructure efficiently.

### Output
Summary:
Cloud computing helps businesses grow infrastructure flexibly.

Questions:
1. What are the advantages of cloud scalability?
2. How does cloud reduce infrastructure cost?
3. What are cloud security challenges?

---

## Example 3

### Input
Python is widely used in machine learning and automation.

### Output
Summary:
Python is popular for automation and machine learning tasks.

Questions:
1. Why is Python popular in AI?
2. Which Python libraries support machine learning?
3. How does Python help automation?

---

# 4. Will this utility use prompt chaining?

Yes.

## Prompt Chain Design

### Step 1 — Summary Generation

Input:
Original article/text

Prompt:
"Summarize the following text in 2–3 sentences."

Output:
Generated summary

↓

### Step 2 — Question Generation

Input:
Summary from Step 1

Prompt:
"Generate 5 important analytical questions from this summary."

Output:
List of key questions

---

# 5. What could go wrong?

## Edge Case 1 — Empty Input

Problem:
User provides no text.

Handling:
Validate input before sending request to Gemini.

---

## Edge Case 2 — Invalid API Key

Problem:
Gemini authentication failure.

Handling:
Show clear error message and stop execution safely.

---

## Edge Case 3 — Invalid JSON or Unexpected Response

Problem:
Gemini returns malformed or incomplete response.

Handling:
Use exception handling and validation before parsing.

---

## Edge Case 4 — API Rate Limits

Problem:
Too many Gemini requests in short time.

Handling:
Retry later using exponential backoff strategy.

---

# Final Design Goal

The utility demonstrates:
- prompt chaining
- sequential LLM workflows
- structured AI processing
- scalable GenAI engineering concepts