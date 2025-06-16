import json
import unicodedata
from src.constants import encoding
from bs4 import BeautifulSoup
import html


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


def escape_text_nodes(s):
    soup = BeautifulSoup(s, "html.parser")

    for text_node in soup.find_all(text=True):
        text_node.replace_with(html.escape(text_node, quote=False))

    return str(soup)
