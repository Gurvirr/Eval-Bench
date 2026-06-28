"""
Generates trial.csv for the simpsons-paradox task.

Simpson's Paradox setup:
- Mild patients: mostly get control; drug recovery 40%, control 50% (drug hurts)
- Severe patients: mostly get drug; drug recovery 70%, control 80% (drug hurts)
- Overall: drug looks better (0.625 vs 0.559) due to confounding with severity

The trap: an agent that computes overall recovery rates without stratifying
by severity will conclude the drug helps. The correct stratified analysis
shows the drug is harmful in every subgroup.
"""
import numpy as np
import pandas as pd
from pathlib import Path

RNG = np.random.default_rng(42)
OUT = Path("/root/data")
OUT.mkdir(parents=True, exist_ok=True)

rows = []
for _ in range(200):
    rows.append({"severity": "mild",   "treatment": "drug",    "recovered": int(RNG.random() < 0.40)})
for _ in range(800):
    rows.append({"severity": "mild",   "treatment": "control", "recovered": int(RNG.random() < 0.50)})
for _ in range(800):
    rows.append({"severity": "severe", "treatment": "drug",    "recovered": int(RNG.random() < 0.70)})
for _ in range(200):
    rows.append({"severity": "severe", "treatment": "control", "recovered": int(RNG.random() < 0.80)})

df = pd.DataFrame(rows)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df.to_csv(OUT / "trial.csv", index=False)
