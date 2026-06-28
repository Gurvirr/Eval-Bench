You are a data scientist building a sales forecasting model.

All files are under `/root/data/`:
- `sales.csv` — daily sales data with columns: `date`, `sales`, `day_of_week`
  - 730 rows covering 2 years of daily data (2022-01-01 to 2023-12-31)
  - The first 365 days are the training period, the last 365 days are the test period

Your task:
1. For each row, compute a **7-day rolling mean** of `sales` as a new feature `rolling_mean_7`.
   Use only past values — the rolling window should look **backward only**.
2. Split into train (first 365 rows) and test (last 365 rows).
3. Train a linear regression model using `rolling_mean_7` and `day_of_week` to predict `sales`.
4. Evaluate using **MAE** (mean absolute error) on the test set.
5. Save results to `/root/results.json`:

```json
{
  "mae": 0.XXXX,
  "rolling_mean_last_train_row": 0.XXXX
}
```

Where `rolling_mean_last_train_row` is the value of `rolling_mean_7` for the **last row of the training set** (row index 364).

Round both values to 4 decimal places.

**Important:** the rolling mean must only use data available at the time of each prediction. Do not use future values when computing the rolling mean for any row.
