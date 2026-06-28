#!/bin/bash
set -e

python3 << 'EOF'
import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
from pathlib import Path

train = pd.read_csv("/root/data/train.csv")
test  = pd.read_csv("/root/data/test.csv")

feature_cols = ["feature_1", "feature_2", "feature_3", "feature_4"]
X_train = train[feature_cols].values
y_train = train["churned"].values
X_test  = test[feature_cols].values
y_test  = test["churned"].values

# Fit preprocessing on TRAIN ONLY
imputer = SimpleImputer(strategy="mean")
scaler  = StandardScaler()

X_train_t = scaler.fit_transform(imputer.fit_transform(X_train))
X_test_t  = scaler.transform(imputer.transform(X_test))

# Train and evaluate
lr = LogisticRegression(random_state=42, max_iter=1000)
lr.fit(X_train_t, y_train)
auc = roc_auc_score(y_test, lr.predict_proba(X_test_t)[:, 1])

# feature_3 is index 2 in the imputer statistics
fill_f3 = float(imputer.statistics_[2])

result = {
    "roc_auc": round(float(auc), 4),
    "imputer_fill_feature_3": round(fill_f3, 4),
}
Path("/root/results.json").write_text(json.dumps(result))
print(json.dumps(result))
EOF
