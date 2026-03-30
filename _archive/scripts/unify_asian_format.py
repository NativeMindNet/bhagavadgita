#!/usr/bin/env python3
"""
Unify Asian translations format for chapters 1-6.

Converts from old format (asian/chapter-XX-asian-translations.json)
to new format (ch-XX/chapter-asian.json).
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent / "data" / "chapters"
ASIAN_DIR = BASE_DIR / "asian"

# Languages in old format: ko, th, zh-CN, zh-TW
# Languages in new format: th, zh-TW, ja, ko
# Note: zh-CN exists in old but not in new format for ch 7-18
# Note: ja exists in new format but not in old format

def convert_chapter(chapter_num: int) -> dict:
    """Convert old format to new format for a single chapter."""

    # Read old format
    old_file = ASIAN_DIR / f"chapter-{chapter_num:02d}-asian-translations.json"
    with open(old_file, 'r', encoding='utf-8') as f:
        old_data = json.load(f)

    # Build new format
    new_data = {
        "chapter": chapter_num,
        "title": {},
        "slokas": {}
    }

    # Convert title
    for lang, text in old_data.get("chapterTitle", {}).items():
        new_data["title"][lang] = text

    # Convert slokas
    for sloka_num, translations in old_data.get("slokas", {}).items():
        new_data["slokas"][sloka_num] = {}
        for lang, text in translations.items():
            new_data["slokas"][sloka_num][lang] = {
                "text": text,
                "approved": False
            }

    return new_data


def main():
    """Convert chapters 1-6 from old to new format."""

    for chapter_num in range(1, 7):
        print(f"Converting chapter {chapter_num}...")

        # Convert
        new_data = convert_chapter(chapter_num)

        # Write to new location
        out_dir = BASE_DIR / f"ch-{chapter_num:02d}"
        out_file = out_dir / "chapter-asian.json"

        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=2)

        # Stats
        sloka_count = len(new_data["slokas"])
        langs = set()
        for sloka_data in new_data["slokas"].values():
            langs.update(sloka_data.keys())

        print(f"  -> {out_file}")
        print(f"     Slokas: {sloka_count}, Languages: {sorted(langs)}")

    print("\nDone! Chapters 1-6 converted to new format.")


if __name__ == "__main__":
    main()
