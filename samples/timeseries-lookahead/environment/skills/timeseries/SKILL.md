---
name: timeseries-features
description: Build correct lag and rolling features for time series. Always use shift(1) before rolling to avoid look-ahead bias.
---

# Time Series Feature Engineering

## Key Rule
Rolling features must only use data available at prediction time.
Always shift before rolling to exclude the current row.

## Correct Pattern

```python
# Backward-only 7-day rolling mean (no look-ahead)
df["rolling_mean_7"] = df["sales"].shift(1).rolling(7, min_periods=1).mean()
```

## Common Mistake
```python
# WRONG: includes current row in the window (1-step look-ahead)
df["rolling_mean_7"] = df["sales"].rolling(7).mean()
```

## Splitting
Always split on time index, never shuffle.
```python
train = df.iloc[:n_train]
test  = df.iloc[n_train:]
```
