---
name: imbalanced-classification
description: Evaluate classifiers on imbalanced datasets using precision, recall, and F1 on the minority class — not accuracy.
---

# Imbalanced Classification Evaluation

## Key Rule
On a 97/3 class split, a model that predicts ALL negatives achieves 97% accuracy.
Always evaluate the minority class separately using precision, recall, and F1.

## Required metrics for imbalanced binary classification

```python
from sklearn.metrics import classification_report, roc_auc_score

print(classification_report(y_test, y_pred))
auc = roc_auc_score(y_test, model.predict_proba(X_test)[:,1])
```

## Deployment decision rule
A fraud detection model is NOT useful if:
- recall_fraud == 0 (catches no fraud)
- f1_fraud < 0.10 (nearly useless on the target class)

High accuracy alone is never sufficient justification for deployment
on imbalanced problems.
