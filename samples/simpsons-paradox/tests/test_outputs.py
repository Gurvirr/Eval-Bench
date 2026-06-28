"""
Verifier for simpsons-paradox (3-hospital multi-file version).

Agent must: normalize 3 different CSV schemas, handle Yes/No encoding,
normalize dirty severity labels, then compute stratified analysis.

Expected: drug_recommended=False, total_patients=2300
Overall drug (0.606) > control (0.592) — paradox holds
Within every subgroup: drug < control
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
                  "total_patients","drug_recommended"]:
            assert k in d, f"Missing key '{k}'"

    def test_total_patients(self):
        """Must have combined all 3 hospital files: 2300 total patients."""
        d = load()
        n = int(d["total_patients"])
        assert abs(n - 2300) < 10, (
            f"total_patients={n}, expected ~2300. "
            f"Check that you loaded and combined all 3 hospital CSV files."
        )

    def test_overall_rates(self):
        d = load()
        drug = float(d["overall_drug_recovery_rate"])
        ctrl = float(d["overall_control_recovery_rate"])
        assert abs(drug - 0.6064) < TOL, f"overall_drug={drug:.4f}, expected ~0.6064"
        assert abs(ctrl - 0.5924) < TOL, f"overall_control={ctrl:.4f}, expected ~0.5924"

    def test_drug_worse_in_every_subgroup(self):
        d = load()
        for sev in ["mild","moderate","severe"]:
            drug = float(d[f"{sev}_drug_recovery_rate"])
            ctrl = float(d[f"{sev}_control_recovery_rate"])
            assert drug < ctrl, (
                f"{sev}: drug={drug:.4f} >= control={ctrl:.4f}. "
                f"Normalize severity labels (strip/lowercase) before groupby."
            )

    def test_drug_not_recommended(self):
        d = load()
        assert d["drug_recommended"] is False, (
            "drug_recommended=True despite drug being worse in every subgroup. "
            "The overall benefit is confounded by severity distribution."
        )
