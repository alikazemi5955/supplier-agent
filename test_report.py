import csv
from src.normalize import read_csv
from src.report import write_priced_report

def test_sample_loads():
    assert len(read_csv("data/sample_products.csv")) >= 3

def test_zero_stock_blocked(tmp_path):
    rows = read_csv("data/sample_products.csv")
    out = tmp_path / "report.csv"
    write_priced_report(rows, out, 5)
    with out.open(encoding="utf-8-sig", newline="") as f:
        result = list(csv.DictReader(f))
    assert any(r["review_status"] == "blocked_out_of_stock" for r in result)
    assert all(r["sale_price"] for r in result)
