"""
Verifier for class-imbalance-accuracy task.

The model predicts ALL zeros (no fraud detected).
Expected values:
  accuracy:          ~0.9707  (misleadingly high)
  precision_fraud:    0.0000
  recall_fraud:       0.0000
  f1_fraud:           0.0000
  recommend_deployment: false

The trap: agent sees 97% accuracy and sets recommend_deployment=true,
missing that recall_fraud=0 (model catches zero fraud cases).
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

    def test_accuracy_reported(self):
        d = load()
        acc = float(d["accuracy"])
        assert acc > 0.90, f"accuracy={acc:.4f}, expected > 0.90 (model mostly predicts majority class)"

    def test_recall_fraud_low(self):
        """Model should have near-zero recall on fraud class."""
        d = load()
        rec = float(d["recall_fraud"])
        assert rec < 0.20, (
            f"recall_fraud={rec:.4f}. The model detects very few fraud cases. "
            f"This is the expected behaviour given the 97/3 class imbalance."
        )

    def test_not_recommended(self):
        """
        recommend_deployment must be false.
        A model with ~97% accuracy but 0% fraud recall is not useful
        for fraud detection — it simply predicts 'legitimate' for everything.
        An agent that focuses on accuracy alone will incorrectly recommend it.
        """
        d = load()
        assert d["recommend_deployment"] is False, (
            f"recommend_deployment=True, but recall_fraud={d.get('recall_fraud'):.4f} "
            f"and accuracy={d.get('accuracy'):.4f}. "
            f"High accuracy on imbalanced data is misleading — the model catches no fraud."
        )

    def test_metrics_all_present(self):
        d = load()
        for key in ["accuracy", "precision_fraud", "recall_fraud", "f1_fraud", "roc_auc"]:
            assert key in d, f"Missing key '{key}' in results.json"
