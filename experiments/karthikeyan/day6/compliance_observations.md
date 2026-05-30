# Compliance Observations
## Summary
I tested 5 inspection paragraphs using the ComplianceCheck schema.
The extraction worked and generated structured output with rule_id, status, evidence quotes, confidence and notes.
## What I Noticed
1.This schema was different from Event and Recipe schema.
2.In Event schema, the model only had to extract information.
3.In Recipe schema, it had to handle nested data.
4.But in Compliance schema, the model had to understand the meaning of the inspection paragraph and decide whether it was compliant, non-compliant or insufficient evidence.
## Output Review
1.For the compliant cases, the model was able to identify the correct rule and provide matching evidence from the paragraph.
2.For the non-compliant cases, the model correctly identified the issue and selected supporting evidence from the inspection text.
3.For the insufficient evidence case, the model understood that there was not enough proof to make a final compliance decision.
## Issue Faced
1.Initially I faced schema-related issues and Gemini rate-limit errors.
2.I also noticed that if the inspection text was not clear, the model could return different status values.
3.After fixing the file content and rerunning the extraction, the results were generated successfully.
## What I Learned
1.This schema feels closer to real compliance and Kavach type use cases.
The most important fields were:
 1.rule_id
 2.status
 3.evidence_quotes
 4.confidence
2.I learned that evidence quotes are very important because they provide justification for the compliance decision.
3.I also understood why schema validation is useful. Even if the model understands the paragraph, the output still needs to follow the expected structure.
## Final Observation
1.Event schema was the easiest.
2.Recipe schema was harder because of nested objects.
3.Compliance schema required more reasoning because the model had to decide the compliance status based on the inspection details.
4.Among all three schemas, ComplianceCheck felt most similar to a real-world compliance validation workflow.