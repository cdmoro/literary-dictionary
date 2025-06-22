import csv

csv_file = "src/scripts/table.csv"
sql_file = "src/scripts/inserts.sql"
nombre_tabla = "entries"

categories = {
    "character": 1,
    "place": 2,
    "object": 3,
    "concept": 4,
    "event": 5,
    "creature": 6,
    "institution": 7,
    "spell": 8,
    "language": 9,
    "quote": 10,
    "group": 11,
    "people": 12,
    "author": 13,
    "book": 14,
    "saga": 15,
    "plant": 16,
    "substance": 17,
    "weapon": 18,
    "rank": 19,
    "technology": 20,
    "ritual": 21,
    "attire": 22,
    "instrument": 23,
    "food": 24,
    "religion": 25,
    "celestial": 26,
}


def escape_sql(value):
    if value is None:
        return "NULL"

    if value in categories:
        return str(categories[value])

    escaped = value.replace("'", "''")
    return f"'{escaped}'"


with open(csv_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    columnas = reader.fieldnames
    columnas_sql = ", ".join([f'"{col}"' for col in columnas])

    with open(sql_file, "w", encoding="utf-8") as salida:
        for fila in reader:
            valores = [
                fila[col].strip() if fila[col].strip() != "" else None
                for col in columnas
            ]
            valores_sql = ", ".join([escape_sql(v) for v in valores])
            sentencia = (
                f"INSERT INTO {nombre_tabla} ({columnas_sql}) VALUES ({valores_sql});\n"
            )
            salida.write(sentencia)

print(f"INSERT statements generated in: {sql_file}")
