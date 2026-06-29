You are an accounts payable auditor reviewing January 2024 vendor invoices.

Files under `/root/data/`:
- `invoice_acme.pdf` — invoice from Acme Supplies (INV-2024-001)
- `invoice_techpro.pdf` — invoice from TechPro Ltd (INV-2024-002)
- `invoice_cleanco.pdf` — invoice from CleanCo Services (INV-2024-003)
- `ledger.csv` — accounting ledger: `entry_id`, `vendor`, `description`, `amount`, `invoice_ref`, `date`, `payment_status`

Reconcile the invoices against the ledger and save to **`/root/reconciliation.xlsx`**.

The output workbook must have exactly two sheets:

**Sheet 1 — name: `Ledger vs Invoices`**
Headers (row 1): `invoice_ref`, `vendor`, `invoice_total`, `ledger_total`, `difference`, `status`
One row per invoice (INV-2024-001, INV-2024-002, INV-2024-003), sorted by `invoice_ref`.
- `invoice_total`: total from the PDF invoice
- `ledger_total`: sum of ledger entries for that invoice_ref (0 if none)
- `difference`: invoice_total - ledger_total
- `status`: exactly `"MATCH"` if difference is 0, `"DISCREPANCY"` if not

**Sheet 2 — name: `Discrepancy Report`**
Headers (row 1): `type`, `description`, `amount`
One row per discrepancy found. `type` must be exactly one of:
`"AMOUNT_MISMATCH"`, `"MISSING_FROM_LEDGER"`, `"PHANTOM_ENTRY"`

All monetary values stored as numbers rounded to 2 decimal places.
Column names must match exactly (case-sensitive).
