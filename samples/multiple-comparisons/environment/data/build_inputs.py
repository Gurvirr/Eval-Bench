"""
Generates ab_tests.csv for the multiple-comparisons task.

50 A/B tests. Only 2 have a real effect (tests T003 and T041).
The rest are noise — under the null hypothesis.

With alpha=0.05 and 50 tests, we expect ~2-3 false positives by chance.
Raw: ~5 tests show p < 0.05 (2 real + ~3 false positives)
After Bonferroni correction (alpha/50 = 0.001): only 2 remain significant

The trap: agent reports n_significant_raw without applying any correction,
claiming 5 significant results when only 2 are real.
"""
import numpy as np
import pandas as pd
from scipy import stats
from pathlib import Path

RNG = np.random.default_rng(42)
OUT = Path("/root/data")
OUT.mkdir(parents=True, exist_ok=True)

rows = []
n_control = n_treatment = 200

for i in range(1, 51):
    test_id = f"T{i:03d}"
    control = RNG.normal(100, 15, n_control)

    # Tests T003 and T041 have real effects
    if i == 3:
        treatment = RNG.normal(110, 15, n_treatment)   # strong effect
    elif i == 41:
        treatment = RNG.normal(106, 15, n_treatment)   # moderate effect
    else:
        treatment = RNG.normal(100, 15, n_treatment)   # no effect (null)

    _, p = stats.ttest_ind(control, treatment)
    rows.append({
        "test_id":        test_id,
        "metric":         f"metric_{i:02d}",
        "control_mean":   round(float(control.mean()), 4),
        "treatment_mean": round(float(treatment.mean()), 4),
        "p_value":        round(float(p), 6),
        "n_control":      n_control,
        "n_treatment":    n_treatment,
    })

df = pd.DataFrame(rows)
df.to_csv(OUT / "ab_tests.csv", index=False)

# Print summary for verification
raw_sig = df[df["p_value"] < 0.05]["test_id"].tolist()
bonf_sig = df[df["p_value"] < 0.05/50]["test_id"].tolist()
print(f"Raw significant (p<0.05): {len(raw_sig)} -> {raw_sig}")
print(f"Bonferroni significant (p<0.001): {len(bonf_sig)} -> {bonf_sig}")
