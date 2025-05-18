import csv
from dotenv import load_dotenv
import os
from utils import get_entries

def generate_csv():
    load_dotenv()
    # Llamamos a la función que carga los personajes desde los archivos YAML
    entries = get_entries()

    # Definimos el nombre del archivo CSV
    output_file = f'output/Bonadeo, Carlos - Diccionario Literario (v{os.getenv('DICT_VERSION')}).csv'

    # Definimos los encabezados del CSV
    fieldnames = ['headword', 'alias', 'description', 'author', 'book', 'saga', 'category']

    # Abrimos el archivo CSV en modo escritura
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Escribimos los encabezados en el archivo
        writer.writeheader()

        # Escribimos cada personaje en el archivo
        for entry in entries:
            # Convertimos la lista de variantes en una cadena de texto separada por comas
            entry['alias'] = ', '.join(entry['alias'])
            
            # Escribimos la información del personaje en el archivo CSV
            writer.writerow(entry)

    print(f"Archivo CSV generado: {output_file}")

# Llamamos a la función para generar el archivo CSV
generate_csv()
