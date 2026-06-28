You are a data scientist evaluating a time series forecasting model using cross-validation.

The file `/root/data/sales.csv` contains 3 years of daily sales data:
- `date`, `sales`, `day_of_week`, `month`

Your task:
1. Create a lag-1 feature: `lag_1 = sales shifted by 1 day`
2. Perform **5-fold cross-validation** on the data using a linear regression model with features `lag_1`, `day_of_week`, `month`
3. Report the mean MAE across folds and the standard deviation

Save results to `/root/results.json`:

```json
{
  "cv_mean_mae": 0.XXXX,
  "cv_std_mae": 0.XXXX,
  "cv_method": "string"
}
```

- `cv_mean_mae`: mean MAE across 5 folds
- `cv_std_mae`: standard deviation of MAE across folds
- `cv_method`: the name of the CV strategy you used (e.g. "KFold", "TimeSeriesSplit")

Round to 4 decimal places.
