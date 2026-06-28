---
name: sklearn-pipeline
description: Build correct train/test ML pipelines with sklearn. Always fit preprocessing on train only, then transform test.
---

# Sklearn Pipeline

## Key Rule
Fit all preprocessing (imputers, scalers, encoders) on training data only.
Apply fitted transformers to test data — never refit.

## Correct Pattern

```python
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="mean")),
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression()),
])
pipe.fit(X_train, y_train)
proba = pipe.predict_proba(X_test)[:, 1]
```

## Common Mistake
Using `fit_transform` on the full dataset before splitting, or calling `.fit()` on test data.
