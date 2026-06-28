"""
Generates weekly_report.xlsx with THREE sections separated by blank rows.

Section 1: Regional summary (rows 1-5)
Section 2: Top products (rows 7-12)
Section 3: Weekly targets/notes (rows 14-17) — distractor section

The trap: naive pd.read_excel() merges all three sections.
A model must identify which section contains which data.
The third section is a distractor with numeric columns that can be confused
with the regional or product data.
"""
from openpyxl import Workbook
from pathlib import Path

OUT = Path("/root/data")
OUT.mkdir(parents=True, exist_ok=True)

wb = Workbook()
ws = wb.active
ws.title = "Report"

# Section 1: Regional summary
ws.append(["region", "total_sales", "total_units", "avg_price"])
ws.append(["North",  45230.50,  312,  145.00])
ws.append(["South",  38910.75,  287,  135.60])
ws.append(["East",   52100.00,  401,  129.93])
ws.append(["West",   29840.25,  198,  150.71])

ws.append([])  # blank row

# Section 2: Top products
ws.append(["product_id", "product_name", "units_sold", "revenue"])
ws.append(["P001", "Wireless Headphones", 89,  13350.00])
ws.append(["P002", "USB-C Hub",           134,  6700.00])
ws.append(["P003", "Laptop Stand",        201,  9045.00])
ws.append(["P004", "Mechanical Keyboard", 76,  11400.00])
ws.append(["P005", "Webcam HD",           98,   4900.00])

ws.append([])  # blank row

# Section 3: Weekly targets (distractor — different schema, should NOT be used)
ws.append(["region", "sales_target", "attainment_pct"])
ws.append(["North",  50000.00,  90.5])
ws.append(["South",  42000.00,  92.6])
ws.append(["East",   55000.00,  94.7])
ws.append(["West",   32000.00,  93.3])

wb.save(OUT / "weekly_report.xlsx")
