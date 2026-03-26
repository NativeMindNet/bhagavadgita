#!/usr/bin/env python3
"""
Convert Bhagavad Gita CSV files to JSON format.
Only processes books by SM/SCSM/ШМ/ШЧСМ (Sri Chaitanya Saraswat Math).
"""

import csv
import json
import os
from datetime import datetime
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
CSV_DIR = BASE_DIR / "legacy" / "csv" / "Books"
OUTPUT_DIR = BASE_DIR / "data" / "chapters"

# Only SM/ШМ books
SM_BOOK_IDS = {1, 2, 11, 14}  # ru, en, de, es

# Language mapping by BookId
BOOK_TO_LANG = {
    1: "ru",
    2: "en",
    11: "de",
    14: "es"
}

def load_csv(filename, delimiter=','):
    """Load CSV file with UTF-8-BOM encoding."""
    filepath = CSV_DIR / filename
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        return list(reader)

def build_chapter_title(chapter_order, chapters_data):
    """Build multilingual title for a chapter."""
    title = {
        "sanskrit": "",
        "transliteration": ""
    }

    for ch in chapters_data:
        book_id = int(ch['BookId'])
        if book_id not in SM_BOOK_IDS:
            continue
        if int(ch['Order']) != chapter_order:
            continue

        lang = BOOK_TO_LANG.get(book_id)
        if lang:
            # Clean up multiline chapter names (especially German)
            name = ch['Name'].replace('\n', ' ').strip()
            title[lang] = {
                "text": name,
                "approved": True
            }

    return title

def get_chapter_ids_for_order(chapter_order, chapters_data):
    """Get all ChapterIds for a given chapter order across SM books."""
    chapter_ids = {}
    for ch in chapters_data:
        book_id = int(ch['BookId'])
        if book_id not in SM_BOOK_IDS:
            continue
        if int(ch['Order']) != chapter_order:
            continue
        chapter_ids[book_id] = ch['Id']
    return chapter_ids

def collect_translations(sloka_number, chapter_order, slokas_by_chapter, chapters_data):
    """Collect translations for a sloka from all SM books."""
    translations = {}
    comment = {}

    chapter_ids = get_chapter_ids_for_order(chapter_order, chapters_data)

    for book_id, chapter_id in chapter_ids.items():
        lang = BOOK_TO_LANG.get(book_id)
        if not lang:
            continue

        # Find sloka with same number in this chapter
        for sloka in slokas_by_chapter.get(chapter_id, []):
            if sloka['Name'] == sloka_number:
                if sloka['Translation'] and sloka['Translation'] != 'NULL':
                    translations[lang] = {
                        "text": sloka['Translation'],
                        "approved": True
                    }
                if sloka.get('Comment') and sloka['Comment'] != 'NULL':
                    comment[lang] = {
                        "text": sloka['Comment'],
                        "approved": True
                    }
                break

    return translations, comment

def build_vocabulary(sloka_id, vocab_data):
    """Build vocabulary array for a sloka."""
    vocabulary = []
    order = 1

    for v in vocab_data:
        if v['SlokaId'] == sloka_id:
            vocabulary.append({
                "word": v['Text'],
                "transliteration": "",  # Not in source data
                "meaning": {
                    "ru": {
                        "text": v['Translation'],
                        "approved": True
                    }
                },
                "order": order
            })
            order += 1

    return vocabulary

def convert():
    """Main conversion function."""
    print("Loading CSV files...")

    # Load metadata
    books = load_csv('db_books.csv')
    chapters = load_csv('db_chapters.csv')

    # Load content (semicolon-delimited)
    slokas = load_csv('Gita_Slokas.csv', delimiter=';')
    vocab = load_csv('Gita_Vocabularies.csv', delimiter=';')

    print(f"Loaded: {len(books)} books, {len(chapters)} chapters, {len(slokas)} slokas, {len(vocab)} vocab items")

    # Filter SM books
    sm_chapters = [ch for ch in chapters if int(ch['BookId']) in SM_BOOK_IDS]
    print(f"SM chapters: {len(sm_chapters)}")

    # Index slokas by ChapterId
    slokas_by_chapter = {}
    for s in slokas:
        ch_id = s['ChapterId']
        if ch_id not in slokas_by_chapter:
            slokas_by_chapter[ch_id] = []
        slokas_by_chapter[ch_id].append(s)

    # Get base book chapter IDs (BookId=1, Russian)
    base_chapter_ids = {}
    for ch in chapters:
        if int(ch['BookId']) == 1:
            base_chapter_ids[int(ch['Order'])] = ch['Id']

    # Process each chapter 1-18
    for chapter_order in range(1, 19):
        print(f"\nProcessing Chapter {chapter_order}...")

        base_chapter_id = base_chapter_ids.get(chapter_order)
        if not base_chapter_id:
            print(f"  WARNING: No base chapter found for order {chapter_order}")
            continue

        base_slokas = slokas_by_chapter.get(base_chapter_id, [])
        print(f"  Found {len(base_slokas)} slokas in base book")

        # Build chapter data
        chapter_data = {
            "chapter": chapter_order,
            "title": build_chapter_title(chapter_order, chapters),
            "meta": {
                "totalSlokas": len(base_slokas),
                "lastUpdated": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "version": "1.0",
                "source": "SM/SCSM/ШМ/ШЧСМ"
            },
            "slokas": []
        }

        # Process each sloka
        for sloka in sorted(base_slokas, key=lambda x: int(x['Order'])):
            translations, comment = collect_translations(
                sloka['Name'],
                chapter_order,
                slokas_by_chapter,
                chapters
            )

            vocabulary = build_vocabulary(sloka['Id'], vocab)

            sloka_data = {
                "number": sloka['Name'],
                "order": int(sloka['Order']),
                "sanskrit": sloka['Text'],
                "transliteration": sloka['Transcription'] if sloka['Transcription'] != 'NULL' else "",
                "translations": translations,
                "audio": {
                    "recitation": sloka['Audio'] if sloka['Audio'] != 'NULL' else "",
                    "sanskrit": sloka['AudioSanskrit'] if sloka['AudioSanskrit'] != 'NULL' else ""
                }
            }

            if comment:
                sloka_data["comment"] = comment

            if vocabulary:
                sloka_data["vocabulary"] = vocabulary

            chapter_data["slokas"].append(sloka_data)

        # Save JSON
        output_file = OUTPUT_DIR / f"chapter-{chapter_order:02d}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chapter_data, f, ensure_ascii=False, indent=2)

        print(f"  Saved: {output_file}")

    print("\n" + "="*50)
    print("Conversion complete!")
    print(f"Output directory: {OUTPUT_DIR}")

if __name__ == "__main__":
    convert()
