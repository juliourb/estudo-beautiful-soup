from __future__ import annotations

from bs4 import BeautifulSoup

from src.crawler.adapters.base import BaseAdapter
from src.crawler.models import Listing
from src.crawler.normalizers import extract_number, normalize_money, normalize_text


class VivaRealAdapter(BaseAdapter):
    site_name = "vivareal"
    base_url = "https://www.vivareal.com.br/aluguel/sp/sao-paulo/"

    def extract(self, html: str) -> list[Listing]:
        soup = BeautifulSoup(html, "lxml")
        cards = soup.select("article, div.property-card, div[data-cy='rp-property-cd']")
        listings: list[Listing] = []
        for card in cards:
            title = normalize_text((card.select_one("h2, h3") or card).get_text(" ", strip=True))
            href = (card.select_one("a[href]") or {}).get("href", "") if card.select_one("a[href]") else ""
            text = normalize_text(card.get_text(" ", strip=True))
            aluguel = normalize_money(text)
            listings.append(
                Listing(
                    site=self.site_name,
                    titulo=title,
                    url=self.absolute_url(href),
                    url=href,
                    cidade="São Paulo",
                    metragem=extract_number(text),
                    preco_aluguel=aluguel,
                    preco_total=aluguel,
                )
            )
        if not listings:
            return self.extract_json_ld(html)
        return listings
