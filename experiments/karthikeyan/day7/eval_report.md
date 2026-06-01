# **Evaluation Report**



#### **Overview**



1. The purpose of this task was to evaluate the compliance extraction system and improve its performance through prompt iterations.
2. To do this, I created a golden dataset with 15 manually written examples. The dataset included normal cases, edge cases, and a few challenging examples to test the model more thoroughly.
3. An evaluation harness was used to compare the model output against the expected output using weighted scoring.



# **Evaluation Setup**

##### **Model Used:**

\- Gemini 2.5 Flash Lite

##### **Dataset:**

\- 15 manually created compliance extraction examples

#### **Scoring Criteria:**

\- Rule ID: 40%

\- Status: 30%

\- Evidence Quotes: 20%

\- Confidence: 10%

# **Baseline Evaluation**



1. The first evaluation produced a score of 0.686.
2. Out of 15 test cases, 7 cases scored above 0.8.
3. After reviewing the failures, I found that most issues were related to incorrect rule ID extraction, confusion when multiple rules appeared in the same paragraph, and a few cases where the expected answer itself could be interpreted differently.

# **Iteration Round 1**



1. For the first improvement round, I focused on the prompt issue.
2. I updated the prompt to tell the model to select the rule that is directly connected to the violation instead of automatically choosing the first rule mentioned in the paragraph.
3. Result:
- Score improved from 0.686 to 0.732.
- Cases above 0.8 increased from 7 to 9.
4. This showed that clearer instructions helped the model make better decisions in multi-rule scenarios.



# **Iteration Round 2**



For the second improvement round, I focused on rule ID accuracy.

I added instructions asking the model to preserve the exact rule ID from the input and avoid changing or replacing rule references.

Result:

\- Score improved from 0.732 to 0.824.

\- Cases above 0.8 increased from 9 to 12.

This was the most effective change and reduced several rule ID related errors.



# **Evaluation Progress**



1. The baseline evaluation achieved a score of 0.686 with 7 out of 15 cases scoring above 0.8.
2. After the first prompt update, the score increased to 0.732 and 9 out of 15 cases scored above 0.8.
3. After the second prompt update, the score increased further to 0.824 with 12 out of 15 cases scoring above 0.8.



# **Key Learnings**



1. Clear prompt instructions improve extraction quality.
2. Multiple rules in a single paragraph can confuse the model.
3. Preserving exact rule IDs is important for compliance extraction tasks.
4. Challenging and adversarial examples are still harder than normal cases.
5. Some examples may require clearer labeling because more than one interpretation is possible.



# **Conclusion**



1. This evaluation helped me understand the strengths and weaknesses of the extraction system.
2. Through two prompt improvements, the overall score increased from 0.686 to 0.824, and the number of high-scoring cases increased from 7 to 12.
3. The final version performs better than the baseline and produces more reliable compliance extraction results.

