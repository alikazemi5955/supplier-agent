import pytest
from src.pricing import apply_markup

def test_five_percent():
    assert str(apply_markup("980000", 5)) == "1029000"

def test_round_half_up():
    assert str(apply_markup("101", 0.5)) == "102"

@pytest.mark.parametrize("price,markup", [("-1", 5), ("100", -1), ("abc", 5)])
def test_reject_invalid(price, markup):
    with pytest.raises(ValueError):
        apply_markup(price, markup)
