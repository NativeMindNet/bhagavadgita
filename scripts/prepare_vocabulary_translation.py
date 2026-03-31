#!/usr/bin/env python3
"""
Prepare vocabulary for batch translation via /translate.sanscrit

Extracts English-only vocabulary entries and creates JSON files
for batch translation to target languages.
"""

import json
from pathlib import Path
from typing import Dict, List

# Directories
TRANSLATED_DIR = Path("/Users/anton/proj/gita/data/translated")
OUTPUT_DIR = Path("/Users/anton/proj/gita/data/translations/vocab")

# Target languages for Thai batch
THAI_LANGS = ['th']
ZH_TW_LANGS = ['zh-TW']
ZH_CN_LANGS = ['zh-CN']

# Chapters that need vocabulary translation
THAI_CHAPTERS = [2, 3, 4, 5, 6, 10]  # Only these have English entries


def is_english_only(text: str) -> bool:
    """Check if text contains only English (ASCII) characters."""
    try:
        text.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False


def extract_english_vocabulary(lang: str, chapters: List[int]) -> Dict:
    """Extract English-only vocabulary entries for translation."""
    all_entries = {}
    
    for chapter in chapters:
        chapter_str = f"{chapter:02d}"
        vocab_file = TRANSLATED_DIR / lang / f"chapter-{chapter_str}-{lang}_vocabulary.json"
        
        if not vocab_file.exists():
            continue
        
        with open(vocab_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        vocabulary = data.get('vocabulary', {})
        
        for word_id, entry in vocabulary.items():
            meaning = entry.get('meaning', '')
            
            if is_english_only(meaning):
                key = f"ch{chapter}_{word_id}"
                all_entries[key] = {
                    'chapter': chapter,
                    'word_id': word_id,
                    'english': meaning,
                    'transliteration': entry.get('transliteration', '')
                }
    
    return all_entries


def prepare_translation_batch(lang: str, output_file: Path):
    """Prepare batch translation file for a language."""
    chapters = THAI_CHAPTERS if lang == 'th' else list(range(1, 19))
    entries = extract_english_vocabulary(lang, chapters)
    
    # Create output directory
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Create translation request format
    batch_data = {
        'meta': {
            'source': f'vocabulary-{lang}',
            'type': 'vocabulary_meaning',
            'target_languages': [lang],
            'total_entries': len(entries)
        },
        'entries': entries
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(batch_data, f, ensure_ascii=False, indent=2)
    
    print(f"Created: {output_file}")
    print(f"  Total entries: {len(entries)}")
    
    # Show sample entries
    print(f"  Sample entries:")
    for i, (key, entry) in enumerate(list(entries.items())[:3]):
        print(f"    {key}: {entry['english'][:60]}...")
    
    return len(entries)


def main():
    print("Preparing vocabulary for batch translation...")
    print("=" * 60)
    
    # Thai vocabulary
    print("\nThai Vocabulary:")
    thai_count = prepare_translation_batch('th', OUTPUT_DIR / 'vocabulary-th-batch.json')
    
    # zh-TW vocabulary
    print("\nzh-TW Vocabulary:")
    zhtw_count = prepare_translation_batch('zh-TW', OUTPUT_DIR / 'vocabulary-zh-TW-batch.json')
    
    # zh-CN vocabulary (all entries, not just English)
    print("\nzh-CN Vocabulary (full translation needed):")
    # For zh-CN, we need to translate ALL vocabulary, not just English
    # This will be handled separately
    
    print("\n" + "=" * 60)
    print(f"Ready for translation:")
    print(f"  Thai: {thai_count} entries")
    print(f"  zh-TW: {zhtw_count} entries")
    print(f"\nUse /translate.sanscrit to translate these batches")


if __name__ == '__main__':
    main()
