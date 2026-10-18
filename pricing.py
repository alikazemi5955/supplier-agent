from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

def apply_markup(price, markup_percent):
    try:
        base = Decimal(str(price).replace(",", "").strip())
        markup = Decimal(str(markup_percent))
    except (InvalidOperation, AttributeError) as exc:
        raise ValueError("قیمت یا درصد افزایش معتبر نیست.") from exc
    if not base.is_finite() or not markup.is_finite() or base < 0 or markup < 0:
        raise ValueError("قیمت و درصد افزایش باید اعداد متناهی و غیرمنفی باشند.")
    return (base * (Decimal("1") + markup / Decimal("100"))).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
