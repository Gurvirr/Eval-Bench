"""
Verifier for simpsons-paradox (severity in separate metadata file).

Agent must join trial.csv with patient_metadata.csv on patient_id,
then stratify by severity_group. Without the join, only overall rates
are visible and the paradox is hidden.

Expected (seed=42):
  overall drug > control (paradox surface)
  within mild/moderate/severe: drug < control (true effect)
  drug_recommended = false
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

    def test_overall_drug_appears_better(self):
        d = load()
        assert float(d["overall_drug_recovery_rate"]) > float(d["overall_control_recovery_rate"]), \
            "Overall drug rate should be higher — check your aggregation"

    def test_subgroup_rates_computed(self):
        """Per-severity rates must be within plausible range — confirms the join was done."""
        d = load()
        for sev in ["mild","moderate","severe"]:
            drug = float(d[f"{sev}_drug_recovery_rate"])
            ctrl = float(d[f"{sev}_control_recovery_rate"])
            assert 0.2 < drug < 0.9, f"{sev} drug rate {drug:.4f} out of plausible range"
            assert 0.2 < ctrl < 0.9, f"{sev} control rate {ctrl:.4f} out of plausible range"

    def test_drug_worse_in_every_subgroup(self):
        d = load()
        for sev in ["mild","moderate","severe"]:
            drug = float(d[f"{sev}_drug_recovery_rate"])
            ctrl = float(d[f"{sev}_control_recovery_rate"])
            assert drug < ctrl, (
                f"{sev}: drug={drug:.4f} >= control={ctrl:.4f}. "
                f"Join trial.csv with patient_metadata.csv to get severity, "
                f"then stratify before concluding."
            )

    def test_drug_not_recommended(self):
        d = load()
        assert d["drug_recommended"] is False, (
            "drug_recommended=True despite drug being worse in every subgroup."
        )
