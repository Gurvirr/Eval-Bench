"""
Generates weekly_report.xlsx for the multimodal-excel task.

The trap: two tables on one sheet separated by a blank row.
Naive pd.read_excel() reads the whole sheet as one table, mixing headers,
data rows, and the second table's header into a garbled DataFrame.

Correct approach: use skiprows/nrows or openpyxl to read each section separately.

Section 1 (rows 1-5): Regional summary
Section 2 (rows 7-12): Top products (row 6 is blank)
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

# Blank row separator
ws.append([])

# Section 2: Top products
ws.append(["product_id", "product_name", "units_sold", "revenue"])
ws.append(["P001", "Wireless Headphones", 89,  13350.00])
ws.append(["P002", "USB-C Hub",           134,  6700.00])
ws.append(["P003", "Laptop Stand",        201,  9045.00])
ws.append(["P004", "Mechanical Keyboard", 76,  11400.00])
ws.append(["P005", "Webcam HD",           98,   4900.00])

wb.save(OUT / "weekly_report.xlsx")
