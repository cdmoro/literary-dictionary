PRAGMA foreign_keys = ON;

CREATE TABLE languages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL
);

CREATE TABLE authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE authors_translations (
    author_id INTEGER NOT NULL,
    language_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    PRIMARY KEY (author_id, language_id),
    FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE,
    FOREIGN KEY (language_id) REFERENCES languages(id) ON DELETE CASCADE
);

CREATE TABLE sagas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE sagas_translations (
    saga_id INTEGER NOT NULL,
    language_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    PRIMARY KEY (saga_id, language_id),
    FOREIGN KEY (saga_id) REFERENCES sagas(id) ON DELETE CASCADE,
    FOREIGN KEY (language_id) REFERENCES languages(id) ON DELETE CASCADE
);

CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    saga_id INTEGER,
    name TEXT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE,
    FOREIGN KEY (saga_id) REFERENCES sagas(id) ON DELETE SET NULL
);

CREATE TABLE books_translations (
    book_id INTEGER NOT NULL,
    language_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    PRIMARY KEY (book_id, language_id),
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
    FOREIGN KEY (language_id) REFERENCES languages(id) ON DELETE CASCADE
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    book_id INTEGER,
    saga_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT,
    FOREIGN KEY (author_id) REFERENCES authors(id),
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (saga_id) REFERENCES sagas(id)
);


CREATE TABLE entries_translations (
    entry_id INTEGER NOT NULL,
    language_id INTEGER NOT NULL,
    headword TEXT NOT NULL,
    description TEXT NOT NULL,
    alias TEXT,
    PRIMARY KEY (entry_id, language_id),
    FOREIGN KEY (entry_id) REFERENCES entries(id) ON DELETE CASCADE,
    FOREIGN KEY (language_id) REFERENCES languages(id) ON DELETE CASCADE
);
