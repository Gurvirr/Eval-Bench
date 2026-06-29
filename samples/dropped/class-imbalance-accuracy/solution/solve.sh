#!/bin/bash
set -e

python3 << 'EOF'
import json
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from pathlib import Path

train = pd.read_csv("/root/data/train.csv")
test  = pd.read_csv("/root/data/test.csv")

feat = [f"f{i}" for i in range(5)]
X_tr, y_tr = train[feat].values, train["is_fraud"].values
X_te, y_te = test[feat].values,  test["is_fraud"].values

lr = LogisticRegression(random_state=42, max_iter=1000)
lr.fit(X_tr, y_tr)
y_pred = lr.predict(X_te)

prec    = precision_score(y_te, y_pred, zero_division=0)
rec     = recall_score(y_te, y_pred, zero_division=0)
f1      = f1_score(y_te, y_pred, zero_division=0)
auc     = roc_auc_score(y_te, lr.predict_proba(X_te)[:,1])
acc     = accuracy_score(y_te, y_pred)

# For a fraud detector: recall < 0.5 means majority of fraud goes undetected
# Not acceptable for a payment processor regardless of accuracy/precision
recommend = bool(rec >= 0.50 and f1 >= 0.30)

result = {
    "accuracy":            round(float(acc),  4),
    "precision_fraud":     round(float(prec), 4),
    "recall_fraud":        round(float(rec),  4),
    "f1_fraud":            round(float(f1),   4),
    "roc_auc":             round(float(auc),  4),
    "recommend_deployment": recommend,
}
Path("/root/results.json").write_text(json.dumps(result))
print(json.dumps(result, indent=2))
EOF
