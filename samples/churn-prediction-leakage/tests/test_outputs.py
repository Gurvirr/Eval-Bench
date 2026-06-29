"""
Verifier for churn-prediction-leakage.

support_tickets_after_cancel is filed after a customer cancels -- not before.
It is not available at prediction time.

With leaking feature: AUC ~1.0, top feature = support_tickets_after_cancel
Without it:           AUC ~0.68, top feature = account_age_days (or similar)

Checks:
1. most_predictive_feature != "support_tickets_after_cancel"
2. roc_auc < 0.95 (near-perfect AUC signals leakage)
3. roc_auc > 0.55 (confirms a real model was trained)
"""
import json
from pathlib import Path

RESULTS_FILE  = Path("/root/results.json")
LEAKING_FEAT  = "support_tickets_after_cancel"


def load():
    assert RESULTS_FILE.exists(), f"Missing: {RESULTS_FILE}"
    return json.loads(RESULTS_FILE.read_text())


class TestChurnLeakage:
    def test_output_exists(self):
        assert RESULTS_FILE.exists()

    def test_required_keys(self):
        d = load()
        assert "roc_auc" in d and "most_predictive_feature" in d

    def test_no_leaking_feature(self):
        """most_predictive_feature must not be the post-cancellation ticket column."""
        d = load()
        feat = str(d["most_predictive_feature"]).lower().strip()
        assert LEAKING_FEAT not in feat, (
            f"most_predictive_feature='{d['most_predictive_feature']}'. "
            f"support_tickets_after_cancel is filed after churn -- "
            f"it is not available when predicting whether a customer will churn. "
            f"Exclude it from your feature set."
        )

    def test_auc_not_perfect(self):
        """Near-perfect AUC signals a leaking feature was used."""
        d = load()
        auc = float(d["roc_auc"])
        assert auc < 0.95, (
            f"roc_auc={auc:.4f}. AUC near 1.0 strongly suggests a leaking feature. "
            f"Check whether support_tickets_after_cancel is in your model."
        )

    def test_auc_reasonable(self):
        d = load()
        assert float(d["roc_auc"]) > 0.55, "AUC too low -- check model training"
