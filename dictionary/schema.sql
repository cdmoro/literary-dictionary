PRAGMA foreign_keys = ON;

CREATE TABLE authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
)

CREATE TABLE sagas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    author_id INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES authors(id)
)

CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    author_id INTEGER NOT NULL,
    saga_id INTEGER,
    FOREIGN KEY (author_id) REFERENCES authors(id),
    FOREIGN KEY (saga_id) REFERENCES sagas(id)
)

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_name TEXT NOT NULL,
    name TEXT NOT NULL UNIQUE,
    abbr TEXT NOT NULL,
    description TEXT NOT NULL
)

CREATE TABLE entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    saga_id INTEGER,
    book_id INTEGER,
    headword TEXT NOT NULL,
    display_name TEXT,
    alias TEXT,
    description TEXT NOT NULL,
    category_id INTEGER NULL,
    draft INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT,
    FOREIGN KEY (author_id) REFERENCES authors(id),
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (saga_id) REFERENCES sagas(id)
)