#!/bin/bash
set -e

python3 << 'EOF'
import pandas as pd
from openpyxl import Workbook
from pathlib import Path

df = pd.read_csv("/root/data/transactions.csv")

def base_fee(ct, a):
    if ct == "debit": return round(a*0.005+0.10, 6)
    elif ct == "credit_standard": return round(a*0.015+0.15,6) if a < 100 else round(a*0.018+0.20,6)
    elif ct == "credit_premium":  return round(a*0.022+0.25,6) if a < 200 else round(a*0.025+0.30,6)
    else: return round(a*0.028+0.35,6)

def final_fee(row):
    f = base_fee(row["card_type"], float(row["amount"]))
    if int(row["is_disputed"]): f *= 2
    if float(row["monthly_volume"]) > 5000: f *= 0.90
    return round(min(f, 25.00), 4)

df["base_fee"]  = df.apply(lambda r: round(base_fee(r["card_type"], float(r["amount"])), 4), axis=1)
df["final_fee"] = df.apply(final_fee, axis=1)
df = df.sort_values("transaction_id").reset_index(drop=True)

merchant_summary = df.groupby("merchant_id", as_index=False).agg(
    n_transactions=("transaction_id","count"),
    total_amount=("amount","sum"),
    total_fees=("final_fee","sum"),
    monthly_volume=("monthly_volume","first"),
).sort_values("merchant_id")
merchant_summary["volume_discount_applied"] = merchant_summary["monthly_volume"].apply(
    lambda v: "YES" if float(v) > 5000 else "NO"
)
merchant_summary["total_amount"] = merchant_summary["total_amount"].round(2)
merchant_summary["total_fees"]   = merchant_summary["total_fees"].round(4)

wb = Workbook()
ws1 = wb.active
ws1.title = "Transaction Fees"
ws1.append(["transaction_id","card_type","amount","is_disputed","monthly_volume","base_fee","final_fee"])
for _, r in df.iterrows():
    ws1.append([r["transaction_id"], r["card_type"], float(r["amount"]),
                int(r["is_disputed"]), float(r["monthly_volume"]),
                float(r["base_fee"]), float(r["final_fee"])])

ws2 = wb.create_sheet("Merchant Summary")
ws2.append(["merchant_id","n_transactions","total_amount","total_fees","volume_discount_applied"])
for _, r in merchant_summary.iterrows():
    ws2.append([int(r["merchant_id"]), int(r["n_transactions"]),
                float(r["total_amount"]), float(r["total_fees"]),
                r["volume_discount_applied"]])

wb.save("/root/fee_audit.xlsx")
print("Saved. Total fees:", df["final_fee"].sum().round(4))
EOF
