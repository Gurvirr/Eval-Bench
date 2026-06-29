"""
Verifier for cohort-retention task.

Expected retention rates (seed=42):
  Jan: [1.0, 0.5960, 0.4340, 0.3080]
  Feb: [1.0, 0.5810, 0.3929, 0.2619]
  Mar: [1.0, 0.5237, 0.3816, 0.2132]

Common errors:
- Off-by-one on month boundaries
- Counting cumulative activity instead of per-month
- Not parsing comma-separated active_months correctly
"""
import json
from pathlib import Path

RESULTS_FILE = Path("/root/results.json")
TOL = 0.02

EXPECTED = {
    "jan": {"month_0":1.0, "month_1":0.5960, "month_2":0.4340, "month_3":0.3080},
    "feb": {"month_0":1.0, "month_1":0.5810, "month_2":0.3929, "month_3":0.2619},
    "mar": {"month_0":1.0, "month_1":0.5237, "month_2":0.3816, "month_3":0.2132},
}


def load():
    assert RESULTS_FILE.exists(), f"Missing: {RESULTS_FILE}"
    return json.loads(RESULTS_FILE.read_text())


class TestCohortRetention:
    def test_output_exists(self):
        assert RESULTS_FILE.exists()

    def test_cohort_sizes(self):
        d = load()
        assert int(d["jan_cohort_size"]) == 500
        assert int(d["feb_cohort_size"]) == 420
        assert int(d["mar_cohort_size"]) == 380

    def test_month_0_is_100_percent(self):
        d = load()
        for cohort in ["jan","feb","mar"]:
            assert float(d["retention"][cohort]["month_0"]) == 1.0, \
                f"{cohort} month_0 != 1.0 — all users are active in their signup month"

    def test_jan_retention(self):
        d = load()
        r = d["retention"]["jan"]
        for key, expected in EXPECTED["jan"].items():
            val = float(r[key])
            assert abs(val - expected) < TOL, \
                f"jan {key}={val:.4f}, expected ~{expected:.4f}"

    def test_feb_retention(self):
        d = load()
        r = d["retention"]["feb"]
        for key, expected in EXPECTED["feb"].items():
            val = float(r[key])
            assert abs(val - expected) < TOL, \
                f"feb {key}={val:.4f}, expected ~{expected:.4f}"

    def test_mar_retention(self):
        d = load()
        r = d["retention"]["mar"]
        for key, expected in EXPECTED["mar"].items():
            val = float(r[key])
            assert abs(val - expected) < TOL, \
                f"mar {key}={val:.4f}, expected ~{expected:.4f}"
