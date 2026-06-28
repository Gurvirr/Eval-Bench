You are a data analyst at a retail company. A colleague has sent you a weekly sales report.

The file `/root/data/weekly_report.xlsx` contains sales data for the week.

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

- `grand_total_sales`: total sales across all regions
- `best_region_by_sales`: region with the highest total sales
- `top_product_by_revenue`: product name with highest revenue
- `avg_price_north_region`: average price in the North region
- `total_units_all_regions`: total units sold across all regions

Round monetary values to 2 decimal places.
