import glob
import os
import shutil
import argparse

from src.db import get_connection

from src.modules.main_module import generate_dictionary
from src.utils import get_translations


def get_lang_from_filename(filename):
    base = os.path.basename(filename)
    return base.split(".")[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--commercial", action="store_true", help="Commercial build")

    args = parser.parse_args()

    base_folder = "output_commercial" if args.commercial else "output"

    db_files = glob.glob("dictionary/dictionary.*.db")

    if os.path.exists(base_folder):
        shutil.rmtree(base_folder)

    for db_path in db_files:
        conn = get_connection(db_path)
        lang = get_lang_from_filename(db_path)
        strings = get_translations(lang)

        generate_dictionary(base_folder, conn, lang, strings, args)
        conn.close()


if __name__ == "__main__":
    main()
