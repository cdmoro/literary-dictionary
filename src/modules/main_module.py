import os
import shutil
import zipfile

from dotenv import load_dotenv

from src.modules.books_module import create_books_files
from src.modules.dictionary_module import create_dictionary_files
from src.modules.sagas_module import create_sagas_files
from src.modules.authors_module import create_authors_files
from src.pages.abbreviations import get_abbreviation_page
from src.pages.container import get_container_page
from src.pages.toc import get_toc_page
from src.pages.copyright import get_copyright_page
from src.pages.cover import get_cover_page
from src.pages.ncx import get_ncx_page
from src.utils import uuid

load_dotenv()

media_type = {
    "css": "text/css",
    "jpg": "image/jpeg",
    "ncx": "application/x-dtbncx+xml",
    "xhtml": "application/xhtml+xml",
}
# encoding = 'utf-8'


def generate_dictionary(conn, lang, strings):
    print(f"\nGenerating dictionary ({lang.upper()})...")

    cur = conn.cursor()
    output_folder = f"output/dictionary_files_{lang}"
    # Common files
    common_files = {
        "Cover.xhtml": get_cover_page(lang),
        "Copyright.xhtml": get_copyright_page(strings),
        "Abbreviations.xhtml": get_abbreviation_page(lang, cur, strings),
        "TOC.xhtml": get_toc_page(lang, strings),
    }
    manifest = [
        "Styles/style.css",
        "Assets/cover.jpg",
        "toc.ncx",
        "Cover.xhtml",
        "Copyright.xhtml",
        "TOC.xhtml",
        "Abbreviations.xhtml",
    ]
    spine = [v for v in manifest if v.endswith(".xhtml")]

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder, exist_ok=True)

    meta_inf_folder = os.path.join(output_folder, "META-INF")
    assets_folder = os.path.join(output_folder, "Assets")
    styles_folder = os.path.join(output_folder, "Styles")

    os.makedirs(meta_inf_folder)
    os.makedirs(assets_folder)
    os.makedirs(styles_folder)

    dictionary_xhtml_files = create_dictionary_files(output_folder, lang, strings, conn)
    book_xhtml_files = create_books_files(output_folder, lang, strings, conn)
    sagas_xhtml_files = create_sagas_files(output_folder, lang, strings, conn)
    authors_xhtml_files = create_authors_files(output_folder, lang, strings, conn)

    # Container
    with open(
        os.path.join(meta_inf_folder, "container.xml"), "w", encoding="utf-8"
    ) as f:
        f.write(get_container_page())

    for file, content in common_files.items():
        with open(os.path.join(output_folder, file), "w", encoding="utf-8") as f:
            f.write(content)

    # NCX file
    ncx_structure = {
        "Dictionary": dictionary_xhtml_files,
        "Books": book_xhtml_files,
        "Sagas": sagas_xhtml_files,
        "Authors": authors_xhtml_files,
    }
    with open(os.path.join(output_folder, "toc.ncx"), "w", encoding="utf-8") as f:
        f.write(get_ncx_page(lang, ncx_structure, strings))

    # OPF file
    with open(os.path.join(output_folder, "content.opf"), "w", encoding="utf-8") as f:
        f.write(
            f"""<?xml version="1.0" encoding="utf-8"?>
        
<package
  version="2.0"
  xmlns="http://www.idpf.org/2007/opf"
  unique-identifier="BookId"
>
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
    <dc:title>{strings["title"]} ({lang.upper()})</dc:title>
    <dc:language>{lang}</dc:language>
    <dc:creator>Carlos Bonadeo</dc:creator>
    <dc:identifier id="BookId" opf:scheme="UUID">urn:uuid:{uuid[lang]}</dc:identifier>
    <x-metadata>
      <DictionaryInLanguage>{lang}</DictionaryInLanguage>
      <DictionaryOutLanguage>{lang}</DictionaryOutLanguage>
      <DefaultLookupIndex>headword</DefaultLookupIndex>
    </x-metadata>
    <meta name="cover" content="cover-image"/>
  </metadata>
  <manifest>\n"""
        )

        for file in manifest:
            f.write(
                f'    <item id="{file.replace("/", "_")}" href="{file}" media-type="{media_type[file.split(".")[1]]}"/>\n'
            )

        f.write(
            '    <item id="dictionary" href="Dictionary.xhtml" media-type="application/xhtml+xml"/>\n'
        )
        f.write(
            '    <item id="dictionary-toc" href="Dictionary_TOC.xhtml" media-type="application/xhtml+xml"/>\n'
        )
        for filename in dictionary_xhtml_files:
            f.write(
                f'    <item id="{filename}" href="Dictionary/{filename}.xhtml" media-type="application/xhtml+xml"/>\n'
            )

        f.write(
            '    <item id="books" href="Books.xhtml" media-type="application/xhtml+xml"/>\n'
        )
        f.write(
            '    <item id="books-toc" href="Books_TOC.xhtml" media-type="application/xhtml+xml"/>\n'
        )
        for filename in book_xhtml_files:
            f.write(
                f'    <item id="{filename}" href="Books/{filename}.xhtml" media-type="application/xhtml+xml"/>\n'
            )

        f.write(
            '    <item id="sagas" href="Sagas.xhtml" media-type="application/xhtml+xml"/>\n'
        )
        f.write(
            '    <item id="sagas-toc" href="Sagas_TOC.xhtml" media-type="application/xhtml+xml"/>\n'
        )
        for filename in sagas_xhtml_files:
            f.write(
                f'    <item id="{filename}" href="Sagas/{filename}.xhtml" media-type="application/xhtml+xml"/>\n'
            )

        f.write(
            '    <item id="authors" href="Authors.xhtml" media-type="application/xhtml+xml"/>\n'
        )
        f.write(
            '    <item id="authors-toc" href="Authors_TOC.xhtml" media-type="application/xhtml+xml"/>\n'
        )
        for filename in authors_xhtml_files:
            f.write(
                f'    <item id="{filename}" href="Authors/{filename}.xhtml" media-type="application/xhtml+xml"/>\n'
            )
        f.write("  </manifest>\n")

        f.write('  <spine toc="ncx">\n')

        for idref in spine:
            f.write(f'    <itemref idref="{idref.replace("/", "_")}"/>\n')

        f.write('    <itemref idref="dictionary"/>\n')
        f.write('    <itemref idref="dictionary-toc"/>\n')
        for filename in dictionary_xhtml_files:
            f.write(f'    <itemref idref="{filename}"/>\n')

        f.write('    <itemref idref="books"/>\n')
        f.write('    <itemref idref="books-toc"/>\n')
        for filename in book_xhtml_files:
            f.write(f'    <itemref idref="{filename}"/>\n')

        f.write('    <itemref idref="sagas"/>\n')
        f.write('    <itemref idref="sagas-toc"/>\n')
        for filename in sagas_xhtml_files:
            f.write(f'    <itemref idref="{filename}"/>\n')

        f.write('    <itemref idref="authors"/>\n')
        f.write('    <itemref idref="authors-toc"/>\n')
        for filename in authors_xhtml_files:
            f.write(f'    <itemref idref="{filename}"/>\n')

        f.write("  </spine>\n")
        f.write("  <guide>\n")
        f.write('    <reference type="cover" title="Cover" href="Cover.xhtml"/>\n')
        f.write(
            '    <reference type="toc" title="Table of Contents" href="TOC.xhtml"/>\n'
        )
        f.write('    <reference type="text" title="Start" href="Copyright.xhtml"/>\n')
        f.write("  </guide>\n")
        f.write("</package>\n")

    # Static files
    shutil.copyfile("styles/style.css", os.path.join(styles_folder, "style.css"))
    shutil.copyfile(
        f"assets/cover_{lang}.jpg", os.path.join(assets_folder, "cover.jpg")
    )
    shutil.copyfile(
        "assets/cc_banner.png", os.path.join(assets_folder, "cc_banner.png")
    )

    print(f"✅ Diccionary files created successfully")
    create_epub(lang, strings["file_name"])


def create_epub(lang, file_name):
    output_folder = f"output/dictionary_files_{lang}"
    epub_path = f'output/{file_name.format(ebook_author=os.getenv("AUTHOR"), lang=lang.upper(), version=os.getenv('DICT_VERSION'))}.epub'
    mimetype_path = os.path.join(output_folder, "mimetype")
    with open(mimetype_path, "w", encoding="utf-8") as f:
        f.write("application/epub+zip")

    with zipfile.ZipFile(epub_path, "w", compression=zipfile.ZIP_DEFLATED) as epub:
        epub.write(mimetype_path, "mimetype", compress_type=zipfile.ZIP_STORED)

        for root, _, files in os.walk(output_folder):
            for file in files:
                if file == "mimetype":
                    continue
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, output_folder)
                epub.write(full_path, arcname)

    print(f"✅ EPUB created successfully")
