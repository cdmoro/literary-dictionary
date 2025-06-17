import os
from collections import defaultdict

from src.pages.section import get_section_page, get_section_toc
from src.utils import normalize_character
from src.pages.sagas import get_sagas_page
from src.constants import encoding


def get_sagas(conn):
    cur = conn.cursor()

    cur.execute(
        """
        SELECT s.id, s.name, s.description, c.abbr, a.name as author, a.id as author_id
        FROM sagas s, authors a
        CROSS JOIN categories c
        WHERE c.id = 15 AND s.author_id == a.id
        ORDER BY s.name
    """
    )

    sagas = []
    for row in cur.fetchall():
        sagas.append(dict(row))

    return sagas


def get_sagas_by_letter(conn):
    sagas = get_sagas(conn)
    sagas_by_letter = defaultdict(list)

    for saga in sagas:
        name = saga["name"]
        first_letter = normalize_character(name[0])

        if first_letter.isalpha():
            sagas_by_letter[first_letter].append(saga)
        else:
            sagas_by_letter["Other"].append(saga)

    return sagas_by_letter


def build_saga_cross_references(conn):
    cur = conn.cursor()

    cur.execute(
        """
        SELECT 
            s.id AS saga_id,
            s.name AS saga_name,
            s.description AS saga_description,
            b.id AS book_id,
            b.name AS book_title,
            b.publication_year,
            a.id AS author_id,
            a.name AS author_name
        FROM sagas s
        JOIN books b ON b.saga_id = s.id
        JOIN authors a ON s.author_id = a.id
        ORDER BY s.id, b.publication_year
    """
    )

    rows = cur.fetchall()

    sagas_cross_references = defaultdict(list)

    for row in rows:
        book_id = row["book_id"]
        title = row["book_title"].strip()
        first_letter = normalize_character(title[0])
        filename = f"B_{first_letter}.xhtml"
        anchor = f"B_{book_id}"
        link = f"{filename}#{anchor}"

        sagas_cross_references[row["saga_id"]].append(
            {
                "book_id": book_id,
                "name": title,
                "publication_year": row["publication_year"],
                "link": link,
                "author_id": row["author_id"],
                "author_name": row["author_name"],
            }
        )

    return sagas_cross_references


def create_sagas_files(output_folder, lang, strings, conn):
    folder = os.path.join(output_folder, "Sagas")
    sagas_by_letter = get_sagas_by_letter(conn)
    cross_references = build_saga_cross_references(conn)
    files = []

    if len(sagas_by_letter) > 0:
        os.makedirs(folder)

        files.append("Sagas")
        files.append("Sagas_TOC")

        with open(
            os.path.join(output_folder, "Sagas", "Sagas.xhtml"), "w", encoding=encoding
        ) as f:
            f.write(get_section_page(lang, strings["appendix"], strings["sagas"]))

        with open(
            os.path.join(output_folder, "Sagas", "Sagas_TOC.xhtml"),
            "w",
            encoding=encoding,
        ) as f:
            f.write(
                get_section_toc(
                    lang,
                    strings["sagas"],
                    sagas_by_letter,
                    strings,
                    prefix="S",
                )
            )

        for letter, group in sorted(
            sagas_by_letter.items(), key=lambda x: (x[0] == "Other", x[0])
        ):
            filename = f"S_{letter}"
            files.append(filename)

            with open(
                os.path.join(folder, f"{filename}.xhtml"), "w", encoding=encoding
            ) as f:
                f.write(get_sagas_page(lang, letter, group, strings, cross_references))

    return files
