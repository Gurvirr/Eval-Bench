"""
Verifier for pdf-invoice-reconciliation task.

Agent must parse 3 PDFs and reconcile against ledger.csv.
3 discrepancies:
1. amount_mismatch: Standing Desks $900 invoiced vs $450 in ledger (delta=$450)
2. missing_from_ledger: TechPro INV-2024-002 not in ledger ($519.87)
3. phantom_ledger_entry: L006 $275 with no invoice

Expected:
  total_invoiced:  2805.37
  total_in_ledger: 2110.50
  n_discrepancies: 3
"""
import json
from pathlib import Path

RESULTS_FILE = Path("/root/results.json")
TOL = 1.0


def load():
    assert RESULTS_FILE.exists(), f"Missing: {RESULTS_FILE}"
    return json.loads(RESULTS_FILE.read_text())


class TestInvoiceReconciliation:
    def test_output_exists(self):
        assert RESULTS_FILE.exists()

    def test_total_invoiced(self):
        d = load()
        val = float(d["total_invoiced"])
        assert abs(val - 2805.37) < TOL, \
            f"total_invoiced={val:.2f}, expected 2805.37 (sum of all 3 PDFs)"

    def test_total_in_ledger(self):
        d = load()
        val = float(d["total_in_ledger"])
        assert abs(val - 2110.50) < TOL, \
            f"total_in_ledger={val:.2f}, expected 2110.50"

    def test_n_discrepancies(self):
        """Must find all 3 discrepancies."""
        d = load()
        n = int(d["n_discrepancies"])
        assert n == 3, (
            f"n_discrepancies={n}, expected 3. "
            f"Discrepancies: (1) amount mismatch on Standing Desks, "
            f"(2) TechPro invoice missing from ledger, "
            f"(3) phantom ledger entry L006."
        )

    def test_discrepancy_types_present(self):
        """All 3 discrepancy types must be identified."""
        d = load()
        types = {disc["type"] for disc in d["discrepancies"]}
        assert "amount_mismatch" in types, "Missing amount_mismatch discrepancy"
        assert "missing_from_ledger" in types, "Missing missing_from_ledger discrepancy"
        assert "phantom_ledger_entry" in types, "Missing phantom_ledger_entry discrepancy"

    def test_amount_mismatch_delta(self):
        """Amount mismatch delta must be ~$450."""
        d = load()
        for disc in d["discrepancies"]:
            if disc["type"] == "amount_mismatch":
                assert abs(float(disc["amount_difference"]) - 450.0) < TOL, \
                    f"amount_mismatch delta={disc['amount_difference']}, expected ~450.00"
                return
        assert False, "No amount_mismatch discrepancy found"

    def test_missing_invoice_amount(self):
        """Missing invoice amount must be ~$519.87."""
        d = load()
        for disc in d["discrepancies"]:
            if disc["type"] == "missing_from_ledger":
                assert abs(float(disc["amount_difference"]) - 519.87) < TOL, \
                    f"missing_from_ledger amount={disc['amount_difference']}, expected ~519.87"
                return
        assert False, "No missing_from_ledger discrepancy found"
