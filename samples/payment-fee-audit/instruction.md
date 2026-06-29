You are a payments analyst auditing interchange fees for Q1 2024.

Files under `/root/data/`:
- `fee_schedule.pdf` — the official interchange fee schedule with rates by card type and amount tier
- `transactions.csv` — processed transactions: `transaction_id`, `card_type`, `amount`, `merchant_id`, `date`

Your task: calculate the correct interchange fee for each transaction using the rates in the PDF, then produce a summary report.

Save results to `/root/results.json`:

```json
{
  "total_fees": 0.0000,
  "fees_by_card_type": {
    "debit": 0.0000,
    "credit_standard": 0.0000,
    "credit_premium": 0.0000,
    "corporate": 0.0000
  },
  "n_transactions_by_card_type": {
    "debit": 0,
    "credit_standard": 0,
    "credit_premium": 0,
    "corporate": 0
  },
  "highest_fee_transaction_id": "string"
}
```

Round all fee values to 4 decimal places.
