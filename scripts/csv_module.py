import csv
from dotenv import load_dotenv
import os

from utils import get_entries

def generate_csv():
    load_dotenv()

    entries = get_entries()
    output_file = f'output/Bonadeo, Carlos - Diccionario Literario (v{os.getenv('DICT_VERSION')}).csv'
    fieldnames = ['id', 'headword', 'displayValue', 'alias', 'description', 'author', 'book', 'saga', 'category', 'abbrev']

    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for entry in entries:
            entry['alias'] = ', '.join(entry['alias'])
            writer.writerow(entry)

    print(f"CSV creado en: {output_file}")
