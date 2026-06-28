#!/bin/bash
set -e

python3 << 'EOF'
import json
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from pathlib import Path

df = pd.read_csv("/root/data/sales.csv")

# Correct: shift(1) then rolling — strictly backward, current row NOT included
df["rolling_mean_7"] = df["sales"].shift(1).rolling(7, min_periods=1).mean()

# Split on row index (first 365 = train, last 365 = test)
train = df.iloc[:365].dropna(subset=["rolling_mean_7"])
test  = df.iloc[365:]

X_train = train[["rolling_mean_7", "day_of_week"]].values
y_train = train["sales"].values
X_test  = test[["rolling_mean_7", "day_of_week"]].values
y_test  = test["sales"].values

lr = LinearRegression()
lr.fit(X_train, y_train)
mae = mean_absolute_error(y_test, lr.predict(X_test))

# Row 364 is the last training row (0-indexed)
rolling_last_train = float(df.iloc[364]["rolling_mean_7"])

result = {
    "mae": round(float(mae), 4),
    "rolling_mean_last_train_row": round(rolling_last_train, 4),
}
Path("/root/results.json").write_text(json.dumps(result))
print(json.dumps(result))
EOF
