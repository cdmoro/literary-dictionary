import json
from dotenv import load_dotenv
import os

from utils import get_entries

def generate_json(lang, strings):
    load_dotenv()
    print(f'\nGenerating JSON ({lang.upper()})...')

    entries = get_entries(lang)
    output_file = f'output/{strings["file_name"].format(lang=lang.upper(), version=os.getenv('DICT_VERSION'))}.json'

    with open(output_file, mode='w', encoding='utf-8') as file:
        json.dump(entries, file, ensure_ascii=False, indent=4)

    print(f"✅ JSON created successfully")
