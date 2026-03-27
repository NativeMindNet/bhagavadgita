#!/usr/bin/env python3
"""
Convert Gita Vocabulary CSV to JSON files (one per chapter).

Reads:
- /legacy/csv/books/Gita_Vocabularies.csv
- /legacy/csv/books/Gita_Slokas.csv (for SlokaId → ChapterId mapping)
- /legacy/csv/books/db_chapters.csv (for ChapterId → BookId mapping)

Writes:
- data/vocabulary/vocab_01.json through vocab_18.json

Merges vocabulary from:
- BookId 1 (RU/ШМ) - Russian translations
- BookId 2 (EN/SM) - English translations for same chapters
"""

import csv
import json
import os
from pathlib import Path
from datetime import datetime

# Paths
BASE_DIR = Path(__file__).parent.parent
LEGACY_DIR = BASE_DIR / 'legacy' / 'csv' / 'books'
OUTPUT_DIR = BASE_DIR / 'data' / 'vocabulary'

VOCAB_CSV = LEGACY_DIR / 'Gita_Vocabularies.csv'
SLOKAS_CSV = LEGACY_DIR / 'Gita_Slokas.csv'
CHAPTERS_CSV = LEGACY_DIR / 'db_chapters.csv'

def load_csv(filepath, delimiter=';'):
    """Load CSV file and return list of dicts."""
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        return list(reader)

def detect_language(text):
    """Detect language of translation text."""
    text_lower = text.lower()
    
    # English indicators (check first, more specific)
    en_patterns = [' the ', ' and ', ' of ', ' to ', ' is ', ' that ', ' for ', ' with ',
                   'thou ', 'hast ', 'shalt ', 'unto ', 'hath ']
    if any(p in text_lower for p in en_patterns):
        return 'en'
    
    # German indicators
    de_patterns = [' der ', ' die ', ' das ', ' und ', ' ist ', ' auf ', ' mit ', ' zu ',
                   'nicht ', 'aber ', 'wenn ', 'als ']
    if any(p in text_lower for p in de_patterns):
        return 'de'
    
    # Spanish indicators
    es_patterns = [' el ', ' la ', ' los ', ' las ', ' de ', ' que ', ' en ', ' con ',
                   'para ', 'por ', 'del ', 'al ', 'se ', 'un ', 'una ']
    if any(p in text_lower for p in es_patterns):
        return 'es'
    
    # Default: Russian (Cyrillic)
    return 'ru'

def cyrillic_to_iast(word):
    """
    Convert Cyrillic Sanskrit transliteration to IAST.
    Simplified mapping for common characters.
    """
    mappings = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'ё': 'o', 'ж': 'j', 'з': 'z', 'и': 'i',
        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'ph', 'х': 'h', 'ц': 'c', 'ч': 'c',
        'ш': 'ś', 'щ': 'ś', 'ъ': 'ḥ', 'ы': 'ī', 'ь': "'",
        'э': 'e', 'ю': 'yu', 'я': 'ya',
        # Diacritics (approximate)
        'ā': 'ā', 'ī': 'ī', 'ū': 'ū',
        'ṛ': 'ṛ', 'ḷ': 'ḷ',
        'ṅ': 'ṅ', 'ñ': 'ñ', 'ṇ': 'ṇ',
        'ś': 'ś', 'ṣ': 'ṣ', 'ḥ': 'ḥ',
    }
    
    result = []
    for char in word:
        result.append(mappings.get(char, char))
    return ''.join(result)

def convert_vocabulary():
    """Convert vocabulary CSV to JSON files per chapter."""
    
    print("Loading CSV files...")
    
    # Load chapters with BookId mapping
    chapters_data = load_csv(CHAPTERS_CSV, delimiter=',')
    chapter_to_book = {}
    for ch in chapters_data:
        chapter_id = int(ch['Id'])
        book_id = int(ch['BookId'])
        chapter_to_book[chapter_id] = book_id
    
    print(f"Loaded {len(chapters_data)} chapters")
    
    # Load slokas for ChapterId mapping
    slokas = load_csv(SLOKAS_CSV)
    sloka_to_chapter = {}
    for s in slokas:
        sloka_id = int(s['Id'])
        chapter_id = int(s['ChapterId'])
        book_id = chapter_to_book.get(chapter_id, 0)
        sloka_to_chapter[sloka_id] = {
            'chapter_id': chapter_id,
            'book_id': book_id
        }
    
    print(f"Loaded {len(slokas)} slokas")
    
    # Load vocabulary
    vocab_data = load_csv(VOCAB_CSV)
    print(f"Loaded {len(vocab_data)} vocabulary entries")
    
    # Group vocabulary by (chapter, book_id, language)
    # Key: (chapter_num, book_id) -> list of vocab entries
    vocab_by_chapter_book = {}
    
    for v in vocab_data:
        sloka_id = int(v['SlokaId'])
        sloka_info = sloka_to_chapter.get(sloka_id)
        
        if sloka_info is None:
            continue
        
        chapter_id = sloka_info['chapter_id']
        book_id = sloka_info['book_id']
        
        # Map ChapterId to chapter number (1-18)
        # BookId 1 (RU): ChapterId 1-18 → chapter 1-18
        # BookId 2 (EN): ChapterId 19-36 → chapter 1-18
        # BookId 11 (DE): ChapterId 37-54 → chapter 1-18
        # BookId 14 (ES): ChapterId 55-72 → chapter 1-18
        if book_id == 1:
            chapter_num = chapter_id
        elif book_id == 2:
            chapter_num = chapter_id - 18
        elif book_id == 11:
            chapter_num = chapter_id - 36
        elif book_id == 14:
            chapter_num = chapter_id - 54
        else:
            continue
        
        if chapter_num < 1 or chapter_num > 18:
            continue
        
        # Detect language
        lang = detect_language(v['Translation'])
        
        key = (chapter_num, book_id)
        if key not in vocab_by_chapter_book:
            vocab_by_chapter_book[key] = {'ru': {}, 'en': {}, 'de': {}, 'es': {}}
        
        # Store by word (Text) to merge RU and EN
        word_key = v['Text'].strip().lower()
        vocab_by_chapter_book[key][lang][word_key] = v
    
    # Create JSON files for each chapter (1-18)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    for chapter_num in range(1, 19):
        vocab_entry = {
            "chapter": chapter_num,
            "meta": {
                "totalWords": 0,
                "lastUpdated": datetime.now().isoformat(),
                "version": "1.0",
                "source": "SM/SCSM/ШМ/ШЧСМ",
                "sources": {
                    "russian": "BookId 1 (ШМ/SM)",
                    "english": "BookId 2 (SM)"
                }
            },
            "vocabulary": []
        }
        
        # Get vocabulary for this chapter from both RU and EN sources
        ru_vocab = vocab_by_chapter_book.get((chapter_num, 1), {}).get('ru', {})
        en_vocab = vocab_by_chapter_book.get((chapter_num, 2), {}).get('en', {})
        
        # Merge vocabulary: use word text as key
        all_words = set(ru_vocab.keys()) | set(en_vocab.keys())
        
        for word_key in sorted(all_words):
            ru_entry = ru_vocab.get(word_key)
            en_entry = en_vocab.get(word_key)
            
            # Get the word text (prefer Russian if available)
            word_text = ru_entry['Text'] if ru_entry else (en_entry['Text'] if en_entry else '')
            
            # Create vocabulary entry
            entry = {
                "id": int(ru_entry['Id']) if ru_entry else (int(en_entry['Id']) if en_entry else 0),
                "slokaId": int(ru_entry['SlokaId']) if ru_entry else (int(en_entry['SlokaId']) if en_entry else 0),
                "word": word_text,
                "transliteration": {
                    "cyrillic": ru_entry['Text'] if ru_entry else "",
                    "iast": cyrillic_to_iast(ru_entry['Text']) if ru_entry else ""
                },
                "meaning": {
                    "ru": {
                        "text": ru_entry['Translation'] if ru_entry else "",
                        "approved": True if ru_entry else False
                    },
                    "en": {
                        "text": en_entry['Translation'] if en_entry else "",
                        "approved": True if en_entry else False
                    },
                    "th": {
                        "text": "",
                        "approved": False
                    },
                    "zh-CN": {
                        "text": "",
                        "approved": False
                    },
                    "zh-TW": {
                        "text": "",
                        "approved": False
                    },
                    "ko": {
                        "text": "",
                        "approved": False
                    },
                    "ja": {
                        "text": "",
                        "approved": False
                    }
                },
                "order": 0  # Will be set during translation
            }
            
            vocab_entry["vocabulary"].append(entry)
        
        vocab_entry["meta"]["totalWords"] = len(vocab_entry["vocabulary"])
        
        # Save JSON file
        output_file = OUTPUT_DIR / f'vocab_{chapter_num:02d}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(vocab_entry, f, ensure_ascii=False, indent=2)
        
        ru_count = sum(1 for e in vocab_entry["vocabulary"] if e['meaning']['ru']['text'])
        en_count = sum(1 for e in vocab_entry["vocabulary"] if e['meaning']['en']['text'])
        print(f"Created {output_file} ({len(vocab_entry['vocabulary'])} words: RU={ru_count}, EN={en_count})")
    
    print(f"\nConversion complete! Created 18 vocabulary files in {OUTPUT_DIR}")

if __name__ == '__main__':
    convert_vocabulary()
