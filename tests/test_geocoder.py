from src.crawler.geocoder import confidence_from_nominatim


def test_confidence_high():
    level, confidence = confidence_from_nominatim("house", 0.9)
    assert level == "house"
    assert confidence == "high"


def test_confidence_medium():
    level, confidence = confidence_from_nominatim("road", 0.1)
    assert confidence == "medium"
