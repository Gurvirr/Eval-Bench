#!/bin/bash
set -e

python3 << 'EOF'
import json
import pandas as pd
from pathlib import Path

sales       = pd.read_excel("/root/data/weekly_report.xlsx", sheet_name="Sales")
returns     = pd.read_excel("/root/data/weekly_report.xlsx", sheet_name="Returns")
corrections = pd.read_csv("/root/data/corrections.csv")

total_gross       = round(float(sales["gross_revenue"].sum()), 2)
total_returns_val = round(float(returns["return_value"].sum()), 2)
total_corr_val    = round(float(corrections["adjustment"].sum()), 2)
total_net         = round(total_gross - total_returns_val + total_corr_val, 2)

merged = sales.merge(returns[["product_id","return_value","return_units"]], on="product_id", how="left").fillna(0)
merged = merged.merge(corrections[["product_id","adjustment"]], on="product_id", how="left").fillna(0)
merged["net_revenue"] = merged["gross_revenue"] - merged["return_value"] + merged["adjustment"]
merged["net_units"]   = merged["units_sold"] - merged["return_units"]

by_region = merged.groupby("region")[["net_revenue","net_units"]].sum()

result = {
    "total_gross_revenue":      total_gross,
    "total_returns_value":      total_returns_val,
    "total_corrections_value":  total_corr_val,
    "total_net_revenue":        total_net,
    "net_revenue_by_region": {r: round(float(v), 2) for r, v in by_region["net_revenue"].items()},
    "best_region_by_net_revenue": str(by_region["net_revenue"].idxmax()),
    "total_net_units": int(by_region["net_units"].sum()),
}
Path("/root/results.json").write_text(json.dumps(result))
print(json.dumps(result, indent=2))
EOF
