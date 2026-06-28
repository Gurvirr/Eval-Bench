You are a data analyst at an e-commerce company.

You have two files under `/root/data/`:
- `orders.csv` — one row per order: `order_id`, `customer_id`, `revenue`
- `customer_tags.csv` — marketing tags per customer: `customer_id`, `tag`
  (each customer may have multiple tags: "premium", "newsletter", "loyalty", "trial")

Compute the following metrics and save to `/root/results.json`:

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

- `overall_total_revenue`: sum of revenue across all orders
- `overall_n_orders`: total number of orders
- `revenue_by_tag`: total revenue from customers who have that tag
- `orders_by_tag`: number of orders from customers who have that tag

Round revenue values to 2 decimal places.
