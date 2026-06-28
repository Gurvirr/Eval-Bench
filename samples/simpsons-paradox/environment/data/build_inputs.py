"""
Generates trial.csv for the simpsons-paradox task (tightened).

Three severity groups: mild, moderate, severe.
- Mild:     drug 40% vs control 50%  -> drug hurts (drug gets fewer)
- Moderate: drug 55% vs control 65%  -> drug hurts (drug gets moderate share)
- Severe:   drug 70% vs control 80%  -> drug hurts (drug gets most)
- Overall:  drug looks better due to confounding with severity

The tightening: three groups instead of two makes the correct
stratified analysis less obvious. The model must check ALL subgroups,
not just split into two.
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

# Verify paradox holds
overall = df.groupby("treatment")["recovered"].mean()
by_group = df.groupby(["severity","treatment"])["recovered"].mean()
assert overall["drug"] > overall["control"], "Paradox broken: drug should look better overall"
for sev in ["mild","moderate","severe"]:
    assert by_group[sev,"drug"] < by_group[sev,"control"], f"Paradox broken in {sev}"

df.to_csv(OUT / "trial.csv", index=False)
