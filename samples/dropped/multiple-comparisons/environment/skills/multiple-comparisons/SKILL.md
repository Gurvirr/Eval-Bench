---
name: multiple-comparisons
description: Apply multiple comparison corrections when running many simultaneous hypothesis tests. With k tests at alpha=0.05, expect ~k*0.05 false positives by chance.
---

# Multiple Comparisons Correction

## Key Rule
With k simultaneous tests at alpha=0.05, expect k*0.05 false positives.
Always apply a correction when running >5 tests simultaneously.

## Bonferroni Correction (conservative)

```python
from statsmodels.stats.multitest import multipletests

reject, p_corrected, _, _ = multipletests(p_values, alpha=0.05, method="bonferroni")
# Equivalent to: p < 0.05/k
```

## FDR Correction (less conservative, controls false discovery rate)

```python
reject, p_corrected, _, _ = multipletests(p_values, alpha=0.05, method="fdr_bh")
```

## Expected false positives without correction
- 10 tests → ~0.5 false positives
- 50 tests → ~2.5 false positives  ← this task
- 100 tests → ~5 false positives
