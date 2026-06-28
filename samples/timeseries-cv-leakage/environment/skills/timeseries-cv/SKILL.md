---
name: timeseries-cv
description: Use TimeSeriesSplit for cross-validation on temporal data. KFold with shuffle destroys temporal ordering and leaks future data.
---

# Time Series Cross-Validation

## Key Rule
Never use KFold(shuffle=True) on time series data.
Always use TimeSeriesSplit to preserve temporal ordering.

## Correct Pattern

```python
from sklearn.model_selection import TimeSeriesSplit, cross_val_score

cv = TimeSeriesSplit(n_splits=5)
scores = cross_val_score(model, X, y, cv=cv, scoring="neg_mean_absolute_error")
```

## Why KFold Fails on Time Series
KFold randomly assigns rows to folds. With temporal data this means:
- Training fold may contain future data
- Test fold may contain past data the model was trained on
- This understates true out-of-sample error, especially with distribution shifts
