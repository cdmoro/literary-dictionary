import os
import unicodedata
import shutil
import zipfile
from collections import defaultdict
from dotenv import load_dotenv

from utils import get_entries
from copyright import get_copyright_html  

output_folder = 'output/dictionary_files'
epub_path = f'output/Bonadeo, Carlos - Diccionario Literario (v{os.getenv('DICT_VERSION')}).epub'

def normalize_character(letra):
    return unicodedata.normalize('NFD', letra).encode('ascii', 'ignore').decode('utf-8').upper()

def generate_dictionary():
    load_dotenv()

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder, exist_ok=True)

    entries = get_entries()

    entradas_por_letra = defaultdict(list)
    for entry in entries:
        headword = entry['headword']
        firstLetter = normalize_character(headword[0])
        if firstLetter.isalpha():
            entradas_por_letra[firstLetter].append(entry)
        else:
            entradas_por_letra['Otros'].append(entry)

    xhtml_files = []
    for firstLetter, entradas in sorted(entradas_por_letra.items()):
        filename = f"{firstLetter}.xhtml"
        xhtml_files.append(filename)
        with open(os.path.join(output_folder, filename), 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            f.write('<!DOCTYPE html>\n')
            f.write('''<html 
    xmlns:math="http://exslt.org/math"
    xmlns:svg="http://www.w3.org/2000/svg"
    xmlns:tl="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"
    xmlns:saxon="http://saxon.sf.net/"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:cx="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:mbp="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"
    xmlns:mmc="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"
    xmlns:idx="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"
>\n''')
            f.write('<head>\n')
            f.write('  <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>\n')
            f.write('  <link rel="stylesheet" type="text/css" href="style.css"/>\n')
            f.write(f'  <title>{firstLetter}</title>\n')
            f.write('</head>\n')
            f.write('<body>\n')
            f.write('  <mbp:frameset>\n')

            for entry in entradas:
                headword = entry['headword']
                descripcion = entry['description']
                abbrev = entry.get('abbrev')
                autor = entry.get('author')
                libro = entry.get('book')
                saga = entry.get('saga')

                f.write('    <idx:entry name="default" scriptable="yes" spell="yes">\n')
                f.write('      <dt>\n')
                f.write(f'        <idx:orth>{headword}')

                aliases = entry.get('alias', [])
                if aliases:
                    f.write('\n          <idx:infl>\n')
                    for alt in aliases:
                        f.write(f'            <idx:iform value="{alt}"/>\n')
                    f.write('          </idx:infl>\n')
                    f.write('        ')
                
                f.write('</idx:orth>\n')
                f.write('      </dt>\n')
                f.write('      <dd>\n')
                
                # if aliases:
                #     f.write(f'<div><strong>Alias:</strong> <em>{", ".join(aliases)}</em></div>\n')

                f.write(f'        <div>')
                if (abbrev):
                    f.write(f'<em>({abbrev})</em> ')
                f.write(f'{descripcion}</div>\n')
                f.write('        <div>')
                if libro:
                    f.write(f'Aparece en <em>{libro}</em> de {autor}.')
                elif saga:
                    f.write(f'Pertenece al universo de <em>{saga}</em> creado por {autor}.')
                else:
                    f.write(f'Figura en la obra de {autor}.')
                f.write('</div>\n')
                
                f.write('      </dd>\n')
                f.write('    </idx:entry>\n')
                f.write('    <hr/>\n\n')

            f.write('  </mbp:frameset>\n')
            f.write('</body>\n')
            f.write('</html>')

    # Copiar estilos y portada
    shutil.copyfile('styles/style.css', os.path.join(output_folder, 'style.css'))
    shutil.copyfile('assets/cover.jpg', os.path.join(output_folder, 'cover.jpg'))

    with open(os.path.join(output_folder, 'Cover.xhtml'), 'w', encoding='utf-8') as f:
        f.write('''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<body>
    <svg viewBox="0 0 600 900" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="100%" preserveAspectRatio="xMidYMid meet" height="100%">
        <image xlink:href="cover.jpg" width="600" height="900"/>
    </svg>
</body>
</html>''')

    # Página copyright
    with open(os.path.join(output_folder, 'Copyright.xhtml'), 'w', encoding='utf-8') as f:
        f.write(get_copyright_html(entries))

    # Abreviaturas
    with open(os.path.join(output_folder, 'Abbreviations.xhtml'), 'w', encoding='utf-8') as f:
        f.write('''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<body>
    <h2>Guía de abreviaturas</h2>
    <div><em>(per.)</em> PersonajePersonajes principales, secundarios, etc.</div>  
    <div><em>(lugar)</em> Lugares importantes para la historia.</div>
    <div><em>(obj.)</em> Objetos especiales que se mencionen en el libro.</div>
    <div><em>(concepto)</em> Concepto particulares.</div>
    <div><em>(evento)</em> Eventos relevantes para la historia.</div>
    <div><em>(criatura)</em> Animales reales o mitológicos, tribus, etc.</div>
    <div><em>(inst.)</em> Parecido a <em>lugar</em> pero más específico.</div>
    <div><em>(hechizo)</em> Ideal para las novelas de fantasía.</div>
    <div><em>(idioma)</em> Por si se menciona algún lenguaje ficticio.</div>
    <div><em>(cita)</em> Citas que tienen algún significado especial para la historia.</div>
</body>
</html>
''')

    # Archivo OPF
    with open(os.path.join(output_folder, 'Dictionary.opf'), 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write('<package version="2.0" xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId">\n')
        f.write('  <metadata>\n')
        f.write('    <dc:title>Diccionario Literario</dc:title>\n')
        f.write('    <dc:language>es</dc:language>\n')
        f.write('    <dc:creator>Carlos Bonadeo</dc:creator>\n')
        f.write('    <x-metadata>\n')
        f.write('      <DictionaryInLanguage>es</DictionaryInLanguage>\n')
        f.write('      <DictionaryOutLanguage>es</DictionaryOutLanguage>\n')
        f.write('      <DefaultLookupIndex>headword</DefaultLookupIndex>\n')
        f.write('    </x-metadata>\n')
        f.write('  </metadata>\n')
        f.write('  <manifest>\n')
        f.write('    <item id="style" href="style.css" media-type="text/css"/>\n')
        f.write('    <item id="cover" href="Cover.xhtml" media-type="application/xhtml+xml"/>\n')
        f.write('    <item id="copyright" href="Copyright.xhtml" media-type="application/xhtml+xml"/>\n')
        f.write('    <item id="abbreviations" href="Abbreviations.xhtml" media-type="application/xhtml+xml"/>\n')
        for filename in xhtml_files:
            f.write(f'    <item id="{filename}" href="{filename}" media-type="application/xhtml+xml"/>\n')
        f.write('  </manifest>\n')
        f.write('  <spine>\n')
        f.write('    <itemref idref="cover"/>\n')
        f.write('    <itemref idref="copyright"/>\n')
        f.write('    <itemref idref="abbreviations"/>\n')
        for filename in xhtml_files:
            f.write(f'    <itemref idref="{filename}"/>\n')
        f.write('  </spine>\n')
        f.write('</package>\n')

    crear_epub()

def crear_epub():
    mimetype_path = os.path.join(output_folder, 'mimetype')
    with open(mimetype_path, 'w', encoding='utf-8') as f:
        f.write('application/epub+zip')

    with zipfile.ZipFile(epub_path, 'w', compression=zipfile.ZIP_DEFLATED) as epub:
        epub.write(mimetype_path, 'mimetype', compress_type=zipfile.ZIP_STORED)

        for root, _, files in os.walk(output_folder):
            for file in files:
                if file == 'mimetype':
                    continue
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, output_folder)
                epub.write(full_path, arcname)

    print(f"EPUB creado en: {epub_path}")
