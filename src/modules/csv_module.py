import csv
from dotenv import load_dotenv
import os

from utils import get_entries

def generate_csv(lang, strings):
    load_dotenv()
    print(f'\nGenerating CSV ({lang.upper()})...')

    entries = get_entries(lang)
    output_file = f'output/{strings["file_name"].format(lang=lang.upper(), version=os.getenv('DICT_VERSION'))}.csv'
    fieldnames = ['id', 'headword', 'displayValue', 'alias', 'description', 'author', 'book', 'saga', 'category', 'abbrev', 'seeAlso']

    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for entry in entries:
            entry['alias'] = ', '.join(entry['alias'])
            entry['seeAlso'] = ', '.join(str(id) for id in entry['seeAlso'])
            writer.writerow(entry)

    print(f"✅ CSV created successfully")
