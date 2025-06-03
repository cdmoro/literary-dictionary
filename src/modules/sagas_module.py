from collections import defaultdict

from src.utils import normalize_character

def get_sagas(conn):
    cur = conn.cursor()

    cur.execute('''
        SELECT s.id, s.name, s.description, c.abbr, a.name as author
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
    cur = conn.cursor()
    sagas = get_sagas(conn)
    sagas_by_letter = defaultdict(list)

    for saga in sagas:
        name = saga['name']
        firstLetter = normalize_character(name[0])
        
        if firstLetter.isalpha():
            sagas_by_letter[firstLetter].append(saga)
        else:
            sagas_by_letter['Other'].append(saga)

    return sagas_by_letter