#!/bin/bash
set -e

python3 << 'EOF'
import json
import pandas as pd
from pathlib import Path

df = pd.read_csv("/root/data/trial.csv")

overall = df.groupby("treatment")["recovered"].mean()
by_group = df.groupby(["severity", "treatment"])["recovered"].mean()

overall_drug    = round(float(overall["drug"]),    4)
overall_control = round(float(overall["control"]), 4)
mild_drug       = round(float(by_group["mild",   "drug"]),    4)
mild_control    = round(float(by_group["mild",   "control"]), 4)
severe_drug     = round(float(by_group["severe", "drug"]),    4)
severe_control  = round(float(by_group["severe", "control"]), 4)

# Correct: drug is worse in EVERY subgroup -> not recommended
drug_recommended = not (mild_drug < mild_control and severe_drug < severe_control)

result = {
    "overall_drug_recovery_rate":    overall_drug,
    "overall_control_recovery_rate": overall_control,
    "mild_drug_recovery_rate":       mild_drug,
    "mild_control_recovery_rate":    mild_control,
    "severe_drug_recovery_rate":     severe_drug,
    "severe_control_recovery_rate":  severe_control,
    "drug_recommended":              drug_recommended,
}
Path("/root/results.json").write_text(json.dumps(result))
print(json.dumps(result, indent=2))
EOF
