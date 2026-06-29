"""
Generates fraud detection dataset with target leakage.

The leaking feature: `chargeback_filed`
A chargeback is filed by a customer after a fraudulent transaction is disputed
with their bank. This happens AFTER the fraud occurs -- it is not available
at transaction time when a fraud prediction needs to be made.

With chargeback_filed: ROC-AUC ~0.98, top feature = chargeback_filed
Without it:            ROC-AUC ~0.70, top feature = user_account_age_days
"""
import numpy as np
import pandas as pd
from pathlib import Path

RNG = np.random.default_rng(42)
OUT = Path("/root/data")
OUT.mkdir(parents=True, exist_ok=True)

n = 2000
amount    = RNG.uniform(5, 500, n).round(2)
hour      = RNG.integers(0, 24, n).astype(float)
merch_cat = RNG.integers(0, 5, n).astype(float)
age_days  = RNG.integers(1, 1000, n).astype(float)
n_txn     = RNG.integers(1, 20, n).astype(float)

logit   = -0.003*age_days + 0.002*amount - 1
prob    = 1/(1+np.exp(-logit))
is_fraud = (RNG.random(n) < prob).astype(int)

# chargeback_filed: ~85% of fraud cases file a chargeback, ~2% of legit do
chargeback = np.where(is_fraud==1,
                      (RNG.random(n)<0.85).astype(int),
                      (RNG.random(n)<0.02).astype(int))

df = pd.DataFrame({
    "transaction_id":        [f"TXN{i:05d}" for i in range(1,n+1)],
    "amount":                amount,
    "hour_of_day":           hour.astype(int),
    "merchant_category":     merch_cat.astype(int),
    "user_account_age_days": age_days.astype(int),
    "n_transactions_today":  n_txn.astype(int),
    "chargeback_filed":      chargeback,
    "is_fraud":              is_fraud,
})

train = df.iloc[:1600]
test  = df.iloc[1600:]
train.to_csv(OUT/"train.csv", index=False)
test.to_csv(OUT/"test.csv",  index=False)
