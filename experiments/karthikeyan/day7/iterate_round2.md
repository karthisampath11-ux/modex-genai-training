# Iteration Round 2
## What I Changed
1.In Round 2, I focused on improving rule ID extraction.
2.I noticed that the model was sometimes changing the original rule ID even though the compliance issue was identified correctly.
To reduce this problem, I added the following instructions to the prompt:
 1.Preserve the exact rule ID from the paragraph.
 2.Do not modify or replace rule IDs.
 3.If a section reference such as NBC-4.5.2 is present, return it exactly as written.
## Why I Made This Change
1.During the baseline evaluation, some cases failed because the model returned a different rule ID than the one mentioned in the input.
2.Since rule ID accuracy is important for compliance extraction, I wanted to make the prompt more specific.
## Results
## Evaluation Progress
Baseline Run:
 Score: 0.686
 Cases above 0.8: 7 out of 15
Round 1:
 Score: 0.732
 Cases above 0.8: 9 out of 15
Round 2:
 Score: 0.824
 Cases above 0.8: 12 out of 15
## What Improved
1.The model became better at keeping the original rule ID.
2.Cases involving section references and exact rule matching performed better after the prompt update.
3.The overall score increased and more cases crossed the 0.8 threshold.
## My Observation
1.This change was more effective than the Round 1 prompt update.
2.Adding clear instructions about preserving exact rule IDs helped improve the quality of extraction.
3.The model still makes mistakes in a few difficult cases, but the overall performance is much better compared to the baseline.
## Conclusion
1.Round 2 gave the best result so far.
2.The evaluation score improved from 0.686 to 0.824, and the number of high-scoring cases increased from 7 to 12.
3.This shows that small prompt improvements can have a noticeable impact on structured compliance extraction tasks.