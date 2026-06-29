---
name: cohort-analysis
description: Compute cohort retention tables from user activity data. Month N retention = % of cohort active exactly N months after signup.
---

# Cohort Retention

## Key Rule
Retention at month N = users active in EXACTLY month N / cohort size.
Not cumulative — a user active in month 2 but not month 1 still counts for month 2 retention.

## Pattern

```python
import pandas as pd

df = pd.read_csv("/root/data/cohort_jan.csv")

# Parse comma-separated active_months
df["months"] = df["active_months"].apply(
    lambda x: set(x.split(",")) if pd.notna(x) and x else set()
)

n = len(df)
for offset in range(4):
    target = f"2024-{1 + offset:02d}"  # adjust base month per cohort
    active = df["months"].apply(lambda m: target in m).sum()
    print(f"month_{offset}: {active/n:.4f}")
```
