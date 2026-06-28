#!/bin/bash
set -e

python3 << 'EOF'
import json
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
from pathlib import Path

train = pd.read_csv("/root/data/train.csv")
test  = pd.read_csv("/root/data/test.csv")

# Correct: exclude days_past_due — it is derived from future collection data
# and is not available at loan origination time (target leakage)
feature_cols = ["credit_score", "income", "loan_amount", "months_employed", "interest_rate"]
X_train, y_train = train[feature_cols].values, train["defaulted"].values
X_test,  y_test  = test[feature_cols].values,  test["defaulted"].values

sc = StandardScaler()
X_train_s = sc.fit_transform(X_train)
X_test_s  = sc.transform(X_test)

lr = LogisticRegression(random_state=42, max_iter=1000)
lr.fit(X_train_s, y_train)

auc = roc_auc_score(y_test, lr.predict_proba(X_test_s)[:, 1])
coefs = dict(zip(feature_cols, abs(lr.coef_[0])))
top_feature = max(coefs, key=coefs.get)

result = {
    "roc_auc": round(float(auc), 4),
    "most_predictive_feature": top_feature,
}
Path("/root/results.json").write_text(json.dumps(result))
print(json.dumps(result, indent=2))
EOF
