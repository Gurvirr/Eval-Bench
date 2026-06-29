"""
Generates fee_schedule.pdf and transactions.csv for the payment-fee-audit task.

Fee rules (from PDF):
1. Base interchange rate by card type + amount tier (same as before)
2. Monthly volume discount: merchants with total monthly volume > $5000 get 10% off all fees
3. Disputed transactions (is_disputed=1) are charged double the base fee
4. Fee cap: no single transaction fee can exceed $25.00

The model must apply all 4 rules in order:
  base_fee = card_type_tier_rate
  if is_disputed: fee *= 2
  if merchant monthly volume > 5000: fee *= 0.90
  fee = min(fee, 25.00)

Getting any rule wrong produces wrong totals.
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

# Generate PDF
doc = SimpleDocTemplate(str(OUT / "fee_schedule.pdf"), pagesize=letter)
content = []
content.append(Paragraph("Interchange Fee Schedule — Q1 2024", styles["Title"]))
content.append(Spacer(1, 8))
content.append(Paragraph("Section 1: Base Interchange Rates", styles["Heading2"]))

fee_data = [
    ["Card Type", "Amount Threshold", "Rate (%)", "Flat Fee ($)"],
    ["debit",           "any amount",    "0.50%", "$0.10"],
    ["credit_standard", "amount < $100", "1.50%", "$0.15"],
    ["credit_standard", "amount >= $100","1.80%", "$0.20"],
    ["credit_premium",  "amount < $200", "2.20%", "$0.25"],
    ["credit_premium",  "amount >= $200","2.50%", "$0.30"],
    ["corporate",       "any amount",    "2.80%", "$0.35"],
]
t = Table(fee_data, colWidths=[130, 140, 80, 90])
t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),colors.grey),
    ("TEXTCOLOR",(0,0),(-1,0),colors.whitesmoke),
    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
    ("GRID",(0,0),(-1,-1),0.5,colors.black),
]))
content.append(t)
content.append(Spacer(1, 10))

content.append(Paragraph("Section 2: Volume Discount", styles["Heading2"]))
content.append(Paragraph(
    "Merchants whose total transaction volume in a calendar month exceeds $5,000.00 "
    "receive a 10% discount on all interchange fees for that month. "
    "Volume is calculated as the sum of transaction amounts (not fees) for that merchant in that month.",
    styles["Normal"]
))
content.append(Spacer(1, 10))

content.append(Paragraph("Section 3: Dispute Surcharge", styles["Heading2"]))
content.append(Paragraph(
    "Transactions marked as disputed (is_disputed = 1) are charged at 2x the base interchange fee "
    "before any volume discount is applied.",
    styles["Normal"]
))
content.append(Spacer(1, 10))

content.append(Paragraph("Section 4: Fee Cap", styles["Heading2"]))
content.append(Paragraph(
    "No single transaction interchange fee may exceed $25.00 after all adjustments. "
    "If the calculated fee exceeds $25.00, it is capped at $25.00.",
    styles["Normal"]
))
doc.build(content)

# Generate transactions
n = 200
card_types = RNG.choice(["debit","credit_standard","credit_premium","corporate"], n, p=[0.35,0.30,0.25,0.10])
amounts = np.round(RNG.uniform(5, 500, n), 2)
merchant_ids = RNG.integers(1, 11, n)  # 10 merchants
is_disputed = (RNG.random(n) < 0.08).astype(int)  # ~8% disputed
dates = pd.date_range("2024-01-01", periods=n, freq="2h").strftime("%Y-%m-%d").tolist()

df = pd.DataFrame({
    "transaction_id": [f"TXN{i:04d}" for i in range(1,n+1)],
    "card_type": card_types,
    "amount": amounts,
    "merchant_id": merchant_ids,
    "date": dates,
    "is_disputed": is_disputed,
})

# Compute correct fees
def base_fee(ct, a):
    if ct == "debit": return round(a*0.005+0.10, 6)
    elif ct == "credit_standard": return round(a*0.015+0.15,6) if a < 100 else round(a*0.018+0.20,6)
    elif ct == "credit_premium":  return round(a*0.022+0.25,6) if a < 200 else round(a*0.025+0.30,6)
    else: return round(a*0.028+0.35,6)

# Merchant monthly volumes
df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)
monthly_vol = df.groupby(["merchant_id","month"])["amount"].sum().reset_index()
monthly_vol.columns = ["merchant_id","month","monthly_volume"]
df = df.merge(monthly_vol, on=["merchant_id","month"])

def compute_fee(row):
    f = base_fee(row["card_type"], row["amount"])
    if row["is_disputed"]: f *= 2
    if row["monthly_volume"] > 5000: f *= 0.90
    return round(min(f, 25.00), 4)

df["correct_fee"] = df.apply(compute_fee, axis=1)

# Save WITHOUT correct_fee — don't leak the answer
df.drop(columns=["correct_fee"]).to_csv(OUT / "transactions.csv", index=False)

print(f"Total correct fees: {df['correct_fee'].sum():.4f}")
print(f"Disputed txns: {df['is_disputed'].sum()}")
print(f"Merchants with volume > 5000: {(df.groupby(['merchant_id','month'])['amount'].sum() > 5000).sum()}")
print(f"Fees capped at $25: {(df.apply(lambda r: min(base_fee(r['card_type'],r['amount'])*(2 if r['is_disputed'] else 1), 999) > 25, axis=1)).sum()}")
