# Nesting Observations
## Summary
I tested 5 recipe inputs using Recipe schema.
Result:
Extracted 5 / 5 recipes successfully.
## What I Noticed
1.Recipe schema was little harder than Event schema.
2.Event schema had simple fields only like title, date, location and summary line.
3.But Recipe schema had nested fields like ingredients list and steps list.
4.Each ingredient also had separate values like name, quantity and unit.
## Issue I Faced
First time the model understood the recipe correctly but it did not follow the exact schema field names.
It gave fields like:
 1.recipe_name instead of title
 2.ingredient instead of name
 3.item instead of name
Because of this Pydantic validation failed.
## Fix I Did
1.I updated the prompt more clearly and mentioned exact field names.
2.I also added small normalization logic before validation to handle common wrong field names.
3.After that all 5 recipe outputs passed successfully.
## What I Learned
1.Nested schema is more difficult than flat schema.
2.Even small field name mismatch can fail the validation.
3.Pydantic helped me find exactly where the issue happened.
4.This will be useful for structured outputs and Kavach type tasks.