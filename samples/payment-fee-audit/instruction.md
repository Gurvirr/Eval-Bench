You are a payments analyst auditing interchange fees for Q1 2024.

Files under `/root/data/`:
- `fee_schedule.pdf` — the official interchange fee schedule with rates by card type and amount tier
- `transactions.csv` — processed transactions: `transaction_id`, `card_type`, `amount`, `merchant_id`, `date`

Compute the correct interchange fee for each transaction using the rates in the PDF and save to **`/root/fee_audit.xlsx`**.

The output workbook must have exactly two sheets:

**Sheet 1 — name: `Transaction Fees`**
Headers (row 1): `transaction_id`, `card_type`, `amount`, `fee`, `rate_tier`
One row per transaction (200 rows), sorted by `transaction_id` ascending.
- `fee`: calculated fee as a number, rounded to 4 decimal places
- `rate_tier`: the tier applied, exactly one of: `"debit"`, `"credit_standard_low"`, `"credit_standard_high"`, `"credit_premium_low"`, `"credit_premium_high"`, `"corporate"`

**Sheet 2 — name: `Summary`**
Headers (row 1): `card_type`, `n_transactions`, `total_fees`, `avg_fee`
One row per card type, sorted alphabetically by `card_type`.
- `total_fees` and `avg_fee`: rounded to 4 decimal places

Column names must match exactly (case-sensitive). Values must be stored as numbers, not strings.
