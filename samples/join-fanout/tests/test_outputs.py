"""
Verifier for join-fanout task (multi-file version).

Orders split across 3 monthly files. Customer tags have M:N relationship.
Naive: join all tags to concatenated orders, sum = 18143 (inflated 1.73x)
Correct: filter by tag membership, sum = 10504

Verifier checks overall_total_revenue and overall_n_orders.
"""
import json
from pathlib import Path

RESULTS_FILE  = Path("/root/results.json")
CORRECT_TOTAL = 10504.00
NAIVE_TOTAL   = 18143.00
TOL = 50.0


def load():
    assert RESULTS_FILE.exists(), f"Missing: {RESULTS_FILE}"
    return json.loads(RESULTS_FILE.read_text())


class TestJoinFanout:
    def test_output_exists(self):
        assert RESULTS_FILE.exists()

    def test_overall_revenue_correct(self):
        """
        overall_total_revenue must be ~10504, not ~18143.
        A value near 18143 means orders were duplicated via M:N tag join.
        """
        d = load()
        total = float(d["overall_total_revenue"])
        assert abs(total - CORRECT_TOTAL) < TOL, (
            f"overall_total_revenue={total:.2f}, expected ~{CORRECT_TOTAL:.2f}. "
            f"If you got ~{NAIVE_TOTAL:.2f}, you joined orders with all tags before summing."
        )

    def test_overall_n_orders(self):
        """Total orders must be 100 across all months — no duplicates."""
        d = load()
        n = int(d["overall_n_orders"])
        assert n == 100, f"overall_n_orders={n}, expected 100. Check for duplicate rows."

    def test_premium_revenue(self):
        d = load()
        rev = float(d["revenue_by_tag"]["premium"])
        assert abs(rev - 4600.0) < TOL, f"premium revenue={rev:.2f}, expected ~4600.00"

    def test_premium_orders(self):
        d = load()
        n = int(d["orders_by_tag"]["premium"])
        assert n == 44, f"premium n_orders={n}, expected 44"
