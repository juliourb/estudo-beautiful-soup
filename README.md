# Crawler de Aluguel Multi-Site

Crawler em Python para coletar anúncios de aluguel em **OLX, Zap Imóveis, Viva Real, ImovelWeb e QuintoAndar** com:

- filtros por cidade e faixa de valores;
- CSV único incremental;
- deduplicação por ID único;
- checkpoint para retomada;
- limitação de taxa e bloqueio automático por 403/captcha;
- fallback para páginas dinâmicas (Playwright, opcional);
- etapa final de geocodificação via **OSMnx/Nominatim** com nível de confiança.

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
# opcional para fallback dinâmico
pip install playwright
playwright install chromium
```

## Execução (CLI)

```bash
python -m src.main \
  --city "São Paulo - SP" \
  --min-rent 1200 \
  --max-rent 6000 \
  --max-pages-per-site 10 \
  --max-records 10000
```

## Execução por JSON (opcional)

Crie `config.json`:

```json
{
  "city": "São Paulo - SP",
  "min_rent": "1200",
  "max_rent": "6000",
  "max_pages_per_site": 10,
  "max_records": 10000,
  "output_csv": "output/imoveis.csv",
  "checkpoint_path": "output/checkpoint.json"
}
```

Execute:

```bash
python -m src.main --config config.json
```

## Saída CSV

Campos:

- `id_unico`, `site`, `titulo`, `url`, `cidade`, `bairro`, `endereco`
- `metragem`, `dormitorios`, `banheiros`, `vagas`
- `preco_total`, `preco_aluguel`, `preco_condominio`, `preco_iptu`
- `data_coleta`
- `lat`, `lon`, `geocode_nivel`, `geocode_confidence`

## Observações de uso responsável

- Use limites moderados de páginas e requisições.
- Respeite termos de uso dos sites e legislação aplicável.
- Alguns sites podem alterar estrutura HTML frequentemente; ajustes de seletores podem ser necessários.
