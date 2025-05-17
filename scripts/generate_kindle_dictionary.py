import os
import unicodedata
import shutil
from collections import defaultdict
from utils import get_entries  # Asegúrate de que esta función esté definida correctamente

output_folder = 'output/kindle'

def normalizar_letra(letra):
    return unicodedata.normalize('NFD', letra).encode('ascii', 'ignore').decode('utf-8').upper()

def generar_diccionario():
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    # Crear directorio de salida
    
    os.makedirs(output_folder, exist_ok=True)

    # Obtener entradas
    personajes = get_entries()

    # Agrupar entradas por letra inicial
    entradas_por_letra = defaultdict(list)
    for personaje in personajes:
        palabra = personaje['word']
        letra = normalizar_letra(palabra[0])
        if letra.isalpha():
            entradas_por_letra[letra].append(personaje)
        else:
            entradas_por_letra['Otros'].append(personaje)

    # Generar archivos XHTML
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
            f.write('</head>\n')
            f.write('<body>\n')
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
                
                if personaje.get('alias'):
                    f.write(f'  <p><strong>Alias:</strong> <em>{', '.join(personaje.get('alias', []))}</em></p>\n')
                f.write(f'  <p>{descripcion}</p>\n')
                if libro:
                    f.write(f'  <p><em>{categoria}</em> aparecido en <em>{libro}</em> ({autor}).</p>\n')
                elif saga:
                    f.write(f'  <p><em>{categoria}</em> de la saga <em>{saga}</em> ({autor}).</p>\n')
                else:
                    f.write(f'  <p><em>{categoria}</em> creado por {autor}.</p>\n')
                f.write(f'</idx:entry>\n')
            f.write('</body>\n')
            f.write('</html>\n')

    # Copiar hoja de estilos
    with open('styles/style.css', 'r', encoding='utf-8') as f_src, open('output/kindle/style.css', 'w', encoding='utf-8') as f_dst:
        f_dst.write(f_src.read())

    # Copiar imagen de portada
    if os.path.exists('assets/cover.jpg'):
        with open('assets/cover.jpg', 'rb') as f_src, open('output/kindle/cover.jpg', 'wb') as f_dst:
            f_dst.write(f_src.read())

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

    # Generar archivo OPF
    with open('output/kindle/diccionario.opf', 'w', encoding='utf-8') as f:
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
        for filename in xhtml_files:
            f.write(f'    <item id="{filename}" href="{filename}" media-type="application/xhtml+xml"/>\n')
        f.write('    <item id="cover" href="cover.jpg" media-type="image/jpeg"/>\n')
        f.write('.   <item id="copyright" href="copyright.xhtml" media-type="application/xhtml+xml"/>\n')
        f.write('  </manifest>\n')
        f.write('  <spine>\n')
        f.write('    <itemref idref="copyright"/>')
        for filename in xhtml_files:
            f.write(f'    <itemref idref="{filename}"/>\n')
        f.write('  </spine>\n')
        f.write('</package>\n')

if __name__ == '__main__':
    generar_diccionario()
