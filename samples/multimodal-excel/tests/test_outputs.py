"""
Verifier for multimodal-excel task (two-sheet reconciliation).

Sales sheet: gross sales by region
Returns sheet: returns by region (uses "Region" capitalized, different schema)

Net = gross - returns. Trap: agent reads only Sales sheet, reports gross figures.

Expected net values:
  North: 45230.50 - 2150.00 = 43080.50
  South: 38910.75 - 1820.50 = 37090.25
  East:  52100.00 - 3100.00 = 49000.00
  West:  29840.25 -  990.75 = 28849.50
  Grand total net: 158020.25
  Best region: East
  Total net units: (312+287+401+198) - (15+13+24+7) = 1198 - 59 = 1139
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

    def test_grand_total_net_sales(self):
        """Must be ~158020.25 (gross minus returns). ~166081.50 means returns were ignored."""
        d = load()
        val = float(d["grand_total_net_sales"])
        assert abs(val - 158020.25) < TOL, (
            f"grand_total_net_sales={val:.2f}, expected ~158020.25. "
            f"If you got ~166081.50, you reported gross sales without subtracting returns."
        )

    def test_best_region(self):
        d = load()
        assert d["best_region_by_net_sales"] == "East", \
            f"best_region='{d['best_region_by_net_sales']}', expected 'East'"

    def test_north_net_sales(self):
        d = load()
        val = float(d["north_net_sales"])
        assert abs(val - 43080.50) < TOL, f"north_net_sales={val:.2f}, expected 43080.50"

    def test_east_net_sales(self):
        d = load()
        val = float(d["east_net_sales"])
        assert abs(val - 49000.00) < TOL, f"east_net_sales={val:.2f}, expected 49000.00"

    def test_total_net_units(self):
        d = load()
        n = int(d["total_net_units"])
        assert n == 1139, f"total_net_units={n}, expected 1139"
