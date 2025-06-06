import json
import unicodedata
from pathlib import Path


def get_translations(lang):
    with open(f"locales/{lang}.json", "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_character(letra):
    return (
        unicodedata.normalize("NFD", letra)
        .encode("ascii", "ignore")
        .decode("utf-8")
        .upper()
    )
