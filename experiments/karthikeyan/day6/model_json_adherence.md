# Model JSON Adherence Comparison
## Objective
1.The purpose of this test was to compare how Gemini and Llama handle structured JSON outputs when extracting Event data from the same set of articles.
2.Both models were tested using the Event schema and the outputs were validated using Pydantic.
## Test Results
1.I ran both models on the same 5 articles.
### Gemini
 1.Successfully extracted all 5 events.
 2.Returned valid JSON for every article.
 3.Followed the schema structure correctly.
 4.No manual correction was required.
Result: 5 / 5 successful extractions
### Llama
 1.Successfully extracted all 5 events.
 2.Returned JSON in the expected format.
 3.Followed the required schema fields.
 4.Validation passed for all test cases.
Result: 5 / 5 successful extractions
## Observations
1.For the Event schema, both models performed well and produced valid structured outputs.
2.Gemini responses were slightly more consistent and required less prompt guidance.
3.Llama also generated good results, but the prompt needed to clearly specify the required JSON structure.
4.Since the Event schema is a simple flat schema, both models handled it without major issues.
## What I Learned
1.Structured output quality improves when the expected schema is clearly defined.
2.Pydantic validation is useful because it quickly identifies missing fields or incorrect formats.
3.Both Gemini and Llama can be used for schema-based extraction tasks, but Gemini provides stronger support for structured output generation.
## Final Finding
1.For simple extraction tasks, both Gemini and Llama produced reliable JSON outputs.
2.For larger workflows involving nested schemas and compliance-style extraction, Gemini appeared more consistent and required less validation handling.