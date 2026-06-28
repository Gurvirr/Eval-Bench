#!/bin/bash
set -e

python3 << 'EOF'
import json
import pandas as pd
from statsmodels.stats.multitest import multipletests
from pathlib import Path

df = pd.read_csv("/root/data/ab_tests.csv")

alpha = 0.05
n_raw = int((df["p_value"] < alpha).sum())

# Bonferroni correction
reject, _, _, _ = multipletests(df["p_value"], alpha=alpha, method="bonferroni")
sig_ids = df[reject]["test_id"].tolist()

result = {
    "n_significant_raw":       n_raw,
    "n_significant_corrected": int(reject.sum()),
    "correction_method":       "bonferroni",
    "alpha":                   alpha,
    "significant_test_ids":    sorted(sig_ids),
}
Path("/root/results.json").write_text(json.dumps(result))
print(json.dumps(result, indent=2))
EOF
