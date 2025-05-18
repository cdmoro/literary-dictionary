from csv_module import generate_csv
from epub_dictionary_module import generate_dictionary
from json_module import generate_json
from stats_module import generate_stats

if __name__ == '__main__':
    generate_stats()
    generate_csv()
    generate_json()
    generate_dictionary()