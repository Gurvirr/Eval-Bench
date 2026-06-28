#!/bin/bash
set -e

python3 << 'EOF'
import json
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, accuracy_score
from pathlib import Path

train = pd.read_csv("/root/data/train.csv")
test  = pd.read_csv("/root/data/test.csv")

feature_cols = [f"feature_{i}" for i in range(6)]
X_train, y_train = train[feature_cols].values, train["label"].values
X_test,  y_test  = test[feature_cols].values,  test["label"].values

lr = LogisticRegression(random_state=42, max_iter=2000, C=0.1)
lr.fit(X_train, y_train)
y_pred = lr.predict(X_test)

result = {
    "f1_macro":    round(float(f1_score(y_test, y_pred, average="macro")),    4),
    "f1_weighted": round(float(f1_score(y_test, y_pred, average="weighted")), 4),
    "accuracy":    round(float(accuracy_score(y_test, y_pred)),               4),
}
Path("/root/results.json").write_text(json.dumps(result))
print(json.dumps(result, indent=2))
EOF
