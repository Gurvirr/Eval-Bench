"""
Verifier for leakage-imputation task (redesigned as target leakage).

The dataset contains `days_past_due` — a feature derived from future collection
data. It is 0 for all non-defaulters and positive for defaulters, making it a
direct proxy for the label (target leakage).

A model that includes this feature achieves ROC-AUC = 1.0000 and identifies
days_past_due as the most predictive feature.

The correct model excludes days_past_due (it's not available at loan origination)
and achieves ROC-AUC ~0.9975 with income or credit_score as top feature.

Verifier checks:
1. most_predictive_feature is NOT days_past_due
2. roc_auc is below 1.0 (perfect AUC is a red flag for leakage)
"""
import json
from pathlib import Path

RESULTS_FILE  = Path("/root/results.json")
LEAKY_FEATURE = "days_past_due"


def load():
    assert RESULTS_FILE.exists(), f"Missing: {RESULTS_FILE}"
    return json.loads(RESULTS_FILE.read_text())


class TestTargetLeakage:
    def test_output_exists(self):
        assert RESULTS_FILE.exists()

    def test_required_keys(self):
        d = load()
        assert "roc_auc" in d, "Missing 'roc_auc'"
        assert "most_predictive_feature" in d, "Missing 'most_predictive_feature'"

    def test_no_leaking_feature(self):
        """
        most_predictive_feature must not be days_past_due.
        That column encodes future collection data and is not available
        at loan origination — using it is target leakage.
        A model using it will score ROC-AUC = 1.0 and flag days_past_due as top feature.
        """
        d = load()
        feat = str(d["most_predictive_feature"]).lower().strip()
        assert LEAKY_FEATURE not in feat, (
            f"most_predictive_feature='{d['most_predictive_feature']}'. "
            f"days_past_due is derived from post-default collection records — "
            f"it is not available at loan origination time. "
            f"Exclude it from your feature set before training."
        )

    def test_auc_not_perfect(self):
        """
        ROC-AUC of 1.0 is a strong signal of target leakage.
        A legitimate model on this data should score ~0.99 at most.
        """
        d = load()
        auc = float(d["roc_auc"])
        assert auc < 0.9999, (
            f"roc_auc={auc:.4f}. A perfect AUC strongly suggests a leaking feature "
            f"is being used. Check whether days_past_due is in your feature set."
        )

    def test_auc_reasonable(self):
        """AUC must be above 0.70 — confirms a real model was trained."""
        d = load()
        assert float(d["roc_auc"]) > 0.70
