from __future__ import annotations

from abc import ABC, abstractmethod
from urllib.parse import quote_plus

from bs4 import BeautifulSoup

from src.crawler.models import Listing
from src.crawler.normalizers import extract_number, normalize_money, normalize_text


class BaseAdapter(ABC):
    site_name: str = ""
    base_url: str = ""

    def build_search_url(self, city: str, min_rent: str, max_rent: str, page: int) -> str:
        city_slug = quote_plus(city)
        return f"{self.base_url}?q={city_slug}&minPrice={min_rent}&maxPrice={max_rent}&page={page}"

    @abstractmethod
    def extract(self, html: str) -> list[Listing]:
        raise NotImplementedError

    def _extract_common(self, card) -> Listing:
        title = normalize_text(card.get_text(" ", strip=True)[:160])
        link_tag = card.select_one("a[href]")
        href = link_tag.get("href", "") if link_tag else ""
        price = normalize_money(card.get_text(" ", strip=True))
        listing = Listing(site=self.site_name, titulo=title, url=href, preco_aluguel=price, preco_total=price)

        meta = card.get_text(" ", strip=True)
        listing.metragem = extract_number(meta)
        return listing


class SoupExtractorMixin:
    def soup(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, "lxml")
