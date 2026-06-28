You are a data analyst at a retail company. A colleague has sent you a weekly sales report as an Excel file.

The file `/root/data/weekly_report.xlsx` contains a single sheet named `Report` with two sections separated by a blank row:

**Section 1 (starts at row 1):** Regional summary table
- Headers: `region`, `total_sales`, `total_units`, `avg_price`
- 4 data rows (North, South, East, West)

**Section 2 (starts after the blank row):** Top products table
- Headers: `product_id`, `product_name`, `units_sold`, `revenue`
- 5 data rows

Your task — compute the following and save to `/root/results.json`:

```json
{
  "grand_total_sales": 0.00,
  "best_region_by_sales": "string",
  "top_product_by_revenue": "string",
  "avg_price_north_region": 0.00,
  "total_units_all_regions": 0
}
```

- `grand_total_sales`: sum of `total_sales` across all 4 regions
- `best_region_by_sales`: name of the region with highest `total_sales`
- `top_product_by_revenue`: `product_name` of the product with highest `revenue`
- `avg_price_north_region`: `avg_price` value for the North region
- `total_units_all_regions`: sum of `total_units` across all 4 regions

Round monetary values to 2 decimal places.
