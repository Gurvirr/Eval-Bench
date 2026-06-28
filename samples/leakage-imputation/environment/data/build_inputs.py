"""
Generates train.csv and test.csv for the leakage-imputation task.

The trap: feature_3 has missing values (25%). The train distribution of
feature_3 is N(0, 1) while the test distribution is N(4, 1) — a large shift.

Correct approach: fit imputer on train only -> fill value ~-0.08
Leaky approach:  fit imputer on train+test -> fill value ~0.71 (pulled toward test mean)

The verifier checks the reported imputer_fill_feature_3 to determine whether
the agent used the correct (train-only) or leaky (combined) approach.
"""
import numpy as np
import pandas as pd
from pathlib import Path

RNG = np.random.default_rng(42)
OUT = Path("/root/data")
OUT.mkdir(parents=True, exist_ok=True)

N_TRAIN, N_TEST = 800, 200

X_train = np.column_stack([
    RNG.normal(0, 1, N_TRAIN),
    RNG.normal(0, 1, N_TRAIN),
    RNG.normal(0.0, 1, N_TRAIN),  # feature_3: train mean ~ 0
    RNG.normal(0, 1, N_TRAIN),
])
X_test = np.column_stack([
    RNG.normal(0, 1, N_TEST),
    RNG.normal(0, 1, N_TEST),
    RNG.normal(4.0, 1, N_TEST),   # feature_3: test mean ~ 4 (distribution shift)
    RNG.normal(0, 1, N_TEST),
])

# Labels: signal from feature_1 and feature_2 only
y_train = (X_train[:,0] - X_train[:,1] + RNG.normal(0, 0.5, N_TRAIN) > 0).astype(int)
y_test  = (X_test[:,0]  - X_test[:,1]  + RNG.normal(0, 0.5, N_TEST)  > 0).astype(int)

# 25% missing in feature_3
X_train[RNG.random(N_TRAIN) < 0.25, 2] = np.nan
X_test[RNG.random(N_TEST)  < 0.25, 2] = np.nan

cols = ["feature_1", "feature_2", "feature_3", "feature_4", "churned"]
train_df = pd.DataFrame(np.column_stack([X_train, y_train]), columns=cols)
test_df  = pd.DataFrame(np.column_stack([X_test,  y_test]),  columns=cols)
train_df["churned"] = train_df["churned"].astype(int)
test_df["churned"]  = test_df["churned"].astype(int)

train_df.round(6).to_csv(OUT / "train.csv", index=False)
test_df.round(6).to_csv(OUT / "test.csv",  index=False)
