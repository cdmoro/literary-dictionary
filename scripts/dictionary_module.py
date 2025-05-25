import os
import unicodedata
import shutil
import zipfile
from collections import defaultdict
from dotenv import load_dotenv

from utils import get_entries
from copyright import get_copyright_html  

load_dotenv()

def normalize_character(letra):
    return unicodedata.normalize('NFD', letra).encode('ascii', 'ignore').decode('utf-8').upper()

def generate_dictionary(lang, strings):
    print(f'\nGenerating dictionary ({lang.upper()})...')

    output_folder = f'output/dictionary_files_{lang}'

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder, exist_ok=True)

    entries = get_entries(lang)

    cross_reference_data = {}
    for entry in entries:
        if "id" in entry and "headword" in entry:
            filename = f'{normalize_character(entry['headword'].strip()[0].upper())}.xhtml'
            cross_reference_data[entry["id"]] = (entry["headword"], filename)

    # Copyright
    with open(os.path.join(output_folder, 'Copyright.xhtml'), 'w', encoding='utf-8') as f:
        f.write(get_copyright_html(strings, entries))

    entradas_por_letra = defaultdict(list)
    for entry in entries:
        headword = entry['headword']
        firstLetter = normalize_character(headword[0])
        if firstLetter.isalpha():
            entradas_por_letra[firstLetter].append(entry)
        else:
            entradas_por_letra['Otros'].append(entry)

    xhtml_files = []
    for firstLetter, entries in sorted(entradas_por_letra.items()):
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
            f.write(f'<h1>{firstLetter}</h1>\n')
            f.write('  <mbp:frameset>\n')

            for entry in entries:
                id = entry["id"]
                headword = entry['headword']
                displayValue = entry.get('displayValue') or headword
                description = entry['description']
                abbrev = entry.get('abbrev')
                author = entry.get('author')
                book = entry.get('book')
                saga = entry.get('saga')
                seeAlso = entry.get('seeAlso')

                f.write(f'    <idx:entry name="default" scriptable="yes" spell="yes" id="{id}">\n')
                f.write(f'      <a id="{id}"></a>\n')
                f.write('      <dt>\n')
                f.write(f'        <idx:orth value="{headword}">{displayValue}</idx:orth>\n')

                aliases = entry.get('alias', [])
                if aliases:
                    for alias in aliases:
                        f.write(f'        <idx:orth value="{alias}" />\n')
                
                f.write('      </dt>\n')
                f.write('      <dd>\n')

                f.write(f'        <div>')
                if (abbrev):
                    f.write(f'<em>{abbrev}</em> ')
                f.write(f'{description}</div>\n')
                f.write('        <br />\n')
                f.write('        <div>')
                if book:
                    f.write(strings["book_origin"].format(book=book, author=author))
                elif saga:
                    f.write(strings["saga_origin"].format(saga=saga, author=author))
                else:
                    f.write(strings["author_origin"].format(author=author))
                f.write('</div>\n')

                if seeAlso:
                    f.write('        <br />\n')
                    f.write('        <div>\n')
                    f.write(f'          <em>{strings["see_also"]}:</em> \n')
                    
                    seeAlso = list(dict.fromkeys(seeAlso))
                    seeAlso = sorted(seeAlso, key=lambda id: cross_reference_data[id][0].lower() if id in cross_reference_data else '')
                    seeAlsoLinks = []
                    for idr in seeAlso:
                        if not idr in cross_reference_data:
                            print(f'  - ⏭️  ID {id}: Cross Reference not found ({idr}), skipped')
                            continue
                        seeAlsoLinks.append(f'          <a href="{cross_reference_data[idr][1]}#{idr}">{cross_reference_data[idr][0]}</a>')
                    f.write(', \n'.join(seeAlsoLinks))
                    f.write('\n        </div>\n')
                
                f.write('      </dd>\n')
                f.write('    </idx:entry>\n')
                f.write('    <hr/>\n\n')

            f.write('  </mbp:frameset>\n')
            f.write('</body>\n')
            f.write('</html>')

    # Copiar estilos y portada
    shutil.copyfile('styles/style.css', os.path.join(output_folder, 'style.css'))
    shutil.copyfile(f'assets/cover_{lang}.jpg', os.path.join(output_folder, 'cover.jpg'))

    with open(os.path.join(output_folder, 'Cover.xhtml'), 'w', encoding='utf-8') as f:
        f.write('''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<body>
    <svg viewBox="0 0 600 900" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="100%" preserveAspectRatio="xMidYMid meet" height="100%">
        <image xlink:href="cover.jpg" width="600" height="900"/>
    </svg>
</body>
</html>''')

    # Index
    with open(os.path.join(output_folder, 'Contents.xhtml'), 'w', encoding='utf-8') as f:
        f.write(f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body>
    <h1>{strings["contents"]}</h1>
    <nav epub:type="toc" class="toc">
        <ol>
            <li><a href="Cover.xhtml">{strings["cover"]}</a></li>
            <li><a href="Copyright.xhtml">{strings["about"]}</a></li>
            <li><a href="A.xhtml">{strings["definitions"]}</a></li>
            <li><a href="Abbreviations.xhtml">{strings["abbr_guide"]}</a></li>
        </ol>
    </nav>
</body>
</html>
''')

    # Abreviaturas
    with open(os.path.join(output_folder, 'Abbreviations.xhtml'), 'w', encoding='utf-8') as f:
        f.write('''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body>
    <h1>{abbr_guide}</h1>
    <div><em>{characters_abbr}</em> — {characters_abbr_desc}</div>  
    <div><em>{places_abbr}</em> — {places_abbr_desc}</div>
    <div><em>{objects_abbr}</em> — {objects_abbr_desc}</div>
    <div><em>{concepts_abbr}</em> — {concepts_abbr_desc}</div>
    <div><em>{events_abbr}</em> — {events_abbr_desc}</div>
    <div><em>{creatures_abbr}</em> — {creatures_abbr_desc}</div>
    <div><em>{institutions_abbr}</em> — {institutions_abbr_desc}</div>
    <div><em>{spells_abbr}</em> — {spells_abbr_desc}</div>
    <div><em>{languages_abbr}</em> — {languages_abbr_desc}</div>
    <div><em>{quotes_abbr}</em> — {quotes_abbr_desc}</div>
</body>
</html>
'''.format(**strings))

    # Archivo OPF
    with open(os.path.join(output_folder, 'Dictionary.opf'), 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write('<package version="2.0" xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId">\n')
        f.write('  <metadata>\n')
        f.write(f'    <dc:title>{strings["title"]} ({lang.upper()})</dc:title>\n')
        f.write(f'    <dc:language>{lang}</dc:language>\n')
        f.write('    <dc:creator>Carlos Bonadeo</dc:creator>\n')
        f.write('    <x-metadata>\n')
        f.write(f'      <DictionaryInLanguage>{lang}</DictionaryInLanguage>\n')
        f.write(f'      <DictionaryOutLanguage>{lang}</DictionaryOutLanguage>\n')
        f.write('      <DefaultLookupIndex>headword</DefaultLookupIndex>\n')
        f.write('    </x-metadata>\n')
        f.write('    <meta name="cover" content="cover-image"/>')
        f.write('  </metadata>\n')
        f.write('  <manifest>\n')
        f.write('    <item id="style" href="style.css" media-type="text/css"/>\n')
        f.write('    <item id="cover-image" href="cover.jpg" media-type="image/jpeg"/>\n')
        f.write('    <item id="cover" href="Cover.xhtml" media-type="application/xhtml+xml"/>\n')
        f.write('    <item id="copyright" href="Copyright.xhtml" media-type="application/xhtml+xml"/>\n')
        f.write('    <item id="index" properties="nav" href="Contents.xhtml" media-type="application/xhtml+xml"/>\n')
        
        for filename in xhtml_files:
            f.write(f'    <item id="{filename}" href="{filename}" media-type="application/xhtml+xml"/>\n')
        
        f.write('    <item id="abbreviations" href="Abbreviations.xhtml" media-type="application/xhtml+xml"/>\n')
        f.write('  </manifest>\n')
        f.write('  <spine>\n')
        f.write('    <itemref idref="cover"/>\n')
        f.write('    <itemref idref="copyright"/>\n')
        f.write('    <itemref idref="index"/>\n')
        
        for filename in xhtml_files:
            f.write(f'    <itemref idref="{filename}"/>\n')
        
        f.write('    <itemref idref="abbreviations"/>\n')
        f.write('  </spine>\n')
        f.write('  <guide>\n')
        f.write('    <reference type="cover" title="Cover" href="Cover.xhtml"/>\n')
        f.write('    <reference type="toc" title="Table of Contents" href="Contents.xhtml"/>\n')
        f.write('    <reference type="text" title="Start" href="Copyright.xhtml"/>\n')
        f.write('  </guide>\n')
        f.write('</package>\n')

    print(f"✅ Diccionary files created successfully")
    crear_epub(lang, strings)

def crear_epub(lang, strings):
    output_folder = f'output/dictionary_files_{lang}'
    epub_path = f'output/{strings["file_name"].format(lang=lang.upper(), version=os.getenv('DICT_VERSION'))}.epub'
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

    print(f"✅ EPUB created successfully")
