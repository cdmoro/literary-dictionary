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

def get_translations(lang):
    with open(f"locales/{lang}.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_entries_from_section(data_section, author, book, saga, category, abbrev = '', cross_ref_ids = {}):
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
        draft = item.get('draft', False)
        filtered_ids = [cid for cid in cross_ref_ids.get(category, []) if cid != id]

        if not id:
            print(f'  - ⚠️  ID missing, entry skipped')
            continue

        if not headword:
            print(f'  - ⚠️  Headword missing for {id}, entry skipped')
            continue

        if draft:
            print(f'  - ⏭️  {id} marked as draft, entry skipped')
            continue

        if headword and not draft:
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
                'seeAlso': filtered_ids + seeAlso,
            })

    return entries

def get_entries(lang):
    base_path = Path(f'dictionary/{lang}')
    entries = []

    for author_dir in base_path.iterdir():
        if not author_dir.is_dir():
            continue

        for book_file in author_dir.glob('*.yaml'):
            with book_file.open(encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}

            author = data.get('author')
            book = data.get('book', '')
            saga = data.get('saga', '')

            if not author:
                print(f"- ⏭️  Missing author data in {book_file.name}")
                continue

            cross_ref_ids = {
                key: [entry.get('id') for entry in data.get(key) or [] if 'id' in entry and not entry.get('draft', False)]
                for key in CATEGORIES
                if key != 'glossary'
            }

            for key, abbrev in CATEGORIES.items():
                entries.extend(load_entries_from_section(
                    data.get(key, []),
                    author,
                    book,
                    saga,
                    key,
                    abbrev,
                    cross_ref_ids,
                ))

    return sorted(entries, key=lambda d: d['headword'].lower())
