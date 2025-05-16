from utils import get_entries
from datetime import datetime

output_file = 'statistics.md'

def generate_stats():
    entries = get_entries()

    stats = {}

    for entry in entries:
        author = entry['author']
        book = entry['book']
        
        if author not in stats:
            stats[author] = {}

        if book not in stats[author]:
            stats[author][book] = 0

        stats[author][book] += 1

    lines = []

    lines.append("# Estadísticas\n")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines.append(f"_Última actualización: {now}_\n")

    total_authors = 0
    total_books = 0
    total_entries = 0

    lines.append("## Por autor\n")

    lines.append("|Autor|Sagas|Libros|Registros|")
    lines.append("|---|---|---|---|")

    for author in sorted(stats.keys()):
        books = stats[author]
        total_por_author = sum(books.values())
        total_authors += 1
        total_books += len(books)
        total_entries += total_por_author

        # Siempre mostrar 0 en Sagas (columna vacía) de forma elegante
        lines.append(f"|{author}|0|{len(books)}|{total_por_author}|")

    lines.append("## Total\n")

    lines.append("|Autores|Sagas|Libros|Registros|")
    lines.append("|---|---|---|---|")
    lines.append(f"|{total_authors}|0|{total_books}|{total_entries}|")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"Archivo '{output_file}' generado correctamente.")

generate_stats()
