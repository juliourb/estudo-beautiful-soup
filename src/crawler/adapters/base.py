from __future__ import annotations

from abc import ABC, abstractmethod
import json
from urllib.parse import quote_plus, urljoin

from bs4 import BeautifulSoup

from src.crawler.models import Listing
from src.crawler.normalizers import normalize_money, normalize_text


class BaseAdapter(ABC):
    site_name: str = ""
    base_url: str = ""

    def build_search_url(self, city: str, min_rent: str, max_rent: str, page: int) -> str:
        # Fallback genérico menos invasivo: evita query params inválidas por site.
        if page <= 1:
            return self.base_url
        return f"{self.base_url}?pagina={page}"

    def absolute_url(self, href: str) -> str:
        if not href:
            return ""
        return urljoin(self.base_url, href)

    @abstractmethod
    def extract(self, html: str) -> list[Listing]:
        raise NotImplementedError

    def extract_json_ld(self, html: str) -> list[Listing]:
        soup = BeautifulSoup(html, "lxml")
        listings: list[Listing] = []
        for script in soup.select("script[type='application/ld+json']"):
            raw = script.get_text(strip=True)
            if not raw:
                continue
            try:
                payload = json.loads(raw)
            except Exception:
                continue

            nodes = payload if isinstance(payload, list) else [payload]
            for node in nodes:
                if not isinstance(node, dict):
                    continue
                if node.get("@type") not in {"Offer", "Product", "Residence", "Apartment"}:
                    continue

                url = self.absolute_url(str(node.get("url", "")))
                title = normalize_text(str(node.get("name", "")))
                price = normalize_money(str(node.get("price", "")))
                if not url and not title:
                    continue
                listings.append(
                    Listing(
                        site=self.site_name,
                        titulo=title,
                        url=url,
                        preco_aluguel=price,
                        preco_total=price,
                    )
                )
        return listings


class SoupExtractorMixin:
    def soup(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, "lxml")
