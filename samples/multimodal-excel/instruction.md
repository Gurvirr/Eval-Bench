You are a data analyst at a retail company. A colleague has sent you a weekly sales report.

The file `/root/data/weekly_report.xlsx` contains a single sheet named `Report`.

Compute the following and save to `/root/results.json`:

```json
{
  "grand_total_sales": 0.00,
  "best_region_by_sales": "string",
  "top_product_by_revenue": "string",
  "avg_price_north_region": 0.00,
  "total_units_all_regions": 0
}
```

- `grand_total_sales`: sum of `total_sales` across all regions
- `best_region_by_sales`: name of the region with highest `total_sales`
- `top_product_by_revenue`: `product_name` of the product with highest `revenue`
- `avg_price_north_region`: `avg_price` for the North region
- `total_units_all_regions`: sum of `total_units` across all regions

Round monetary values to 2 decimal places.
