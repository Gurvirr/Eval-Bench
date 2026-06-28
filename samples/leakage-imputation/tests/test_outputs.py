"""
Verifier for leakage-imputation task.

Two checks:
1. roc_auc is reasonable (> 0.70) — confirms the model actually ran
2. imputer_fill_feature_3 is close to the train-only mean (~-0.08)
   and NOT close to the combined mean (~0.71)

The train-only fill value for feature_3 is approximately -0.08.
The combined (leaky) fill value is approximately 0.71.
We check that the reported value is within 0.25 of the train-only mean.
Any value > 0.30 indicates the agent fit on combined data (leakage).
"""
import json
from pathlib import Path
import pytest

RESULTS_FILE = Path("/root/results.json")
CORRECT_FILL = -0.0834   # train-only mean of feature_3 (seed=42)
LEAKY_FILL   =  0.7097   # combined mean of feature_3 (seed=42)
TOLERANCE    =  0.25     # acceptable deviation from correct fill value


def load_results():
    assert RESULTS_FILE.exists(), f"Missing output file: {RESULTS_FILE}"
    data = json.loads(RESULTS_FILE.read_text())
    assert "roc_auc" in data, "results.json must contain 'roc_auc'"
    assert "imputer_fill_feature_3" in data, "results.json must contain 'imputer_fill_feature_3'"
    return data


class TestLeakageImputation:
    def test_output_file_exists(self):
        """results.json must exist at /root/results.json"""
        assert RESULTS_FILE.exists(), f"Missing: {RESULTS_FILE}"

    def test_roc_auc_reasonable(self):
        """ROC-AUC must be > 0.70 — confirms a real model was trained"""
        data = load_results()
        auc = float(data["roc_auc"])
        assert auc > 0.70, f"ROC-AUC too low ({auc:.4f}); expected > 0.70"
        assert auc <= 1.0, f"ROC-AUC > 1.0 is impossible: {auc}"

    def test_imputer_fit_on_train_only(self):
        """
        imputer_fill_feature_3 must be close to the train-only mean (~-0.08).
        A value near 0.71 indicates the imputer was fit on combined train+test
        data (leakage). The threshold is 0.30: values above it indicate leakage.
        """
        data = load_results()
        fill = float(data["imputer_fill_feature_3"])
        assert abs(fill - CORRECT_FILL) < TOLERANCE, (
            f"imputer_fill_feature_3={fill:.4f} is too far from the correct "
            f"train-only mean ({CORRECT_FILL:.4f}). "
            f"A value near {LEAKY_FILL:.4f} indicates the imputer was fit on "
            f"combined train+test data (preprocessing leakage)."
        )

    def test_no_leaky_fill_value(self):
        """
        Explicitly check that the fill value is not the leaky (combined) mean.
        """
        data = load_results()
        fill = float(data["imputer_fill_feature_3"])
        assert abs(fill - LEAKY_FILL) > TOLERANCE, (
            f"imputer_fill_feature_3={fill:.4f} matches the leaky combined mean "
            f"({LEAKY_FILL:.4f}). Fit preprocessing on training data only."
        )
