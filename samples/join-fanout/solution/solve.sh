#!/bin/bash
set -e

python3 << 'EOF'
import json
import pandas as pd
from pathlib import Path

orders = pd.read_csv("/root/data/orders.csv")
tags   = pd.read_csv("/root/data/customer_tags.csv")

# Overall: count each order once
overall_revenue = round(float(orders["revenue"].sum()), 2)
overall_n       = int(len(orders))

# Per-tag: filter orders by customers with that tag
revenue_by_tag = {}
orders_by_tag  = {}
for tag in ["premium", "newsletter", "loyalty", "trial"]:
    cids = tags[tags["tag"] == tag]["customer_id"].unique()
    subset = orders[orders["customer_id"].isin(cids)]
    revenue_by_tag[tag] = round(float(subset["revenue"].sum()), 2)
    orders_by_tag[tag]  = int(len(subset))

result = {
    "overall_total_revenue": overall_revenue,
    "overall_n_orders": overall_n,
    "revenue_by_tag": revenue_by_tag,
    "orders_by_tag": orders_by_tag,
}
Path("/root/results.json").write_text(json.dumps(result))
print(json.dumps(result, indent=2))
EOF
