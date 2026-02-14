from __future__ import annotations

from dataclasses import dataclass



@dataclass
class GeocodeResult:
    lat: str = ""
    lon: str = ""
    nivel: str = ""
    confidence: str = ""


def confidence_from_nominatim(addresstype: str, importance: float | None) -> tuple[str, str]:
    level = (addresstype or "unknown").lower()
    imp = importance if importance is not None else 0.0
    if level in {"house", "building", "residential"} and imp >= 0.4:
        return level, "high"
    if level in {"road", "neighbourhood", "suburb"} or imp >= 0.2:
        return level, "medium"
    return level, "low"


def geocode_address(address: str, city_hint: str = "São Paulo, SP, Brasil") -> GeocodeResult:
    if not address:
        return GeocodeResult()

    query = f"{address}, {city_hint}"
    try:
        import osmnx as ox
        gdf = ox.geocode_to_gdf(query)
        if gdf.empty:
            return GeocodeResult()
        row = gdf.iloc[0]
        lat = f"{row.geometry.centroid.y:.7f}"
        lon = f"{row.geometry.centroid.x:.7f}"
        addresstype = str(row.get("addresstype", "unknown"))
        importance = row.get("importance", 0.0)
        nivel, confidence = confidence_from_nominatim(addresstype, float(importance or 0.0))
        return GeocodeResult(lat=lat, lon=lon, nivel=nivel, confidence=confidence)
    except Exception:  # noqa: BLE001
        return GeocodeResult()
