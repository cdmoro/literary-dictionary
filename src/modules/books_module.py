import os
from collections import defaultdict

from src.utils import normalize_character
from src.pages.section import get_section_page, get_section_toc
from src.pages.books import get_books_page


def get_books(conn):
    cur = conn.cursor()

    cur.execute(
        """
        SELECT 
            b.id, 
            b.name, 
            b.description, 
            b.publication_year,
            c.abbr, 
            a.name AS author, 
            a.id AS author_id,
            s.name AS saga,
            s.id AS saga_id
        FROM books b
        JOIN authors a ON b.author_id = a.id
        CROSS JOIN categories c
        LEFT JOIN sagas s ON b.saga_id = s.id
        WHERE c.id = 14
        ORDER BY b.name;
    """
    )

    books = []
    for row in cur.fetchall():
        books.append(dict(row))

    return books


def get_books_by_letter(conn):
    books = get_books(conn)
    books_by_letter = defaultdict(list)

    for book in books:
        title = book["name"]
        firstLetter = normalize_character(title[0])

        if firstLetter.isalpha():
            books_by_letter[firstLetter].append(book)
        else:
            books_by_letter["Other"].append(book)

    return books_by_letter


def build_book_cross_references(conn):
    books = get_books(conn)
    book_reference_data = {}

    for book in books:
        if "id" in book and "title" in book:
            filename = f"{normalize_character(book['name'].strip()[0].upper())}.xhtml"
            book_reference_data[book["id"]] = (book["name"], filename)

    by_saga = defaultdict(list)
    by_author = defaultdict(list)

    for book in books:
        if book["saga_id"]:
            by_saga[book["saga_id"]].append(book)
        else:
            by_author[book["author_id"]].append(book)

    cross_references = {}

    for book in books:
        book_id = book["id"]
        related = []

        if book["saga_id"]:
            same_saga = sorted(
                by_saga.get(book["saga_id"], []),
                key=lambda b: b["publication_year"] or 0,
            )
            related = [b for b in same_saga if b["id"] != book_id]

        if not related:
            same_author = sorted(
                by_author.get(book["author_id"], []),
                key=lambda b: b["publication_year"] or 0,
            )
            related = [b for b in same_author if b["id"] != book_id]

        related_links = []
        for b in related:
            title, filename = book_reference_data.get(b["id"], (None, None))
            if title and filename:
                related_links.append(
                    {"id": b["id"], "name": title, "link": f"B_{filename}#B_{b['id']}"}
                )

        cross_references[book_id] = related_links

    return cross_references


def create_books_files(output_folder, lang, strings, conn):
    folder = os.path.join(output_folder, "Books")
    books_by_letter = get_books_by_letter(conn)
    cross_references = build_book_cross_references(conn)
    files = []

    if len(books_by_letter) > 0:
        os.makedirs(folder)

        files.append("Books")
        files.append("Books_TOC")

        with open(
            os.path.join(output_folder, "Books", "Books.xhtml"), "w", encoding="utf-8"
        ) as f:
            f.write(get_section_page(lang, strings["books"]))

        with open(
            os.path.join(output_folder, "Books", "Books_TOC.xhtml"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(
                get_section_toc(
                    lang,
                    strings["books"],
                    books_by_letter,
                    strings,
                    prefix="B",
                )
            )

        for letter, group in sorted(
            books_by_letter.items(), key=lambda x: (x[0] == "Other", x[0])
        ):
            filename = f"B_{letter}"
            files.append(filename)

            with open(
                os.path.join(folder, f"{filename}.xhtml"), "w", encoding="utf-8"
            ) as f:
                f.write(get_books_page(lang, letter, group, strings, cross_references))

    return files
