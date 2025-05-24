import os
import shutil

from csv_module import generate_csv
from dictionary_module import generate_dictionary
from json_module import generate_json
from stats_module import generate_stats

if __name__ == '__main__':
    output_folder = 'output'
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
        os.makedirs(output_folder, exist_ok=True)

    generate_stats()
    # generate_csv()
    # generate_json()
    generate_dictionary()