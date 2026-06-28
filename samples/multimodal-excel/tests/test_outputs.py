"""
Verifier for multimodal-excel (3-sheet Excel + corrections CSV).

Agent must read Sales, Returns, corrections.csv, join on product_id,
compute net = gross - returns + corrections by region.

Traps:
- Ignore Returns sheet → total too high (~54965 vs 52935)
- Ignore corrections.csv → total off by 570
- Use Targets sheet instead of Returns
- Fail to join returns/corrections to regions

Expected values:
  total_gross: 54965.00
  total_returns: 1460.00
  total_corrections: -570.00
  total_net: 52935.00
  best_region: North
  total_net_units: 866
"""
import json
from pathlib import Path

RESULTS_FILE = Path("/root/results.json")
TOL = 1.0


def load():
    assert RESULTS_FILE.exists(), f"Missing: {RESULTS_FILE}"
    return json.loads(RESULTS_FILE.read_text())


class TestMultimodalExcel:
    def test_output_exists(self):
        assert RESULTS_FILE.exists()

    def test_total_gross_revenue(self):
        d = load()
        val = float(d["total_gross_revenue"])
        assert abs(val - 54965.00) < TOL, f"total_gross={val:.2f}, expected 54965.00"

    def test_total_net_revenue(self):
        """
        Must be 52935.00. If ~54965 → returns/corrections ignored.
        If ~53505 → corrections ignored. If ~54395 → returns ignored.
        """
        d = load()
        val = float(d["total_net_revenue"])
        assert abs(val - 52935.00) < TOL, (
            f"total_net_revenue={val:.2f}, expected 52935.00. "
            f"Formula: gross ({d.get('total_gross_revenue')}) "
            f"- returns ({d.get('total_returns_value')}) "
            f"+ corrections ({d.get('total_corrections_value')})"
        )

    def test_best_region(self):
        d = load()
        assert d["best_region_by_net_revenue"] == "North", \
            f"best_region='{d['best_region_by_net_revenue']}', expected 'North'"

    def test_north_net_revenue(self):
        d = load()
        val = float(d["net_revenue_by_region"]["North"])
        assert abs(val - 17350.00) < TOL, f"North net={val:.2f}, expected 17350.00"

    def test_total_net_units(self):
        d = load()
        n = int(d["total_net_units"])
        assert n == 866, f"total_net_units={n}, expected 866"
