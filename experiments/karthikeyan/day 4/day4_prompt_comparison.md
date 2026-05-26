# Day 4 — Prompt Comparison Notes

## Objective

Compare different prompting techniques and evaluate their strengths, weaknesses, and practical engineering tradeoffs.

---

# 1. Zero-Shot Prompting

## Definition
The model receives only the task instruction without examples.

## Example
"Classify the sentiment as Positive, Negative, or Neutral."

## Advantages
- Fast
- Low token cost
- Simple implementation
- Good for straightforward tasks

## Disadvantages
- Lower consistency
- More formatting variation
- Weak performance on ambiguous tasks

## Best Use Cases
- Simple classification
- Quick prototyping
- Low-cost inference systems

---

# 2. Few-Shot Prompting

## Definition
The model receives task instructions along with multiple examples.

## Example
Input/output sentiment examples before the actual task.

## Advantages
- Better consistency
- Improved formatting reliability
- Stronger task understanding

## Disadvantages
- Higher token usage
- More expensive
- Example quality strongly affects outputs

## Best Use Cases
- Structured outputs
- JSON extraction
- Controlled formatting tasks

---

# 3. Chain-of-Thought Prompting

## Definition
The model is instructed to reason step-by-step before answering.

## Example
"Analyze positive words, negative words, then decide sentiment."

## Advantages
- Better reasoning
- Improved complex problem solving
- More transparent logic

## Disadvantages
- Slower responses
- Higher token cost
- Sometimes overly verbose

## Best Use Cases
- Complex reasoning
- Multi-step decision tasks
- Analytical workflows

---

# 4. Prompt Engineering Observations

## Observation 1
Small wording changes significantly affected output quality.

## Observation 2
Explicit formatting instructions improved JSON consistency.

## Observation 3
Few-shot examples reduced hallucinated fields.

## Observation 4
Chain-of-thought improved reasoning accuracy but increased latency.

---

# 5. Production Engineering Learnings

## Reliability
Production AI systems require:
- retry logic
- caching
- rate-limit handling
- fallback strategies

## Cost Awareness
Long prompts increase:
- latency
- token usage
- API costs

## Scalability
Prompt design directly affects:
- throughput
- infrastructure cost
- user experience

---

# 6. Final Comparison Table

| Prompt Type | Accuracy | Speed | Token Cost | Reliability |
|---|---|---|---|---|
| Zero-Shot | Medium | Fast | Low | Medium |
| Few-Shot | High | Medium | Medium | High |
| Chain-of-Thought | High | Slow | High | Medium |

---

# Conclusion

Day 4 practicals demonstrated that prompt engineering is a balance between accuracy, cost, speed, consistency, and scalability. Different prompting techniques are useful for different production scenarios, and selecting the right approach depends on the engineering requirements of the application.