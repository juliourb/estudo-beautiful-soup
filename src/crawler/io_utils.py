from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable


HEADER = [
    "id_unico",
    "site",
    "titulo",
    "url",
    "cidade",
    "bairro",
    "endereco",
    "metragem",
    "dormitorios",
    "banheiros",
    "vagas",
    "preco_total",
    "preco_aluguel",
    "preco_condominio",
    "preco_iptu",
    "data_coleta",
    "lat",
    "lon",
    "geocode_nivel",
    "geocode_confidence",
]


def read_existing_ids(csv_path: Path) -> set[str]:
    if not csv_path.exists():
        return set()
    ids = set()
    with csv_path.open("r", newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            if row.get("id_unico"):
                ids.add(row["id_unico"])
    return ids


def append_rows(csv_path: Path, rows: Iterable[dict]) -> int:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    exists = csv_path.exists()
    count = 0
    with csv_path.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=HEADER)
        if not exists:
            writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in HEADER})
            count += 1
    return count


def load_checkpoint(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_checkpoint(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
