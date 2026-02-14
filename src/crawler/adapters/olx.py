from __future__ import annotations

from bs4 import BeautifulSoup

from src.crawler.adapters.base import BaseAdapter
from src.crawler.models import Listing
from src.crawler.normalizers import normalize_money, normalize_text


class OLXAdapter(BaseAdapter):
    site_name = "olx"
    base_url = "https://www.olx.com.br/imoveis/aluguel/estado-sp/sao-paulo-e-regiao/sao-paulo"

    def extract(self, html: str) -> list[Listing]:
        soup = BeautifulSoup(html, "lxml")
        cards = soup.select("section[data-testid='adcard-body'], li[data-testid='adcard-container']")
        results: list[Listing] = []
        for card in cards:
            title = normalize_text((card.select_one("h2") or card).get_text(" ", strip=True))
            link = card.select_one("a[href]")
            price_txt = normalize_text((card.select_one("h3") or card).get_text(" ", strip=True))
            results.append(
                Listing(
                    site=self.site_name,
                    titulo=title,
                    url=self.absolute_url(link.get("href", "") if link else ""),
                    url=link.get("href", "") if link else "",
                    cidade="São Paulo",
                    preco_aluguel=normalize_money(price_txt),
                    preco_total=normalize_money(price_txt),
                )
            )
        if not results:
            return self.extract_json_ld(html)
        return results
