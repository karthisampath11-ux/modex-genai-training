# Prompt Experiment Comparison — Day 1

**Model Used**: gemini-2.5-flash  
**Date**: 2026-05-21

---

# Prompt 1 — Factual

| Category | Variation A | Variation B |
|---|---|---|
| Style | Direct answer | Detailed explanation |
| Length | Very short | Very long |
| Followed instructions | Yes | Partially |
| Reasoning included | No | Yes |
| Hallucinations | None | None |

## Observations
- Variation A answered quickly and directly.
- Variation B added unnecessary reasoning for a simple factual question.
- The step-by-step prompt caused the response to become overly verbose.

---

# Prompt 2 — Creative

| Category | Variation A | Variation B |
|---|---|---|
| Style | Simple poem | Detailed reasoning + poem |
| Creativity | Good | Higher |
| Length | Short | Very long |
| Followed instructions | Yes | Yes |
| Hallucinations | None | None |

## Observations
- Variation B explained the poem creation process in detail.
- The reasoning version produced a more polished poem.
- Step-by-step prompting improved creativity but increased response length significantly.

---

# Prompt 3 — Summarization

| Category | Variation A | Variation B |
|---|---|---|
| Style | Concise summary | Detailed reasoning + summary |
| Length | Short | Very long |
| Followed instructions | Yes | Partially |
| Reasoning included | No | Yes |
| Hallucinations | None | None |

## Observations
- Variation A followed the summarization instruction correctly.
- Variation B added unnecessary explanation before the summary.
- The reasoning prompt reduced conciseness.

---

# Overall Patterns I Noticed

- Step-by-step prompts significantly increased output length.
- Creative tasks benefited more from reasoning prompts.
- Simple factual tasks became unnecessarily verbose with reasoning instructions.
- Gemini followed formatting instructions well in most cases.

---

# Failure Modes

- Step-by-step prompts sometimes ignored concise response requirements.
- Responses became too long for simple tasks.
- Reasoning prompts may reduce efficiency for straightforward questions.

---

# What This Tells Me About Prompt Engineering

Prompt wording strongly affects Gemini's output style, length, and reasoning depth. Concise prompts work better for simple factual tasks, while reasoning prompts can improve creativity and explanation quality for complex or creative tasks.