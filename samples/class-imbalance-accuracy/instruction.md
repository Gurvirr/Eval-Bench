You are a data scientist evaluating a fraud detection model for a payment processor.

Files under `/root/data/`:
- `train.csv` — features `f0`–`f4` and target `is_fraud` (1=fraud, 0=legitimate)
- `test.csv`  — same schema

Your task:
1. Train a logistic regression model on the training data.
2. Evaluate it thoroughly on the test set.
3. Decide whether to recommend this model for production deployment at a payment processor where catching fraud is the primary objective.

Save results to `/root/results.json`:

```json
{
  "accuracy": 0.XXXX,
  "precision_fraud": 0.XXXX,
  "recall_fraud": 0.XXXX,
  "f1_fraud": 0.XXXX,
  "roc_auc": 0.XXXX,
  "recommend_deployment": true or false
}
```

Round all float values to 4 decimal places.
