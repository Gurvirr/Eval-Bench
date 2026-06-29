"""
Generates churn prediction dataset with target leakage.

The leaking feature: `support_tickets_after_cancel`
When a customer churns, they often file support tickets to cancel their account,
request refunds, or dispute charges. These tickets are filed AFTER the churn
decision -- they are not available when predicting whether a customer will churn.

With support_tickets_after_cancel: ROC-AUC ~1.0, top feature = support_tickets_after_cancel
Without it:                        ROC-AUC ~0.68, top feature = account_age_days
"""
import numpy as np
import pandas as pd
from pathlib import Path

RNG = np.random.default_rng(42)
OUT = Path("/root/data")
OUT.mkdir(parents=True, exist_ok=True)

n = 2000
acc_age  = RNG.integers(30, 1000, n).astype(float)
spend    = RNG.uniform(20, 500, n).round(2)
logins   = RNG.integers(0, 50, n).astype(float)
features = RNG.integers(0, 10, n).astype(float)
plan     = RNG.integers(0, 3, n).astype(float)

logit   = -0.002*acc_age - 0.001*spend + 0.02*(50-logins) - 0.5
prob    = 1/(1+np.exp(-logit))
churned = (RNG.random(n) < prob).astype(int)

# support_tickets_after_cancel: only churned customers generate these
tickets = np.where(churned==1, RNG.integers(1,10,n), 0).astype(int)

df = pd.DataFrame({
    "customer_id":                  [f"CUST{i:05d}" for i in range(1,n+1)],
    "account_age_days":             acc_age.astype(int),
    "monthly_spend":                spend,
    "n_logins_last30":              logins.astype(int),
    "n_features_used":              features.astype(int),
    "plan_tier":                    plan.astype(int),
    "support_tickets_after_cancel": tickets,
    "churned":                      churned,
})

train = df.iloc[:1600]
test  = df.iloc[1600:]
train.to_csv(OUT/"train.csv", index=False)
test.to_csv(OUT/"test.csv",  index=False)
