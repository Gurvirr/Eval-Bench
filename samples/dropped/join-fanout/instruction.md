You are a data analyst at an e-commerce company.

You have the following files under `/root/data/`:
- `orders_jan.csv`, `orders_feb.csv`, `orders_mar.csv` — monthly order records: `order_id`, `customer_id`, `revenue`, `month`
- `customer_tags.csv` — marketing segment data: `customer_id`, `tag`

Compute the following metrics across all three months combined and save to `/root/results.json`:

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

- `overall_total_revenue`: total revenue across all orders (all months)
- `overall_n_orders`: total number of orders (all months)
- `revenue_by_tag` / `orders_by_tag`: revenue and order count for customers who have each tag

Round revenue values to 2 decimal places.
