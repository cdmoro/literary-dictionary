import os
import yaml
import unicodedata

def get_characters(base_dir='authors'):
    personajes = []
    for autor_dir in os.listdir(base_dir):
        autor_path = os.path.join(base_dir, autor_dir)
        if not os.path.isdir(autor_path):
            continue

        for libro_file in os.listdir(autor_path):
            if not libro_file.endswith('.yml'):
                continue

            with open(os.path.join(autor_path, libro_file), 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file) or {}

                # Leemos el autor y libro directamente del archivo YAML
                autor = data.get('autor', 'Desconocido')
                libro = data.get('libro', 'Desconocido')

                if not autor or not libro:
                    print(f"⚠️ Faltan datos de autor o libro en {libro_file}")
                    continue

                for personaje in data.get('personajes', []):
                    nombre = personaje.get('nombre', '')
                    variantes = personaje.get('variantes', [])
                    descripcion = personaje.get('descripcion', '')

                    personajes.append({
                        'autor': autor,
                        'libro': libro,
                        'nombre': nombre,
                        'variantes': variantes,
                        'descripcion': descripcion
                    })

    return personajes