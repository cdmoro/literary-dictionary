from collections import defaultdict

from src.utils import normalize_character


def get_author_cr_link(name: str, id: int):
    return get_cross_reference_link(name, id, prefix="A", folder="Authors")


def get_saga_cr_link(name: str, id: int):
    return get_cross_reference_link(name, id, prefix="S", folder="Sagas")


def get_book_cr_link(name: str, id: int):
    return get_cross_reference_link(name, id, prefix="B", folder="Books")


def get_cross_reference_link(name: str, id: int, prefix: str, folder: str):
    if not name:
        return

    first_letter = normalize_character(name.strip()[0])
    filename = f"{prefix}{'_' if prefix else ''}{first_letter}.xhtml"
    anchor = f"{prefix}{'_' if prefix else ''}{id}"
    path = f"{folder}/{filename}" if folder else filename

    return f"../{path}#{anchor}"


def cross_reference_markup(cross_reference, prefix="./"):
    cr_links = []

    for ref in cross_reference:
        cr_links.append(f'<a href="{prefix}{ref["link"]}">{ref["name"]}</a>')

    return ", ".join(cr_links)
