import json
from dotenv import load_dotenv
import os

from utils import get_entries

def generate_json():
    load_dotenv()
    print('\nGenerating JSON...')

    entries = get_entries()
    output_file = f"output/Bonadeo, Carlos - Diccionario Literario (v{os.getenv('DICT_VERSION')}).json"

    # Preparar las entradas para JSON (por si alias es lista, convertir a string o dejarla así)
    # for entry in entries:
        # Si querés mantener alias como lista, no hagas nada
        # Pero si querés que sea string separado por comas, descomenta la línea siguiente:
        # entry['alias'] = ', '.join(entry['alias']) if isinstance(entry.get('alias'), list) else entry.get('alias')

        # Asegurarse que no haya datos que no se serializan bien (opcional)
        # por ejemplo, si hay sets u objetos no serializables, hay que convertirlos.

    with open(output_file, mode='w', encoding='utf-8') as file:
        json.dump(entries, file, ensure_ascii=False, indent=4)

    print(f"✅ JSON created successfully")
