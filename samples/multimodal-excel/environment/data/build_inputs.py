"""
Generates weekly_report.xlsx (3 sheets) + corrections.csv.

Sheet 1 (Sales): gross sales by region and product
Sheet 2 (Targets): sales targets (distractor)
Sheet 3 (Returns): returns by product_id

corrections.csv: post-submission corrections to 3 specific orders
(must be applied before computing final net revenue)

The trap: agent reads only Sales sheet, ignores Returns and corrections.
Correct: Sales - Returns - Corrections = net revenue.

Net revenue by region requires joining products to regions via product_id.
"""
from openpyxl import Workbook
import pandas as pd
from pathlib import Path

OUT = Path("/root/data")
OUT.mkdir(parents=True, exist_ok=True)

wb = Workbook()

# Sheet 1: Sales (gross, by product+region)
ws1 = wb.active
ws1.title = "Sales"
ws1.append(["product_id","product_name","region","units_sold","gross_revenue"])
sales_rows = [
    ("P001","Wireless Headphones","North",  89, 13350.00),
    ("P002","USB-C Hub",          "East",  134,  6700.00),
    ("P003","Laptop Stand",       "South", 201,  9045.00),
    ("P004","Mechanical Keyboard","West",   76, 11400.00),
    ("P005","Webcam HD",          "North",  98,  4900.00),
    ("P006","Monitor Arm",        "East",   55,  5500.00),
    ("P007","Desk Lamp",          "South",  88,  2640.00),
    ("P008","Cable Organizer",    "West",  143,  1430.00),
]
for row in sales_rows:
    ws1.append(list(row))

# Sheet 2: Targets (distractor — do NOT use for revenue calculation)
ws2 = wb.create_sheet("Targets")
ws2.append(["region","revenue_target","units_target"])
ws2.append(["North", 20000, 200])
ws2.append(["South", 15000, 350])
ws2.append(["East",  18000, 220])
ws2.append(["West",  15000, 250])

# Sheet 3: Returns (by product_id)
ws3 = wb.create_sheet("Returns")
ws3.append(["product_id","return_units","return_value"])
ws3.append(["P001", 5,  750.00])
ws3.append(["P003", 8,  360.00])
ws3.append(["P005", 3,  150.00])
ws3.append(["P006", 2,  200.00])

wb.save(OUT / "weekly_report.xlsx")

# corrections.csv: 3 post-submission order corrections (revenue adjustments)
corrections = pd.DataFrame([
    {"product_id":"P002","adjustment": -200.00, "reason":"pricing_error"},
    {"product_id":"P004","adjustment": -450.00, "reason":"bulk_discount_applied"},
    {"product_id":"P007","adjustment":  +80.00, "reason":"reprocessed_order"},
])
corrections.to_csv(OUT / "corrections.csv", index=False)
