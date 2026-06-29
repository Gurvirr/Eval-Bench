You are a payments analyst auditing interchange fees for Q1 2024.

Files under `/root/data/`:
- `fee_schedule.pdf` — the official interchange fee schedule (4 sections: base rates, volume discount, dispute surcharge, fee cap)
- `transactions.csv` — transactions: `transaction_id`, `card_type`, `amount`, `merchant_id`, `date`, `is_disputed`, `month`, `monthly_volume`

Apply all fee rules from the PDF to each transaction and save to **`/root/fee_audit.xlsx`**.

The output workbook must have exactly two sheets:

**Sheet 1 — name: `Transaction Fees`**
Headers (row 1): `transaction_id`, `card_type`, `amount`, `is_disputed`, `monthly_volume`, `base_fee`, `final_fee`
One row per transaction (200 rows), sorted by `transaction_id`.
- `base_fee`: fee before dispute surcharge and volume discount
- `final_fee`: fee after applying all rules from the PDF, rounded to 4 decimal places

**Sheet 2 — name: `Merchant Summary`**
Headers (row 1): `merchant_id`, `n_transactions`, `total_amount`, `total_fees`, `volume_discount_applied`
One row per merchant (10 merchants), sorted by `merchant_id` ascending.
- `volume_discount_applied`: `"YES"` if merchant received volume discount, `"NO"` if not

All monetary values stored as numbers. Column names must match exactly (case-sensitive).
