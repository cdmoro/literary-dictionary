import sqlite3
import os
import glob
import yaml
import argparse
from collections import defaultdict
from pathlib import Path

CHECK_FIELDS = {
    "entries": ["saga_id", "author_id", "category_id", "book_id"],
    "books": ["author_id", "saga_id", "publication_year"],
    "authors": ["birth_year", "death_year"],
    "sagas": ["author_id"],
}

TABLES_TO_CHECK = list(CHECK_FIELDS.keys()) + ["categories"]
IGNORE_LANGS = []


def extract_lang_from_filename(filename):
    return filename.split(".")[-2]


def load_data():
    data = {table: defaultdict(dict) for table in TABLES_TO_CHECK}
    categories_by_lang = {}

    for filepath in glob.glob("dictionary/dictionary.*.db"):
        lang = extract_lang_from_filename(filepath)
        if lang in IGNORE_LANGS:
            print(f"⚠️  Skipping language: {lang}")
            continue
        conn = sqlite3.connect(filepath)
        cursor = conn.cursor()

        for table in CHECK_FIELDS:
            cursor.execute(
                f"SELECT global_id, {', '.join(CHECK_FIELDS[table])} FROM {table}"
            )
            for row in cursor.fetchall():
                global_id, *fields = row
                data[table][global_id][lang] = dict(zip(CHECK_FIELDS[table], fields))

        cursor.execute("SELECT global_id FROM categories")
        categories_by_lang[lang] = set(row[0] for row in cursor.fetchall())

        conn.close()

    return data, categories_by_lang


def find_conflicts(data):
    conflicts = {table: [] for table in CHECK_FIELDS}
    for table, entries in data.items():
        for global_id, lang_map in entries.items():
            values_list = list(lang_map.values())
            if not all(v == values_list[0] for v in values_list):
                conflicts[table].append({"id": global_id, "conflicts": lang_map})
    return conflicts


def find_missing_ids(data, langs):
    missing = {table: defaultdict(list) for table in CHECK_FIELDS}
    for table, entries in data.items():
        all_ids = set(entries.keys())
        for global_id, lang_map in entries.items():
            for lang in langs:
                if lang not in lang_map:
                    missing[table][lang].append(global_id)
    return missing


def check_categories_consistency(categories_by_lang):
    langs = list(categories_by_lang.keys())
    if not langs:
        return {}

    reference_lang = langs[0]
    reference_ids = categories_by_lang[reference_lang]
    issues = {}

    mismatches = {
        lang: len(ids)
        for lang, ids in categories_by_lang.items()
        if len(ids) != len(reference_ids)
    }
    if mismatches:
        issues["count_mismatch"] = {
            "expected": len(reference_ids),
            "langs": mismatches,
        }

    missing = defaultdict(list)
    for lang, ids in categories_by_lang.items():
        missing_ids = reference_ids - ids
        if missing_ids:
            missing[lang] = sorted(list(missing_ids))

    if missing:
        issues["missing_ids"] = dict(missing)

    return issues


def write_report(conflicts, missing, categories_issues):
    report_data = {}
    if any(conflicts.values()):
        report_data["conflicts"] = conflicts
    if any(missing[table] for table in missing):
        report_data["missing_global_ids"] = missing
    if categories_issues:
        report_data["categories_consistency_issues"] = categories_issues

    if report_data:
        Path("reports").mkdir(exist_ok=True)
        with open("reports/report.yaml", "w", encoding="utf-8") as f:
            yaml.dump(report_data, f, allow_unicode=True, sort_keys=False)
        print("Inconsistencies found. Report saved to reports/report.yaml")
        return True
    else:
        print("No inconsistencies found. No report generated.")
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--full-report", action="store_true", help="Write detailed reports"
    )
    parser.add_argument(
        "--precommit", action="store_true", help="Run in pre-commit mode"
    )
    args = parser.parse_args()

    data, categories_by_lang = load_data()
    langs = list(categories_by_lang.keys())

    conflicts = find_conflicts(data)
    missing_ids = find_missing_ids(data, langs)
    category_issues = check_categories_consistency(categories_by_lang)

    has_issues = write_report(conflicts, missing_ids, category_issues)

    if args.precommit and has_issues:
        answer = input(
            "⚠ Conflicts detected. Do you want to continue with commit? [y/N]: "
        ).lower()
        if answer != "y":
            print("Commit aborted.")
            exit(2)
        else:
            print("Continuing with commit.")


if __name__ == "__main__":
    main()
