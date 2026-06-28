"""
Generates train.csv and test.csv for the macro-vs-micro-f1 task.

Class distribution (heavily imbalanced):
  0 (safe):         1600 / 2000 = 80%
  1 (spam):          200 / 2000 = 10%
  2 (harassment):    120 / 2000 =  6%
  3 (hate speech):    80 / 2000 =  4%

Minority classes (1,2,3) overlap heavily with class 0 in feature space,
so logistic regression ignores them -> accuracy ~80% but macro F1 ~0.22.

The trap: an agent that reports accuracy (0.80) or weighted F1 (0.71)
instead of macro F1 (0.22) misses the critical finding that the model
completely fails on the minority classes that matter most for safety.
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path

RNG = np.random.default_rng(42)
OUT = Path("/root/data")
OUT.mkdir(parents=True, exist_ok=True)

n = 2000
y = np.array([0]*1600 + [1]*200 + [2]*120 + [3]*80)
X = np.zeros((n, 6))
X[:1600]     = RNG.normal(0.0,  1.0, (1600, 6))
X[1600:1800] = RNG.normal(0.3,  1.2, (200,  6))
X[1800:1920] = RNG.normal(-0.3, 1.2, (120,  6))
X[1920:]     = RNG.normal(0.1,  1.3, (80,   6))

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

cols = [f"feature_{i}" for i in range(6)]
train_df = pd.DataFrame(X_train, columns=cols)
train_df["label"] = y_train
test_df  = pd.DataFrame(X_test,  columns=cols)
test_df["label"]  = y_test

train_df.round(6).to_csv(OUT / "train.csv", index=False)
test_df.round(6).to_csv(OUT / "test.csv",   index=False)
