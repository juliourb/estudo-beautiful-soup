from __future__ import annotations

import re


def normalize_money(value: str) -> str:
    if not value:
        return ""
    text = value.strip().replace("R$", "").replace(".", "").replace(" ", "")
    text = text.replace(",", ".")
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    return match.group(0) if match else ""


def extract_number(value: str) -> str:
    if not value:
        return ""
    match = re.search(r"\d+", value)
    return match.group(0) if match else ""


def normalize_text(value: str) -> str:
    return " ".join((value or "").split())
