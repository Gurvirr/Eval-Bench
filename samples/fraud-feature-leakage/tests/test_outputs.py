"""
Verifier for fraud-feature-leakage.

chargeback_filed: a chargeback is filed by the customer AFTER a fraudulent
transaction is disputed with their bank. It is not available at transaction
time when a fraud prediction needs to be made.

With leaking feature: AUC ~0.98, top feature = chargeback_filed
Without it:           AUC ~0.70, top feature = user_account_age_days

Checks:
1. most_predictive_feature != "chargeback_filed"
2. roc_auc < 0.95 (near-perfect AUC signals leakage)
3. roc_auc > 0.55 (confirms a real model was trained)
"""
import json
from pathlib import Path

RESULTS_FILE = Path("/root/results.json")
LEAKING_FEAT = "chargeback_filed"


def load():
    assert RESULTS_FILE.exists(), f"Missing: {RESULTS_FILE}"
    return json.loads(RESULTS_FILE.read_text())


class TestFraudLeakage:
    def test_output_exists(self):
        assert RESULTS_FILE.exists()

    def test_required_keys(self):
        d = load()
        assert "roc_auc" in d and "most_predictive_feature" in d

    def test_no_leaking_feature(self):
        """most_predictive_feature must not be chargeback_filed."""
        d = load()
        feat = str(d["most_predictive_feature"]).lower().strip()
        assert LEAKING_FEAT not in feat, (
            f"most_predictive_feature='{d['most_predictive_feature']}'. "
            f"chargeback_filed is a post-transaction signal -- "
            f"chargebacks are filed after fraud is detected, not before. "
            f"Exclude it from your feature set."
        )

    def test_auc_not_perfect(self):
        """Near-perfect AUC signals a leaking feature was used."""
        d = load()
        auc = float(d["roc_auc"])
        assert auc < 0.95, (
            f"roc_auc={auc:.4f}. AUC near 1.0 strongly suggests leakage. "
            f"Check whether chargeback_filed is in your feature set."
        )

    def test_auc_reasonable(self):
        d = load()
        assert float(d["roc_auc"]) > 0.55, "AUC too low -- check model training"
