"""
Generates orders.csv and customer_tags.csv for the join-fanout task.

The trap: customers can have multiple tags (M:N relationship between orders
and tags). A naive merge(orders, tags) then sum(revenue) inflates the total
by ~1.8x because orders are duplicated for each tag a customer has.

Correct approach: filter premium customer IDs first, then sum their orders.
- Correct total revenue from premium customers: computed from orders only
- Naive (join-first) total: ~1.8x inflated
"""
import numpy as np
import pandas as pd
from pathlib import Path

RNG = np.random.default_rng(42)
OUT = Path("/root/data")
OUT.mkdir(parents=True, exist_ok=True)

orders = pd.DataFrame({
    "order_id":    range(1, 101),
    "customer_id": RNG.integers(1, 41, 100),
    "revenue":     RNG.integers(10, 200, 100).astype(float),
})

tags = []
for cid in range(1, 41):
    n_tags = RNG.integers(1, 4)
    for tag in RNG.choice(["premium", "newsletter", "loyalty", "trial"], n_tags, replace=False):
        tags.append({"customer_id": int(cid), "tag": tag})
tags_df = pd.DataFrame(tags)

orders.to_csv(OUT / "orders.csv", index=False)
tags_df.to_csv(OUT / "customer_tags.csv", index=False)
