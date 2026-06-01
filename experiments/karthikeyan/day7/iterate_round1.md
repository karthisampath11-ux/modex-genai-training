# Iteration Round 1
## Target Category
PROMPT ISSUE
## Change Made
For this iteration, I focused on the prompt issue identified during the baseline evaluation.
I added two instructions to the prompt:
 1.If multiple rules are mentioned, choose the rule that is directly related to the violation or missing evidence.
 2.Do not automatically select the first rule mentioned.
## Reason for the Change
During the baseline analysis, I noticed that the model struggled when a paragraph contained more than one rule.
In Case 12, the model selected the first rule it saw instead of the rule connected to the actual compliance issue.
To reduce this confusion, I added a more specific instruction to guide rule selection.
## Results

 1.Baseline Score: 0.686
 2.Round 1 Score: 0.732
 3.Improvement: +0.046
Cases scoring 0.8 or higher:
  Before: 7/15
  After: 9/15
## Observations
 1.The updated prompt improved the overall performance of the model.
 2.The model handled multi-rule scenarios better compared to the baseline run.
 3.The increase in score shows that providing clearer instructions can improve extraction quality.
## Conclusion
 1.This prompt modification had a positive impact on the evaluation results.
 2.Although the improvement was not very large, it helped reduce some of the errors related to rule selection.
 3.Further improvements are still needed, especially for exact rule ID extraction and section-based rule references.