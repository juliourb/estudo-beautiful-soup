from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib


@dataclass
class Listing:
    site: str
    titulo: str = ""
    url: str = ""
    cidade: str = ""
    bairro: str = ""
    endereco: str = ""
    metragem: str = ""
    dormitorios: str = ""
    banheiros: str = ""
    vagas: str = ""
    preco_total: str = ""
    preco_aluguel: str = ""
    preco_condominio: str = ""
    preco_iptu: str = ""
    data_coleta: str = ""
    lat: str = ""
    lon: str = ""
    geocode_nivel: str = ""
    geocode_confidence: str = ""

    @property
    def id_unico(self) -> str:
        base = f"{self.site}|{self.url}|{self.endereco}|{self.preco_aluguel}"
        return hashlib.sha256(base.encode("utf-8")).hexdigest()[:20]

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["id_unico"] = self.id_unico
        if not payload["data_coleta"]:
            payload["data_coleta"] = datetime.now(timezone.utc).isoformat()
        return payload
