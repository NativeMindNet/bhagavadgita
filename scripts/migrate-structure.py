#!/usr/bin/env python3
"""
GitaBook Structure Migration Script

Migrates from old structure:
  data/chapters/original/chapter-XX.json

To new structure:
  data/sanskrit/chapter-XX-sanskrit/
  data/original/{ru,en,de,es}/chapter-XX-{lang}/
  data/translated/{ko,th,...}/chapter-XX-{lang}/
"""

import json
import os
import shutil
from pathlib import Path
from datetime import datetime

# Configuration
BASE_DIR = Path(__file__).parent.parent / "data"
OLD_CHAPTERS_DIR = BASE_DIR / "chapters" / "original"
OLD_VOCABULARY_DIR = BASE_DIR / "vocabulary" / "original"

NEW_SANSKRIT_DIR = BASE_DIR / "sanskrit"
NEW_ORIGINAL_DIR = BASE_DIR / "original"
NEW_TRANSLATED_DIR = BASE_DIR / "translated"
NEW_META_DIR = BASE_DIR / "meta"

BACKUP_DIR = BASE_DIR.parent / "data.backup"

# Languages
ORIGINAL_LANGUAGES = ["ru", "en", "de", "es"]
TRANSLATED_LANGUAGES = ["ko", "th", "zh-CN", "zh-TW", "el", "ka", "hy", "he", "ar", "tr", "sw"]
ALL_LANGUAGES = ORIGINAL_LANGUAGES + TRANSLATED_LANGUAGES

# Transliteration mapping
TRANSLITERATION_MAP = {
    "ru": "cyrillic",
    "en": "iast",
    "de": "iast",
    "es": "iast",
    "ko": "hangul",
    "th": "thai",
    "zh-CN": "hanzi-simplified",
    "zh-TW": "hanzi-traditional",
    "el": "greek",
    "ka": "georgian",
    "hy": "armenian",
    "he": "hebrew",
    "ar": "arabic",
    "tr": "iast",
    "sw": "iast",
}


def create_backup():
    """Create backup of current data."""
    print("Creating backup...")
    if BACKUP_DIR.exists():
        shutil.rmtree(BACKUP_DIR)
    shutil.copytree(BASE_DIR, BACKUP_DIR)
    print(f"Backup created at {BACKUP_DIR}")


def create_directory_structure():
    """Create new directory structure."""
    print("Creating directory structure...")

    # Sanskrit
    for chapter in range(1, 19):
        chapter_dir = NEW_SANSKRIT_DIR / f"chapter-{chapter:02d}-sanskrit"
        chapter_dir.mkdir(parents=True, exist_ok=True)

    # Original languages
    for lang in ORIGINAL_LANGUAGES:
        for chapter in range(1, 19):
            chapter_dir = NEW_ORIGINAL_DIR / lang / f"chapter-{chapter:02d}-{lang}"
            chapter_dir.mkdir(parents=True, exist_ok=True)

    # Translated languages
    for lang in TRANSLATED_LANGUAGES:
        for chapter in range(1, 19):
            chapter_dir = NEW_TRANSLATED_DIR / lang / f"chapter-{chapter:02d}-{lang}"
            chapter_dir.mkdir(parents=True, exist_ok=True)

    # Meta
    NEW_META_DIR.mkdir(parents=True, exist_ok=True)

    print("Directory structure created.")


def format_sloka_number(sloka_num):
    """Format sloka number for filename (handle combined slokas like 1.4-6)."""
    return str(sloka_num).replace(".", ".").replace("-", "-")


def write_text_file(path, content):
    """Write content to text file."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() if content else "")


def write_json_file(path, data):
    """Write data to JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def migrate_chapter(chapter_num):
    """Migrate a single chapter."""
    chapter_file = OLD_CHAPTERS_DIR / f"chapter-{chapter_num:02d}.json"

    if not chapter_file.exists():
        print(f"  Warning: {chapter_file} not found, skipping...")
        return

    with open(chapter_file, "r", encoding="utf-8") as f:
        chapter_data = json.load(f)

    slokas = chapter_data.get("slokas", [])
    title_data = chapter_data.get("title", {})
    meta_data = chapter_data.get("meta", {})

    sloka_list = []

    # Process each sloka
    for sloka in slokas:
        sloka_num = sloka.get("number", "")
        sloka_list.append(sloka_num)

        # Sanskrit
        sanskrit_text = sloka.get("sanskrit", "")
        if sanskrit_text:
            sanskrit_dir = NEW_SANSKRIT_DIR / f"chapter-{chapter_num:02d}-sanskrit"
            sloka_file = sanskrit_dir / f"chapter-{chapter_num:02d}-{sloka_num}-sanskrit_sloka.txt"
            write_text_file(sloka_file, sanskrit_text)

        # Transliteration (same for all languages currently, but stored per language)
        transliteration = sloka.get("transliteration", "")

        # Translations
        translations = sloka.get("translations", {})
        comments = sloka.get("comment", {})

        for lang in ALL_LANGUAGES:
            translation = translations.get(lang, {})
            text = translation.get("text", "")

            if not text:
                continue

            # Determine target directory
            if lang in ORIGINAL_LANGUAGES:
                lang_dir = NEW_ORIGINAL_DIR / lang / f"chapter-{chapter_num:02d}-{lang}"
            else:
                lang_dir = NEW_TRANSLATED_DIR / lang / f"chapter-{chapter_num:02d}-{lang}"

            # Write sloka
            sloka_file = lang_dir / f"chapter-{chapter_num:02d}-{sloka_num}-{lang}_sloka.txt"
            write_text_file(sloka_file, text)

            # Write transliteration
            if transliteration:
                translit_file = lang_dir / f"chapter-{chapter_num:02d}-{sloka_num}-{lang}_translit.txt"
                write_text_file(translit_file, transliteration)

            # Write comment if exists
            comment = comments.get(lang, {})
            comment_text = comment.get("text", "")
            if comment_text:
                comment_file = lang_dir / f"chapter-{chapter_num:02d}-{sloka_num}-{lang}_comment.txt"
                write_text_file(comment_file, comment_text)

    # Create meta files
    # Sanskrit meta
    sanskrit_meta = {
        "chapter": chapter_num,
        "language": "sanskrit",
        "totalSlokas": len(sloka_list),
        "lastUpdated": datetime.now().isoformat()[:10],
        "slokaList": sloka_list
    }
    sanskrit_meta_file = NEW_SANSKRIT_DIR / f"chapter-{chapter_num:02d}-sanskrit" / f"chapter-{chapter_num:02d}-sanskrit_meta.json"
    write_json_file(sanskrit_meta_file, sanskrit_meta)

    # Language meta files
    for lang in ALL_LANGUAGES:
        title = title_data.get(lang, {})
        title_text = title.get("text", "") if isinstance(title, dict) else title

        if lang in ORIGINAL_LANGUAGES:
            lang_dir = NEW_ORIGINAL_DIR / lang / f"chapter-{chapter_num:02d}-{lang}"
        else:
            lang_dir = NEW_TRANSLATED_DIR / lang / f"chapter-{chapter_num:02d}-{lang}"

        lang_meta = {
            "chapter": chapter_num,
            "language": lang,
            "title": title_text,
            "totalSlokas": len(sloka_list),
            "approved": title.get("approved", False) if isinstance(title, dict) else False,
            "lastUpdated": datetime.now().isoformat()[:10]
        }

        meta_file = lang_dir / f"chapter-{chapter_num:02d}-{lang}_meta.json"
        write_json_file(meta_file, lang_meta)

    return sloka_list


def migrate_vocabulary(chapter_num):
    """Migrate vocabulary for a chapter."""
    vocab_file = OLD_VOCABULARY_DIR / f"vocab_{chapter_num:02d}.json"

    if not vocab_file.exists():
        print(f"  Warning: {vocab_file} not found, skipping vocabulary...")
        return

    with open(vocab_file, "r", encoding="utf-8") as f:
        vocab_data = json.load(f)

    vocabulary = vocab_data.get("vocabulary", [])

    # Group vocabulary by language
    for lang in ORIGINAL_LANGUAGES:
        lang_vocab = {
            "meta": {
                "chapter": chapter_num,
                "language": lang,
                "totalWords": len(vocabulary),
                "lastUpdated": datetime.now().isoformat()[:10]
            },
            "slokas": {}
        }

        for word_entry in vocabulary:
            sloka_id = word_entry.get("slokaId", "")
            word = word_entry.get("word", "")
            meaning = word_entry.get("meaning", {}).get(lang, {})
            meaning_text = meaning.get("text", "") if isinstance(meaning, dict) else ""
            order = word_entry.get("order", 0)

            # We need to map slokaId to sloka number - this is tricky
            # For now, store as-is and can be post-processed
            sloka_key = f"sloka_{sloka_id}"

            if sloka_key not in lang_vocab["slokas"]:
                lang_vocab["slokas"][sloka_key] = []

            lang_vocab["slokas"][sloka_key].append({
                "sanskrit": "",  # Will need to be filled from chapter data
                "word": word,
                "meaning": meaning_text,
                "order": order
            })

        lang_dir = NEW_ORIGINAL_DIR / lang / f"chapter-{chapter_num:02d}-{lang}"
        vocab_out_file = lang_dir / f"chapter-{chapter_num:02d}-{lang}_vocabulary.json"
        write_json_file(vocab_out_file, lang_vocab)


def create_languages_json():
    """Create updated languages.json."""
    print("Creating languages.json...")

    languages = {
        "sanskrit": {
            "name": "Sanskrit",
            "nativeName": "संस्कृतम्",
            "script": "devanagari",
            "direction": "ltr",
            "type": "source"
        }
    }

    # Original languages
    original_info = {
        "ru": ("Russian", "Русский", "cyrillic"),
        "en": ("English", "English", "latin"),
        "de": ("German", "Deutsch", "latin"),
        "es": ("Spanish", "Español", "latin"),
    }

    for lang, (name, native, script) in original_info.items():
        languages[lang] = {
            "name": name,
            "nativeName": native,
            "script": script,
            "direction": "ltr",
            "type": "original",
            "transliteration": TRANSLITERATION_MAP[lang]
        }

    # Translated languages
    translated_info = {
        "ko": ("Korean", "한국어", "hangul", "ltr"),
        "th": ("Thai", "ไทย", "thai", "ltr"),
        "zh-CN": ("Chinese (Simplified)", "简体中文", "hanzi-simplified", "ltr"),
        "zh-TW": ("Chinese (Traditional)", "繁體中文", "hanzi-traditional", "ltr"),
        "el": ("Greek", "Ελληνικά", "greek", "ltr"),
        "ka": ("Georgian", "ქართული", "georgian", "ltr"),
        "hy": ("Armenian", "Հայdelays", "armenian", "ltr"),
        "he": ("Hebrew", "עברית", "hebrew", "rtl"),
        "ar": ("Arabic", "العربية", "arabic", "rtl"),
        "tr": ("Turkish", "Türkçe", "latin", "ltr"),
        "sw": ("Swahili", "Kiswahili", "latin", "ltr"),
    }

    for lang, (name, native, script, direction) in translated_info.items():
        languages[lang] = {
            "name": name,
            "nativeName": native,
            "script": script,
            "direction": direction,
            "type": "translated",
            "transliteration": TRANSLITERATION_MAP[lang]
        }

    write_json_file(NEW_META_DIR / "languages.json", languages)
    print("languages.json created.")


def create_chapters_json(all_sloka_lists):
    """Create chapters.json."""
    print("Creating chapters.json...")

    chapters_data = {
        "totalChapters": 18,
        "chapters": []
    }

    for chapter_num in range(1, 19):
        sloka_list = all_sloka_lists.get(chapter_num, [])
        chapters_data["chapters"].append({
            "number": chapter_num,
            "slokaCount": len(sloka_list),
            "slokaList": sloka_list
        })

    write_json_file(NEW_META_DIR / "chapters.json", chapters_data)
    print("chapters.json created.")


def validate_migration():
    """Validate the migration results."""
    print("\nValidating migration...")

    stats = {
        "directories": 0,
        "txt_files": 0,
        "json_files": 0,
        "errors": []
    }

    for root, dirs, files in os.walk(NEW_SANSKRIT_DIR):
        stats["directories"] += len(dirs)
        for f in files:
            if f.endswith(".txt"):
                stats["txt_files"] += 1
            elif f.endswith(".json"):
                stats["json_files"] += 1
                # Validate JSON
                try:
                    with open(os.path.join(root, f), "r", encoding="utf-8") as jf:
                        json.load(jf)
                except json.JSONDecodeError as e:
                    stats["errors"].append(f"Invalid JSON: {os.path.join(root, f)}: {e}")

    for base_dir in [NEW_ORIGINAL_DIR, NEW_TRANSLATED_DIR]:
        for root, dirs, files in os.walk(base_dir):
            stats["directories"] += len(dirs)
            for f in files:
                if f.endswith(".txt"):
                    stats["txt_files"] += 1
                elif f.endswith(".json"):
                    stats["json_files"] += 1
                    try:
                        with open(os.path.join(root, f), "r", encoding="utf-8") as jf:
                            json.load(jf)
                    except json.JSONDecodeError as e:
                        stats["errors"].append(f"Invalid JSON: {os.path.join(root, f)}: {e}")

    print(f"\nValidation Results:")
    print(f"  Directories: {stats['directories']}")
    print(f"  TXT files: {stats['txt_files']}")
    print(f"  JSON files: {stats['json_files']}")
    print(f"  Errors: {len(stats['errors'])}")

    if stats["errors"]:
        print("\nErrors found:")
        for err in stats["errors"][:10]:
            print(f"  - {err}")
        if len(stats["errors"]) > 10:
            print(f"  ... and {len(stats['errors']) - 10} more")

    return stats


def main():
    print("=" * 60)
    print("GitaBook Structure Migration")
    print("=" * 60)

    # Phase 1: Backup
    create_backup()

    # Phase 2: Create directory structure
    create_directory_structure()

    # Phase 3-5: Migrate chapters
    print("\nMigrating chapters...")
    all_sloka_lists = {}

    for chapter_num in range(1, 19):
        print(f"  Processing chapter {chapter_num}...")
        sloka_list = migrate_chapter(chapter_num)
        if sloka_list:
            all_sloka_lists[chapter_num] = sloka_list
        migrate_vocabulary(chapter_num)

    # Phase 6: Create meta files
    create_languages_json()
    create_chapters_json(all_sloka_lists)

    # Phase 7: Validate
    stats = validate_migration()

    print("\n" + "=" * 60)
    print("Migration complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review the migrated data")
    print("2. If satisfied, delete old structure:")
    print(f"   rm -rf {OLD_CHAPTERS_DIR.parent}")
    print(f"   rm -rf {OLD_VOCABULARY_DIR.parent}")
    print(f"3. If issues found, restore from backup:")
    print(f"   rm -rf {BASE_DIR} && mv {BACKUP_DIR} {BASE_DIR}")


if __name__ == "__main__":
    main()
