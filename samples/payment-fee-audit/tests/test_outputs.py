"""
Verifier for payment-fee-audit task.

Agent must read the PDF fee schedule to extract tiered rates, then apply them.
A model that guesses typical interchange rates (1.5-2% flat) will produce
wrong totals and fail.

Expected values (seed=42):
  total_fees: 827.4824
  debit fees: 97.6967 (n=71)
  credit_standard fees: 293.4092 (n=58)
  credit_premium fees: 324.9452 (n=55)
  corporate fees: 111.4313 (n=16)
"""
import json
from pathlib import Path

RESULTS_FILE = Path("/root/results.json")
TOL = 1.0  # allow $1 tolerance for rounding differences


def load():
    assert RESULTS_FILE.exists(), f"Missing: {RESULTS_FILE}"
    return json.loads(RESULTS_FILE.read_text())


class TestPaymentFeeAudit:
    def test_output_exists(self):
        assert RESULTS_FILE.exists()

    def test_total_fees_correct(self):
        """
        Total fees must be ~827.48. A model using flat 1.5% rate gets ~518.
        A model using flat 2% gets ~690. Only the tiered rates from the PDF give ~827.
        """
        d = load()
        total = float(d["total_fees"])
        assert abs(total - 827.4824) < TOL, (
            f"total_fees={total:.4f}, expected ~827.4824. "
            f"Check that you read the tiered rates from fee_schedule.pdf. "
            f"A flat 1.5% rate gives ~518; correct tiered rates give ~827."
        )

    def test_debit_fees_correct(self):
        d = load()
        fees = float(d["fees_by_card_type"]["debit"])
        assert abs(fees - 97.6967) < TOL, \
            f"debit fees={fees:.4f}, expected ~97.6967 (rate: 0.5% + $0.10)"

    def test_credit_standard_fees_correct(self):
        d = load()
        fees = float(d["fees_by_card_type"]["credit_standard"])
        assert abs(fees - 293.4092) < TOL, \
            f"credit_standard fees={fees:.4f}, expected ~293.4092 (tiered: 1.5%+$0.15 / 1.8%+$0.20)"

    def test_credit_premium_fees_correct(self):
        d = load()
        fees = float(d["fees_by_card_type"]["credit_premium"])
        assert abs(fees - 324.9452) < TOL, \
            f"credit_premium fees={fees:.4f}, expected ~324.9452 (tiered: 2.2%+$0.25 / 2.5%+$0.30)"

    def test_transaction_counts_correct(self):
        d = load()
        counts = d["n_transactions_by_card_type"]
        assert int(counts["debit"]) == 71, f"debit count={counts['debit']}, expected 71"
        assert int(counts["credit_standard"]) == 58
        assert int(counts["credit_premium"]) == 55
        assert int(counts["corporate"]) == 16
