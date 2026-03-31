#!/usr/bin/env python3
"""
Translate vocabulary entries that are English-only to target language.

This script analyzes vocabulary files, identifies English-only entries,
and translates them to the target language.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple

# Directories
TRANSLATED_DIR = Path("/Users/anton/proj/gita/data/translated")

# Target languages for vocabulary translation
TARGET_LANGS = {
    'th': 'Thai',
    'zh-TW': 'Traditional Chinese',
    'zh-CN': 'Simplified Chinese',
}


def is_english_only(text: str) -> bool:
    """Check if text contains only English (ASCII) characters."""
    # If all characters are ASCII, it's English
    try:
        text.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False


def has_native_script(text: str, lang: str) -> bool:
    """Check if text contains characters in the target script."""
    if lang == 'th':
        # Thai Unicode range: U+0E00 to U+0E7F
        return any('\u0E00' <= c <= '\u0E7F' for c in text)
    elif lang == 'zh-TW' or lang == 'zh-CN':
        # CJK Unicode range: U+4E00 to U+9FFF
        return any('\u4E00' <= c <= '\u9FFF' for c in text)
    return False


def analyze_vocabulary(lang: str, chapter: int) -> Dict:
    """Analyze vocabulary file for a language and chapter."""
    chapter_str = f"{chapter:02d}"
    vocab_file = TRANSLATED_DIR / lang / f"chapter-{chapter_str}-{lang}_vocabulary.json"
    
    if not vocab_file.exists():
        return {'error': 'File not found'}
    
    with open(vocab_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    vocabulary = data.get('vocabulary', {})
    total = len(vocabulary)
    english_only = 0
    has_native = 0
    mixed = 0
    
    for word_id, entry in vocabulary.items():
        meaning = entry.get('meaning', '')
        
        if is_english_only(meaning):
            english_only += 1
        elif has_native_script(meaning, lang):
            has_native += 1
        else:
            mixed += 1
    
    return {
        'total': total,
        'english_only': english_only,
        'has_native': has_native,
        'mixed': mixed,
        'percent_complete': round((has_native / total) * 100, 1) if total > 0 else 0
    }


def translate_vocabulary_batch(lang: str, chapters: List[int], dry_run: bool = True) -> Dict:
    """
    Translate English-only vocabulary entries to target language.
    
    For now, this is a placeholder that shows what needs to be done.
    Actual translation would require calling a translation API or service.
    """
    results = []
    
    for chapter in chapters:
        chapter_str = f"{chapter:02d}"
        vocab_file = TRANSLATED_DIR / lang / f"chapter-{chapter_str}-{lang}_vocabulary.json"
        
        if not vocab_file.exists():
            print(f"  Chapter {chapter}: File not found")
            continue
        
        with open(vocab_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        vocabulary = data.get('vocabulary', {})
        to_translate = []
        
        for word_id, entry in vocabulary.items():
            meaning = entry.get('meaning', '')
            if is_english_only(meaning):
                to_translate.append({
                    'word_id': word_id,
                    'english': meaning,
                    'transliteration': entry.get('transliteration', '')
                })
        
        results.append({
            'chapter': chapter,
            'to_translate': len(to_translate),
            'entries': to_translate if not dry_run else None
        })
        
        print(f"  Chapter {chapter}: {len(to_translate)} entries need translation")
        
        if not dry_run and to_translate:
            # Here would be the translation logic
            # For now, just show what would be translated
            print(f"    Sample entries:")
            for entry in to_translate[:3]:
                print(f"      {entry['word_id']}: {entry['english'][:50]}...")
    
    return {'results': results}


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze and translate vocabulary')
    parser.add_argument('--language', choices=['th', 'zh-TW', 'zh-CN'], required=True,
                       help='Target language')
    parser.add_argument('--chapter', type=int, help='Specific chapter (1-18)')
    parser.add_argument('--translate', action='store_true', 
                       help='Run translation (default: analyze only)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be translated without making changes')
    
    args = parser.parse_args()
    
    chapters = range(1, 19)
    if args.chapter:
        chapters = [args.chapter]
    
    print(f"Vocabulary Analysis for {args.language}")
    print("=" * 60)
    
    # Analyze each chapter
    total_entries = 0
    total_english = 0
    
    for chapter in chapters:
        stats = analyze_vocabulary(args.language, chapter)
        if 'error' not in stats:
            print(f"Chapter {chapter:2d}: {stats['total']:4d} entries, "
                  f"{stats['english_only']:4d} English ({100-stats['percent_complete']:.1f}% to translate), "
                  f"{stats['has_native']:4d} native ({stats['percent_complete']}% complete)")
            total_entries += stats['total']
            total_english += stats['english_only']
    
    print("=" * 60)
    print(f"TOTAL: {total_entries} entries, {total_english} need translation "
          f"({100-(total_english/total_entries)*100:.1f}% complete)")
    
    if args.translate:
        print("\nStarting translation...")
        translate_vocabulary_batch(args.language, chapters, dry_run=args.dry_run)


if __name__ == '__main__':
    main()
