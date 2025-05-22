from pathlib import Path
import yaml

CATEGORIES = {
    'characters': 'per.',
    'places': 'lug.',
    'objects': 'obj.',
    'concepts': 'con.',
    'events': 'ev.',
    'creatures': 'cri.',
    'institutions': 'inst.',
    'spells': 'hech.',
    'languages': 'leng.',
    'quotes': 'cit.',
    'glossary': None,
}
CATEGORY_KEYS = CATEGORIES.keys()

def load_entries_from_section(data_section, author, book, saga, category, abbrev = ''):
    entries = []
    for item in data_section:
        headword = item.get('headword')
        displayValue = item.get('displayValue')
        alias = item.get('alias')
        if not isinstance(alias, list):
            alias = []
        description = item.get('description', '')
        skip = item.get('skip', False)

        if headword and not skip:
            entries.append({
                'headword': headword,
                'displayValue': displayValue,
                'alias': alias,
                'description': description,
                'author': author,
                'book': book,
                'saga': saga,
                'category': category,
                'abbrev': abbrev,
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

            for key, abbrev in CATEGORIES.items():
                entries.extend(load_entries_from_section(
                    data.get(key, []),
                    author,
                    book,
                    saga,
                    key,
                    abbrev
                ))

    return sorted(entries, key=lambda d: d['headword'].lower())
