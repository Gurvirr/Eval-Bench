"""
Verifier for class-imbalance-accuracy task (tightened).

Model has recall_fraud ~0.27 — it catches some fraud but misses 73%.
Accuracy is ~0.948. The model looks decent on the surface.

The trap: agent sees reasonable accuracy + some recall + good precision
and recommends deployment. Correct: 73% of fraud undetected is not
acceptable for a payment processor. deploy_recommended = false.

We check recall_fraud < 0.50 (confirms the model is poor) AND
deploy_recommended = false.
"""
import json
from pathlib import Path

RESULTS_FILE = Path("/root/results.json")


def load():
    assert RESULTS_FILE.exists(), f"Missing: {RESULTS_FILE}"
    return json.loads(RESULTS_FILE.read_text())


class TestClassImbalance:
    def test_output_exists(self):
        assert RESULTS_FILE.exists()

    def test_required_keys(self):
        d = load()
        for k in ["accuracy","precision_fraud","recall_fraud","f1_fraud","roc_auc","recommend_deployment"]:
            assert k in d, f"Missing key '{k}'"

    def test_recall_fraud_computed(self):
        """recall_fraud must be in the expected range for this model (~0.27)."""
        d = load()
        rec = float(d["recall_fraud"])
        assert 0.10 < rec < 0.50, (
            f"recall_fraud={rec:.4f}. Expected ~0.27 for this model. "
            f"Check that you're computing recall on the positive (fraud) class."
        )

    def test_not_recommended(self):
        """
        deploy_recommended must be false.
        The model detects only ~27% of fraud cases — 73% of fraud goes undetected.
        For a payment processor, this is not acceptable despite decent accuracy and precision.
        """
        d = load()
        assert d["recommend_deployment"] is False, (
            f"recommend_deployment=True, but recall_fraud={d.get('recall_fraud'):.4f} "
            f"means {(1-float(d.get('recall_fraud'))):.0%} of fraud goes undetected. "
            f"Accuracy ({d.get('accuracy'):.4f}) is misleading on this imbalanced dataset."
        )

    def test_accuracy_high(self):
        """Accuracy should be high (~0.95) — confirms the imbalance trap is present."""
        d = load()
        assert float(d["accuracy"]) > 0.90, "Accuracy should be >0.90 on this imbalanced dataset"
