"""
Generates train.csv and test.csv for the class-imbalance-accuracy task.

97% negative (legitimate), 3% positive (fraud).
Positive class heavily overlaps with negative in feature space.
Logistic regression predicts ALL zeros -> accuracy=0.97, recall_fraud=0.

The trap: agent sees 97% accuracy and recommends deployment,
missing that the model detects ZERO fraud cases.
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path

RNG = np.random.default_rng(42)
OUT = Path("/root/data")
OUT.mkdir(parents=True, exist_ok=True)

n = 3000
y = np.array([0]*2910 + [1]*90)
X = np.zeros((n, 5))
X[:2910] = RNG.normal(0,   1.0, (2910, 5))
X[2910:] = RNG.normal(0.2, 1.1, (90,   5))

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

cols = [f"f{i}" for i in range(5)]
pd.DataFrame(X_train, columns=cols).assign(is_fraud=y_train).round(6).to_csv(OUT/"train.csv", index=False)
pd.DataFrame(X_test,  columns=cols).assign(is_fraud=y_test).round(6).to_csv(OUT/"test.csv",  index=False)
