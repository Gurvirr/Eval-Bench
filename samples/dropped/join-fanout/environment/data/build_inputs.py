"""
Generates orders split across 3 monthly files + customer_tags.csv.

The fanout trap is now harder to spot:
- orders are in orders_jan.csv, orders_feb.csv, orders_mar.csv
- Must concatenate all three before computing metrics
- customer_tags.csv has the same M:N structure (customers with multiple tags)

A model that joins tags to orders before concatenating, or that joins
the concatenated orders with all tags and sums without deduplication,
inflates the overall_total_revenue by ~1.8x.
"""
import numpy as np
import pandas as pd
from pathlib import Path

RNG = np.random.default_rng(42)
OUT = Path("/root/data")
OUT.mkdir(parents=True, exist_ok=True)

# Generate 100 orders split across 3 months
n_per_month = [34, 33, 33]
months = ["jan", "feb", "mar"]
all_orders = []
order_id = 1
for n, month in zip(n_per_month, months):
    df = pd.DataFrame({
        "order_id":    range(order_id, order_id + n),
        "customer_id": RNG.integers(1, 41, n),
        "revenue":     RNG.integers(10, 200, n).astype(float),
        "month":       month,
    })
    df.to_csv(OUT / f"orders_{month}.csv", index=False)
    all_orders.append(df)
    order_id += n

orders = pd.concat(all_orders, ignore_index=True)

# Customer tags: M:N (same as before)
tags = []
for cid in range(1, 41):
    n_tags = RNG.integers(1, 4)
    for tag in RNG.choice(["premium","newsletter","loyalty","trial"], n_tags, replace=False):
        tags.append({"customer_id": int(cid), "tag": tag})
tags_df = pd.DataFrame(tags)
tags_df.to_csv(OUT / "customer_tags.csv", index=False)
