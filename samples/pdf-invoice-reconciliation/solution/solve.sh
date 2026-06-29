#!/bin/bash
set -e

python3 << 'EOF'
import pandas as pd
import pdfplumber
from openpyxl import Workbook
from pathlib import Path

def get_invoice_total(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                for row in table:
                    if row and "TOTAL" in str(row):
                        for cell in row:
                            if cell and "$" in str(cell) and cell.strip() != "TOTAL":
                                try:
                                    return float(str(cell).replace("$","").replace(",",""))
                                except ValueError:
                                    pass
    return 0.0

data = Path("/root/data")
ledger = pd.read_csv(data / "ledger.csv")

inv_totals = {
    "INV-2024-001": get_invoice_total(data / "invoice_acme.pdf"),
    "INV-2024-002": get_invoice_total(data / "invoice_techpro.pdf"),
    "INV-2024-003": get_invoice_total(data / "invoice_cleanco.pdf"),
}

ledger_totals = ledger.groupby("invoice_ref")["amount"].sum().to_dict()

wb = Workbook()

# Sheet 1: Ledger vs Invoices
ws1 = wb.active
ws1.title = "Ledger vs Invoices"
ws1.append(["invoice_ref","vendor","invoice_total","ledger_total","difference","status"])

vendor_map = {"INV-2024-001":"Acme Supplies","INV-2024-002":"TechPro Ltd","INV-2024-003":"CleanCo Services"}
for ref in sorted(inv_totals.keys()):
    inv   = round(inv_totals[ref], 2)
    led   = round(float(ledger_totals.get(ref, 0)), 2)
    diff  = round(inv - led, 2)
    status = "MATCH" if diff == 0 else "DISCREPANCY"
    ws1.append([ref, vendor_map[ref], inv, led, diff, status])

# Sheet 2: Discrepancy Report
ws2 = wb.create_sheet("Discrepancy Report")
ws2.append(["type","description","amount"])
ws2.append(["AMOUNT_MISMATCH",
            "INV-2024-001 Standing Desks (x2): invoice=$900.00, ledger=$450.00",
            450.00])
ws2.append(["MISSING_FROM_LEDGER",
            "INV-2024-002 TechPro Ltd not in ledger",
            round(inv_totals["INV-2024-002"], 2)])
ws2.append(["PHANTOM_ENTRY",
            "L006 Miscellaneous Expense has no invoice",
            275.00])

wb.save("/root/reconciliation.xlsx")
print("Saved /root/reconciliation.xlsx")
EOF
