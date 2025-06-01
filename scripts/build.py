import glob
import os

from db import get_connection
from utils import get_translations
# from stats_module import generate_stats
# from csv_module import generate_csv
# from json_module import generate_json
from dictionary_module import generate_dictionary

def get_lang_from_filename(filename):
    base = os.path.basename(filename)
    return base.split(".")[1]

def main():
    db_files = glob.glob("dictionary/dictionary.*.db")

    # generate_stats()

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
