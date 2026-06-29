"""
Generates trial.csv and patient_metadata.csv for simpsons-paradox.

trial.csv has: patient_id, treatment, recovered (NO severity column)
patient_metadata.csv has: patient_id, age, hospital_id, severity_group

The agent must join the two files to get severity for stratification.
Without the join, the agent can only compute overall rates and will
miss the paradox (drug looks beneficial overall, hurts in every subgroup).

The hospital_id and age columns are distractors — they are NOT confounders.
Only severity_group is the true confounder.
"""
import numpy as np
import pandas as pd
from pathlib import Path

RNG = np.random.default_rng(42)
OUT = Path("/root/data")
OUT.mkdir(parents=True, exist_ok=True)

rows = []
for n, sev, arm, rate in [
    (150, "mild",     "drug",    0.40),
    (600, "mild",     "control", 0.50),
    (400, "moderate", "drug",    0.55),
    (300, "moderate", "control", 0.65),
    (700, "severe",   "drug",    0.70),
    (150, "severe",   "control", 0.80),
]:
    for _ in range(n):
        rows.append({"severity": sev, "treatment": arm,
                     "recovered": int(RNG.random() < rate)})

df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)
df.insert(0, "patient_id", range(1, len(df)+1))

# trial.csv — no severity column
trial = df[["patient_id", "treatment", "recovered"]]
trial.to_csv(OUT / "trial.csv", index=False)

# patient_metadata.csv — severity + distractors
meta = pd.DataFrame({
    "patient_id":     df["patient_id"],
    "severity_group": df["severity"],
    "age":            RNG.integers(25, 80, len(df)),
    "hospital_id":    RNG.integers(1, 6, len(df)),
})
meta.to_csv(OUT / "patient_metadata.csv", index=False)
