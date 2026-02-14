from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.crawler.adapters.imovelweb import ImovelWebAdapter
from src.crawler.adapters.olx import OLXAdapter
from src.crawler.adapters.quintoandar import QuintoAndarAdapter
from src.crawler.adapters.vivareal import VivaRealAdapter
from src.crawler.adapters.zap import ZapAdapter
from src.crawler.dynamic_fetch import fetch_dynamic_html
from src.crawler.geocoder import geocode_address
from src.crawler.http_client import SafeSession
from src.crawler.io_utils import append_rows, load_checkpoint, read_existing_ids, save_checkpoint
from src.crawler.models import Listing


@dataclass
class CrawlConfig:
    city: str = "São Paulo - SP"
    min_rent: str = ""
    max_rent: str = ""
    min_condo: str = ""
    max_condo: str = ""
    min_iptu: str = ""
    max_iptu: str = ""
    dormitorios: str = ""
    vagas: str = ""
    tipo_imovel: str = ""
    metragem_min: str = ""
    max_pages_per_site: int = 5
    max_records: int = 10000
    output_csv: str = "output/imoveis.csv"
    checkpoint_path: str = "output/checkpoint.json"
    use_dynamic_fallback: bool = True


class CrawlerEngine:
    def __init__(self, config: CrawlConfig):
        self.config = config
        self.session = SafeSession(rate_limit_s=1.0, jitter_s=0.35, block_threshold=4)
        self.adapters = [
            OLXAdapter(),
            ZapAdapter(),
            VivaRealAdapter(),
            ImovelWebAdapter(),
            QuintoAndarAdapter(),
        ]

    def run(self) -> dict:
        csv_path = Path(self.config.output_csv)
        checkpoint_path = Path(self.config.checkpoint_path)
        existing_ids = read_existing_ids(csv_path)
        checkpoint = load_checkpoint(checkpoint_path)
        total_added = 0

        for adapter in self.adapters:
            if self.session.is_blocked(adapter.site_name):
                continue
            site_ck = checkpoint.get(adapter.site_name, {})
            start_page = int(site_ck.get("last_page", 0)) + 1

            for page in range(start_page, self.config.max_pages_per_site + 1):
                if total_added >= self.config.max_records:
                    break

                url = adapter.build_search_url(
                    city=self.config.city,
                    min_rent=self.config.min_rent,
                    max_rent=self.config.max_rent,
                    page=page,
                )

                try:
                    html = self.session.get(adapter.site_name, url)
                    listings = adapter.extract(html)

                    if not listings and self.config.use_dynamic_fallback:
                        html = fetch_dynamic_html(url)
                        listings = adapter.extract(html)
                except Exception:
                    checkpoint[adapter.site_name] = {"last_page": page, "error": True}
                    save_checkpoint(checkpoint_path, checkpoint)
                    continue

                enriched_rows = []
                for listing in listings:
                    if not listing.url:
                        continue
                    if listing.id_unico in existing_ids:
                        continue

                    if listing.endereco:
                        geo = geocode_address(listing.endereco)
                        listing.lat = geo.lat
                        listing.lon = geo.lon
                        listing.geocode_nivel = geo.nivel
                        listing.geocode_confidence = geo.confidence

                    row = listing.to_dict()
                    existing_ids.add(row["id_unico"])
                    enriched_rows.append(row)

                    if len(enriched_rows) + total_added >= self.config.max_records:
                        break

                added = append_rows(csv_path, enriched_rows)
                total_added += added

                checkpoint[adapter.site_name] = {
                    "last_page": page,
                    "error": False,
                    "records_added": total_added,
                }
                save_checkpoint(checkpoint_path, checkpoint)

                if added == 0:
                    break

        return {"records_added": total_added, "output_csv": self.config.output_csv}
