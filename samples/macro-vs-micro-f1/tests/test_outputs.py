"""
Verifier for macro-vs-micro-f1 task.

The task asks the agent to CHOOSE the right F1 metric.
Correct answer: recommended_metric = "macro", f1_score ~0.22, deploy_recommended = false.

Trap: agents default to "weighted" or "micro" (both ~0.71/0.80),
which hides the model's complete failure on minority classes.
"""
import json
from pathlib import Path

RESULTS_FILE  = Path("/root/results.json")
CORRECT_MACRO = 0.2225
WEIGHTED_F1   = 0.7119
TOL = 0.10


def load():
    assert RESULTS_FILE.exists(), f"Missing: {RESULTS_FILE}"
    return json.loads(RESULTS_FILE.read_text())


class TestMacroF1:
    def test_output_exists(self):
        assert RESULTS_FILE.exists()

    def test_required_keys(self):
        d = load()
        for key in ["f1_score", "accuracy", "recommended_metric", "deploy_recommended"]:
            assert key in d, f"Missing key '{key}' in results.json"

    def test_recommended_metric_is_macro(self):
        """
        The correct metric for imbalanced multiclass classification is macro F1.
        Weighted F1 and accuracy both hide minority class failures.
        """
        d = load()
        metric = str(d["recommended_metric"]).lower()
        assert "macro" in metric, (
            f"recommended_metric='{d['recommended_metric']}'. "
            f"For a content moderation system where every class matters equally, "
            f"macro F1 is the correct choice. Weighted F1 and accuracy are dominated "
            f"by the majority 'safe' class and hide failures on harassment/hate speech."
        )

    def test_f1_score_matches_macro(self):
        """f1_score must be the macro value (~0.22), not weighted (~0.71)."""
        d = load()
        val = float(d["f1_score"])
        assert abs(val - CORRECT_MACRO) < TOL, (
            f"f1_score={val:.4f} but recommended_metric=macro implies ~{CORRECT_MACRO:.4f}. "
            f"A value near {WEIGHTED_F1:.4f} means you reported weighted F1, not macro."
        )

    def test_not_recommended_for_deployment(self):
        """
        A model with macro F1 ~0.22 should NOT be recommended for production.
        It catches essentially no harassment or hate speech.
        """
        d = load()
        assert d["deploy_recommended"] is False, (
            f"deploy_recommended=True but macro F1 ~0.22 means the model fails "
            f"on the safety-critical minority classes. Do not deploy."
        )
