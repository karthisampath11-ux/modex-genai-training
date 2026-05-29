# Routing Decision — Hybrid Utility

## Day 3 Chain Steps

### Step 1 — Summarization
This step summarizes the input text.

- Task type: simple summarization
- Complexity: simple/repetitive
- Strict JSON needed: no
- Selected model: llama-3.1-8b-instant
- Reason: Llama is faster and good for simple summarization.

---

### Step 2 — Action Item / Structured Output Generation
This step creates structured action items from the summary.

- Task type: structured output generation
- Complexity: moderate
- Strict JSON needed: yes
- Selected model: gemini-2.5-flash-lite
- Reason: Gemini follows JSON and formatting instructions better.

---

## Final Routing Plan

- Step 1: Llama 3.1 8B Instant
- Step 2: Gemini 2.5 Flash-Lite