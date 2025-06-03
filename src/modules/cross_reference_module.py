from collections import defaultdict

from src.utils import normalize_character

def build_cross_references(entries):
    cross_reference_data = {}
    for entry in entries:
        if "id" in entry and "headword" in entry:
            filename = f'{normalize_character(entry['headword'].strip()[0].upper())}.xhtml'
            cross_reference_data[entry["id"]] = (entry["headword"], filename)

    # Group entries
    by_saga = defaultdict(list)
    by_book = defaultdict(list)
    by_author = defaultdict(list)

    for entry in entries:
        if entry["draft"]:
            continue
        category_id = entry["category_id"]
        if entry["saga_id"]:
            key = (category_id, entry["saga_id"])
            by_saga[key].append(entry)
        elif entry["book_id"]:
            key = (category_id, entry["book_id"])
            by_book[key].append(entry)
        elif entry["author_id"]:
            key = (category_id, entry["author_id"])
            by_author[key].append(entry)

    cross_references = {}

    for entry in entries:
        if entry["draft"]:
            continue

        entry_id = entry["id"]
        category_id = entry["category_id"]
        related = []

        if entry["saga_id"]:
            key = (category_id, entry["saga_id"])
            related = by_saga.get(key, [])
        elif entry["book_id"]:
            key = (category_id, entry["book_id"])
            related = by_book.get(key, [])
        elif entry["author_id"]:
            key = (category_id, entry["author_id"])
            related = by_author.get(key, [])

        # Avoid self-reference
        related_filtered = [e for e in related if e["id"] != entry_id]

        # Build links
        related_links = []
        for e in related_filtered:
            target_headword, target_file = cross_reference_data.get(e["id"], (None, None))
            if target_headword and target_file:
                related_links.append({
                    "id": e["id"],
                    "headword": target_headword,
                    "link": f"{target_file}#D-{e['id']}"
                })

        cross_references[entry_id] = related_links

    return cross_references
