import csv

REQUIRED_COLUMNS = {"supplier", "title", "price", "currency"}

def read_csv(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError("ستون‌های ضروری وجود ندارند: " + ", ".join(sorted(missing)))
        rows = []
        for line_no, row in enumerate(reader, start=2):
            try:
                raw_price = str(row.get("price", "")).replace(",", "").strip()
                price = float(raw_price)
                if price < 0:
                    raise ValueError("negative price")
            except Exception as exc:
                raise ValueError(f"قیمت نامعتبر در خط {line_no}") from exc
            for key in ("supplier", "title", "currency"):
                row[key] = (row.get(key) or "").strip()
                if not row[key]:
                    raise ValueError(f"ستون {key} در خط {line_no} خالی است.")
            row["price"] = price
            row["currency"] = row["currency"].upper()
            for key in ("supplier_sku", "brand", "model", "color", "product_url"):
                row[key] = (row.get(key) or "").strip()
            stock = (row.get("stock") or "").strip()
            if stock:
                try:
                    row["stock"] = int(float(stock))
                    if row["stock"] < 0: raise ValueError()
                except Exception as exc:
                    raise ValueError(f"موجودی نامعتبر در خط {line_no}") from exc
            else:
                row["stock"] = None
            rows.append(row)
        return rows
