# Day 2 Findings

## Task Completed
Built 3 versions of a structured JSON extractor using Gemini API.

Files created:
- json_extractor.py
- json_extractor_v2.py
- json_extractor_v3.py

Output files:
- json_extractor_output_v1.txt
- json_extractor_output_v2.txt
- json_extractor_output_v3.txt

---

# What I Learned

## Version 1
- Gemini sometimes returned JSON inside markdown code blocks.
- Direct JSON parsing failed.
- Needed cleanup before parsing.

## Version 2
- Better prompts improved output quality.
- Explicit formatting instructions reduced markdown wrapping.
- JSON parsing became more stable.

## Version 3
- Gemini handled more complex extraction tasks.
- Successfully extracted:
  - name
  - age
  - city
  - profession
  - company
  - experience
  - skills

---

# Key Observations

- Prompt clarity strongly affects output quality.
- Structured prompts produce cleaner JSON.
- LLM outputs are not always directly parseable.
- Output validation is important in production systems.

---

# Issues Faced

- API quota limits (429 RESOURCE_EXHAUSTED)
- JSON parsing errors
- Markdown formatting inside responses
- Environment variable loading issues

---

# Unclear Questions

1. What is the best production method to guarantee valid JSON from LLMs?

2. When should prompt engineering be preferred over post-processing cleanup?

3. How do enterprise systems handle rate limits and retries at scale?