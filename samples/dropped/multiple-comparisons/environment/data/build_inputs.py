"""
Generates 50 individual CSV files under /root/data/tests/T001.csv...T050.csv.

Only T003 and T041 have real effects. The rest are noise.
Raw p<0.05: ~4 tests. After Bonferroni: 2 (T003, T041).

The trap is harder now because:
1. Agent must discover and load 50 files (not told how many there are)
2. Without seeing all 50 at once, the correction context is less obvious
3. Agent may run tests individually and accept raw p-values
"""
import numpy as np
import pandas as pd
from scipy import stats
from pathlib import Path

RNG = np.random.default_rng(42)
OUT = Path("/root/data/tests")
OUT.mkdir(parents=True, exist_ok=True)

n = 200
summary = []

for i in range(1, 51):
    control   = RNG.normal(100, 15, n)
    treatment = RNG.normal(110 if i == 3 else (106 if i == 41 else 100), 15, n)

    df = pd.DataFrame({
        "group": ["control"]*n + ["treatment"]*n,
        "value": np.concatenate([control, treatment]).round(4),
    })
    df.to_csv(OUT / f"T{i:03d}.csv", index=False)

    _, p = stats.ttest_ind(control, treatment)
    summary.append({"test_id": f"T{i:03d}", "p_value": round(float(p), 6)})

# Print verification
sig_raw  = [r["test_id"] for r in summary if r["p_value"] < 0.05]
sig_bonf = [r["test_id"] for r in summary if r["p_value"] < 0.05/50]
print(f"Raw (p<0.05): {len(sig_raw)} -> {sig_raw}")
print(f"Bonferroni:   {len(sig_bonf)} -> {sig_bonf}")
