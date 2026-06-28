"""
Verifier for join-fanout task.

The trap: joining orders with customer_tags (M:N) then summing revenue
inflates the total by ~1.81x because customers with multiple tags have
their orders duplicated in the joined table.

Correct overall_total_revenue: 10283.00
Naive (join-all-then-sum) total: 18641.00

We check overall_total_revenue is close to 10283, NOT close to 18641.
"""
import json
from pathlib import Path

RESULTS_FILE = Path("/root/results.json")
CORRECT_TOTAL = 10283.00
NAIVE_TOTAL   = 18641.00
TOL = 50.0  # allow small floating point variance


def load():
    assert RESULTS_FILE.exists(), f"Missing: {RESULTS_FILE}"
    return json.loads(RESULTS_FILE.read_text())


class TestJoinFanout:
    def test_output_exists(self):
        assert RESULTS_FILE.exists()

    def test_overall_revenue_correct(self):
        """
        overall_total_revenue must be ~10283, not ~18641.
        A value near 18641 means the agent joined orders with all tags
        (creating duplicate rows per customer) before summing revenue.
        """
        d = load()
        total = float(d["overall_total_revenue"])
        assert abs(total - CORRECT_TOTAL) < TOL, (
            f"overall_total_revenue={total:.2f}, expected ~{CORRECT_TOTAL:.2f}. "
            f"If you got ~{NAIVE_TOTAL:.2f}, you joined orders with all customer tags "
            f"before summing — customers with multiple tags had their orders counted multiple times."
        )

    def test_overall_n_orders(self):
        """Total order count must be 100 (no duplicates)."""
        d = load()
        n = int(d["overall_n_orders"])
        assert n == 100, f"overall_n_orders={n}, expected 100. Check for duplicate rows after join."

    def test_per_tag_revenue_premium(self):
        """Premium tag revenue should be ~5741 (53 orders from premium customers)."""
        d = load()
        rev = float(d["revenue_by_tag"]["premium"])
        assert abs(rev - 5741.0) < TOL, f"premium revenue={rev:.2f}, expected ~5741.00"

    def test_per_tag_orders_premium(self):
        d = load()
        n = int(d["orders_by_tag"]["premium"])
        assert n == 53, f"premium n_orders={n}, expected 53"
