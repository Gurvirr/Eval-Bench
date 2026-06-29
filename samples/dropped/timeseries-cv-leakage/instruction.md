You are a data scientist evaluating a sales forecasting model.

The file `/root/data/sales.csv` contains 3 years of daily sales data:
- `date`, `sales`, `day_of_week`, `month`

Your task:
1. Create a lag-1 feature: `lag_1 = sales shifted by 1 day`
2. Evaluate a linear regression model (features: `lag_1`, `day_of_week`, `month`) using **5-fold cross-validation**
3. Report the mean MAE and standard deviation across folds

Save results to `/root/results.json`:

```json
{
  "cv_mean_mae": 0.XXXX,
  "cv_std_mae": 0.XXXX,
  "cv_method": "string"
}
```

Round to 4 decimal places.
