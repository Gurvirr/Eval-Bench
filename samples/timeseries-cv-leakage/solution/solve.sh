#!/bin/bash
set -e

python3 << 'EOF'
import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from pathlib import Path

df = pd.read_csv("/root/data/sales.csv")
df["lag_1"] = df["sales"].shift(1)
df = df.dropna()

X = df[["lag_1", "day_of_week", "month"]].values
y = df["sales"].values

cv = TimeSeriesSplit(n_splits=5)
scores = -cross_val_score(LinearRegression(), X, y, cv=cv,
                          scoring="neg_mean_absolute_error")

result = {
    "cv_mean_mae": round(float(scores.mean()), 4),
    "cv_std_mae":  round(float(scores.std()),  4),
    "cv_method":   "TimeSeriesSplit",
}
Path("/root/results.json").write_text(json.dumps(result))
print(json.dumps(result, indent=2))
EOF
