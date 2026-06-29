"""
Generates cohort retention data across 3 monthly CSV files.

cohort_jan.csv: users who signed up in January
cohort_feb.csv: users who signed up in February
cohort_mar.csv: users who signed up in March

Each file has: user_id, signup_date, activity_dates (comma-separated)

The task asks: compute the cohort retention table.
Month 0 = signup month (always 100%)
Month 1 = % of cohort active in month after signup
Month 2 = % of cohort active 2 months after signup
etc.

The trap: agents often make off-by-one errors on cohort month boundaries,
or count users who were active in ANY prior month instead of the specific month.
Retention = active in EXACTLY month N after signup, not cumulative.
"""
import numpy as np
import pandas as pd
from pathlib import Path

RNG = np.random.default_rng(42)
OUT = Path("/root/data")
OUT.mkdir(parents=True, exist_ok=True)

def make_cohort(signup_month, n_users, retention_rates, rng):
    """retention_rates[i] = P(user active in month i after signup), i=0 is signup month"""
    rows = []
    for uid in range(1, n_users + 1):
        activity = []
        for i, rate in enumerate(retention_rates):
            if rng.random() < rate:
                # active in month i after signup
                month_offset = i
                if signup_month == 1:
                    year, month = 2024, 1 + month_offset
                elif signup_month == 2:
                    year, month = 2024, 2 + month_offset
                else:
                    year, month = 2024, 3 + month_offset
                # normalize month overflow
                while month > 12:
                    month -= 12; year += 1
                activity.append(f"2024-{month:02d}")
        rows.append({
            "user_id": f"U{signup_month:02d}{uid:04d}",
            "signup_date": f"2024-0{signup_month}-01",
            "active_months": ",".join(activity) if activity else "",
        })
    return pd.DataFrame(rows)

# Jan cohort: 500 users, retention drops sharply
jan = make_cohort(1, 500, [1.0, 0.60, 0.42, 0.30], RNG)
# Feb cohort: 420 users
feb = make_cohort(2, 420, [1.0, 0.55, 0.38, 0.25], RNG)
# Mar cohort: 380 users
mar = make_cohort(3, 380, [1.0, 0.50, 0.35, 0.22], RNG)

# Add leaking column: final_status is determined at END of observation period
# (future data — not available at the time of each monthly measurement)
# Users with any activity in month 3+ are "retained", others "churned"
def add_final_status(df, base_month):
    def status(active_months):
        if not active_months:
            return "churned"
        months = active_months.split(",")
        # retained if active in last observed month
        last = f"2024-{base_month+3:02d}" if base_month+3 <= 12 else f"2025-{base_month+3-12:02d}"
        return "retained" if last in months else "churned"
    df = df.copy()
    df["final_status"] = df["active_months"].apply(status)
    return df

jan = add_final_status(jan, 1)
feb = add_final_status(feb, 2)
mar = add_final_status(mar, 3)

jan.to_csv(OUT / "cohort_jan.csv", index=False)
feb.to_csv(OUT / "cohort_feb.csv", index=False)
mar.to_csv(OUT / "cohort_mar.csv", index=False)

# Print expected values
for name, df, base_month in [("Jan", jan, 1), ("Feb", feb, 2), ("Mar", mar, 3)]:
    n = len(df)
    for m_offset in range(4):
        month = base_month + m_offset
        col = f"2024-{month:02d}"
        active = df["active_months"].apply(lambda x: col in x.split(",") if x else False).sum()
        print(f"{name} cohort month+{m_offset}: {active}/{n} = {active/n:.4f}")
