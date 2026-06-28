You are a data analyst at a retail company. A colleague has sent you a weekly sales report.

The file `/root/data/weekly_report.xlsx` contains two sheets: `Sales` and `Returns`.

Compute the following **net** figures (gross sales minus returns) and save to `/root/results.json`:

```json
{
  "grand_total_net_sales": 0.00,
  "best_region_by_net_sales": "string",
  "north_net_sales": 0.00,
  "south_net_sales": 0.00,
  "east_net_sales": 0.00,
  "west_net_sales": 0.00,
  "total_net_units": 0
}
```

- All revenue figures must be **net** (after subtracting returns)
- `total_net_units`: net units sold across all regions (units_sold minus return_units)
- `best_region_by_net_sales`: region with highest net sales

Round monetary values to 2 decimal places.
