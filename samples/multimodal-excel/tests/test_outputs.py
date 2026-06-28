"""
Verifier for multimodal-excel task.

The trap: naive pd.read_excel() reads the whole sheet as one table,
mixing the regional summary and product table headers/data together.

Expected values (hardcoded from build_inputs.py):
  grand_total_sales:       166081.50
  best_region_by_sales:    "East"
  top_product_by_revenue:  "Wireless Headphones"
  avg_price_north_region:  145.00
  total_units_all_regions: 1198
"""
import json
from pathlib import Path

RESULTS_FILE = Path("/root/results.json")


def load():
    assert RESULTS_FILE.exists(), f"Missing: {RESULTS_FILE}"
    return json.loads(RESULTS_FILE.read_text())


class TestMultimodalExcel:
    def test_output_exists(self):
        assert RESULTS_FILE.exists()

    def test_grand_total_sales(self):
        d = load()
        val = float(d["grand_total_sales"])
        assert abs(val - 166081.50) < 1.0, (
            f"grand_total_sales={val:.2f}, expected 166081.50. "
            f"Check that you read only the regional summary section (rows 1-4)."
        )

    def test_best_region(self):
        d = load()
        assert d["best_region_by_sales"] == "East", (
            f"best_region_by_sales='{d['best_region_by_sales']}', expected 'East'."
        )

    def test_top_product(self):
        d = load()
        assert d["top_product_by_revenue"] == "Wireless Headphones", (
            f"top_product_by_revenue='{d['top_product_by_revenue']}', "
            f"expected 'Wireless Headphones'. "
            f"Check that you read the products section starting after the blank row."
        )

    def test_avg_price_north(self):
        d = load()
        val = float(d["avg_price_north_region"])
        assert abs(val - 145.00) < 0.5, (
            f"avg_price_north_region={val:.2f}, expected 145.00."
        )

    def test_total_units(self):
        d = load()
        n = int(d["total_units_all_regions"])
        assert n == 1198, (
            f"total_units_all_regions={n}, expected 1198. "
            f"Ensure you only sum units from the regional section, not the products section."
        )
