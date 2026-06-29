You are a data analyst at a retail company finalizing the weekly revenue report.

Files under `/root/data/`:
- `weekly_report.xlsx` — Excel workbook with 3 sheets:
  - `Sales`: gross sales by product and region (`product_id`, `product_name`, `region`, `units_sold`, `gross_revenue`)
  - `Targets`: regional sales targets (for reference only — do not include in output)
  - `Returns`: product returns (`product_id`, `return_units`, `return_value`)
- `corrections.csv` — post-submission revenue adjustments (`product_id`, `adjustment`, `reason`)

Compute net revenue figures (gross - returns + corrections) and save to **`/root/output_report.xlsx`**.

The output workbook must have exactly two sheets:

**Sheet 1 — name: `Regional Summary`**
Headers (row 1): `region`, `gross_revenue`, `total_returns`, `total_adjustments`, `net_revenue`, `net_units`
One row per region (North, South, East, West), sorted alphabetically by region.
All monetary values stored as numbers rounded to 2 decimal places.

**Sheet 2 — name: `Product Detail`**
Headers (row 1): `product_id`, `product_name`, `region`, `gross_revenue`, `return_value`, `adjustment`, `net_revenue`
One row per product, sorted by `product_id` ascending.
All monetary values stored as numbers rounded to 2 decimal places.

Do not include any other sheets. Column names must match exactly (case-sensitive).
