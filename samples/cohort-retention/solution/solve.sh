#!/bin/bash
set -e

python3 << 'EOF'
import json
import pandas as pd
from pathlib import Path

def compute_retention(df, base_month_str):
    """base_month_str like '2024-01'"""
    n = len(df)
    base_year, base_month = int(base_month_str[:4]), int(base_month_str[5:7])
    retention = {}
    for offset in range(4):
        m = base_month + offset
        y = base_year + (m-1)//12
        m = ((m-1) % 12) + 1
        target = f"{y}-{m:02d}"
        active = df["active_months"].apply(
            lambda x: target in x.split(",") if pd.notna(x) and x else False
        ).sum()
        retention[f"month_{offset}"] = round(float(active / n), 4)
    return retention

jan = pd.read_csv("/root/data/cohort_jan.csv")
feb = pd.read_csv("/root/data/cohort_feb.csv")
mar = pd.read_csv("/root/data/cohort_mar.csv")

result = {
    "jan_cohort_size": len(jan),
    "feb_cohort_size": len(feb),
    "mar_cohort_size": len(mar),
    "retention": {
        "jan": compute_retention(jan, "2024-01"),
        "feb": compute_retention(feb, "2024-02"),
        "mar": compute_retention(mar, "2024-03"),
    }
}
Path("/root/results.json").write_text(json.dumps(result))
print(json.dumps(result, indent=2))
EOF
