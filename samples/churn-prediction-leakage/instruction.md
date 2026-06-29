You are a data scientist at a SaaS company building a churn prediction model.

Files under `/root/data/`:
- `train.csv` — customer records with features and target `churned` (1=churned, 0=active)
- `test.csv` — same schema

Features: `account_age_days`, `monthly_spend`, `n_logins_last30`, `n_features_used`, `plan_tier`, `support_tickets_after_cancel`, `churned`

Train a logistic regression classifier and evaluate on the test set.

Save results to `/root/results.json`:

```json
{
  "roc_auc": 0.XXXX,
  "most_predictive_feature": "string"
}
```

- `roc_auc`: ROC-AUC on the test set
- `most_predictive_feature`: feature with highest absolute coefficient

Round roc_auc to 4 decimal places.
