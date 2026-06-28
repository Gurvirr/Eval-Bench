"""
Verifier for simpsons-paradox task.

The trap: overall drug recovery rate (0.625) > control (0.559), so a naive
agent concludes the drug works. But within every severity group, drug < control.

Correct answer: drug_recommended = false
Naive (wrong) answer: drug_recommended = true

We also verify the group-level rates are computed correctly.
"""
import json
from pathlib import Path

RESULTS_FILE = Path("/root/results.json")

# Expected values (seed=42)
OVERALL_DRUG    = 0.625
OVERALL_CONTROL = 0.559
MILD_DRUG       = 0.395
MILD_CONTROL    = 0.4988
SEVERE_DRUG     = 0.6825
SEVERE_CONTROL  = 0.800
TOL = 0.02


def load():
    assert RESULTS_FILE.exists(), f"Missing: {RESULTS_FILE}"
    return json.loads(RESULTS_FILE.read_text())


class TestSimpsonParadox:
    def test_output_file_exists(self):
        assert RESULTS_FILE.exists()

    def test_overall_rates_correct(self):
        """Overall rates must match the dataset values."""
        d = load()
        assert abs(float(d["overall_drug_recovery_rate"]) - OVERALL_DRUG) < TOL
        assert abs(float(d["overall_control_recovery_rate"]) - OVERALL_CONTROL) < TOL

    def test_group_rates_correct(self):
        """Per-severity group rates must be computed correctly."""
        d = load()
        assert abs(float(d["mild_drug_recovery_rate"])    - MILD_DRUG)     < TOL
        assert abs(float(d["mild_control_recovery_rate"]) - MILD_CONTROL)  < TOL
        assert abs(float(d["severe_drug_recovery_rate"])  - SEVERE_DRUG)   < TOL
        assert abs(float(d["severe_control_recovery_rate"]) - SEVERE_CONTROL) < TOL

    def test_drug_not_recommended(self):
        """
        drug_recommended must be false.
        The drug appears beneficial overall (0.625 vs 0.559) but is harmful
        within every severity subgroup — a textbook Simpson's Paradox.
        An agent that only looks at overall rates will incorrectly recommend it.
        """
        d = load()
        assert d["drug_recommended"] is False, (
            f"drug_recommended={d['drug_recommended']}. "
            f"Overall drug rate ({d.get('overall_drug_recovery_rate')}) > control "
            f"({d.get('overall_control_recovery_rate')}) is misleading. "
            f"Stratify by severity: drug is worse in both mild and severe groups."
        )
