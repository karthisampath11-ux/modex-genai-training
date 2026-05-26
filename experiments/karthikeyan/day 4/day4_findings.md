# Day 4 — Final Findings & Reflection

## Overview

Day 4 focused on advanced prompting techniques and practical experimentation using Gemini 2.5 Flash.

The work included:
- zero-shot prompting
- few-shot prompting
- chain-of-thought reasoning
- extraction systems
- summarization variants
- prompt failure analysis
- prompt comparison experiments

---

# 1. Most Effective Prompting Technique

## Few-Shot Prompting

Few-shot prompting produced the most reliable and consistent outputs.

### Benefits Observed
- Better formatting consistency
- Improved JSON reliability
- Stronger classification accuracy
- Reduced ambiguity

### Why It Worked Well
Providing examples helped the model better understand:
- expected structure
- task intent
- formatting requirements

---

# 2. Most Expensive Prompting Technique

## Chain-of-Thought Prompting

Chain-of-thought prompting generated:
- longer outputs
- higher token usage
- slower responses

### Tradeoff
Although reasoning quality improved, latency and API cost also increased significantly.

---

# 3. Most Common Failure Cases

## Observed Failures
- hallucinated fields
- inconsistent formatting
- instruction ignoring
- ambiguous interpretation
- excessive verbosity

### Example
Some extraction outputs added unnecessary explanation text instead of pure JSON.

---

# 4. Engineering Improvements Applied

To improve reliability:
- retry logic was added
- API backoff handling was implemented
- prompt wording was refined
- datasets were reduced to avoid quota exhaustion

---

# 5. API Reliability Learnings

## Major Challenge
Gemini free-tier rate limits interrupted experiments multiple times.

## Practical Solutions Used
- exponential backoff
- delayed requests
- reduced request frequency
- safer execution pacing

---

# 6. Most Important Learning

Prompt engineering is not only about writing prompts.

It also involves:
- reliability engineering
- cost optimization
- formatting control
- scalability planning
- production-safe API usage

---

# 7. Real-World Engineering Understanding

Production GenAI systems must carefully balance:
- speed
- quality
- token cost
- reliability
- scalability

Different prompting strategies are useful for different business requirements.

---

# 8. What I Would Improve Next Time

If repeating the experiments:
- I would optimize prompts further
- add caching earlier
- reduce unnecessary API calls
- benchmark prompts more systematically
- validate outputs programmatically

---

# Final Conclusion

Day 4 practicals demonstrated that advanced prompting is a core engineering skill in GenAI systems. Prompt design directly impacts model accuracy, output quality, cost, latency, and production reliability.

These experiments provided practical understanding of how real-world AI systems are designed, tested, debugged, and optimized.