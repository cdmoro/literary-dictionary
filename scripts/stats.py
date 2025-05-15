from utils import get_entries

def get_stats():
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

    print("📊 Estadísticas\n")

    total_authors = 0
    total_entries = 0

    for author, books in stats.items():
        total_por_author = 0
        print(f"🖋️ {author}")
        total_authors += 1

        for book, cantidad in books.items():
            print(f"   📖 {book}: {cantidad} registros")
            total_por_author += cantidad

        print(f"   👥 Total registros: {total_por_author}\n")
        total_entries += total_por_author

    print("\nTotal\n")
    print(f"🖋️ Autores: {total_authors}")
    print(f"👥 registros: {total_entries}")

get_stats()