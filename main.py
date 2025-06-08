import glob
import os
import shutil

from src.db import get_connection

# from csv_module import generate_csv
# from json_module import generate_json
from src.modules.main_module import generate_dictionary
from src.utils import get_translations


def get_lang_from_filename(filename):
    base = os.path.basename(filename)
    return base.split(".")[1]


def main():
    db_files = glob.glob("dictionary/dictionary.*.db")

    if os.path.exists("output"):
        shutil.rmtree("output")

    for db_path in db_files:
        conn = get_connection(db_path)
        lang = get_lang_from_filename(db_path)
        strings = get_translations(lang)

        # generate_csv(subdir.name, strings)
        # generate_json(subdir.name, strings)
        generate_dictionary(conn, lang, strings)
        conn.close()


if __name__ == "__main__":
    main()
