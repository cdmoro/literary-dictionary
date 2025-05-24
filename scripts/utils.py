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

def load_entries_from_section(data_section, author, book, saga, category, abbrev = '', characters_ids = []):
    entries = []
    for item in data_section:
        id = item.get('id')
        headword = item.get('headword')
        displayValue = item.get('displayValue')
        alias = item.get('alias')
        if not isinstance(alias, list):
            alias = []
        description = item.get('description', '')
        seeAlso = item.get('seeAlso')
        if not isinstance(seeAlso, list):
            seeAlso = []
        skip = item.get('skip', False)
        filtered_ids = [cid for cid in characters_ids if cid != id] if category == 'characters' else []

        if headword and not skip:
            entries.append({
                'id': id,
                'headword': headword,
                'displayValue': displayValue,
                'alias': alias,
                'description': description,
                'author': author,
                'book': book,
                'saga': saga,
                'category': category,
                'abbrev': abbrev,
                'seeAlso': seeAlso + filtered_ids,
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
            characters = data.get('characters', [])
            characters_ids = []

            if not author:
                print(f"- ⏭️  Missing author data in {book_file.name}")
                continue

            if characters:
                characters_ids = [c['id'] for c in characters]

            for key, abbrev in CATEGORIES.items():
                entries.extend(load_entries_from_section(
                    data.get(key, []),
                    author,
                    book,
                    saga,
                    key,
                    abbrev,
                    characters_ids,
                ))

    return sorted(entries, key=lambda d: d['headword'].lower())
