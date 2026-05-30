# Retry Wrapper Observations
## Summary
1.I added the retry wrapper to extract_compliance.py and tested it with 5 inspection paragraphs.
2.The main purpose was to see whether the extraction process could recover automatically when the model returned data that did not match the schema.
## What I Observed
1.Most of the inspections worked correctly on the first attempt.
2.However, for one inspection, Gemini returned the evidence_quotes field as a string instead of a list.
Because of this, Pydantic validation failed and the extraction could not be completed on the first attempt.
3.The retry wrapper detected the validation error and automatically tried again.
4.On the second attempt, Gemini returned the correct format and the validation passed successfully.
## Result
1.All 5 inspection paragraphs were processed successfully.
2.The retry wrapper helped prevent the extraction from failing completely when the model returned an invalid structure.
3.The final output showed that all compliance checks were extracted successfully with zero failures.
## What I Learned
1.This exercise helped me understand why retry logic is important in structured output workflows.
2.Even when the model returns JSON, there is no guarantee that every field will follow the expected schema.
3.Pydantic validation helps identify these issues, and the retry wrapper provides an additional layer of reliability.
4.I also learned that retry mechanisms can improve the overall stability of schema-based applications.
## Final Observation
1.The retry wrapper worked as expected and successfully handled a real validation failure during testing.
2.This approach can be reused in future projects where structured JSON output and schema validation are important requirements.