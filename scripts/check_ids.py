import os
import re
import yaml

def map_files_by_prefix(directory):
    files = os.listdir(directory)
    mapping = {}
    for f in files:
        if os.path.isfile(os.path.join(directory, f)):
            match = re.match(r'^(\d+)-', f)
            if match:
                prefix = match.group(1)
                mapping[prefix] = f
    return mapping

def load_yaml(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def compare_languages(base_dir, base_lang, other_lang):
    print(f"\nComparing '{base_lang}' with '{other_lang}'...")

    base_lang_dir = os.path.join(base_dir, base_lang)
    other_lang_dir = os.path.join(base_dir, other_lang)

    total_files = 0
    files_with_issues = 0
    missing_folders = 0
    missing_files = 0
    total_missing_ids = 0

    for root, dirs, files in os.walk(base_lang_dir):
        rel_path = os.path.relpath(root, base_lang_dir)
        other_root = os.path.join(other_lang_dir, rel_path)

        if not os.path.exists(other_root):
            print(f"  Folder '{rel_path}' missing in {other_lang}")
            missing_folders += 1
            continue

        base_files = map_files_by_prefix(root)
        other_files = map_files_by_prefix(other_root)

        for prefix, base_file in base_files.items():
            total_files += 1
            base_path = os.path.join(root, base_file)
            other_file = other_files.get(prefix)
            if not other_file:
                print(f"  File with prefix {prefix} ('{base_file}') missing in {other_lang} at '{rel_path}'")
                missing_files += 1
                continue
            other_path = os.path.join(other_root, other_file)

            base_data = load_yaml(base_path)
            other_data = load_yaml(other_path)

            def extract_ids(data):
                ids = set()
                if isinstance(data, list):
                    for entry in data:
                        if isinstance(entry, dict) and 'id' in entry:
                            ids.add(entry['id'])
                elif isinstance(data, dict):
                    for key, val in data.items():
                        if isinstance(val, dict) and 'id' in val:
                            ids.add(val['id'])
                        elif isinstance(val, list):
                            for entry in val:
                                if isinstance(entry, dict) and 'id' in entry:
                                    ids.add(entry['id'])
                return ids

            base_ids = extract_ids(base_data)
            other_ids = extract_ids(other_data)

            missing_in_other = base_ids - other_ids
            missing_in_base = other_ids - base_ids

            if missing_in_other or missing_in_base:
                files_with_issues += 1
                missing_count = len(missing_in_other) + len(missing_in_base)
                total_missing_ids += missing_count

                print(f"  Differences in '{rel_path}' file prefix {prefix}:")
                if missing_in_other:
                    print(f"    IDs missing in {other_lang}: {missing_in_other}")
                if missing_in_base:
                    print(f"    IDs missing in {base_lang}: {missing_in_base}")

    print(f"\nSummary for comparison '{base_lang}' vs '{other_lang}':")
    print(f"  Total files compared: {total_files}")
    print(f"  Folders missing in {other_lang}: {missing_folders}")
    print(f"  Files missing in {other_lang}: {missing_files}")
    print(f"  Files with ID differences: {files_with_issues}")
    print(f"  Total missing IDs found: {total_missing_ids}")

    if missing_folders == 0 and missing_files == 0 and files_with_issues == 0:
        print(f"  All entries match perfectly between '{base_lang}' and '{other_lang}'. 🎉")
    else:
        print(f"  Some differences detected. Please review the messages above.")
        

def main():
    base_dir = "dictionary"
    base_lang = "es"

    langs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

    for lang in langs:
        if lang == base_lang:
            continue
        compare_languages(base_dir, base_lang, lang)

if __name__ == "__main__":
    main()