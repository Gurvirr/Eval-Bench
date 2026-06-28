You are a data analyst at an e-commerce company.

You have two files under `/root/data/`:
- `orders.csv` — one row per order: `order_id`, `customer_id`, `revenue`
- `customer_tags.csv` — marketing segment tags per customer: `customer_id`, `tag`
  (each customer may have multiple tags: "premium", "newsletter", "loyalty", "trial")

Your task:
1. Compute total revenue and order count for each segment tag (e.g., total revenue from "premium" customers, from "newsletter" customers, etc.)
2. Also compute the **overall** total revenue and order count across all orders (regardless of tag).

Save results to `/root/results.json`:

```json
{
  "overall_total_revenue": 0.00,
  "overall_n_orders": 0,
  "revenue_by_tag": {
    "premium": 0.00,
    "newsletter": 0.00,
    "loyalty": 0.00,
    "trial": 0.00
  },
  "orders_by_tag": {
    "premium": 0,
    "newsletter": 0,
    "loyalty": 0,
    "trial": 0
  }
}
```

Round revenue values to 2 decimal places.

**Important:** `overall_total_revenue` should be the true total across all orders — each order counted once regardless of how many tags its customer has.
