"""
Generates sales.csv for the timeseries-lookahead task.

The trap: agents commonly write df["rolling_mean_7"] = df["sales"].rolling(7).mean()
which includes the current row in the window (look-ahead by 1 step).
The correct approach uses shift(1) first to exclude the current row.

The verifier checks rolling_mean_last_train_row (row index 364):
- Correct (shift+rolling): ~117.35
- Leaky (rolling without shift): ~116.95

It also checks rolling_mean_row3:
- Correct: ~88.38 (uses only rows 0-2, i.e. 3 values before row 3)
- Leaky:   ~97.11 (uses rows 1-3 including current row 3)
"""
import numpy as np
import pandas as pd
from pathlib import Path

RNG = np.random.default_rng(42)
OUT = Path("/root/data")
OUT.mkdir(parents=True, exist_ok=True)

dates = pd.date_range("2022-01-01", periods=730)
dow = dates.dayofweek
t = np.arange(730)
sales = 100 + 0.05*t + 20*np.sin(2*np.pi*dow/7) + RNG.normal(0, 8, 730)
sales = np.round(sales, 2)

df = pd.DataFrame({"date": dates.strftime("%Y-%m-%d"), "sales": sales, "day_of_week": dow.astype(int)})
df.to_csv(OUT / "sales.csv", index=False)
