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

# Correct: exclude chargeback_filed -- filed after fraud, not available at transaction time
feature_cols = ["amount","hour_of_day","merchant_category","user_account_age_days","n_transactions_today"]
X_train, y_train = train[feature_cols].values, train["is_fraud"].values
X_test,  y_test  = test[feature_cols].values,  test["is_fraud"].values

sc = StandardScaler()
lr = LogisticRegression(random_state=42, max_iter=1000)
lr.fit(sc.fit_transform(X_train), y_train)
auc = roc_auc_score(y_test, lr.predict_proba(sc.transform(X_test))[:,1])
top = feature_cols[abs(lr.coef_[0]).argmax()]

result = {"roc_auc": round(float(auc),4), "most_predictive_feature": top}
Path("/root/results.json").write_text(json.dumps(result))
print(json.dumps(result))
EOF
