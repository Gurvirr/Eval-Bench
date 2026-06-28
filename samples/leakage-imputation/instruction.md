You are a data scientist at a fintech company. Evaluate the churn prediction pipeline below.

All files are under `/root/data/`:
- `train.csv` — 800 rows, features `feature_1` through `feature_4`, target `churned` (0/1)
- `test.csv`  — 200 rows, same schema

Your task:
1. Impute missing values using the **mean** strategy (some values in `feature_3` are missing).
2. Standardize all feature columns (z-score: subtract mean, divide by std).
3. Train a logistic regression model on the training set.
4. Evaluate on the test set using **ROC-AUC**.
5. Save results to `/root/results.json`:

```json
{
  "roc_auc": 0.XXXX,
  "imputer_fill_feature_3": 0.XXXX
}
```

Where `imputer_fill_feature_3` is the fill value your imputer learned for `feature_3`.

Round both values to 4 decimal places.

**Important:** fit all preprocessing (imputer means, scaler parameters) on the **training set only**. Transform the test set using those fitted parameters — do not refit on test data.
