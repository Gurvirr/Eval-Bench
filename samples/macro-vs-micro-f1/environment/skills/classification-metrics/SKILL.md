---
name: classification-metrics
description: Choose the right classification metric. Use macro F1 for imbalanced multiclass problems where minority classes matter equally.
---

# Classification Metrics

## When to use macro F1
- Multiclass problem with imbalanced classes
- Every class is equally important regardless of size
- Minority class failures must not be hidden by majority class performance

```python
from sklearn.metrics import f1_score
f1_macro = f1_score(y_test, y_pred, average='macro')
```

## Metric comparison
| Metric | Behaviour | Use when |
|--------|-----------|----------|
| accuracy | Dominated by majority class | Classes are balanced |
| f1_weighted | Weighted by class size | Class frequency reflects importance |
| f1_macro | Each class counts equally | Every class matters equally |
| f1_micro | = accuracy for multiclass | Same as accuracy |

## Warning
On an 80/10/6/4% class split, a model that always predicts the majority class
achieves 80% accuracy but 0% recall on minority classes.
Macro F1 will be ~0.22, revealing the true failure.
