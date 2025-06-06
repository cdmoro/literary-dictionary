from collections import defaultdict

from src.utils import normalize_character


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
    cur = conn.cursor()
    authors = get_authors(conn)
    authors_by_letter = defaultdict(list)

    for author in authors:
        name = author["name"]
        first_letter = normalize_character(name[0])

        if first_letter.isalpha():
            authors_by_letter[first_letter].append(author)
        else:
            authors_by_letter["A_Other"].append(author)

    return authors_by_letter


def build_author_cross_references(conn, max_books_per_author=6):
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
            b.title AS book_title,
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
        if len(authors_cross_references[author_id]) >= max_books_per_author:
            continue

        book_id = row["book_id"]
        title = row["book_title"].strip()
        first_letter = normalize_character(title[0])
        filename = f"B_{first_letter}.xhtml"
        anchor = f"B_{book_id}"
        link = f"{filename}#{anchor}"

        authors_cross_references[author_id].append(
            {
                "book_id": book_id,
                "value": title,
                "publication_year": row["publication_year"],
                "link": link,
                "author_name": row["author_name"],
            }
        )

    return authors_cross_references
