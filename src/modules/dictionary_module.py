import os
import shutil
import zipfile
from collections import defaultdict
from dotenv import load_dotenv

from src.utils import normalize_character
from src.pages.container import get_container_page
from src.pages.cover import get_cover_page
from src.pages.copyright import get_copyright_page  
from src.pages.abbreviations import get_abbreviation_page
from src.pages.contents import get_contents_page
from src.pages.dictionary import get_dictionary_page
from src.pages.authors import get_authors_page
from src.pages.books import get_books_page
from src.pages.sagas import get_sagas_page
from src.pages.section import get_section_page
from src.pages.ncx import get_ncx_page

from src.modules.cross_reference_module import build_cross_references
from src.modules.books_module import get_books_by_letter, build_book_cross_references
from src.modules.sagas_module import get_sagas_by_letter, build_saga_cross_references
from src.modules.authors_module import get_authors_by_letter, build_author_cross_references
from src.modules.entries_module import get_entries

load_dotenv()

def generate_dictionary(conn, lang, strings):
    print(f'\nGenerating dictionary ({lang.upper()})...')

    cur = conn.cursor()
    output_folder = f'output/dictionary_files_{lang}'

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder, exist_ok=True)

    meta_inf_folder = os.path.join(output_folder, 'META-INF')
    dictionary_folder = os.path.join(output_folder, 'Dictionary')
    authors_folder = os.path.join(output_folder, 'Authors')
    books_folder = os.path.join(output_folder, 'Books')
    sagas_folder = os.path.join(output_folder, 'Sagas')
    assets_folder = os.path.join(output_folder, 'Assets')
    styles_folder = os.path.join(output_folder, 'Styles')

    os.makedirs(meta_inf_folder)
    os.makedirs(dictionary_folder)
    os.makedirs(authors_folder)
    os.makedirs(books_folder)
    os.makedirs(sagas_folder)
    os.makedirs(assets_folder)
    os.makedirs(styles_folder)

    entries = get_entries(conn)
    books_by_letter = get_books_by_letter(conn)
    sagas_by_letter = get_sagas_by_letter(conn)
    authors_by_letter = get_authors_by_letter(conn)
    
    books_cross_references = build_book_cross_references(conn)
    sagas_cross_references = build_saga_cross_references(conn)
    authors_cross_references = build_author_cross_references(conn)

    entries_by_letter = defaultdict(list)
    for entry in entries:
        headword = entry['headword']
        firstLetter = normalize_character(headword[0])
        if firstLetter.isalpha():
            entries_by_letter[firstLetter].append(entry)
        else:
            entries_by_letter['D_Other'].append(entry)

    cross_references = build_cross_references(entries)

    dictionary_xhtml_files = []
    book_xhtml_files = []
    sagas_xhtml_files = []
    authors_xhtml_files = []

    with open(os.path.join(meta_inf_folder, 'container.xml'), 'w', encoding='utf-8') as f:
        f.write(get_container_page('content.opf'))
    
    with open(os.path.join(output_folder, 'Cover.xhtml'), 'w', encoding='utf-8') as f:
        f.write(get_cover_page(lang))

    with open(os.path.join(output_folder, 'Copyright.xhtml'), 'w', encoding='utf-8') as f:
        f.write(get_copyright_page(strings, entries))

    with open(os.path.join(output_folder, 'TOC.xhtml'), 'w', encoding='utf-8') as f:
        f.write(get_contents_page(lang, strings))

    with open(os.path.join(output_folder, 'Abbreviations.xhtml'), 'w', encoding='utf-8') as f:
        f.write(get_abbreviation_page(lang, cur, strings))

    # Dictionary
    with open(os.path.join(output_folder, 'Dictionary.xhtml'), 'w', encoding='utf-8') as f:
        f.write(get_section_page(lang, strings["definitions"]))

    for letter, group in sorted(entries_by_letter.items(), key=lambda x: (x[0] == "Other", x[0])):
        filename = f"D_{letter}"
        dictionary_xhtml_files.append(filename)

        with open(os.path.join(dictionary_folder, f'{filename}.xhtml'), 'w', encoding='utf-8') as f:
            f.write(get_dictionary_page(lang, letter, group, strings, cross_references))

    # Books
    with open(os.path.join(output_folder, 'Books.xhtml'), 'w', encoding='utf-8') as f:
        f.write(get_section_page(lang, strings["books"]))

    for letter, group in sorted(books_by_letter.items(), key=lambda x: (x[0] == "Other", x[0])):
        filename = f"B_{letter}"
        book_xhtml_files.append(filename)

        with open(os.path.join(books_folder, f'{filename}.xhtml'), 'w', encoding='utf-8') as f:
            f.write(get_books_page(lang, letter, group, strings, books_cross_references))

    # Sagas
    with open(os.path.join(output_folder, 'Sagas.xhtml'), 'w', encoding='utf-8') as f:
        f.write(get_section_page(lang, strings["sagas"]))

    for letter, group in sorted(sagas_by_letter.items(), key=lambda x: (x[0] == "Other", x[0])):
        filename = f"S_{letter}"
        sagas_xhtml_files.append(filename)

        with open(os.path.join(sagas_folder, f'{filename}.xhtml'), 'w', encoding='utf-8') as f:
            f.write(get_sagas_page(lang, letter, group, strings, sagas_cross_references))

    # Authors
    with open(os.path.join(output_folder, 'Authors.xhtml'), 'w', encoding='utf-8') as f:
        f.write(get_section_page(lang, strings["authors"]))

    for letter, group in sorted(authors_by_letter.items(), key=lambda x: (x[0] == "Other", x[0])):
        filename = f"A_{letter}"
        authors_xhtml_files.append(filename)

        with open(os.path.join(authors_folder, f'{filename}.xhtml'), 'w', encoding='utf-8') as f:
            f.write(get_authors_page(lang, letter, group, strings, authors_cross_references))

    # NCX file
    ncx_structure = {
        "Dictionary": dictionary_xhtml_files,
        "Books": book_xhtml_files,
        "Authors": authors_xhtml_files,
        "Sagas": sagas_xhtml_files
    }
    with open(os.path.join(output_folder, 'toc.ncx'), 'w', encoding='utf-8') as f:
        f.write(get_ncx_page(lang, ncx_structure, strings))

    # OPF file
    with open(os.path.join(output_folder, 'content.opf'), 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write(f'''<package
  version="2.0"
  xmlns="http://www.idpf.org/2007/opf"
  unique-identifier="BookId"
>\n''')
        f.write('  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">\n')
        f.write(f'    <dc:title>{strings["title"]} ({lang.upper()})</dc:title>\n')
        f.write(f'    <dc:language>{lang}</dc:language>\n')
        f.write(f'    <dc:creator>Carlos Bonadeo</dc:creator>\n')
        f.write(f'    <dc:identifier id="BookId" opf:scheme="UUID">urn:uuid:a46ba639-014f-44de-a6af-de509e96798d</dc:identifier>\n')
        f.write('    <x-metadata>\n')
        f.write(f'      <DictionaryInLanguage>{lang}</DictionaryInLanguage>\n')
        f.write(f'      <DictionaryOutLanguage>{lang}</DictionaryOutLanguage>\n')
        f.write('      <DefaultLookupIndex>headword</DefaultLookupIndex>\n')
        f.write('    </x-metadata>\n')
        f.write('    <meta name="cover" content="cover-image"/>\n')
        f.write('  </metadata>\n')
        f.write('  <manifest>\n')
        f.write('    <item id="style" href="Styles/style.css" media-type="text/css"/>\n')
        f.write('    <item id="cover-image" href="Assets/cover.jpg" media-type="image/jpeg"/>\n')
        f.write('    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>\n')
        f.write('    <item id="cover" href="Cover.xhtml" media-type="application/xhtml+xml"/>\n')
        f.write('    <item id="copyright" href="Copyright.xhtml" media-type="application/xhtml+xml"/>\n')
        f.write('    <item id="toc" href="TOC.xhtml" media-type="application/xhtml+xml"/>\n')
        f.write('    <item id="abbreviations" href="Abbreviations.xhtml" media-type="application/xhtml+xml"/>\n')
        
        f.write('    <item id="dictionary" href="Dictionary.xhtml" media-type="application/xhtml+xml"/>\n')   
        for filename in dictionary_xhtml_files:
            f.write(f'    <item id="{filename}" href="Dictionary/{filename}.xhtml" media-type="application/xhtml+xml"/>\n')

        f.write('    <item id="books" href="Books.xhtml" media-type="application/xhtml+xml"/>\n')
        for filename in book_xhtml_files:
            f.write(f'    <item id="{filename}" href="Books/{filename}.xhtml" media-type="application/xhtml+xml"/>\n')

        f.write('    <item id="sagas" href="Sagas.xhtml" media-type="application/xhtml+xml"/>\n')
        for filename in sagas_xhtml_files:
            f.write(f'    <item id="{filename}" href="Sagas/{filename}.xhtml" media-type="application/xhtml+xml"/>\n')

        f.write('    <item id="authors" href="Authors.xhtml" media-type="application/xhtml+xml"/>\n')
        for filename in authors_xhtml_files:
            f.write(f'    <item id="{filename}" href="Authors/{filename}.xhtml" media-type="application/xhtml+xml"/>\n')
        f.write('  </manifest>\n')

        f.write('  <spine toc="ncx">\n')
        f.write('    <itemref idref="cover"/>\n')
        f.write('    <itemref idref="copyright"/>\n')
        f.write('    <itemref idref="toc"/>\n')
        f.write('    <itemref idref="abbreviations"/>\n')

        f.write('    <itemref idref="dictionary"/>\n')
        for filename in dictionary_xhtml_files:
            f.write(f'    <itemref idref="{filename}"/>\n')

        f.write('    <itemref idref="books"/>\n')
        for filename in book_xhtml_files:
            f.write(f'    <itemref idref="{filename}"/>\n')

        f.write('    <itemref idref="sagas"/>\n')
        for filename in sagas_xhtml_files:
            f.write(f'    <itemref idref="{filename}"/>\n')

        f.write('    <itemref idref="authors"/>\n')
        for filename in authors_xhtml_files:
            f.write(f'    <itemref idref="{filename}"/>\n')

        f.write('  </spine>\n')
        f.write('  <guide>\n')
        f.write('    <reference type="cover" title="Cover" href="Cover.xhtml"/>\n')
        f.write('    <reference type="toc" title="Table of Contents" href="TOC.xhtml"/>\n')
        f.write('    <reference type="text" title="Start" href="Copyright.xhtml"/>\n')
        f.write('  </guide>\n')
        f.write('</package>\n')

    # Copy static files
    shutil.copyfile('styles/style.css', os.path.join(styles_folder, 'style.css'))
    shutil.copyfile(f'assets/cover_{lang}.jpg', os.path.join(assets_folder, 'cover.jpg'))

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
