import unicodedata

def normalize_key(value):
    value = unicodedata.normalize("NFKC", str(value or "")).casefold()
    return "".join(ch for ch in value if ch.isalnum())

def candidate_group_key(row):
    brand, model = normalize_key(row.get("brand")), normalize_key(row.get("model"))
    return f"{brand}:{model}" if brand and model else ""
