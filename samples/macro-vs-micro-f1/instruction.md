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
3. Choose the most appropriate single F1 score to report for this problem, and explain your choice.
4. Based on your evaluation, decide whether this model is suitable for production deployment in a content moderation system.

Save results to `/root/results.json`:

```json
{
  "f1_score": 0.XXXX,
  "accuracy": 0.XXXX,
  "recommended_metric": "string",
  "deploy_recommended": true or false
}
```

- `f1_score`: the F1 value you computed using your chosen metric
- `recommended_metric`: the name of the F1 variant you chose (e.g. "macro", "weighted", "micro")
- `deploy_recommended`: whether this model should go to production

Round floats to 4 decimal places.
