from collections import defaultdict

from src.utils import normalize_character

def get_authors(conn):
    cur = conn.cursor()

    cur.execute('''
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
    ''')

    authors = []
    for row in cur.fetchall():
        authors.append(dict(row))

    return authors

def get_authors_by_letter(conn):
    cur = conn.cursor()
    authors = get_authors(conn)
    authors_by_letter = defaultdict(list)

    for author in authors:
        name = author['name']
        firstLetter = normalize_character(name[0])
        
        if firstLetter.isalpha():
            authors_by_letter[firstLetter].append(author)
        else:
            authors_by_letter['Other'].append(author)

    return authors_by_letter