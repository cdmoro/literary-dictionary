from pathlib import Path
import unicodedata
import json

def get_translations(lang):
    with open(f"locales/{lang}.json", "r", encoding="utf-8") as f:
        return json.load(f)
    
def normalize_character(letra):
    return unicodedata.normalize('NFD', letra).encode('ascii', 'ignore').decode('utf-8').upper()

def get_entries(conn):
    cur = conn.cursor()

    cur.execute("""
        SELECT
        e.id,
        e.headword,
        e.display_name,
        e.alias,
        e.description,
        a.id           AS author_id,
        a.name         AS author,
        s.id           AS saga_id,
        s.name         AS saga,
        b.id           AS book_id,
        b.title        AS book,
        c.abbr         AS category,
        c.id           AS category_id,
        e.draft
        FROM entries e
        LEFT JOIN authors a ON e.author_id = a.id
        LEFT JOIN sagas s   ON e.saga_id = s.id
        LEFT JOIN books b   ON e.book_id = b.id
        LEFT JOIN categories c ON e.category_id = c.id
        ORDER BY e.headword COLLATE NOCASE
    """)

    entries = []
    for row in cur.fetchall():
        entries.append(dict(row))

    return entries