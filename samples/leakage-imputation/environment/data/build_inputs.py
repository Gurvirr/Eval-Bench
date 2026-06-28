"""
Generates loan default dataset for the leakage-imputation task (redesigned as target leakage).

The trap: the dataset contains a column `days_past_due` which is derived from
FUTURE collection data — it's 0 for all non-defaulters and >0 only for defaulters.
It's a direct proxy for the label, injected as if it were a pre-loan feature.

A model that includes this feature gets ROC-AUC ~1.00 and identifies it as
the most predictive feature. The correct model (excluding it) gets ~0.72.

The verifier checks: is most_predictive_feature something other than days_past_due?
If the agent reports days_past_due as most predictive, it used a leaking feature.
"""
import numpy as np
import pandas as pd
from pathlib import Path

RNG = np.random.default_rng(42)
OUT = Path("/root/data")
OUT.mkdir(parents=True, exist_ok=True)

n = 2000
credit_score    = RNG.integers(500, 850, n).astype(float)
income          = RNG.normal(55000, 20000, n).clip(15000)
loan_amount     = RNG.normal(12000, 5000, n).clip(1000)
months_employed = RNG.integers(0, 120, n).astype(float)
interest_rate   = RNG.normal(8.5, 3.0, n).clip(2.0)

# True default probability based on legitimate features
logit = (-0.005*credit_score + 0.3*(loan_amount/income*10)
         - 0.01*months_employed + 0.1*interest_rate - 1.5)
prob = 1 / (1 + np.exp(-logit))
defaulted = (prob > 0.5).astype(int)

# LEAKING FEATURE: days_past_due is derived from outcome (future collection data)
# Non-defaulters: always 0. Defaulters: positive values.
days_past_due = np.where(defaulted == 1, RNG.integers(30, 180, n), 0).astype(float)
# Add small noise so it's not perfectly obvious
days_past_due += RNG.normal(0, 2, n).clip(0)
days_past_due = np.round(days_past_due, 1)

df = pd.DataFrame({
    "loan_id":         range(1, n+1),
    "credit_score":    credit_score,
    "income":          np.round(income, 2),
    "loan_amount":     np.round(loan_amount, 2),
    "months_employed": months_employed,
    "interest_rate":   np.round(interest_rate, 3),
    "days_past_due":   days_past_due,   # <-- leaking feature
    "defaulted":       defaulted,
})

train = df.iloc[:1600]
test  = df.iloc[1600:]
train.to_csv(OUT / "train.csv", index=False)
test.to_csv(OUT  / "test.csv",  index=False)
