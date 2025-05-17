import os
import yaml
import unicodedata

def get_entries(base_dir='dictionary'):
    entries = []
    for author_dir in os.listdir(base_dir):
        author_path = os.path.join(base_dir, author_dir)
        if not os.path.isdir(author_path):
            continue

        for book_file in os.listdir(author_path):
            if not book_file.endswith('.yml'):
                continue

            with open(os.path.join(author_path, book_file), 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file) or {}

                author = data.get('author')
                book = data.get('book', '')
                saga = data.get('saga', '')

                if not author:
                    print(f"⚠️ Faltan datos de autor en {book_file}")
                    continue

                for personaje in data.get('characters', []):
                    name = personaje.get('name', '')
                    alias = personaje.get('alias', [])
                    description = personaje.get('description', '')

                    entries.append({
                        'word': name,
                        'alias': alias,
                        'description': description,
                        'author': author,
                        'book': book,
                        'saga': saga,
                        'category': 'Personaje'
                    })

                for word in data.get('words', []):
                    entryName = word.get('word', '')
                    alias = word.get('alias', [])
                    description = word.get('description', '')

                    entries.append({
                        'word': entryName,
                        'alias': alias,
                        'description': description,
                        'author': author,
                        'book': book,
                        'saga': saga,
                        'category': 'Concepto'
                    })

    return sorted(entries, key=lambda d: d['word'])
