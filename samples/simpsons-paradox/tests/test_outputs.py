"""
Verifier for simpsons-paradox task (3 severity groups).

Overall drug rate > control (paradox holds).
Within every subgroup (mild, moderate, severe), drug < control.
Correct answer: drug_recommended = false.
"""
import json
from pathlib import Path

RESULTS_FILE = Path("/root/results.json")
TOL = 0.03


def load():
    assert RESULTS_FILE.exists(), f"Missing: {RESULTS_FILE}"
    return json.loads(RESULTS_FILE.read_text())


class TestSimpsonParadox:
    def test_output_exists(self):
        assert RESULTS_FILE.exists()

    def test_required_keys(self):
        d = load()
        for k in ["overall_drug_recovery_rate","overall_control_recovery_rate",
                  "mild_drug_recovery_rate","mild_control_recovery_rate",
                  "moderate_drug_recovery_rate","moderate_control_recovery_rate",
                  "severe_drug_recovery_rate","severe_control_recovery_rate",
                  "drug_recommended"]:
            assert k in d, f"Missing key '{k}'"

    def test_overall_drug_looks_better(self):
        """Overall drug rate must be higher than control (the paradox surface)."""
        d = load()
        assert float(d["overall_drug_recovery_rate"]) > float(d["overall_control_recovery_rate"]), \
            "Overall drug rate should be higher — check your aggregation"

    def test_drug_worse_in_every_subgroup(self):
        """Drug must be worse than control within every severity group."""
        d = load()
        for sev in ["mild", "moderate", "severe"]:
            drug    = float(d[f"{sev}_drug_recovery_rate"])
            control = float(d[f"{sev}_control_recovery_rate"])
            assert drug < control, (
                f"{sev}: drug={drug:.4f} >= control={control:.4f}. "
                f"Check your per-severity groupby."
            )

    def test_drug_not_recommended(self):
        """
        drug_recommended must be false.
        The drug appears beneficial overall but is harmful in every subgroup.
        """
        d = load()
        assert d["drug_recommended"] is False, (
            f"drug_recommended=True despite drug being worse in every severity subgroup. "
            f"The overall benefit is a Simpson's Paradox caused by severity confounding."
        )
