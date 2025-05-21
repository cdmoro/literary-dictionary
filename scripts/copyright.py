from dotenv import load_dotenv
import os

load_dotenv()

def get_copyright_html(registros):
    total_registros = len(registros)
    autores = set()
    sagas = set()
    libros = set()

    for p in registros:
        if p.get('author'):
            autores.add(p['author'])
        if p.get('saga'):
            sagas.add(p['saga'])
        if p.get('book'):
            libros.add(p['book'])

    total_autores = len(autores)
    total_sagas = len(sagas)
    total_libros = len(libros)

    return f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<body>
    <p><strong>Diccionario Literario</strong></p>
    <p><em>Desde Aurelieano a Zaratustra: personajes y jergas de la literatura universal</em></p>
    <br>
    <p>© 2025 Carlos Bonadeo. Ningún derecho reservado. Queda alentada la distribución de esta obra citando en lo posible las fuentes.</p>
    <p><strong>Versión {os.getenv('DICT_VERSION')}</p>
    <ul>
        <li>Registros: {total_registros}</li>
        <li>Autores: {total_autores}</li>
        <li>Sagas: {total_sagas}</li>
        <li>Libros: {total_libros}</li>
    </ul>
</body>
</html>
'''