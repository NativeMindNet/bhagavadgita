#!/usr/bin/env python3
"""
Apply translated vocabulary to the original vocabulary files.

Merges translated meanings back into chapter vocabulary JSON files.
"""

import json
from pathlib import Path

# Directories
TRANSLATED_DIR = Path("/Users/anton/proj/gita/data/translated")
TRANSLATIONS_DIR = Path("/Users/anton/proj/gita/data/translations/vocab")


def apply_translations(lang: str, translated_file: Path):
    """Apply translations to vocabulary files."""
    
    # Load translations
    with open(translated_file, 'r', encoding='utf-8') as f:
        trans_data = json.load(f)
    
    translations = trans_data.get('translations', {})
    
    # Group by chapter
    by_chapter = {}
    for key, trans in translations.items():
        parts = key.split('_')
        chapter = int(parts[0].replace('ch', ''))
        word_id = parts[1]
        
        if chapter not in by_chapter:
            by_chapter[chapter] = {}
        
        by_chapter[chapter][word_id] = trans.get(lang, {}).get('meaning', '')
    
    # Apply to each chapter file
    total_applied = 0
    
    for chapter, entries in by_chapter.items():
        chapter_str = f"{chapter:02d}"
        vocab_file = TRANSLATED_DIR / lang / f"chapter-{chapter_str}-{lang}_vocabulary.json"
        
        if not vocab_file.exists():
            print(f"  Warning: {vocab_file} not found")
            continue
        
        # Load original vocabulary
        with open(vocab_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        vocabulary = data.get('vocabulary', {})
        applied = 0
        
        for word_id, thai_meaning in entries.items():
            if word_id in vocabulary:
                vocabulary[word_id]['meaning'] = thai_meaning
                applied += 1
                total_applied += 1
        
        # Save updated vocabulary
        with open(vocab_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"  Chapter {chapter}: Applied {applied} translations")
    
    return total_applied


def main():
    print("Applying Thai vocabulary translations...")
    print("=" * 60)
    
    # Thai
    print("\nThai:")
    thai_count = apply_translations('th', TRANSLATIONS_DIR / 'vocabulary-th-translated.json')
    print(f"  Total applied: {thai_count}")
    
    print("\n" + "=" * 60)
    print(f"COMPLETE: Applied {thai_count} Thai translations")


if __name__ == '__main__':
    main()
