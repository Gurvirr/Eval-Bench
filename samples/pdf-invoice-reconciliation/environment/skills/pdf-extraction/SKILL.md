---
name: pdf-extraction
description: Extract structured data from PDF documents using pdfplumber. Use for invoices, fee schedules, and tabular data in PDFs.
---

# PDF Data Extraction

```python
import pdfplumber

with pdfplumber.open("/root/data/invoice.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                print(row)  # list of cell strings
        text = page.extract_text()
```

## Tips
- Strip `$`, `,`, whitespace before converting to float
- TOTAL row is usually the last row with a dollar amount
- `extract_tables()` is more reliable than `extract_text()` for tabular data
