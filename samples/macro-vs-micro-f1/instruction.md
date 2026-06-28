You are a data scientist evaluating a multi-class content moderation classifier.

The model classifies content into 4 categories:
- `0` — safe
- `1` — spam
- `2` — harassment
- `3` — hate speech

Files under `/root/data/`:
- `train.csv` — features `feature_0` through `feature_5` and `label`
- `test.csv`  — same schema

Your task:
1. Train a logistic regression classifier on the training data.
2. Evaluate on the test set.
3. Report the appropriate F1 score for this problem, along with accuracy.

Save results to `/root/results.json`:

```json
{
  "f1_macro": 0.XXXX,
  "f1_weighted": 0.XXXX,
  "accuracy": 0.XXXX
}
```

Round all values to 4 decimal places.
