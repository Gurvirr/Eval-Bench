#!/bin/bash
set -e

python3 << 'EOF'
import json
import pandas as pd
from pathlib import Path

trial = pd.read_csv("/root/data/trial.csv")
meta  = pd.read_csv("/root/data/patient_metadata.csv")

df = trial.merge(meta[["patient_id","severity_group"]], on="patient_id")
df["severity_group"] = df["severity_group"].str.strip().str.lower()

overall  = df.groupby("treatment")["recovered"].mean()
by_group = df.groupby(["severity_group","treatment"])["recovered"].mean()

result = {
    "overall_drug_recovery_rate":     round(float(overall["drug"]),    4),
    "overall_control_recovery_rate":  round(float(overall["control"]), 4),
    "mild_drug_recovery_rate":        round(float(by_group["mild",     "drug"]),    4),
    "mild_control_recovery_rate":     round(float(by_group["mild",     "control"]), 4),
    "moderate_drug_recovery_rate":    round(float(by_group["moderate", "drug"]),    4),
    "moderate_control_recovery_rate": round(float(by_group["moderate", "control"]), 4),
    "severe_drug_recovery_rate":      round(float(by_group["severe",   "drug"]),    4),
    "severe_control_recovery_rate":   round(float(by_group["severe",   "control"]), 4),
    "drug_recommended":               False,
}
Path("/root/results.json").write_text(json.dumps(result))
print(json.dumps(result, indent=2))
EOF
