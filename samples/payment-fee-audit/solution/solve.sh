#!/bin/bash
set -e

python3 << 'EOF'
import pandas as pd
from openpyxl import Workbook
from pathlib import Path

df = pd.read_csv("/root/data/transactions.csv")

def compute_fee_and_tier(row):
    ct = row["card_type"]
    a  = float(row["amount"])
    if ct == "debit":
        return round(a * 0.005 + 0.10, 4), "debit"
    elif ct == "credit_standard":
        if a < 100:
            return round(a * 0.015 + 0.15, 4), "credit_standard_low"
        else:
            return round(a * 0.018 + 0.20, 4), "credit_standard_high"
    elif ct == "credit_premium":
        if a < 200:
            return round(a * 0.022 + 0.25, 4), "credit_premium_low"
        else:
            return round(a * 0.025 + 0.30, 4), "credit_premium_high"
    else:
        return round(a * 0.028 + 0.35, 4), "corporate"

fees, tiers = zip(*df.apply(compute_fee_and_tier, axis=1))
df["fee"]       = fees
df["rate_tier"] = tiers
df = df.sort_values("transaction_id").reset_index(drop=True)

summary = df.groupby("card_type", as_index=False).agg(
    n_transactions=("fee","count"),
    total_fees=("fee","sum"),
    avg_fee=("fee","mean"),
).sort_values("card_type").reset_index(drop=True)
summary["total_fees"] = summary["total_fees"].round(4)
summary["avg_fee"]    = summary["avg_fee"].round(4)

wb = Workbook()
ws1 = wb.active
ws1.title = "Transaction Fees"
ws1.append(["transaction_id","card_type","amount","fee","rate_tier"])
for _, r in df.iterrows():
    ws1.append([r["transaction_id"], r["card_type"], float(r["amount"]),
                float(r["fee"]), r["rate_tier"]])

ws2 = wb.create_sheet("Summary")
ws2.append(["card_type","n_transactions","total_fees","avg_fee"])
for _, r in summary.iterrows():
    ws2.append([r["card_type"], int(r["n_transactions"]),
                float(r["total_fees"]), float(r["avg_fee"])])

wb.save("/root/fee_audit.xlsx")
print("Saved /root/fee_audit.xlsx")
print(summary.to_string())
EOF
