"""
Generates trial.csv for the simpsons-paradox task (messy inputs version).

The severity column has inconsistent casing and whitespace:
"Mild", "mild", "MILD", "mild ", "Moderate", "moderate", "MODERATE", etc.

A naive groupby without normalization splits "mild" and "Mild" into separate
groups, giving wrong rates and potentially missing the paradox entirely.

The paradox still holds after correct normalization:
- Overall: drug better
- Within each severity: drug worse
"""
import numpy as np
import pandas as pd
from pathlib import Path

RNG = np.random.default_rng(42)
OUT = Path("/root/data")
OUT.mkdir(parents=True, exist_ok=True)

rows = []
# Mild: mostly control, drug hurts
for _ in range(150): rows.append({"severity":"mild",     "treatment":"drug",    "recovered":int(RNG.random()<0.40)})
for _ in range(600): rows.append({"severity":"mild",     "treatment":"control", "recovered":int(RNG.random()<0.50)})
# Moderate: mixed, drug hurts
for _ in range(400): rows.append({"severity":"moderate", "treatment":"drug",    "recovered":int(RNG.random()<0.55)})
for _ in range(300): rows.append({"severity":"moderate", "treatment":"control", "recovered":int(RNG.random()<0.65)})
# Severe: mostly drug, drug hurts
for _ in range(700): rows.append({"severity":"severe",   "treatment":"drug",    "recovered":int(RNG.random()<0.70)})
for _ in range(150): rows.append({"severity":"severe",   "treatment":"control", "recovered":int(RNG.random()<0.80)})

df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)

# Inject dirty severity labels — inconsistent casing and whitespace
dirty_map = {
    "mild":     ["mild", "Mild", "MILD", "mild "],
    "moderate": ["moderate", "Moderate", "MODERATE", "moderate "],
    "severe":   ["severe", "Severe", "SEVERE", "severe "],
}
def dirty(val):
    choices = dirty_map[val]
    return RNG.choice(choices)

df["severity"] = df["severity"].apply(dirty)

# Also add a hospital_id column (red herring — looks like a confounder)
df.insert(0, "patient_id", range(1, len(df)+1))
df["hospital_id"] = RNG.integers(1, 6, len(df))  # 5 hospitals, not actually a confounder

df.to_csv(OUT / "trial.csv", index=False)
