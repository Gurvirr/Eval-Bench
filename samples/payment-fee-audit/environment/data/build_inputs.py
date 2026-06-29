"""
Generates fee_schedule.pdf and transactions.csv for the payment-fee-audit task.

The fee schedule has tiered interchange rates:
- debit cards: 0.5% + $0.10 flat (all amounts)
- credit_standard: 1.5% + $0.15 (amount < $100), 1.8% + $0.20 (amount >= $100)
- credit_premium: 2.2% + $0.25 (amount < $200), 2.5% + $0.30 (amount >= $200)
- corporate: 2.8% + $0.35 flat (all amounts)

The model must read the PDF to get these rates — guessing typical interchange
rates (1.5-2%) will produce wrong totals.
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

# --- Generate PDF fee schedule ---
doc = SimpleDocTemplate(str(OUT / "fee_schedule.pdf"), pagesize=letter)
styles = getSampleStyleSheet()
content = []

content.append(Paragraph("Interchange Fee Schedule — Q1 2024", styles["Title"]))
content.append(Spacer(1, 12))
content.append(Paragraph(
    "The following rates apply to all processed transactions. "
    "Fees are calculated as: fee = amount × rate + flat_fee. "
    "Tiered rates apply based on transaction amount thresholds.",
    styles["Normal"]
))
content.append(Spacer(1, 12))

fee_data = [
    ["Card Type", "Amount Threshold", "Rate (%)", "Flat Fee ($)"],
    ["debit",          "any amount",   "0.50%", "$0.10"],
    ["credit_standard","amount < $100","1.50%", "$0.15"],
    ["credit_standard","amount >= $100","1.80%","$0.20"],
    ["credit_premium", "amount < $200","2.20%", "$0.25"],
    ["credit_premium", "amount >= $200","2.50%","$0.30"],
    ["corporate",      "any amount",   "2.80%", "$0.35"],
]

t = Table(fee_data, colWidths=[120, 140, 80, 90])
t.setStyle(TableStyle([
    ("BACKGROUND",  (0,0), (-1,0), colors.grey),
    ("TEXTCOLOR",   (0,0), (-1,0), colors.whitesmoke),
    ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
    ("GRID",        (0,0), (-1,-1), 0.5, colors.black),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.lightgrey]),
    ("ALIGN",       (0,0), (-1,-1), "CENTER"),
]))
content.append(t)
content.append(Spacer(1, 12))
content.append(Paragraph(
    "Note: For credit_standard transactions, the tier is determined by the transaction amount. "
    "Transactions of exactly $100.00 use the >= $100 tier. "
    "For credit_premium, transactions of exactly $200.00 use the >= $200 tier.",
    styles["Normal"]
))
doc.build(content)

# --- Generate transactions CSV ---
n = 200
card_types = RNG.choice(["debit","credit_standard","credit_premium","corporate"],
                         n, p=[0.35, 0.30, 0.25, 0.10])
amounts = np.round(RNG.uniform(5, 500, n), 2)
txn_ids = [f"TXN{i:04d}" for i in range(1, n+1)]

def compute_fee(card_type, amount):
    if card_type == "debit":
        return round(amount * 0.005 + 0.10, 4)
    elif card_type == "credit_standard":
        if amount < 100:
            return round(amount * 0.015 + 0.15, 4)
        else:
            return round(amount * 0.018 + 0.20, 4)
    elif card_type == "credit_premium":
        if amount < 200:
            return round(amount * 0.022 + 0.25, 4)
        else:
            return round(amount * 0.025 + 0.30, 4)
    else:  # corporate
        return round(amount * 0.028 + 0.35, 4)

fees = [compute_fee(c, a) for c, a in zip(card_types, amounts)]

df = pd.DataFrame({
    "transaction_id": txn_ids,
    "card_type": card_types,
    "amount": amounts,
    "merchant_id": RNG.integers(1, 21, n),
    "date": pd.date_range("2024-01-01", periods=n, freq="h").strftime("%Y-%m-%d").tolist(),
})
df.to_csv(OUT / "transactions.csv", index=False)

# Save expected totals for verification
total_fees = sum(fees)
by_card = {}
for ct in ["debit","credit_standard","credit_premium","corporate"]:
    mask = df["card_type"] == ct
    by_card[ct] = {
        "total_fees": round(sum(f for f, c in zip(fees, card_types) if c == ct), 4),
        "n_transactions": int(mask.sum()),
    }

print(f"Total fees: {total_fees:.4f}")
for ct, v in by_card.items():
    print(f"  {ct}: fees={v['total_fees']:.4f}, n={v['n_transactions']}")
