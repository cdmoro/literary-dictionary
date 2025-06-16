import glob
import os
import shutil

from src.db import get_connection

from src.modules.main_module import generate_dictionary
from src.utils import get_translations
from src.config import ARGS


def get_lang_from_filename(filename):
    base = os.path.basename(filename)
    return base.split(".")[1]


def main():
    base_folder = "output"

    if ARGS.epub:
        base_folder += "_epub"

    db_files = glob.glob("dictionary/dictionary.*.db")

    if os.path.exists(base_folder):
        shutil.rmtree(base_folder)

    for db_path in db_files:
        conn = get_connection(db_path)
        lang = get_lang_from_filename(db_path)
        strings = get_translations(lang)

        generate_dictionary(base_folder, conn, lang, strings)
        conn.close()


if __name__ == "__main__":
    main()
