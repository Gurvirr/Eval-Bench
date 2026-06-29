#!/bin/bash
set -e

python3 << 'EOF'
import json
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests
from pathlib import Path

tests_dir = Path("/root/data/tests")
rows = []
for f in sorted(tests_dir.glob("T*.csv")):
    df = pd.read_csv(f)
    control   = df[df["group"]=="control"]["value"].values
    treatment = df[df["group"]=="treatment"]["value"].values
    _, p = stats.ttest_ind(control, treatment)
    rows.append({"test_id": f.stem, "p_value": float(p)})

results_df = pd.DataFrame(rows)
alpha = 0.05
n_raw = int((results_df["p_value"] < alpha).sum())

reject, _, _, _ = multipletests(results_df["p_value"], alpha=alpha, method="bonferroni")
sig_ids = sorted(results_df[reject]["test_id"].tolist())

result = {
    "n_significant_raw":       n_raw,
    "n_significant_corrected": int(reject.sum()),
    "correction_method":       "bonferroni",
    "significant_test_ids":    sig_ids,
}
Path("/root/results.json").write_text(json.dumps(result))
print(json.dumps(result, indent=2))
EOF
