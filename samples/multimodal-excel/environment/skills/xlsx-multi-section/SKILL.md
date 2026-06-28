---
name: xlsx-multi-section
description: Parse Excel files with multiple tables on one sheet separated by blank rows. Use skiprows and nrows parameters to read each section independently.
---

# Multi-Section Excel Parsing

## Key Rule
Never use pd.read_excel() on a whole sheet with multiple tables.
Identify each section's start row and use skiprows/nrows to read them separately.

## Pattern

```python
import pandas as pd

# Section 1: starts at row 0 (0-indexed header), 4 data rows
section1 = pd.read_excel("file.xlsx", sheet_name="Report",
                         header=0, nrows=4)

# Section 2: starts after a blank row (row 6 = 0-indexed)
section2 = pd.read_excel("file.xlsx", sheet_name="Report",
                         skiprows=6, header=0, nrows=5)
```

## Using openpyxl to detect section boundaries

```python
from openpyxl import load_workbook
wb = load_workbook("file.xlsx", data_only=True)
ws = wb["Report"]
for i, row in enumerate(ws.iter_rows(values_only=True), start=1):
    if all(v is None for v in row):
        print(f"Blank row at {i}")  # section boundary
```
