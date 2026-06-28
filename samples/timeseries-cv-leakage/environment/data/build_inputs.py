"""
Generates sales.csv for the timeseries-cv-leakage task.

3 years of daily sales with a regime change at day 730 (year 3):
- Year 3 has a sudden +50 level shift and higher variance
- This makes KFold(shuffle=True) significantly underestimate MAE
  because future high-variance data leaks into early training folds

KFold(shuffle=True) MAE: ~14.95 (underestimates true error)
TimeSeriesSplit MAE:      ~19.30 (correct — model hasn't seen year 3 patterns)

The verifier checks: cv_method == "TimeSeriesSplit" AND cv_mean_mae > 17
"""
import numpy as np
import pandas as pd
from pathlib import Path

RNG = np.random.default_rng(42)
OUT = Path("/root/data")
OUT.mkdir(parents=True, exist_ok=True)

dates = pd.date_range("2022-01-01", periods=1095)
t   = np.arange(1095)
dow = dates.dayofweek.values
month = dates.month.values

sales = 100 + 0.08*t + 15*np.sin(2*np.pi*dow/7) + RNG.normal(0, 8, 1095)
sales[730:] += 50 + RNG.normal(0, 20, 365)  # regime change in year 3
sales = np.round(sales, 2)

df = pd.DataFrame({"date": dates.strftime("%Y-%m-%d"), "sales": sales,
                   "day_of_week": dow.astype(int), "month": month.astype(int)})
df.to_csv(OUT / "sales.csv", index=False)
