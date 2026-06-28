---
name: stratified-analysis
description: Always stratify comparisons by potential confounders before drawing conclusions. Aggregate statistics can reverse direction when a confounder is uncontrolled (Simpson's Paradox).
---

# Stratified Analysis

## Key Rule
Before concluding A causes B, check whether a third variable C confounds the relationship.
Always compare groups within levels of potential confounders.

## Pattern

```python
# Don't just do this:
df.groupby("treatment")["outcome"].mean()

# Also do this:
df.groupby(["confounder", "treatment"])["outcome"].mean()
```

## Simpson's Paradox
An overall trend can reverse direction within every subgroup.
If overall drug rate > control rate, but within every severity group
drug rate < control rate — the subgroup analysis is correct.
The confounder (severity) drives the apparent overall benefit.
