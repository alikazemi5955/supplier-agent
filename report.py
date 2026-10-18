import csv
from pathlib import Path
from collections import defaultdict
from .pricing import apply_markup
from .matching import candidate_group_key

def write_priced_report(rows, output_path, markup_percent):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    groups = defaultdict(list)
    for i, row in enumerate(rows):
        key = candidate_group_key(row)
        if key: groups[key].append(i)
    fields = list(rows[0].keys()) if rows else []
    for key in ("sale_price", "review_status", "review_note", "match_candidate_group"):
        if key not in fields: fields.append(key)
    with output_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            out = dict(row)
            out["sale_price"] = str(apply_markup(row["price"], markup_percent))
            key = candidate_group_key(row)
            out["match_candidate_group"] = key
            if row.get("stock") == 0:
                out["review_status"] = "blocked_out_of_stock"
                out["review_note"] = "موجودی صفر است؛ پیش از انتشار بررسی شود."
            elif key and len(groups[key]) > 1:
                out["review_status"] = "needs_match_review"
                out["review_note"] = "برند/مدل مشابه در چند ردیف دیده شد؛ ادغام خودکار انجام نشده است."
            elif row.get("stock") is None:
                out["review_status"] = "needs_stock_review"
                out["review_note"] = "موجودی مشخص نیست؛ قبل از انتشار بررسی شود."
            else:
                out["review_status"] = "ready_for_manual_review"
                out["review_note"] = "قیمت محاسبه شد؛ انتشار خودکار غیرفعال است."
            writer.writerow(out)
