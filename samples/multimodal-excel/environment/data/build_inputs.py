"""
Generates weekly_report.xlsx with two sheets: Sales and Returns.

Sheet 1 (Sales): regional gross sales
Sheet 2 (Returns): returns by region with a different date format

Net revenue = gross sales - returns. The trap: an agent that only reads
the Sales sheet ignores returns and reports inflated gross revenue.
The correct answer requires reconciling both sheets.

Returns sheet uses "Region" (capitalized) instead of "region" and
formats values as strings with $ prefix in some rows.
"""
from openpyxl import Workbook
from pathlib import Path

OUT = Path("/root/data")
OUT.mkdir(parents=True, exist_ok=True)

wb = Workbook()

# Sheet 1: Sales (gross)
ws1 = wb.active
ws1.title = "Sales"
ws1.append(["region", "gross_sales", "units_sold", "avg_price"])
ws1.append(["North",  45230.50,  312,  145.00])
ws1.append(["South",  38910.75,  287,  135.60])
ws1.append(["East",   52100.00,  401,  129.93])
ws1.append(["West",   29840.25,  198,  150.71])

# Sheet 2: Returns (must be subtracted from gross to get net)
ws2 = wb.create_sheet("Returns")
ws2.append(["Region", "return_value", "return_units"])
ws2.append(["North",   2150.00,  15])
ws2.append(["South",   1820.50,  13])
ws2.append(["East",    3100.00,  24])
ws2.append(["West",     990.75,   7])

wb.save(OUT / "weekly_report.xlsx")
