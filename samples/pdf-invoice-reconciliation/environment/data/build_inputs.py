"""
Generates 3 vendor invoice PDFs + ledger.csv for reconciliation task.

The invoices total $X but the ledger has 3 discrepancies:
1. One invoice line item recorded at wrong amount ($450 vs $540)
2. One invoice not recorded in ledger at all (missing)
3. One ledger entry has no corresponding invoice (phantom charge)

Agent must: parse 3 PDFs, compare to ledger, identify all 3 discrepancies.
"""
import numpy as np
import pandas as pd
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

RNG = np.random.default_rng(42)
OUT = Path("/root/data")
OUT.mkdir(parents=True, exist_ok=True)

styles = getSampleStyleSheet()

def make_invoice_pdf(path, vendor, invoice_num, date, items):
    doc = SimpleDocTemplate(str(path), pagesize=letter)
    content = []
    content.append(Paragraph(f"Invoice #{invoice_num}", styles["Title"]))
    content.append(Paragraph(f"Vendor: {vendor} | Date: {date}", styles["Normal"]))
    content.append(Spacer(1, 12))

    total = sum(qty * price for _, qty, price in items)
    data = [["Description", "Qty", "Unit Price", "Total"]]
    for desc, qty, price in items:
        data.append([desc, str(qty), f"${price:.2f}", f"${qty*price:.2f}"])
    data.append(["", "", "TOTAL", f"${total:.2f}"])

    t = Table(data, colWidths=[200, 50, 80, 80])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.whitesmoke),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("GRID",       (0,0), (-1,-1), 0.5, colors.black),
        ("FONTNAME",   (0,-1), (-1,-1), "Helvetica-Bold"),
    ]))
    content.append(t)
    doc.build(content)
    return total

# Invoice 1: Acme Supplies
inv1_items = [
    ("Office Chairs (x5)", 5, 120.00),   # 600.00
    ("Standing Desks (x2)", 2, 450.00),  # 900.00  <- ledger records this as $450 TOTAL not $900
    ("Monitor Stands (x10)", 10, 35.00), # 350.00
]
inv1_total = make_invoice_pdf(OUT/"invoice_acme.pdf", "Acme Supplies", "INV-2024-001", "2024-01-15", inv1_items)

# Invoice 2: TechPro (this invoice is NOT in the ledger at all)
inv2_items = [
    ("Laptop Dock x3", 3, 89.99),   # 269.97
    ("USB Hubs x10", 10, 24.99),    # 249.90
]
inv2_total = make_invoice_pdf(OUT/"invoice_techpro.pdf", "TechPro Ltd", "INV-2024-002", "2024-01-22", inv2_items)

# Invoice 3: CleanCo
inv3_items = [
    ("Cleaning Service - Jan", 1, 350.00),  # 350.00
    ("Supplies Restocking", 1, 85.50),       # 85.50
]
inv3_total = make_invoice_pdf(OUT/"invoice_cleanco.pdf", "CleanCo Services", "INV-2024-003", "2024-01-31", inv3_items)

# Ledger CSV — contains discrepancies
ledger_rows = [
    {"entry_id": "L001", "vendor": "Acme Supplies",   "description": "Office Chairs (x5)",  "amount": 600.00, "invoice_ref": "INV-2024-001", "date": "2024-01-15", "payment_status": "paid"},
    {"entry_id": "L002", "vendor": "Acme Supplies",   "description": "Standing Desks (x2)", "amount": 450.00, "invoice_ref": "INV-2024-001", "date": "2024-01-15", "payment_status": "paid"},  # WRONG: should be 900.00
    {"entry_id": "L003", "vendor": "Acme Supplies",   "description": "Monitor Stands (x10)","amount": 350.00, "invoice_ref": "INV-2024-001", "date": "2024-01-15", "payment_status": "paid"},
    # Invoice 2 NOT in ledger (missing)
    {"entry_id": "L004", "vendor": "CleanCo Services","description": "Cleaning Service - Jan","amount": 350.00,"invoice_ref": "INV-2024-003","date": "2024-01-31", "payment_status": "paid"},
    {"entry_id": "L005", "vendor": "CleanCo Services","description": "Supplies Restocking",  "amount":  85.50, "invoice_ref": "INV-2024-003","date": "2024-01-31", "payment_status": "paid"},
    # Phantom entry — no invoice, marked as "pending" (not paid) — model may skip it
    {"entry_id": "L006", "vendor": "Unknown Vendor",  "description": "Miscellaneous Expense","amount": 275.00, "invoice_ref": None,          "date": "2024-01-28", "payment_status": "pending"},
]

pd.DataFrame(ledger_rows).to_csv(OUT / "ledger.csv", index=False)

print(f"Invoice 1 (Acme) total:   ${inv1_total:.2f}")
print(f"Invoice 2 (TechPro) total:${inv2_total:.2f}")
print(f"Invoice 3 (CleanCo) total:${inv3_total:.2f}")
print(f"Total invoiced: ${inv1_total+inv2_total+inv3_total:.2f}")
print(f"Total in ledger: {sum(r['amount'] for r in ledger_rows):.2f}")
print("Discrepancies:")
print("  1. L002 Standing Desks: ledger=$450, invoice=$900 (delta=$450)")
print("  2. INV-2024-002 TechPro missing from ledger ($519.87)")
print("  3. L006 phantom entry ($275.00, no invoice)")
