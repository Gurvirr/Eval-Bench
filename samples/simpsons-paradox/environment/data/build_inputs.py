"""
Generates 3 hospital CSV files for the simpsons-paradox task.

hospital_a.csv — columns: pid, sev_group, arm, outcome
hospital_b.csv — columns: patient_id, severity, treatment, recovered
hospital_c.csv — columns: ID, Severity_Level, Treatment_Arm, Recovery_Status

The agent must:
1. Normalize all 3 files to the same schema
2. Concatenate into one dataset
3. Normalize severity labels (dirty casing/whitespace)
4. Compute stratified analysis

Without correct normalization, the groupby produces wrong rates.
Without noticing the paradox, the wrong recommendation is made.
"""
import numpy as np
import pandas as pd
from pathlib import Path

RNG = np.random.default_rng(42)
OUT = Path("/root/data")
OUT.mkdir(parents=True, exist_ok=True)

def make_patients(n_mild_drug, n_mild_ctrl, n_mod_drug, n_mod_ctrl, n_sev_drug, n_sev_ctrl, rng):
    rows = []
    for n, sev, arm, rate in [
        (n_mild_drug, "mild",     "drug",    0.40),
        (n_mild_ctrl, "mild",     "control", 0.50),
        (n_mod_drug,  "moderate", "drug",    0.55),
        (n_mod_ctrl,  "moderate", "control", 0.65),
        (n_sev_drug,  "severe",   "drug",    0.70),
        (n_sev_ctrl,  "severe",   "control", 0.80),
    ]:
        for _ in range(n):
            rows.append({"severity": sev, "treatment": arm,
                         "recovered": int(rng.random() < rate)})
    return pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)

# Hospital A — small, uses abbreviated column names
df_a = make_patients(50, 200, 130, 100, 230, 50, RNG)
dirty = {"mild": ["mild","Mild","MILD"], "moderate": ["moderate","Moderate","MODERATE"], "severe": ["severe","Severe","SEVERE"]}
df_a["severity"] = df_a["severity"].apply(lambda x: RNG.choice(dirty[x]))
df_a = df_a.rename(columns={"severity":"sev_group","treatment":"arm","recovered":"outcome"})
df_a.insert(0, "pid", range(1, len(df_a)+1))
df_a.to_csv(OUT / "hospital_a.csv", index=False)

# Hospital B — medium, standard names but severity has trailing spaces
df_b = make_patients(60, 250, 150, 120, 280, 60, RNG)
df_b["severity"] = df_b["severity"].apply(lambda x: x + (" " if RNG.random() < 0.3 else ""))
df_b.insert(0, "patient_id", range(1001, 1001+len(df_b)))
df_b.to_csv(OUT / "hospital_b.csv", index=False)

# Hospital C — large, capitalized column names, Recovery_Status is "Yes"/"No" not 1/0
df_c = make_patients(40, 150, 120, 80, 190, 40, RNG)
df_c["severity"] = df_c["severity"].str.title()  # "Mild", "Moderate", "Severe"
df_c["recovered"] = df_c["recovered"].map({1:"Yes", 0:"No"})
df_c = df_c.rename(columns={"severity":"Severity_Level","treatment":"Treatment_Arm","recovered":"Recovery_Status"})
df_c.insert(0, "ID", range(2001, 2001+len(df_c)))
df_c.to_csv(OUT / "hospital_c.csv", index=False)
