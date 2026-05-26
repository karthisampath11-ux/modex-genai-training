# Day 4 — Failure Mode Analysis

## Objective

Analyze weaknesses and failure cases observed during advanced prompting experiments.

---

# 1. Zero-Shot Prompt Weaknesses

## Observed Issues
- Sometimes returned inconsistent labels.
- Misclassified emotionally weak sentences.
- Short prompts occasionally lacked reasoning quality.

## Example Failure
Input:
"The service was okay."

Expected:
Neutral

Observed:
Positive (sometimes)

## Reason
The model interpreted "okay" as slightly positive.

---

# 2. Few-Shot Prompt Weaknesses

## Observed Issues
- Output quality depended heavily on example quality.
- Poor examples caused inconsistent formatting.
- Longer prompts increased token usage.

## Example Failure
If examples were too repetitive, the model copied patterns incorrectly.

## Reason
Few-shot prompting biases the model strongly toward examples.

---

# 3. Chain-of-Thought Weaknesses

## Observed Issues
- Responses became too verbose.
- Extra reasoning increased latency.
- Sometimes generated unnecessary analysis.

## Example Failure
Simple sentiment tasks produced overly detailed reasoning.

## Reason
Chain-of-thought encourages expanded reasoning behavior.

---

# 4. Extraction Prompt Weaknesses

## Observed Issues
- JSON formatting was inconsistent in basic prompts.
- Some outputs included extra explanations.
- Field naming occasionally varied.

## Example Failure
Returned:
"product_name"

instead of:
"product"

## Reason
Prompt instructions were not strict enough.

---

# 5. Summarization Prompt Weaknesses

## Observed Issues
- Tweet summaries sometimes exceeded character expectations.
- Executive summaries occasionally became too generic.
- Bullet summaries sometimes omitted important details.

## Reason
Different summary styles optimize for different goals.

---

# 6. API Reliability Issues

## Major Issue
Frequent Gemini API rate limits (429 errors).

## Impact
- Delayed testing
- Interrupted workflows
- Increased waiting time

## Engineering Solution Applied
- Retry logic
- Backoff waiting
- Reduced API calls
- Smaller datasets
- Safer execution pacing

---

# 7. Key Engineering Learnings

- Prompt wording significantly affects output quality.
- Few-shot prompting improves formatting consistency.
- Chain-of-thought improves reasoning but increases token cost.
- Production AI systems require retry handling.
- API quotas strongly influence system design decisions.

---

# Conclusion

# 8. Failure Categorization

## A. Prompt Issues

### Description
Failures caused by unclear, weak, or incomplete prompts.

### Examples
- Extraction prompts sometimes returned extra explanation text instead of pure JSON.
- Short classification prompts produced inconsistent labels.
- Tweet summaries occasionally exceeded requested limits.

### Root Cause
Prompt instructions were not strict or specific enough.

### Improvement Strategy
- Use clearer formatting instructions
- Add output constraints
- Use few-shot examples

---

## B. Data Issues

### Description
Failures caused by ambiguous or insufficient input data.

### Examples
- Sentences like "The service was okay" were interpreted differently.
- Very short inputs lacked emotional context.
- Minimal product descriptions reduced extraction reliability.

### Root Cause
Input data did not provide enough context for confident predictions.

### Improvement Strategy
- Provide richer context
- Use better-quality examples
- Preprocess ambiguous inputs

---

## C. Model Limitations

### Description
Failures caused by limitations of the LLM itself.

### Examples
- Occasional hallucinated fields in extraction tasks.
- Overly verbose chain-of-thought reasoning.
- Inconsistent formatting despite explicit instructions.

### Root Cause
LLMs are probabilistic systems and may not always follow instructions perfectly.

### Improvement Strategy
- Add validation layers
- Use structured output parsing
- Implement post-processing checks
- Use retry/reformatting systems

---

# Final Observation

Most failures observed during Day 4 practicals were a combination of:
- prompt design weaknesses
- ambiguous inputs
- natural limitations of large language models

This demonstrated that successful GenAI engineering requires both strong prompt design and robust system-level reliability handling.