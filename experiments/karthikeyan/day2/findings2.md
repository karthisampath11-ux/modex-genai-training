# Day 2 Findings

## What I Completed

- Built a JSON extractor using Gemini API.
- Created 3 prompt iterations:
  - json_extractor.py
  - json_extractor_v2.py
  - json_extractor_v3.py
- Saved outputs into text files.
- Completed Gemini Vision Test using office.jpg image.
- Tested 3 different image prompts.
- Built Compare Two Prompts Tool.
- Compared concise prompts vs detailed prompts.

---

## Key Learnings

### JSON Extraction
- Gemini can return structured JSON accurately.
- Prompt wording affects JSON formatting.
- Sometimes Gemini adds markdown formatting like ```json blocks.
- Cleaning the response before parsing helps avoid JSON errors.

### Vision Testing
- Gemini Vision can describe images very accurately.
- Different prompts produce different response styles:
  - detailed descriptions
  - object lists
  - captions

### Prompt Comparison
- Short prompts create concise answers.
- Detailed prompts create long explanatory answers.
- Prompt engineering strongly affects:
  - response quality
  - detail level
  - structure

---

## Problems Faced

- API quota exceeded multiple times (429 errors).
- Missing image file caused FileNotFoundError.
- JSON parsing initially failed because of markdown formatting.
- Incorrect Gemini SDK function caused AttributeError.

---

## Unclear Questions

1. When should gemini-2.5-flash-lite be preferred over flash?
2. What is the best way to enforce strict JSON output from Gemini?
3. How can prompt engineering reduce unnecessary long responses?

---

## Overall Reflection

Day 2 helped me understand:
- prompt engineering
- structured extraction
- vision capabilities
- response comparison techniques

I also learned how important debugging and prompt iteration are while working with AI APIs.