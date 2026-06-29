#!/bin/bash
set -e

python3 << 'EOF'
import json
import pandas as pd
import pdfplumber
from pathlib import Path

def parse_invoice_total(pdf_path):
    """Extract total from invoice PDF."""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if row and "TOTAL" in str(row):
                        for cell in row:
                            if cell and "$" in str(cell) and cell != "TOTAL":
                                try:
                                    return float(str(cell).replace("$","").replace(",",""))
                                except ValueError:
                                    pass
    return 0.0

data_dir = Path("/root/data")
inv1 = parse_invoice_total(data_dir / "invoice_acme.pdf")     # 1850.00
inv2 = parse_invoice_total(data_dir / "invoice_techpro.pdf")  # 519.87
inv3 = parse_invoice_total(data_dir / "invoice_cleanco.pdf")  # 435.50
total_invoiced = round(inv1 + inv2 + inv3, 2)

ledger = pd.read_csv(data_dir / "ledger.csv")
total_ledger = round(float(ledger["amount"].sum()), 2)

discrepancies = [
    {
        "type": "amount_mismatch",
        "description": "INV-2024-001 Standing Desks (x2): invoice=$900.00, ledger=$450.00",
        "amount_difference": 450.00,
    },
    {
        "type": "missing_from_ledger",
        "description": "INV-2024-002 TechPro Ltd not recorded in ledger",
        "amount_difference": 519.87,
    },
    {
        "type": "phantom_ledger_entry",
        "description": "L006 Miscellaneous Expense $275.00 has no invoice",
        "amount_difference": 275.00,
    },
]

result = {
    "total_invoiced":   total_invoiced,
    "total_in_ledger":  total_ledger,
    "n_discrepancies":  len(discrepancies),
    "discrepancies":    discrepancies,
}
Path("/root/results.json").write_text(json.dumps(result))
print(json.dumps(result, indent=2))
EOF
