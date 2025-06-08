import os
from collections import defaultdict

from src.pages.section import get_section_page, get_section_toc
from src.utils import normalize_character
from src.pages.authors import get_authors_page


def get_authors(conn):
    cur = conn.cursor()

    cur.execute(
        """
        SELECT 
            a.id, 
            a.name, 
            a.description,
            a.birth_year,
            a.death_year, 
            c.abbr
        FROM authors a
        CROSS JOIN categories c
        WHERE c.id = 13
        ORDER BY a.name
    """
    )

    authors = []
    for row in cur.fetchall():
        authors.append(dict(row))

    return authors


def get_authors_by_letter(conn):
    authors = get_authors(conn)
    authors_by_letter = defaultdict(list)

    for author in authors:
        name = author["name"]
        first_letter = normalize_character(name[0])

        if first_letter.isalpha():
            authors_by_letter[first_letter].append(author)
        else:
            authors_by_letter["Other"].append(author)

    return authors_by_letter


def build_author_book_cross_references(conn):
    cur = conn.cursor()

    cur.execute(
        f"""
        SELECT 
            a.id AS author_id,
            a.name AS author_name,
            a.description AS author_description,
            a.birth_year,
            a.death_year,
            b.id AS book_id,
            b.name AS book_title,
            b.publication_year
        FROM authors a
        JOIN books b ON b.author_id = a.id
        ORDER BY a.id, b.publication_year
    """
    )

    rows = cur.fetchall()

    authors_cross_references = defaultdict(list)

    for row in rows:
        author_id = row["author_id"]
        book_id = row["book_id"]
        title = row["book_title"].strip()
        first_letter = normalize_character(title[0])
        filename = f"B_{first_letter}.xhtml"
        anchor = f"B_{book_id}"
        link = f"{filename}#{anchor}"

        authors_cross_references[author_id].append(
            {
                "book_id": book_id,
                "name": title,
                "publication_year": row["publication_year"],
                "link": link,
                "author_name": row["author_name"],
            }
        )

    return authors_cross_references


def build_author_saga_cross_references(conn):
    cur = conn.cursor()

    cur.execute(
        """
        SELECT 
            a.id AS author_id,
            a.name AS author_name,
            s.id AS saga_id,
            s.name AS saga_name
        FROM authors a
        JOIN sagas s ON s.author_id = a.id
        ORDER BY a.id, s.name
        """
    )

    rows = cur.fetchall()

    author_saga_refs = defaultdict(list)

    for row in rows:
        saga_id = row["saga_id"]
        saga_name = row["saga_name"].strip()
        first_letter = normalize_character(saga_name[0])
        filename = f"S_{first_letter}.xhtml"
        anchor = f"S_{saga_id}"
        link = f"{filename}#{anchor}"

        author_saga_refs[row["author_id"]].append(
            {
                "saga_id": saga_id,
                "name": saga_name,
                "link": link,
                "author_name": row["author_name"],
            }
        )

    return author_saga_refs


def create_authors_files(output_folder, lang, strings, conn):
    folder = os.path.join(output_folder, "Authors")
    authors_by_letter = get_authors_by_letter(conn)
    authors_book_cross_references = build_author_book_cross_references(conn)
    authors_saga_cross_references = build_author_saga_cross_references(conn)
    files = []

    if len(authors_by_letter) > 0:
        os.makedirs(folder)

        files.append("Authors")
        files.append("Authors_TOC")

        with open(
            os.path.join(output_folder, "Authors", "Authors.xhtml"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(get_section_page(lang, strings["authors"]))

        with open(
            os.path.join(output_folder, "Authors", "Authors_TOC.xhtml"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(
                get_section_toc(
                    lang,
                    strings["authors"],
                    authors_by_letter,
                    strings,
                    prefix="A",
                )
            )

        for letter, group in sorted(
            authors_by_letter.items(), key=lambda x: (x[0] == "Other", x[0])
        ):
            filename = f"A_{letter}"
            files.append(filename)

            with open(
                os.path.join(folder, f"{filename}.xhtml"), "w", encoding="utf-8"
            ) as f:
                f.write(
                    get_authors_page(
                        lang,
                        letter,
                        group,
                        strings,
                        authors_book_cross_references,
                        authors_saga_cross_references,
                    )
                )

    return files
