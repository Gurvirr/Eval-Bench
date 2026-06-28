---
name: join-safety
description: Avoid row duplication (fanout) when joining tables with one-to-many or many-to-many relationships. Always verify row counts before and after joins.
---

# Join Safety

## Key Rule
When joining a fact table (orders) with a dimension table that has multiple
rows per key (tags), the join creates duplicate fact rows.
Always check: `len(result) == len(original_fact_table)` after joining.

## Pattern: filter before join
```python
# Safe: get the IDs first, then filter
target_ids = tags[tags["tag"] == "premium"]["customer_id"].unique()
revenue = orders[orders["customer_id"].isin(target_ids)]["revenue"].sum()
```

## Pattern: aggregate before join
```python
# Safe: reduce dimension table to one row per key before joining
tag_counts = tags.groupby("customer_id")["tag"].count().reset_index()
merged = orders.merge(tag_counts, on="customer_id", how="left")
# Now merged has same row count as orders
```

## Danger sign
If `len(merged) > len(orders)` after a join, you have fanout — rows are duplicated.
