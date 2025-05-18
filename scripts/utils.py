from pathlib import Path
import yaml

def load_entries_from_section(data_section, author, book, saga, category=''):
    entries = []
    for item in data_section:
        headword = item.get('name') or item.get('entry') or ''
        alias = item.get('alias')
        if not isinstance(alias, list):
            alias = []
        description = item.get('description', '')

        if headword:
            entries.append({
                'headword': headword,
                'alias': alias,
                'description': description,
                'author': author,
                'book': book,
                'saga': saga,
                'category': category
            })
    return entries

def get_entries(base_dir='dictionary'):
    base_path = Path(base_dir)
    entries = []

    for author_dir in base_path.iterdir():
        if not author_dir.is_dir():
            continue

        for book_file in author_dir.glob('*.yml'):
            with book_file.open(encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}

            author = data.get('author')
            book = data.get('book', '')
            saga = data.get('saga', '')

            if not author:
                print(f"⚠️ Faltan datos de autor en {book_file.name}")
                continue

            characters = data.get('characters', [])
            entries.extend(load_entries_from_section(characters, author, book, saga, 'Personaje'))

            glossary = data.get('glossary', [])
            entries.extend(load_entries_from_section(glossary, author, book, saga))

    return sorted(entries, key=lambda d: d['headword'].lower())
