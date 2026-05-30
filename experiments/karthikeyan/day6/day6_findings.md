# Day 6 Findings
## Overview
1.Today I learned how to work with structured outputs using Pydantic schemas and JSON extraction.
2.The main focus was creating schemas, extracting structured data from text, validating model responses, and improving reliability using retry logic.
## Tasks Completed
### Schema Creation
1.I created three Pydantic schemas:
 1.Event
 2.Recipe
 3.ComplianceCheck
These schemas helped ensure that the model outputs followed a fixed structure.
### Event Extraction
I built an event extraction program that reads article text and converts it into structured Event objects.
The extracted data included:

 1.title
 2.date
 3.location
 4.summary_line
All outputs were validated using the Event schema.
### Recipe Extraction
1.I created a recipe extraction workflow that converts recipe text into structured Recipe objects.
2.This helped me understand nested schemas because ingredients were stored as a list of objects.
3.I also learned how to validate quantities, units, and cooking steps.
### Compliance Extraction
I built a compliance extraction workflow using inspection paragraphs.
The model extracted:
 1.rule_id
 2.status
 3.evidence_quotes
 4.confidence
 5.notes
This exercise felt closer to a real-world compliance use case because the model had to understand the inspection text before generating structured output.
### Retry Wrapper
I implemented a retry wrapper to handle validation failures.
During testing, one compliance extraction returned evidence_quotes as a string instead of a list.
Pydantic validation detected the issue and the retry wrapper automatically retried the extraction.
The second attempt returned the correct format and the extraction completed successfully.
This helped me understand the importance of reliability handling in AI applications.
### Cross-Model Comparison
I compared Gemini and Llama using the Event schema.
Both models were able to generate valid JSON outputs.
Gemini was slightly more consistent and required less prompt guidance.
Llama also performed well when clear instructions were provided.
## Challenges Faced
1.Gemini free-tier rate limits caused temporary interruptions during testing.
2.Some responses required validation because fields were not always returned in the expected format.
3.Compliance extraction needed more careful prompting compared to event extraction.
## What I Learned
1.Today I learned that generating JSON alone is not enough.
2.The output should also be validated against a schema to ensure the structure is correct.
3.I also learned that retry mechanisms can improve reliability when the model returns invalid data.
4.Using schemas together with validation makes AI outputs more predictable and easier to use in applications.
## Kavach Relevance
1.The ComplianceCheck schema is the most useful example for Kavach-style workflows.
2.The combination of rule identification, evidence extraction, confidence scoring, and validation can be reused in future compliance and inspection systems.
## Final Conclusion
1.Day 6 helped me understand how structured outputs work in practical applications.
2.Using Pydantic schemas, validation checks, and retry mechanisms makes AI-generated data more reliable and easier to integrate into real-world workflows.