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

Se quiser validar rápido tudo de uma vez:

```bash
make install
make test
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

## Como testar (passo a passo)

### 1) Teste de unidade (sem internet)

```bash
python -m pytest -q
```

### 2) Teste da CLI

```bash
python -m src.main --help
```

### 3) Teste real curto (com coleta)

```bash
python -m src.main \
  --city "São Paulo - SP" \
  --min-rent 1200 \
  --max-rent 4000 \
  --max-pages-per-site 1 \
  --max-records 30 \
  --output-csv output/imoveis_sample.csv \
  --checkpoint output/checkpoint_sample.json
```

Depois valide o CSV gerado:

```bash
python - <<'PY'
import pandas as pd
df = pd.read_csv("output/imoveis_sample.csv")
print(df.head(5))
print(df.columns.tolist())
print(f"Registros: {len(df)}")
PY
```

### 4) Retomada por checkpoint

Rode o mesmo comando do passo 3 novamente. O crawler usará `checkpoint_sample.json` e continuará da última página processada por site.


## Como executar no Google Colab (passo a passo)

A forma mais simples no Colab é clonar o repositório e rodar o script via terminal (`!`).

### Célula 1 — clonar e entrar na pasta

```python
!git clone <URL_DO_SEU_REPOSITORIO>
%cd estudo-beautiful-soup
```

> Se você já subiu os arquivos para o Colab manualmente, só use `%cd` para a pasta correta.

### Célula 2 — instalar dependências

```python
!python -m pip install -U pip
!python -m pip install -e .
```

Opcional (fallback para páginas dinâmicas):

```python
!python -m pip install playwright
!playwright install chromium
```

### Célula 3 — testar se a CLI está ok

```python
!python -m src.main --help
```

### Célula 4 — executar uma coleta curta (teste)

```python
!python -m src.main \
  --city "São Paulo - SP" \
  --min-rent 1200 \
  --max-rent 4000 \
  --max-pages-per-site 1 \
  --max-records 30 \
  --output-csv output/imoveis_sample.csv \
  --checkpoint output/checkpoint_sample.json
```

### Célula 5 — abrir o CSV no próprio Colab

```python
import pandas as pd

df = pd.read_csv("output/imoveis_sample.csv")
print("Linhas:", len(df))
display(df.head(10))
```

### Célula 6 — baixar o CSV para seu computador

```python
from google.colab import files
files.download("output/imoveis_sample.csv")
```

### Retomar do checkpoint no Colab

Para continuar de onde parou, rode **de novo** a célula de execução (Célula 4) com o mesmo `--checkpoint`.

### Dica importante sobre Colab

Se o runtime reiniciar, os arquivos locais podem ser perdidos. Para evitar isso:
- salve o CSV/JSON no Google Drive, ou
- baixe os artefatos ao fim da execução (`files.download`).

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
