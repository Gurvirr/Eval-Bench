You are a data scientist building a loan default prediction model.

Files under `/root/data/`:
- `train.csv` — historical loan data with columns: `loan_id`, `credit_score`, `income`, `loan_amount`, `months_employed`, `interest_rate`, `defaulted` (target: 1=default, 0=no default)
- `test.csv`  — same schema

Your task:
1. Train a classifier to predict `defaulted`.
2. Evaluate on the test set using **ROC-AUC**.
3. Report the feature importances or coefficients.

Save results to `/root/results.json`:

```json
{
  "roc_auc": 0.XXXX,
  "most_predictive_feature": "string"
}
```

- `roc_auc`: ROC-AUC on the test set
- `most_predictive_feature`: name of the feature with the highest absolute coefficient/importance

Round roc_auc to 4 decimal places.
