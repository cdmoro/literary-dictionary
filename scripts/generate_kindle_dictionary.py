import os
import unicodedata
import shutil
import zipfile
from collections import defaultdict
from utils import get_entries  # Asegúrate de que esta función esté definida correctamente

output_folder = 'output/kindle'
epub_filename = 'output/Diccionario_Literario.epub'

def normalizar_letra(letra):
    return unicodedata.normalize('NFD', letra).encode('ascii', 'ignore').decode('utf-8').upper()

def generar_diccionario():
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder, exist_ok=True)

    personajes = get_entries()

    entradas_por_letra = defaultdict(list)
    for personaje in personajes:
        palabra = personaje['word']
        letra = normalizar_letra(palabra[0])
        if letra.isalpha():
            entradas_por_letra[letra].append(personaje)
        else:
            entradas_por_letra['Otros'].append(personaje)

    xhtml_files = []
    for letra, entradas in sorted(entradas_por_letra.items()):
        filename = f"{letra}.xhtml"
        xhtml_files.append(filename)
        with open(os.path.join(output_folder, filename), 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            f.write('<!DOCTYPE html>\n')
            f.write('<html xmlns="http://www.w3.org/1999/xhtml" xmlns:idx="http://www.mobipocket.com/idx">\n')
            f.write('<head>\n')
            f.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>\n')
            f.write('<link rel="stylesheet" type="text/css" href="style.css"/>\n')
            f.write(f'<title>{letra}</title>\n')
            f.write('</head>\n<body>\n')
            for personaje in entradas:
                palabra = personaje['word']
                descripcion = personaje['description']
                categoria = personaje.get('category')
                autor = personaje.get('author')
                libro = personaje.get('book')
                saga = personaje.get('saga')

                f.write(f'<idx:entry name="main" scriptable="yes" spell="yes">\n')
                f.write(f'  <idx:orth>{palabra}\n')
                aliases = personaje.get('alias', [])
                if aliases:
                    f.write(f'    <idx:infl>\n')
                    for alt in aliases:
                        f.write(f'      <idx:iform value="{alt}"/>\n')
                    f.write(f'    </idx:infl>\n')
                f.write(f'  </idx:orth>\n')
                
                if aliases:
                    f.write(f'  <p><strong>Alias:</strong> <em>{", ".join(aliases)}</em></p>\n')
                f.write(f'  <p>{descripcion}</p>\n')
                if libro:
                    f.write(f'  <p><em>{categoria}</em> aparecido en <em>{libro}</em> ({autor}).</p>\n')
                elif saga:
                    f.write(f'  <p><em>{categoria}</em> de la saga <em>{saga}</em> ({autor}).</p>\n')
                else:
                    f.write(f'  <p><em>{categoria}</em> creado por {autor}.</p>\n')
                f.write(f'</idx:entry>\n')
            f.write('</body>\n</html>\n')

    # Copiar estilos y portada
    shutil.copyfile('styles/style.css', os.path.join(output_folder, 'style.css'))
    if os.path.exists('assets/cover.jpg'):
        shutil.copyfile('assets/cover.jpg', os.path.join(output_folder, 'cover.jpg'))

    # Página copyright
    with open(os.path.join(output_folder, 'copyright.xhtml'), 'w', encoding='utf-8') as f:
        f.write('''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<body>
<h1>Diccionario Literario</h1>
<p>© 2025 Carlos Bonadeo. Ningún derecho reservado.</p>
<p>Este diccionario fue creado con fines educativos y no comerciales.</p>
</body>
</html>
''')

    # Archivo OPF
    with open(os.path.join(output_folder, 'diccionario.opf'), 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write('<package version="2.0" xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId">\n')
        f.write('  <metadata>\n')
        f.write('    <dc:title>Diccionario Literario</dc:title>\n')
        f.write('    <dc:language>es</dc:language>\n')
        f.write('    <dc:creator>Carlos Bonadeo</dc:creator>\n')
        f.write('    <x-metadata>\n')
        f.write('      <DictionaryInLanguage>es</DictionaryInLanguage>\n')
        f.write('      <DictionaryOutLanguage>es</DictionaryOutLanguage>\n')
        f.write('    </x-metadata>\n')
        f.write('  </metadata>\n')
        f.write('  <manifest>\n')
        f.write('    <item id="style" href="style.css" media-type="text/css"/>\n')
        f.write('    <item id="cover" href="cover.jpg" media-type="image/jpeg"/>\n')
        f.write('    <item id="copyright" href="copyright.xhtml" media-type="application/xhtml+xml"/>\n')
        for filename in xhtml_files:
            f.write(f'    <item id="{filename}" href="{filename}" media-type="application/xhtml+xml"/>\n')
        f.write('  </manifest>\n')
        f.write('  <spine>\n')
        f.write('    <itemref idref="copyright"/>\n')
        for filename in xhtml_files:
            f.write(f'    <itemref idref="{filename}"/>\n')
        f.write('  </spine>\n')
        f.write('</package>\n')

    # Ahora, crear el EPUB (zip con estructura especial)
    crear_epub()

def crear_epub():
    # Ruta de salida EPUB
    epub_path = epub_filename

    # El archivo mimetype debe ser el primer archivo y sin compresión
    mimetype_path = os.path.join(output_folder, 'mimetype')
    with open(mimetype_path, 'w', encoding='utf-8') as f:
        f.write('application/epub+zip')

    # Crear archivo ZIP con extensión epub
    with zipfile.ZipFile(epub_path, 'w', compression=zipfile.ZIP_DEFLATED) as epub:
        # Agregar mimetype primero sin compresión
        epub.write(mimetype_path, 'mimetype', compress_type=zipfile.ZIP_STORED)

        # Agregar resto de archivos
        for root, _, files in os.walk(output_folder):
            for file in files:
                if file == 'mimetype':
                    continue
                full_path = os.path.join(root, file)
                # La ruta dentro del epub debe ser relativa a output_folder
                arcname = os.path.relpath(full_path, output_folder)
                epub.write(full_path, arcname)

    print(f"EPUB creado en: {epub_path}")

if __name__ == '__main__':
    generar_diccionario()
