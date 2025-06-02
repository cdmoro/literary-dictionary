import os
import shutil
import zipfile
from collections import defaultdict
from dotenv import load_dotenv

from src.utils import get_entries, normalize_character
from src.pages.cover import get_cover_page
from src.pages.copyright import get_copyright_page  
from src.pages.abbreviations import get_abbreviation_page
from src.pages.contents import get_contents_page
from src.pages.letter import get_letter_page
from src.modules.cross_reference_module import build_cross_references

load_dotenv()

def generate_dictionary(conn, lang, strings):
    print(f'\nGenerating dictionary ({lang.upper()})...')

    cur = conn.cursor()
    output_folder = f'output/dictionary_files_{lang}'

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder, exist_ok=True)

    entries = get_entries(conn)

    entries_by_letter = defaultdict(list)
    for entry in entries:
        headword = entry['headword']
        firstLetter = normalize_character(headword[0])
        if firstLetter.isalpha():
            entries_by_letter[firstLetter].append(entry)
        else:
            entries_by_letter['Other'].append(entry)

    cross_references = build_cross_references(entries)

    xhtml_files = []

    for letter, group in sorted(entries_by_letter.items(), key=lambda x: (x[0] == "Other", x[0])):
        filename = f"{letter}.xhtml"
        xhtml_files.append(filename)

        with open(os.path.join(output_folder, filename), 'w', encoding='utf-8') as f:
            f.write(get_letter_page(letter, group, strings, cross_references))

    with open(os.path.join(output_folder, 'Cover.xhtml'), 'w', encoding='utf-8') as f:
        f.write(get_cover_page())

    with open(os.path.join(output_folder, 'Copyright.xhtml'), 'w', encoding='utf-8') as f:
        f.write(get_copyright_page(strings, entries))

    with open(os.path.join(output_folder, 'Contents.xhtml'), 'w', encoding='utf-8') as f:
        f.write(get_contents_page(strings))

    with open(os.path.join(output_folder, 'Abbreviations.xhtml'), 'w', encoding='utf-8') as f:
        f.write(get_abbreviation_page(cur, strings))

    # OPF file
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

    # Copy static files
    shutil.copyfile('styles/style.css', os.path.join(output_folder, 'style.css'))
    shutil.copyfile(f'assets/cover_{lang}.jpg', os.path.join(output_folder, 'cover.jpg'))

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
