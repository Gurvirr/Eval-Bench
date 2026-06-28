You are a data scientist evaluating a multi-class text classifier for a content moderation system.

The model must classify content into 4 categories:
- `0` — safe (majority class)
- `1` — spam
- `2` — harassment
- `3` — hate speech (rare but critical to detect)

Files under `/root/data/`:
- `train.csv` — training set with columns `feature_0` through `feature_5` and `label`
- `test.csv`  — test set, same schema

Your task:
1. Train a logistic regression classifier on the training data.
2. Evaluate on the test set.
3. Report the **macro-averaged F1 score** — this is the correct metric for imbalanced multiclass problems where each class must be treated equally regardless of size.

Save results to `/root/results.json`:

```json
{
  "f1_macro": 0.XXXX,
  "f1_weighted": 0.XXXX,
  "accuracy": 0.XXXX
}
```

Round all values to 4 decimal places.

**Important:** the primary metric for this system is `f1_macro` (macro-averaged F1), not accuracy or weighted F1. The system must perform well on minority classes (harassment, hate speech), not just on the dominant "safe" category.
