import sqlite3
from collections import defaultdict

# Conexión a la DB
conn = sqlite3.connect('dictionary/dictionary.es.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Consultamos todas las entries que no sean draft (si querés incluir drafts sacá el filtro)
cur.execute("""
SELECT id, author_id, saga_id, book_id, category_id, headword, draft
FROM entries
WHERE draft = 0
""")
entries = cur.fetchall()

# Índices para agrupar: estructura {clave: list of entries}
by_book_cat = defaultdict(list)      # key: (book_id, category_id)
by_saga_cat = defaultdict(list)      # key: (saga_id, category_id)
by_author_cat = defaultdict(list)    # key: (author_id, category_id)

# Map id to entry for lookup
id_to_entry = {}

for e in entries:
    id_to_entry[e['id']] = e
    # Solo si tiene category_id para indexar
    cat = e['category_id']
    if cat is None:
        continue
    book = e['book_id']
    saga = e['saga_id']
    author = e['author_id']
    if book is not None:
        by_book_cat[(book, cat)].append(e)
    if saga is not None:
        by_saga_cat[(saga, cat)].append(e)
    if author is not None:
        by_author_cat[(author, cat)].append(e)

# Función para obtener relacionados por entry
def get_related(entry):
    cat = entry['category_id']
    if cat is None:
        return []  # o podés definir otra lógica para entries sin categoría

    # Prioridad: book > saga > author
    if entry['book_id'] is not None:
        group = by_book_cat.get((entry['book_id'], cat), [])
    elif entry['saga_id'] is not None:
        group = by_saga_cat.get((entry['saga_id'], cat), [])
    else:
        group = by_author_cat.get((entry['author_id'], cat), [])

    # Excluir la misma entry
    related = [(e['id'], e['headword']) for e in group if e['id'] != entry['id']]
    return related

# Ejemplo: obtener relacionados para todas las entries
for entry in entries:
    related = get_related(entry)
    print(f"Entry: {entry['headword']} (id {entry['id']})")
    print(" Related entries (id, headword):", related)
    print()
