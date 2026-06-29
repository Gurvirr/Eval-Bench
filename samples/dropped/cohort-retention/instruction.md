You are a product analyst computing user retention for Q1 2024.

Files under `/root/data/`:
- `cohort_jan.csv` — users who signed up in January 2024
- `cohort_feb.csv` — users who signed up in February 2024
- `cohort_mar.csv` — users who signed up in March 2024

Each file has columns:
- `user_id`: unique identifier
- `signup_date`: date of signup
- `active_months`: comma-separated list of months the user was active (e.g. "2024-01,2024-02")

Compute the cohort retention table. Retention at month N = percentage of the cohort that was active exactly N months after their signup month (month 0 = signup month = 100%).

Save results to `/root/results.json`:

```json
{
  "jan_cohort_size": 0,
  "feb_cohort_size": 0,
  "mar_cohort_size": 0,
  "retention": {
    "jan": {"month_0": 1.0, "month_1": 0.0, "month_2": 0.0, "month_3": 0.0},
    "feb": {"month_0": 1.0, "month_1": 0.0, "month_2": 0.0, "month_3": 0.0},
    "mar": {"month_0": 1.0, "month_1": 0.0, "month_2": 0.0, "month_3": 0.0}
  }
}
```

Round retention rates to 4 decimal places.
