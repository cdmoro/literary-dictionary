from pathlib import Path
import sqlite3
import yaml

CATEGORIES = [
    'characters',
    'places',
    'objects',
    'concepts',
    'events',
    'creatures',
    'institutions',
    'spells',
    'languages',
    'quotes',
    'glossary',
]

def get_translations(lang):
    with open(f"locales/{lang}.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def get_entries_v2(conn):
    # conn = sqlite3.connect(f'dictionary/dictionary.{lang}.db')
    # conn.row_factory = sqlite3.Row
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

    # conn.close()
    return entries