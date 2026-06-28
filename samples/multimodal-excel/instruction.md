You are a data analyst at a retail company finalizing the weekly revenue report.

Files under `/root/data/`:
- `weekly_report.xlsx` — Excel workbook with 3 sheets:
  - `Sales`: gross sales by product and region (`product_id`, `product_name`, `region`, `units_sold`, `gross_revenue`)
  - `Targets`: regional sales targets (for reference only)
  - `Returns`: product returns (`product_id`, `return_units`, `return_value`)
- `corrections.csv` — post-submission revenue adjustments (`product_id`, `adjustment`, `reason`)

Compute **final net revenue** figures after applying returns and corrections, then save to `/root/results.json`:

```json
{
  "total_gross_revenue": 0.00,
  "total_returns_value": 0.00,
  "total_corrections_value": 0.00,
  "total_net_revenue": 0.00,
  "net_revenue_by_region": {
    "North": 0.00,
    "South": 0.00,
    "East": 0.00,
    "West": 0.00
  },
  "best_region_by_net_revenue": "string",
  "total_net_units": 0
}
```

- `total_net_revenue = total_gross_revenue - total_returns_value + total_corrections_value`
- Net revenue by region requires allocating returns and corrections to regions via `product_id`
- `total_net_units = total units_sold - total return_units`

Round all monetary values to 2 decimal places.
