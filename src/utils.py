import json
import unicodedata
from src.constants import encoding


def get_translations(lang):
    with open(f"locales/{lang}.json", "r", encoding=encoding) as f:
        return json.load(f)


def normalize_character(letra):
    return (
        unicodedata.normalize("NFD", letra)
        .encode("ascii", "ignore")
        .decode("utf-8")
        .upper()
    )
