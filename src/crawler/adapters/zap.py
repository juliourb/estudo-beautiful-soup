from __future__ import annotations

from bs4 import BeautifulSoup

from src.crawler.adapters.base import BaseAdapter
from src.crawler.models import Listing
from src.crawler.normalizers import extract_number, normalize_money, normalize_text


class ZapAdapter(BaseAdapter):
    site_name = "zap_imoveis"
    base_url = "https://www.zapimoveis.com.br/aluguel/imoveis/sp+sao-paulo/"

    def extract(self, html: str) -> list[Listing]:
        soup = BeautifulSoup(html, "lxml")
        cards = soup.select("div[data-position], article, div.listing-card")
        out: list[Listing] = []
        for card in cards:
            title = normalize_text((card.select_one("h2, h3") or card).get_text(" ", strip=True))
            link = card.select_one("a[href]")
            all_text = normalize_text(card.get_text(" ", strip=True))
            aluguel = normalize_money(all_text)
            out.append(
                Listing(
                    site=self.site_name,
                    titulo=title,
                    url=self.absolute_url(link.get("href", "") if link else ""),
                    cidade="São Paulo",
                    metragem=extract_number(all_text),
                    preco_aluguel=aluguel,
                    preco_total=aluguel,
                )
            )
        if not out:
            return self.extract_json_ld(html)
        return out
