import argparse, os
from src.normalize import read_csv
from src.report import write_priced_report

def main():
    parser = argparse.ArgumentParser(description="Supplier agent — report-only safe mode")
    parser.add_argument("--input", default="data/sample_products.csv")
    parser.add_argument("--output", default="output/priced_products.csv")
    parser.add_argument("--markup", type=float, default=float(os.getenv("MARKUP_PERCENT", "5")))
    args = parser.parse_args()
    if args.markup < 0: parser.error("درصد افزایش باید صفر یا بیشتر باشد.")
    rows = read_csv(args.input)
    write_priced_report(rows, args.output, args.markup)
    print(f"Processed rows: {len(rows)}")
    print(f"Markup: {args.markup}%")
    print(f"Report: {args.output}")
    print("SAFE MODE: no store products were changed.")
if __name__ == "__main__":
    main()
