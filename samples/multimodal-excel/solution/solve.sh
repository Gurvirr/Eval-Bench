#!/bin/bash
set -e

python3 << 'EOF'
import pandas as pd
from openpyxl import Workbook
from pathlib import Path

sales       = pd.read_excel("/root/data/weekly_report.xlsx", sheet_name="Sales")
returns     = pd.read_excel("/root/data/weekly_report.xlsx", sheet_name="Returns")
corrections = pd.read_csv("/root/data/corrections.csv")

merged = sales.merge(returns[["product_id","return_value","return_units"]], on="product_id", how="left").fillna(0)
merged = merged.merge(corrections[["product_id","adjustment"]], on="product_id", how="left").fillna(0)
merged["net_revenue"] = merged["gross_revenue"] - merged["return_value"] + merged["adjustment"]
merged["net_units"]   = merged["units_sold"] - merged["return_units"]

# Regional Summary
regional = merged.groupby("region", as_index=False).agg(
    gross_revenue=("gross_revenue", "sum"),
    total_returns=("return_value",  "sum"),
    total_adjustments=("adjustment","sum"),
    net_revenue=("net_revenue",     "sum"),
    net_units=("net_units",         "sum"),
).sort_values("region").reset_index(drop=True)

for col in ["gross_revenue","total_returns","total_adjustments","net_revenue"]:
    regional[col] = regional[col].round(2)
regional["net_units"] = regional["net_units"].astype(int)

# Product Detail
detail = merged[["product_id","product_name","region","gross_revenue","return_value","adjustment","net_revenue"]].copy()
for col in ["gross_revenue","return_value","adjustment","net_revenue"]:
    detail[col] = detail[col].round(2)
detail = detail.sort_values("product_id").reset_index(drop=True)

# Write Excel output
wb = Workbook()
ws1 = wb.active
ws1.title = "Regional Summary"
ws1.append(["region","gross_revenue","total_returns","total_adjustments","net_revenue","net_units"])
for _, row in regional.iterrows():
    ws1.append([row["region"], row["gross_revenue"], row["total_returns"],
                row["total_adjustments"], row["net_revenue"], row["net_units"]])

ws2 = wb.create_sheet("Product Detail")
ws2.append(["product_id","product_name","region","gross_revenue","return_value","adjustment","net_revenue"])
for _, row in detail.iterrows():
    ws2.append([row["product_id"], row["product_name"], row["region"],
                row["gross_revenue"], row["return_value"], row["adjustment"], row["net_revenue"]])

wb.save("/root/output_report.xlsx")
print("Saved /root/output_report.xlsx")
print(regional[["region","net_revenue","net_units"]].to_string())
EOF
