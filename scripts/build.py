import os
import shutil
from pathlib import Path

from utils import get_translations
from stats_module import generate_stats
from csv_module import generate_csv
from dictionary_module import generate_dictionary
from json_module import generate_json

if __name__ == '__main__':
    output_folder = 'output'
    base_path = Path("dictionary")

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
        os.makedirs(output_folder, exist_ok=True)

    generate_stats()

    for subdir in base_path.iterdir():
        strings = get_translations(subdir.name)
        # generate_csv(subdir.name, strings)
        # generate_json(subdir.name, strings)
        generate_dictionary(subdir.name, strings)