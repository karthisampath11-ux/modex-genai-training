# Day 3 Testing Report

## 1. mini_utility.py Testing

### Test Case 1 — Normal Input

Input:
"AI improves healthcare."

Result:
- Summary generated successfully
- Sentiment identified correctly
- Keywords extracted successfully

Status:
PASS

---

### Test Case 2 — Empty Input

Input:
""

Result:
- argparse validation triggered correctly
- Program rejected empty command-line input
- Prevented invalid execution

Observed Error:
argument --text: expected one argument

Status:
PASS

---

### Test Case 3 — Long Input

Input:
Large paragraph text

Result:
- Program processed successfully
- Response time slightly increased
- JSON output remained valid

Status:
PASS

---

# 2. mini_utility_v2.py Testing

### Test Case 4 — Invalid API Key

Result:
- Authentication error displayed correctly
- Program did not crash unexpectedly

Status:
PASS

---

# 3. batch_processor.py Testing

### Batch Processing Validation

Result:
- All texts processed successfully
- Loop execution worked correctly
- Structured JSON outputs generated

Status:
PASS

---

# 4. batch_processor_v2.py Testing

### File Generation Validation

Result:
- batch_results.json created successfully
- Timestamps generated correctly
- Outputs saved properly

Status:
PASS

---

# Overall Testing Observation

The Day 3 utilities performed successfully under:
- normal conditions
- edge-case inputs
- batch workflows

Error handling improved application stability and prevented unexpected crashes.

---

# Final Status

All Day 3 practical utilities tested successfully.