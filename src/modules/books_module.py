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
            a.id AS author_id,
            s.name AS saga,
            s.id AS saga_id
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
    books = get_books(conn)
    books_by_letter = defaultdict(list)

    for book in books:
        title = book['title']
        firstLetter = normalize_character(title[0])
        
        if firstLetter.isalpha():
            books_by_letter[firstLetter].append(book)
        else:
            books_by_letter['B_Other'].append(book)

    return books_by_letter

def build_book_cross_references(conn):
    books = get_books(conn)
    # Armamos un índice por libro para saber en qué archivo está
    book_reference_data = {}
    for book in books:
        if "id" in book and "title" in book:
            filename = f"{normalize_character(book['title'].strip()[0].upper())}.xhtml"
            book_reference_data[book["id"]] = (book["title"], filename)

    # Agrupamos los libros por saga y por autor
    by_saga = defaultdict(list)
    by_author = defaultdict(list)

    for book in books:
        if book["saga_id"]:
            by_saga[book["saga_id"]].append(book)
        else:
            by_author[book["author_id"]].append(book)

    # Creamos el diccionario de cross references
    cross_references = {}

    for book in books:
        book_id = book["id"]
        related = []

        if book["saga_id"]:
            same_saga = sorted(by_saga.get(book["saga_id"], []), key=lambda b: b["publication_year"] or 0)
            related = [b for b in same_saga if b["id"] != book_id]

        if not related:
            same_author = sorted(by_author.get(book["author_id"], []), key=lambda b: b["publication_year"] or 0)
            related = [b for b in same_author if b["id"] != book_id]

        # Armamos los links
        related_links = []
        for b in related:
            title, filename = book_reference_data.get(b["id"], (None, None))
            if title and filename:
                related_links.append({
                    "id": b["id"],
                    "title": title,
                    "link": f"B_{filename}#B_{b['id']}"
                })

        cross_references[book_id] = related_links

    return cross_references