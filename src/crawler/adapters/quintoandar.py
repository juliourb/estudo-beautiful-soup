from __future__ import annotations

from bs4 import BeautifulSoup

from src.crawler.adapters.base import BaseAdapter
from src.crawler.models import Listing
from src.crawler.normalizers import extract_number, normalize_money, normalize_text


class QuintoAndarAdapter(BaseAdapter):
    site_name = "quintoandar"
    base_url = "https://www.quintoandar.com.br/alugar/imovel/sao-paulo-sp-brasil"

    def extract(self, html: str) -> list[Listing]:
        soup = BeautifulSoup(html, "lxml")
        cards = soup.select("article, div[data-testid='house-card'], div[data-testid='property-card']")
        out: list[Listing] = []
        for card in cards:
            text = normalize_text(card.get_text(" ", strip=True))
            title = normalize_text((card.select_one("h2, h3") or card).get_text(" ", strip=True))
            link = card.select_one("a[href]")
            aluguel = normalize_money(text)
            out.append(
                Listing(
                    site=self.site_name,
                    titulo=title,
                    url=self.absolute_url(link.get("href", "") if link else ""),
                    url=link.get("href", "") if link else "",
                    cidade="São Paulo",
                    metragem=extract_number(text),
                    preco_aluguel=aluguel,
                    preco_total=aluguel,
                )
            )
        if not out:
            return self.extract_json_ld(html)
        return out
