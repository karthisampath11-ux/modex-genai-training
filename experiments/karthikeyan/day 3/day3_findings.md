# Day 3 Findings

## Practical Tasks Completed

### 1. mini_utility.py
- Built a command-line AI utility using Gemini API
- Accepted user text input using argparse
- Generated:
  - summary
  - sentiment
  - keywords
- Returned structured JSON output

### 2. mini_utility_v2.py
- Improved code structure using functions
- Added exception handling
- Added reusable Gemini setup
- Improved JSON parsing and formatting

### 3. batch_processor.py
- Processed multiple text inputs using loops
- Implemented batch AI processing
- Aggregated multiple JSON outputs
- Added try-except error handling

### 4. batch_processor_v2.py
- Added timestamp logging
- Saved AI outputs into JSON file
- Implemented production-style workflow
- Generated persistent structured dataset

---

# Key Concepts Learned

## 1. Gemini API Integration
Connected Python applications with Gemini AI using API key configuration.

## 2. Prompt Engineering
Designed prompts to control:
- summaries
- sentiment analysis
- keyword extraction

## 3. JSON Processing
Converted Gemini responses into structured Python dictionaries.

## 4. Command-Line Utilities
Used argparse for dynamic terminal input.

## 5. Batch Processing
Automated processing of multiple AI requests using loops.

## 6. Error Handling
Used try-except blocks to prevent application crashes.

## 7. File Handling
Saved outputs into:
- .txt files
- .json files

## 8. Production Workflow
Simulated scalable AI processing pipelines.

---

# Output Files Generated

- mini_utility_output.txt
- mini_utility_v2_output.txt
- batch_processor_output.txt
- batch_results.json

---

# Overall Observation

Prompt quality and application structure significantly affect:
- output consistency
- response formatting
- scalability
- maintainability

Day 3 practicals provided hands-on experience in building structured GenAI utilities using Python and Gemini API.