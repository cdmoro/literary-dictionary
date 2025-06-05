from collections import defaultdict

from src.utils import normalize_character

def get_sagas(conn):
    cur = conn.cursor()

    cur.execute('''
        SELECT s.id, s.name, s.description, c.abbr, a.name as author, a.id as author_id
        FROM sagas s, authors a
        CROSS JOIN categories c
        WHERE c.id = 15 AND s.author_id == a.id
        ORDER BY s.name
    ''')

    sagas = []
    for row in cur.fetchall():
        sagas.append(dict(row))

    return sagas

def get_sagas_by_letter(conn):
    sagas = get_sagas(conn)
    sagas_by_letter = defaultdict(list)

    for saga in sagas:
        name = saga['name']
        first_letter = normalize_character(name[0])
        
        if first_letter.isalpha():
            sagas_by_letter[first_letter].append(saga)
        else:
            sagas_by_letter['S_Other'].append(saga)

    return sagas_by_letter

def build_saga_cross_references(conn):
    cur = conn.cursor()

    cur.execute('''
        SELECT 
            s.id AS saga_id,
            s.name AS saga_name,
            s.description AS saga_description,
            b.id AS book_id,
            b.title AS book_title,
            b.publication_year,
            a.id AS author_id,
            a.name AS author_name
        FROM sagas s
        JOIN books b ON b.saga_id = s.id
        JOIN authors a ON s.author_id = a.id
        ORDER BY s.id, b.publication_year
    ''')

    rows = cur.fetchall()

    sagas_cross_references = defaultdict(list)

    for row in rows:
        book_id = row["book_id"]
        title = row["book_title"].strip()
        first_letter = normalize_character(title[0])
        filename = f"B_{first_letter}.xhtml"
        anchor = f"B_{book_id}"
        link = f"{filename}#{anchor}"

        sagas_cross_references[row["saga_id"]].append({
            "book_id": book_id,
            "value": title,
            "publication_year": row["publication_year"],
            "link": link,
            "author_id": row["author_id"],
            "author_name": row["author_name"]
        })

    return sagas_cross_references