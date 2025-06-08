import os
from collections import defaultdict
from src.pages.dictionary import get_dictionary_page
from src.utils import normalize_character
from src.pages.section import get_section_page, get_section_toc


def get_entries(conn):
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            e.id,
            e.name,
            e.display_name,
            e.alias,
            e.description,
            a.id           AS author_id,
            a.name         AS author,
            s.id           AS saga_id,
            s.name         AS saga,
            b.id           AS book_id,
            b.name         AS book,
            c.abbr         AS category,
            c.id           AS category_id
        FROM entries e
        LEFT JOIN authors a ON e.author_id = a.id
        LEFT JOIN sagas s   ON e.saga_id = s.id
        LEFT JOIN books b   ON e.book_id = b.id
        LEFT JOIN categories c ON e.category_id = c.id
        WHERE e.draft = 0
        ORDER BY e.name COLLATE NOCASE
    """
    )

    entries = []
    for row in cur.fetchall():
        entries.append(dict(row))

    return entries


def get_entries_by_letter(entries):
    entries_by_letter = defaultdict(list)

    for entry in entries:
        name = entry["name"]
        firstLetter = normalize_character(name[0])
        if firstLetter.isalpha():
            entries_by_letter[firstLetter].append(entry)
        else:
            entries_by_letter["Other"].append(entry)

    return entries_by_letter


def build_cross_references(entries):
    cross_reference_data = {}
    for entry in entries:
        if "id" in entry and "name" in entry:
            filename = f"{normalize_character(entry['name'].strip()[0].upper())}.xhtml"
            cross_reference_data[entry["id"]] = (entry["name"], filename)

    # Group entries
    by_saga = defaultdict(list)
    by_book = defaultdict(list)
    by_author = defaultdict(list)

    for entry in entries:
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
            target_name, target_file = cross_reference_data.get(e["id"], (None, None))
            if target_name and target_file:
                related_links.append(
                    {
                        "id": e["id"],
                        "name": target_name,
                        "link": f"D_{target_file}#D_{e['id']}",
                    }
                )

        cross_references[entry_id] = related_links

    return cross_references


def create_dictionary_files(output_folder, lang, strings, conn):
    folder = os.path.join(output_folder, "Dictionary")
    entries = get_entries(conn)
    entries_by_letter = get_entries_by_letter(entries)
    cross_references = build_cross_references(entries)
    files = []

    if len(entries) > 0:
        os.makedirs(folder)

        files.append("Dictionary")
        files.append("Dictionary_TOC")

        # Dictionary
        with open(
            os.path.join(output_folder, "Dictionary", "Dictionary.xhtml"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(get_section_page(lang, strings["dictionary"]))

        with open(
            os.path.join(output_folder, "Dictionary", "Dictionary_TOC.xhtml"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(
                get_section_toc(
                    lang,
                    strings["dictionary"],
                    entries_by_letter,
                    strings,
                    prefix="D",
                )
            )

        for letter, group in sorted(
            entries_by_letter.items(), key=lambda x: (x[0] == "Other", x[0])
        ):
            filename = f"D_{letter}"
            files.append(filename)

            with open(
                os.path.join(folder, f"{filename}.xhtml"), "w", encoding="utf-8"
            ) as f:
                f.write(
                    get_dictionary_page(lang, letter, group, strings, cross_references)
                )

    return files
