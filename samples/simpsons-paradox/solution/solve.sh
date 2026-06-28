#!/bin/bash
set -e

python3 << 'EOF'
import json
import pandas as pd
from pathlib import Path

# Hospital A: pid, sev_group, arm, outcome
a = pd.read_csv("/root/data/hospital_a.csv")[["sev_group","arm","outcome"]]
a.columns = ["severity","treatment","recovered"]

# Hospital B: patient_id, severity, treatment, recovered
b = pd.read_csv("/root/data/hospital_b.csv")[["severity","treatment","recovered"]]

# Hospital C: ID, Severity_Level, Treatment_Arm, Recovery_Status (Yes/No)
c = pd.read_csv("/root/data/hospital_c.csv")[["Severity_Level","Treatment_Arm","Recovery_Status"]]
c.columns = ["severity","treatment","recovered"]
c["recovered"] = c["recovered"].map({"Yes":1,"No":0})

df = pd.concat([a, b, c], ignore_index=True)
df["severity"]  = df["severity"].str.strip().str.lower()
df["treatment"] = df["treatment"].str.strip().str.lower()

overall  = df.groupby("treatment")["recovered"].mean()
by_group = df.groupby(["severity","treatment"])["recovered"].mean()

result = {
    "overall_drug_recovery_rate":     round(float(overall["drug"]),    4),
    "overall_control_recovery_rate":  round(float(overall["control"]), 4),
    "mild_drug_recovery_rate":        round(float(by_group["mild",     "drug"]),    4),
    "mild_control_recovery_rate":     round(float(by_group["mild",     "control"]), 4),
    "moderate_drug_recovery_rate":    round(float(by_group["moderate", "drug"]),    4),
    "moderate_control_recovery_rate": round(float(by_group["moderate", "control"]), 4),
    "severe_drug_recovery_rate":      round(float(by_group["severe",   "drug"]),    4),
    "severe_control_recovery_rate":   round(float(by_group["severe",   "control"]), 4),
    "total_patients":                 int(len(df)),
    "drug_recommended":               False,
}
Path("/root/results.json").write_text(json.dumps(result))
print(json.dumps(result, indent=2))
EOF
