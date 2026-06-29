#!/bin/bash
set -e

python3 << 'EOF'
import json
import pandas as pd
from pathlib import Path

df = pd.read_csv("/root/data/transactions.csv")

def compute_fee(row):
    ct = row["card_type"]
    a  = float(row["amount"])
    if ct == "debit":
        return round(a * 0.005 + 0.10, 4)
    elif ct == "credit_standard":
        return round(a * 0.015 + 0.15, 4) if a < 100 else round(a * 0.018 + 0.20, 4)
    elif ct == "credit_premium":
        return round(a * 0.022 + 0.25, 4) if a < 200 else round(a * 0.025 + 0.30, 4)
    else:  # corporate
        return round(a * 0.028 + 0.35, 4)

df["fee"] = df.apply(compute_fee, axis=1)

fees_by_type = df.groupby("card_type")["fee"].sum().round(4).to_dict()
n_by_type    = df.groupby("card_type").size().to_dict()
top_txn      = df.loc[df["fee"].idxmax(), "transaction_id"]

result = {
    "total_fees":               round(float(df["fee"].sum()), 4),
    "fees_by_card_type":        {k: round(float(v), 4) for k, v in fees_by_type.items()},
    "n_transactions_by_card_type": {k: int(v) for k, v in n_by_type.items()},
    "highest_fee_transaction_id": str(top_txn),
}
Path("/root/results.json").write_text(json.dumps(result))
print(json.dumps(result, indent=2))
EOF
