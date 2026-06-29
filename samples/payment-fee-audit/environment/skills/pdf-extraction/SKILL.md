---
name: pdf-extraction
description: Extract structured data from PDF documents using pdfplumber. Use for fee schedules, invoices, and tabular data embedded in PDFs.
---

# PDF Data Extraction

## Pattern

```python
import pdfplumber

with pdfplumber.open("/root/data/fee_schedule.pdf") as pdf:
    for page in pdf.pages:
        # Extract tables
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                print(row)
        # Extract raw text
        text = page.extract_text()
        print(text)
```

## Tips
- `extract_tables()` returns lists of rows, each row is a list of cell strings
- Header rows typically have bold text or distinct formatting
- Always validate extracted values against document totals
- Strip whitespace and currency symbols before parsing numbers
