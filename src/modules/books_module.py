from collections import defaultdict

from src.utils import normalize_character

def get_books(conn):
    cur = conn.cursor()

    cur.execute('''
        SELECT 
            b.id, 
            b.title, 
            b.description, 
            b.publication_year,
            c.abbr, 
            a.name AS author, 
            s.name AS saga
        FROM books b
        JOIN authors a ON b.author_id = a.id
        CROSS JOIN categories c
        LEFT JOIN sagas s ON b.saga_id = s.id
        WHERE c.id = 14
        ORDER BY b.title;
    ''')

    books = []
    for row in cur.fetchall():
        books.append(dict(row))

    return books

def get_books_by_letter(conn):
    cur = conn.cursor()
    books = get_books(conn)
    books_by_letter = defaultdict(list)

    for book in books:
        title = book['title']
        firstLetter = normalize_character(title[0])
        
        if firstLetter.isalpha():
            books_by_letter[firstLetter].append(book)
        else:
            books_by_letter['Other'].append(book)

    return books_by_letter