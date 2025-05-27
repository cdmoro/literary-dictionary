import os
import yaml

from utils import CATEGORIES

ROOT_FOLDER = "dictionary/es"

def find_max_id():
    max_id = 0
    for root, _, files in os.walk(ROOT_FOLDER):
        for filename in files:
            if filename.endswith((".yaml")):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                    if not data:
                        continue
                except Exception:
                    continue

                for field in CATEGORIES:
                    if field in data:
                        for entry in data[field]:
                            if isinstance(entry, dict) and "id" in entry:
                                max_id = max(max_id, entry["id"])

    print(f'Next ID number: {max_id + 1}')
    return max_id

if __name__ == '__main__':
    find_max_id()