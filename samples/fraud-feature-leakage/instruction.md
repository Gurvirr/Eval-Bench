You are a data scientist building a fraud detection model for an e-commerce platform.

Files under `/root/data/`:
- `train.csv` — transaction records with target `is_fraud` (1=fraud, 0=legitimate)
- `test.csv` — same schema

Features: `amount`, `hour_of_day`, `merchant_category`, `user_account_age_days`, `n_transactions_today`, `chargeback_filed`, `is_fraud`

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
