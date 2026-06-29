You are an accounts payable auditor reviewing January 2024 vendor invoices.

Files under `/root/data/`:
- `invoice_acme.pdf` — invoice from Acme Supplies (INV-2024-001)
- `invoice_techpro.pdf` — invoice from TechPro Ltd (INV-2024-002)
- `invoice_cleanco.pdf` — invoice from CleanCo Services (INV-2024-003)
- `ledger.csv` — accounting ledger entries: `entry_id`, `vendor`, `description`, `amount`, `invoice_ref`, `date`

Your task: reconcile the invoices against the ledger and identify all discrepancies.

Save results to `/root/results.json`:

```json
{
  "total_invoiced": 0.00,
  "total_in_ledger": 0.00,
  "n_discrepancies": 0,
  "discrepancies": [
    {
      "type": "string",
      "description": "string",
      "amount_difference": 0.00
    }
  ]
}
```

Discrepancy types:
- `"amount_mismatch"` — invoice and ledger record different amounts for the same item
- `"missing_from_ledger"` — invoice exists but no ledger entry
- `"phantom_ledger_entry"` — ledger entry with no corresponding invoice

Round all monetary values to 2 decimal places.
