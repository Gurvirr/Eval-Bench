#!/bin/bash
set -e

python3 << 'EOF'
import json
import pandas as pd
from pathlib import Path

# Section 1: 4 data rows starting at row 0 (header), nrows=4
regions = pd.read_excel("/root/data/weekly_report.xlsx", sheet_name="Report",
                        header=0, nrows=4)

# Section 2: starts at row 6 (0-indexed), skip 6 rows to reach it
products = pd.read_excel("/root/data/weekly_report.xlsx", sheet_name="Report",
                         header=0, skiprows=6, nrows=5)

result = {
    "grand_total_sales":       round(float(regions["total_sales"].sum()), 2),
    "best_region_by_sales":    str(regions.loc[regions["total_sales"].idxmax(), "region"]),
    "top_product_by_revenue":  str(products.loc[products["revenue"].idxmax(), "product_name"]),
    "avg_price_north_region":  round(float(regions.loc[regions["region"] == "North", "avg_price"].iloc[0]), 2),
    "total_units_all_regions": int(regions["total_units"].sum()),
}
Path("/root/results.json").write_text(json.dumps(result))
print(json.dumps(result, indent=2))
EOF
