import glob
import os
import sqlite3

from db import get_connection
from utils import get_translations
from dictionary_module import generate_dictionary

def get_lang_from_filename(filename):
    base = os.path.basename(filename)
    return base.split(".")[1]

def main():
    db_files = glob.glob("dictionary/dictionary.*.db")

    for db_path in db_files:
        conn = get_connection(db_path)
        lang = get_lang_from_filename(db_path)
        strings = get_translations(lang)

        generate_dictionary(conn, lang, strings)
        conn.close()

if __name__ == "__main__":
    main()
