"""
Verifier for payment-fee-audit task (Excel output with strict format).

Agent must produce /root/fee_audit.xlsx with:
- Sheet "Transaction Fees": exact headers, 200 rows sorted by transaction_id
  - rate_tier must use exact string values (e.g. "credit_standard_low")
  - fee must match rates from PDF exactly
- Sheet "Summary": exact headers, sorted alphabetically by card_type

Traps:
- Wrong sheet names
- Wrong rate_tier strings
- Using flat rate instead of tiered rates from PDF
- Storing fees as strings
- Wrong sort order
"""
from openpyxl import load_workbook
from pathlib import Path

OUTPUT_FILE = Path("/root/fee_audit.xlsx")
TOL = 0.01

VALID_TIERS = {"debit","credit_standard_low","credit_standard_high",
               "credit_premium_low","credit_premium_high","corporate"}

EXPECTED_SUMMARY = {
    "corporate":        {"n": 16,  "total": 111.4313},
    "credit_premium":   {"n": 55,  "total": 324.9452},
    "credit_standard":  {"n": 58,  "total": 293.4092},
    "debit":            {"n": 71,  "total":  97.6967},
}


def header_map(ws, row=1):
    return {str(c.value).strip(): i for i, c in enumerate(ws[row], 1) if c.value}


class TestPaymentFeeAudit:
    def test_output_exists(self):
        assert OUTPUT_FILE.exists(), f"Missing: {OUTPUT_FILE}"

    def test_required_sheets(self):
        wb = load_workbook(OUTPUT_FILE, data_only=True)
        assert "Transaction Fees" in wb.sheetnames, \
            f"Missing 'Transaction Fees'. Found: {wb.sheetnames}"
        assert "Summary" in wb.sheetnames, \
            f"Missing 'Summary'. Found: {wb.sheetnames}"

    def test_transaction_fees_headers(self):
        wb = load_workbook(OUTPUT_FILE, data_only=True)
        cols = header_map(wb["Transaction Fees"])
        for h in ["transaction_id","card_type","amount","fee","rate_tier"]:
            assert h in cols, f"Missing column '{h}' in Transaction Fees"

    def test_row_count(self):
        wb = load_workbook(OUTPUT_FILE, data_only=True)
        ws = wb["Transaction Fees"]
        rows = [r for r in ws.iter_rows(min_row=2, values_only=True) if r[0]]
        assert len(rows) == 200, f"Expected 200 rows, got {len(rows)}"

    def test_rate_tier_values(self):
        """rate_tier must use exact tier string names."""
        wb = load_workbook(OUTPUT_FILE, data_only=True)
        ws = wb["Transaction Fees"]
        cols = header_map(ws)
        for row in ws.iter_rows(min_row=2, values_only=True):
            if not row[0]: continue
            tier = str(row[cols["rate_tier"]-1])
            assert tier in VALID_TIERS, \
                f"Invalid rate_tier='{tier}'. Must be one of {sorted(VALID_TIERS)}"

    def test_summary_total_fees(self):
        """Total fees by card type must match tiered rates from PDF."""
        wb = load_workbook(OUTPUT_FILE, data_only=True)
        ws = wb["Summary"]
        cols = header_map(ws)
        for row in ws.iter_rows(min_row=2, values_only=True):
            if not row[0]: continue
            ct    = str(row[cols["card_type"]-1])
            total = float(row[cols["total_fees"]-1])
            if ct in EXPECTED_SUMMARY:
                exp = EXPECTED_SUMMARY[ct]["total"]
                assert abs(total - exp) < TOL, \
                    f"{ct} total_fees={total:.4f}, expected ~{exp:.4f}"

    def test_summary_sorted_alphabetically(self):
        wb = load_workbook(OUTPUT_FILE, data_only=True)
        ws = wb["Summary"]
        cols = header_map(ws)
        card_types = [str(r[cols["card_type"]-1]) for r in ws.iter_rows(min_row=2, values_only=True) if r[0]]
        assert card_types == sorted(card_types), \
            f"Summary not sorted alphabetically by card_type: {card_types}"
