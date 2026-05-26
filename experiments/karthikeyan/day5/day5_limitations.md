# Day 5 — Limitations & Challenges

## Technical Challenges
- Gemini API free-tier rate limits
- Unicode encoding errors in PowerShell
- Multiple API calls consuming quota quickly

## Model Limitations
- Occasional hallucinated details
- JSON formatting inconsistencies
- OCR struggles with unclear images

## Prompting Challenges
- Generic prompts produced weak outputs
- Extraction quality depended heavily on prompt clarity

## Engineering Learnings
- Need retry handling for production systems
- Need caching for repeated requests
- Need response validation for JSON extraction