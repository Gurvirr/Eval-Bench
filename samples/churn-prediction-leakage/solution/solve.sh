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

# Correct: exclude support_tickets_after_cancel -- filed after cancellation, not before
feature_cols = ["account_age_days","monthly_spend","n_logins_last30","n_features_used","plan_tier"]
X_train, y_train = train[feature_cols].values, train["churned"].values
X_test,  y_test  = test[feature_cols].values,  test["churned"].values

sc = StandardScaler()
lr = LogisticRegression(random_state=42, max_iter=1000)
lr.fit(sc.fit_transform(X_train), y_train)
auc = roc_auc_score(y_test, lr.predict_proba(sc.transform(X_test))[:,1])
top = feature_cols[abs(lr.coef_[0]).argmax()]

result = {"roc_auc": round(float(auc),4), "most_predictive_feature": top}
Path("/root/results.json").write_text(json.dumps(result))
print(json.dumps(result))
EOF
