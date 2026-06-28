#!/bin/bash
set -e

python3 << 'EOF'
import json
import pandas as pd
from pathlib import Path

sales   = pd.read_excel("/root/data/weekly_report.xlsx", sheet_name="Sales")
returns = pd.read_excel("/root/data/weekly_report.xlsx", sheet_name="Returns")

# Normalize region column name
returns = returns.rename(columns={"Region": "region"})

merged = sales.merge(returns, on="region")
merged["net_sales"] = merged["gross_sales"] - merged["return_value"]
merged["net_units"] = merged["units_sold"]  - merged["return_units"]

result = {
    "grand_total_net_sales":    round(float(merged["net_sales"].sum()), 2),
    "best_region_by_net_sales": str(merged.loc[merged["net_sales"].idxmax(), "region"]),
    "north_net_sales":          round(float(merged.loc[merged["region"]=="North", "net_sales"].iloc[0]), 2),
    "south_net_sales":          round(float(merged.loc[merged["region"]=="South", "net_sales"].iloc[0]), 2),
    "east_net_sales":           round(float(merged.loc[merged["region"]=="East",  "net_sales"].iloc[0]), 2),
    "west_net_sales":           round(float(merged.loc[merged["region"]=="West",  "net_sales"].iloc[0]), 2),
    "total_net_units":          int(merged["net_units"].sum()),
}
Path("/root/results.json").write_text(json.dumps(result))
print(json.dumps(result, indent=2))
EOF
