from utils import get_entries
from dotenv import load_dotenv
import os

output_file = 'Statistics.md'

def generate_stats():
    load_dotenv()
    entries = get_entries()

    stats = {}

    for entry in entries:
        author = entry.get('author', 'Unknown')

        if author not in stats:
            stats[author] = {
                'sagas': set(),
                'books': set(),
                'entries_count': 0
            }

        stats[author]['entries_count'] += 1

        if 'saga' in entry and entry['saga'].strip():
            stats[author]['sagas'].add(entry['saga'].strip())

        if 'book' in entry and entry['book'].strip():
            stats[author]['books'].add(entry['book'].strip())

    lines = []

    lines.append("# Estadísticas\n")
    lines.append(f"_Versión: {os.getenv('DICT_VERSION')}_\n")

    total_authors = len(stats)
    total_sagas = 0
    total_books = 0
    total_entries = 0

    lines.append("## Por autor\n")

    lines.append("|Autor|Sagas|Libros|Registros|")
    lines.append("|---|---|---|---|")

    for author in sorted(stats.keys()):
        sagas_count = len(stats[author]['sagas'])
        books_count = len(stats[author]['books'])
        entries_count = stats[author]['entries_count']

        total_sagas += sagas_count
        total_books += books_count
        total_entries += entries_count

        lines.append(f"|{author}|{sagas_count}|{books_count}|{entries_count}|")

    lines.append("\n## Total\n")

    lines.append("|Autores|Sagas|Libros|Registros|")
    lines.append("|---|---|---|---|")
    lines.append(f"|{total_authors}|{total_sagas}|{total_books}|{total_entries}|")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"Archivo '{output_file}' generado correctamente.")

if __name__ == '__main__':
    generate_stats()
