import csv
from utils import get_characters  # Asumiendo que la función está en otro archivo

def generar_csv():
    # Llamamos a la función que carga los personajes desde los archivos YAML
    personajes = get_characters()

    # Definimos el nombre del archivo CSV
    output_file = 'output/diccionario.csv'

    # Definimos los encabezados del CSV
    fieldnames = ['autor', 'libro', 'nombre', 'variantes', 'descripcion']

    # Abrimos el archivo CSV en modo escritura
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Escribimos los encabezados en el archivo
        writer.writeheader()

        # Escribimos cada personaje en el archivo
        for personaje in personajes:
            # Convertimos la lista de variantes en una cadena de texto separada por comas
            personaje['variantes'] = ', '.join(personaje['variantes'])
            
            # Escribimos la información del personaje en el archivo CSV
            writer.writerow(personaje)

    print(f"Archivo CSV generado: {output_file}")

# Llamamos a la función para generar el archivo CSV
generar_csv()
