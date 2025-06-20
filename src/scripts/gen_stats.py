import sqlite3

DB_PATH = "dictionary/dictionary.en.db"
OUTPUT_FILE = "Dictionary_Coverage.md"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


def fetch_totals():
    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(DISTINCT sagas.id) FROM sagas JOIN entries ON entries.saga_id = sagas.id WHERE entries.draft = 0"
    )
    total_series = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(DISTINCT authors.id) FROM authors JOIN entries ON entries.author_id = authors.id WHERE entries.draft = 0"
    )
    total_authors = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM entries WHERE draft = 0")
    total_entries = cursor.fetchone()[0]

    return total_books, total_series, total_authors, total_entries


def fetch_books():
    # List all books with author, series, and number of entries (including series entries if applicable)
    query = """
        SELECT 
            books.name,
            COALESCE(sagas.name, '') as saga_name,
            COALESCE(authors.name, '') as author_name,
            books.id,
            books.saga_id
        FROM books
        LEFT JOIN sagas ON books.saga_id = sagas.id
        LEFT JOIN authors ON books.author_id = authors.id
        ORDER BY books.name COLLATE NOCASE
    """
    cursor.execute(query)
    books = cursor.fetchall()

    result = []
    for book_name, saga_name, author_name, book_id, saga_id in books:
        cursor.execute(
            "SELECT COUNT(*) FROM entries WHERE draft = 0 AND book_id = ?", (book_id,)
        )
        book_entries = cursor.fetchone()[0]

        total_entries = book_entries

        if saga_id:
            cursor.execute(
                "SELECT COUNT(*) FROM entries WHERE draft = 0 AND saga_id = ?",
                (saga_id,),
            )
            saga_entries = cursor.fetchone()[0]
            total_entries += saga_entries
            result.append((book_name, saga_name, author_name, f"{total_entries}*"))
        else:
            result.append((book_name, "", author_name, str(total_entries)))

    return result


def fetch_series():
    # List all series with author and number of entries
    query = """
        SELECT 
            sagas.name,
            COALESCE(authors.name, '') as author_name,
            COUNT(entries.id)
        FROM entries
        JOIN sagas ON entries.saga_id = sagas.id
        LEFT JOIN authors ON sagas.author_id = authors.id
        WHERE entries.draft = 0
        GROUP BY sagas.id
        ORDER BY sagas.name COLLATE NOCASE
    """
    cursor.execute(query)
    return cursor.fetchall()


def fetch_authors():
    # List all authors with number of entries
    query = """
        SELECT 
            authors.name,
            COUNT(entries.id)
        FROM entries
        JOIN authors ON entries.author_id = authors.id
        WHERE entries.draft = 0
        GROUP BY authors.id
        ORDER BY authors.name COLLATE NOCASE
    """
    cursor.execute(query)
    return cursor.fetchall()


def write_markdown(title, headers, rows, file):
    file.write(f"## {title}\n\n")
    file.write("| " + " | ".join(headers) + " |\n")
    file.write("|" + "|".join("-" * (len(h) + 2) for h in headers) + "|\n")
    for row in rows:
        file.write("| " + " | ".join(str(col) for col in row) + " |\n")
    file.write("\n")


# Fetch data
books = fetch_books()
series = fetch_series()
authors = fetch_authors()
totals = fetch_totals()

# Write Markdown
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("# 📖 Dictionary Coverage\n\n")
    f.write(
        "This index lists all authors, books, and series included in the dictionary, along with the number of entries available for each.\n\n"
    )
    f.write(
        "_Note: If a book belongs to a series, its count includes entries from the series too (marked with an asterisk)._ \n\n"
    )

    f.write("## 📊 Summary\n\n")
    f.write("| Type    | Count |\n")
    f.write("|---------|-------|\n")
    f.write(f"| Books   | {totals[0]} |\n")
    f.write(f"| Series  | {totals[1]} |\n")
    f.write(f"| Authors | {totals[2]} |\n")
    f.write(f"| Entries | {totals[3]} |\n\n")

    write_markdown("📚 Books", ["Title", "Series", "Author", "Entries"], books, f)
    write_markdown("📕 Series", ["Series", "Author", "Entries"], series, f)
    write_markdown("✍️ Authors", ["Author", "Entries"], authors, f)

print(f"✅ Markdown file '{OUTPUT_FILE}' generated.")
conn.close()
