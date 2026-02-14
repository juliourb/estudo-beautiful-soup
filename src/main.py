from __future__ import annotations

import argparse
import json

from src.crawler.engine import CrawlConfig, CrawlerEngine


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Crawler de aluguel multi-site")
    parser.add_argument("--config", type=str, default="", help="Arquivo JSON opcional de configuração")
    parser.add_argument("--city", type=str, default="São Paulo - SP")
    parser.add_argument("--min-rent", type=str, default="")
    parser.add_argument("--max-rent", type=str, default="")
    parser.add_argument("--min-condo", type=str, default="")
    parser.add_argument("--max-condo", type=str, default="")
    parser.add_argument("--min-iptu", type=str, default="")
    parser.add_argument("--max-iptu", type=str, default="")
    parser.add_argument("--dormitorios", type=str, default="")
    parser.add_argument("--vagas", type=str, default="")
    parser.add_argument("--tipo-imovel", type=str, default="")
    parser.add_argument("--metragem-min", type=str, default="")
    parser.add_argument("--max-pages-per-site", type=int, default=5)
    parser.add_argument("--max-records", type=int, default=10000)
    parser.add_argument("--output-csv", type=str, default="output/imoveis.csv")
    parser.add_argument("--checkpoint", type=str, default="output/checkpoint.json")
    parser.add_argument("--disable-dynamic-fallback", action="store_true")
    return parser.parse_args()


def load_config(args: argparse.Namespace) -> dict:
def load_config(args: argparse.Namespace) -> CrawlConfig:
    base = {}
    if args.config:
        with open(args.config, "r", encoding="utf-8") as fh:
            base = json.load(fh)

    merged = {
        "city": args.city,
        "min_rent": args.min_rent,
        "max_rent": args.max_rent,
        "min_condo": args.min_condo,
        "max_condo": args.max_condo,
        "min_iptu": args.min_iptu,
        "max_iptu": args.max_iptu,
        "dormitorios": args.dormitorios,
        "vagas": args.vagas,
        "tipo_imovel": args.tipo_imovel,
        "metragem_min": args.metragem_min,
        "max_pages_per_site": args.max_pages_per_site,
        "max_records": args.max_records,
        "output_csv": args.output_csv,
        "checkpoint_path": args.checkpoint,
        "use_dynamic_fallback": not args.disable_dynamic_fallback,
    }
    base.update({k: v for k, v in merged.items() if v not in (None, "")})
    return base
    return CrawlConfig(**base)


def main() -> None:
    args = parse_args()
    # Lazy import para permitir `--help` mesmo sem dependências de runtime instaladas.
    from src.crawler.engine import CrawlConfig, CrawlerEngine

    config = CrawlConfig(**load_config(args))
    config = load_config(args)
    result = CrawlerEngine(config).run()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
