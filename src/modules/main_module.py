import os
import shutil
import zipfile

from dotenv import load_dotenv

from src.pages.opf import get_opf_file
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
from src.constants import encoding

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
        os.path.join(meta_inf_folder, "container.xml"), "w", encoding=encoding
    ) as f:
        f.write(get_container_page())

    # NCX file
    ncx_structure = {
        "Dictionary": dictionary_xhtml_files,
        "Books": book_xhtml_files,
        "Sagas": sagas_xhtml_files,
        "Authors": authors_xhtml_files,
    }
    with open(os.path.join(output_folder, "toc.ncx"), "w", encoding=encoding) as f:
        f.write(get_ncx_page(lang, ncx_structure, strings))

    # Common files
    common_files = {
        "Cover.xhtml": get_cover_page(lang),
        "Copyright.xhtml": get_copyright_page(strings),
        "Abbreviations.xhtml": get_abbreviation_page(lang, cur, strings),
        "TOC.xhtml": get_toc_page(lang, strings, ncx_structure),
    }

    for file, content in common_files.items():
        with open(os.path.join(output_folder, file), "w", encoding=encoding) as f:
            f.write(content)

    # OPF file
    with open(os.path.join(output_folder, "content.opf"), "w", encoding=encoding) as f:
        f.write(get_opf_file(lang, strings, ncx_structure))

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
    with open(mimetype_path, "w", encoding=encoding) as f:
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
