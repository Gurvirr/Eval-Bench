You are a data scientist building a sales forecasting model.

The file `/root/data/sales.csv` contains 730 rows of daily sales data:
- `date`, `sales`, `day_of_week`
- First 365 rows = training period, last 365 rows = test period

Your task:
1. Compute a **7-day rolling mean** of `sales` as a new feature `rolling_mean_7`.
2. Split into train (first 365 rows) and test (last 365 rows).
3. Train a linear regression model using `rolling_mean_7` and `day_of_week` to predict `sales`.
4. Evaluate using **MAE** on the test set.
5. Save results to `/root/results.json`:

```json
{
  "mae": 0.XXXX,
  "rolling_mean_last_train_row": 0.XXXX
}
```

Where `rolling_mean_last_train_row` is the value of `rolling_mean_7` for row index 364 (the last training row).

Round both values to 4 decimal places.
