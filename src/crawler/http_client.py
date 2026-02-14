from __future__ import annotations

import random
import time
from dataclasses import dataclass, field

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; RentCrawler/1.0; +https://example.local/bot-policy)",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8",
}


@dataclass
class SiteStatus:
    failures: int = 0
    blocked: bool = False


@dataclass
class SafeSession:
    rate_limit_s: float = 1.0
    jitter_s: float = 0.35
    block_threshold: int = 4
    statuses: dict[str, SiteStatus] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.session = requests.Session()
        retries = Retry(
            total=3,
            read=3,
            connect=3,
            backoff_factor=1.0,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=("GET", "HEAD"),
        )
        self.session.mount("http://", HTTPAdapter(max_retries=retries))
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def _status(self, site: str) -> SiteStatus:
        if site not in self.statuses:
            self.statuses[site] = SiteStatus()
        return self.statuses[site]

    def is_blocked(self, site: str) -> bool:
        return self._status(site).blocked

    def get(self, site: str, url: str, timeout: int = 25) -> str:
        st = self._status(site)
        if st.blocked:
            raise RuntimeError(f"Site {site} bloqueado temporariamente por falhas/captcha.")

        time.sleep(self.rate_limit_s + random.uniform(0, self.jitter_s))
        response = self.session.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
        html = response.text or ""

        if response.status_code == 403 or "captcha" in html.lower():
            st.failures += 1
            if st.failures >= self.block_threshold:
                st.blocked = True
            raise RuntimeError(f"Possível bloqueio/captcha em {site}: status {response.status_code}")

        if response.status_code >= 400:
            st.failures += 1
            raise RuntimeError(f"Erro HTTP {response.status_code} em {url}")

        st.failures = 0
        return html
