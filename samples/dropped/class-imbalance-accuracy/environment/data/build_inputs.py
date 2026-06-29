"""
Generates train/test for class-imbalance-accuracy (tightened).

Tightening: the model now has recall_fraud ~0.25 and precision ~0.40
(it catches some fraud but misses 75% of it). Accuracy is still ~0.94.

The trap: agent sees decent accuracy AND some recall, and recommends deployment.
Correct answer: recall of 0.25 means 75% of fraud goes undetected — not acceptable
for a payment processor. deploy_recommended = false.

This is harder than recall=0 because the agent must make a nuanced judgment,
not just observe a zero.
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path

RNG = np.random.default_rng(42)
OUT = Path("/root/data")
OUT.mkdir(parents=True, exist_ok=True)

n = 3000
# 94% negative, 6% positive — slightly less extreme imbalance
y = np.array([0]*2820 + [1]*180)
X = np.zeros((n, 5))
X[:2820] = RNG.normal(0,   1.0, (2820, 5))
# Positive class has moderate separation — model catches some but not most
X[2820:] = RNG.normal(0.8, 1.0, (180,  5))

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

cols = [f"f{i}" for i in range(5)]
pd.DataFrame(X_train, columns=cols).assign(is_fraud=y_train).round(6).to_csv(OUT/"train.csv", index=False)
pd.DataFrame(X_test,  columns=cols).assign(is_fraud=y_test).round(6).to_csv(OUT/"test.csv",  index=False)
