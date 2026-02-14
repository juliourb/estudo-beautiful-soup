from src.crawler.normalizers import extract_number, normalize_money


def test_normalize_money():
    assert normalize_money("R$ 3.450,90") == "3450.90"


def test_extract_number():
    assert extract_number("82 m²") == "82"
