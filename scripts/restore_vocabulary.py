#!/usr/bin/env python3
"""
Restore vocabulary files from archive backup to data/translated/ structure.

This script reads vocabulary-asian.json and vocabulary-other.json files from
the archive and creates the corresponding vocabulary files in the
data/translated/{lang}/ directories.
"""

import json
import os
from pathlib import Path
from typing import Dict, List

# Directories
ARCHIVE_DIR = Path("/Users/anton/proj/gita/_archive/data.backup/chapters")
TRANSLATED_DIR = Path("/Users/anton/proj/gita/data/translated")

# Language mappings
ASIAN_LANGS = ["ko", "th", "zh-CN", "zh-TW"]
OTHER_LANGS = ["ja", "el", "ka", "hy", "he", "ar", "tr", "sw"]

# Note: vocabulary files contain different languages than chapter files
# vocabulary-asian.json: ko, th, zh-TW, ja (NOT zh-CN)
# vocabulary-other.json: he, ar, tr, sw (NOT el, ka, hy)


def get_archive_files(chapter_num: int) -> List[Path]:
    """Get archive vocabulary JSON files for a chapter."""
    chapter_str = f"{chapter_num:02d}"
    files = []
    
    # Check for asian vocabulary
    asian_file = ARCHIVE_DIR / f"ch-{chapter_str}" / "vocabulary-asian.json"
    if asian_file.exists():
        files.append(asian_file)
    
    # Check for other vocabulary
    other_file = ARCHIVE_DIR / f"ch-{chapter_str}" / "vocabulary-other.json"
    if other_file.exists():
        files.append(other_file)
    
    return files


def restore_vocabulary(chapter_num: int, dry_run: bool = False) -> Dict[str, int]:
    """
    Restore vocabulary for a chapter from archive.
    
    Returns dict with counts of entries restored per language.
    """
    chapter_str = f"{chapter_num:02d}"
    stats = {lang: 0 for lang in ASIAN_LANGS + OTHER_LANGS}
    
    archive_files = get_archive_files(chapter_num)
    
    if not archive_files:
        print(f"  No vocabulary files found for chapter {chapter_num}")
        return stats
    
    for archive_file in archive_files:
        print(f"  Processing {archive_file.name}...")
        
        with open(archive_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        chapter = data.get('chapter', chapter_num)
        vocabulary = data.get('vocabulary', {})
        meta = data.get('meta', {})
        languages = meta.get('languages', [])
        
        # Determine which languages this file contains
        if 'asian' in archive_file.name:
            # vocabulary-asian.json contains: ko, th, zh-TW, ja
            file_langs = ['ko', 'th', 'zh-TW', 'ja']
        else:
            # vocabulary-other.json contains: he, ar, tr, sw
            file_langs = ['he', 'ar', 'tr', 'sw']
        
        # Process each word entry
        for word_id, word_data in vocabulary.items():
            meaning_data = word_data.get('meaning', {})
            translit_data = word_data.get('transliteration', {})
            
            for lang in file_langs:
                if lang not in stats:
                    continue
                
                meaning = meaning_data.get(lang, '')
                translit = translit_data.get(lang, '')
                
                if not meaning and not translit:
                    continue
                
                # Create directory
                lang_dir = TRANSLATED_DIR / lang
                lang_dir.mkdir(parents=True, exist_ok=True)
                
                # Write vocabulary file for this chapter
                vocab_file = lang_dir / f"chapter-{chapter_str}-{lang}_vocabulary.json"
                
                # Load existing vocabulary or create new
                existing_vocab = {}
                if vocab_file.exists() and not dry_run:
                    with open(vocab_file, 'r', encoding='utf-8') as vf:
                        existing_vocab = json.load(vf)
                
                # Update vocabulary entry
                if 'vocabulary' not in existing_vocab:
                    existing_vocab['vocabulary'] = {}
                
                existing_vocab['vocabulary'][word_id] = {
                    'meaning': meaning,
                    'transliteration': translit
                }
                
                if dry_run:
                    stats[lang] += 1
                else:
                    # Save updated vocabulary
                    with open(vocab_file, 'w', encoding='utf-8') as vf:
                        json.dump(existing_vocab, vf, ensure_ascii=False, indent=2)
                    stats[lang] += 1
    
    return stats


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Restore vocabulary from archive')
    parser.add_argument('--chapter', type=int, help='Specific chapter to restore (1-18)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    
    args = parser.parse_args()
    
    chapters = range(1, 19)
    if args.chapter:
        chapters = [args.chapter]
    
    print(f"Restoring vocabulary from archive...")
    if args.dry_run:
        print(f"(DRY RUN - no files will be written)")
    print("=" * 60)
    
    total_stats = {lang: 0 for lang in ASIAN_LANGS + OTHER_LANGS}
    
    for chapter in chapters:
        print(f"\nChapter {chapter}:")
        stats = restore_vocabulary(chapter, dry_run=args.dry_run)
        
        for lang, count in stats.items():
            total_stats[lang] += count
            if count > 0:
                print(f"  {lang}: {count} words")
    
    print("\n" + "=" * 60)
    print("Summary:")
    grand_total = 0
    for lang, count in sorted(total_stats.items()):
        if count > 0:
            print(f"  {lang}: {count} vocabulary entries")
            grand_total += count
    print(f"  TOTAL: {grand_total} entries across all languages")


if __name__ == '__main__':
    main()
