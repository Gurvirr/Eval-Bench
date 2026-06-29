"""
Verifier for multimodal-excel task (Excel output with strict format).

Agent must produce /root/output_report.xlsx with:
- Sheet "Regional Summary": exact headers, alphabetical order, correct net values
- Sheet "Product Detail": exact headers, sorted by product_id, correct values

Traps:
- Wrong sheet names (case-sensitive)
- Wrong column names
- Ignoring Returns or corrections.csv
- Wrong sort order
- Storing values as text instead of numbers
"""
from openpyxl import load_workbook
from pathlib import Path

OUTPUT_FILE = Path("/root/output_report.xlsx")
TOL = 0.05


def header_map(ws, row=1):
    return {str(cell.value).strip(): idx for idx, cell in enumerate(ws[row], 1) if cell.value}


class TestMultimodalExcel:
    def test_output_file_exists(self):
        assert OUTPUT_FILE.exists(), f"Missing: {OUTPUT_FILE}"

    def test_required_sheets(self):
        wb = load_workbook(OUTPUT_FILE, data_only=True)
        assert "Regional Summary" in wb.sheetnames, \
            f"Missing sheet 'Regional Summary'. Found: {wb.sheetnames}"
        assert "Product Detail" in wb.sheetnames, \
            f"Missing sheet 'Product Detail'. Found: {wb.sheetnames}"

    def test_regional_summary_headers(self):
        wb = load_workbook(OUTPUT_FILE, data_only=True)
        ws = wb["Regional Summary"]
        cols = header_map(ws)
        for h in ["region","gross_revenue","total_returns","total_adjustments","net_revenue","net_units"]:
            assert h in cols, f"Missing column '{h}' in Regional Summary"

    def test_regional_net_revenue(self):
        """Net revenue per region must reflect gross - returns + corrections."""
        wb = load_workbook(OUTPUT_FILE, data_only=True)
        ws = wb["Regional Summary"]
        cols = header_map(ws)
        data = {}
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[cols["region"]-1]:
                data[str(row[cols["region"]-1])] = float(row[cols["net_revenue"]-1])

        expected = {"East": 11800.00, "North": 17350.00, "South": 11405.00, "West": 12380.00}
        for region, exp in expected.items():
            assert region in data, f"Missing region '{region}'"
            assert abs(data[region] - exp) < TOL, \
                f"{region} net_revenue={data[region]:.2f}, expected {exp:.2f}"

    def test_regional_sorted_alphabetically(self):
        wb = load_workbook(OUTPUT_FILE, data_only=True)
        ws = wb["Regional Summary"]
        cols = header_map(ws)
        regions = [str(row[cols["region"]-1]) for row in ws.iter_rows(min_row=2, values_only=True)
                   if row[cols["region"]-1]]
        assert regions == sorted(regions), \
            f"Regions not sorted alphabetically: {regions}"

    def test_product_detail_headers(self):
        wb = load_workbook(OUTPUT_FILE, data_only=True)
        ws = wb["Product Detail"]
        cols = header_map(ws)
        for h in ["product_id","product_name","region","gross_revenue","return_value","adjustment","net_revenue"]:
            assert h in cols, f"Missing column '{h}' in Product Detail"

    def test_product_detail_row_count(self):
        """Must have 8 product rows (one per product)."""
        wb = load_workbook(OUTPUT_FILE, data_only=True)
        ws = wb["Product Detail"]
        rows = [r for r in ws.iter_rows(min_row=2, values_only=True) if r[0]]
        assert len(rows) == 8, f"Expected 8 product rows, got {len(rows)}"
