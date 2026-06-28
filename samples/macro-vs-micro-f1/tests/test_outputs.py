"""
Verifier for macro-vs-micro-f1 task.

Expected values (seed=42, C=0.1):
  f1_macro:    ~0.2225  (correct — penalizes minority class failures equally)
  f1_weighted: ~0.7119  (misleading — dominated by majority class)
  accuracy:    ~0.8000  (most misleading — model just predicts class 0)

The task asks for f1_macro. An agent that computes the correct value passes.
We check f1_macro is in [0.15, 0.35] — the correct range given the model behaviour.
A value > 0.60 suggests the agent reported weighted F1 or accuracy instead.
"""
import json
from pathlib import Path

RESULTS_FILE  = Path("/root/results.json")
CORRECT_MACRO = 0.2225
TOL = 0.08


def load():
    assert RESULTS_FILE.exists(), f"Missing: {RESULTS_FILE}"
    return json.loads(RESULTS_FILE.read_text())


class TestMacroF1:
    def test_output_exists(self):
        assert RESULTS_FILE.exists()

    def test_f1_macro_reported(self):
        """results.json must contain f1_macro."""
        d = load()
        assert "f1_macro" in d, "Missing key 'f1_macro' in results.json"

    def test_f1_macro_correct(self):
        """
        f1_macro must be in the correct range (~0.22).
        A value > 0.60 means the agent reported weighted F1 or accuracy instead —
        both of which hide the model's complete failure on minority classes.
        """
        d = load()
        val = float(d["f1_macro"])
        assert abs(val - CORRECT_MACRO) < TOL, (
            f"f1_macro={val:.4f}, expected ~{CORRECT_MACRO:.4f}. "
            f"If you got ~0.71 or ~0.80, you reported weighted F1 or accuracy. "
            f"Use f1_score(y_test, y_pred, average='macro')."
        )

    def test_f1_macro_not_weighted(self):
        """Confirm the reported f1_macro is not actually weighted F1."""
        d = load()
        val = float(d["f1_macro"])
        assert val < 0.60, (
            f"f1_macro={val:.4f} is too high. "
            f"This looks like weighted F1 (~0.71) or accuracy (~0.80), not macro F1 (~0.22)."
        )
