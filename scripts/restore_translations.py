#!/usr/bin/env python3
"""
Restore translations from archive backup to data/translated/ structure.

This script reads chapter-asian.json and chapter-other.json files from
the archive and creates the corresponding _sloka.txt files in the
data/translated/{lang}/chapter-XX-{lang}/ directories.
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

# Chapter files mapping
def get_archive_files(chapter_num: int) -> List[Path]:
    """Get archive JSON files for a chapter."""
    chapter_str = f"{chapter_num:02d}"
    files = []
    
    # Check for asian translations
    asian_file = ARCHIVE_DIR / f"ch-{chapter_str}" / "chapter-asian.json"
    if asian_file.exists():
        files.append(asian_file)
    
    # Check for other translations
    other_file = ARCHIVE_DIR / f"ch-{chapter_str}" / "chapter-other.json"
    if other_file.exists():
        files.append(other_file)
    
    return files


def restore_translations(chapter_num: int, dry_run: bool = False) -> Dict[str, int]:
    """
    Restore translations for a chapter from archive.
    
    Returns dict with counts of files restored per language.
    """
    chapter_str = f"{chapter_num:02d}"
    stats = {lang: 0 for lang in ASIAN_LANGS + OTHER_LANGS}
    
    archive_files = get_archive_files(chapter_num)
    
    if not archive_files:
        print(f"  No archive files found for chapter {chapter_num}")
        return stats
    
    for archive_file in archive_files:
        print(f"  Processing {archive_file.name}...")
        
        with open(archive_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        chapter = data.get('chapter', chapter_num)
        slokas = data.get('slokas', {})
        
        for sloka_id, translations in slokas.items():
            # Handle combined slokas (e.g., "1.4-6")
            sloka_num = sloka_id
            
            for lang, trans_data in translations.items():
                if lang not in stats:
                    continue
                
                # Handle both formats: {"text": "...", "approved": false} and direct string
                if isinstance(trans_data, dict):
                    text = trans_data.get('text', '')
                else:
                    text = trans_data
                
                if not text:
                    continue
                
                # Create directory
                lang_dir = TRANSLATED_DIR / lang / f"chapter-{chapter_str}-{lang}"
                lang_dir.mkdir(parents=True, exist_ok=True)
                
                # Write sloka file
                sloka_file = lang_dir / f"chapter-{chapter_str}-{sloka_num}-{lang}_sloka.txt"
                
                if dry_run:
                    print(f"    Would create: {sloka_file}")
                else:
                    with open(sloka_file, 'w', encoding='utf-8') as f:
                        f.write(text)
                
                stats[lang] += 1
    
    return stats


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Restore translations from archive')
    parser.add_argument('--chapter', type=int, help='Specific chapter to restore (1-18)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    
    args = parser.parse_args()
    
    chapters = range(1, 19)
    if args.chapter:
        chapters = [args.chapter]
    
    print(f"Restoring translations from archive...")
    if args.dry_run:
        print(f"(DRY RUN - no files will be written)")
    print("=" * 60)
    
    total_stats = {lang: 0 for lang in ASIAN_LANGS + OTHER_LANGS}
    
    for chapter in chapters:
        print(f"\nChapter {chapter}:")
        stats = restore_translations(chapter, dry_run=args.dry_run)
        
        for lang, count in stats.items():
            total_stats[lang] += count
            if count > 0:
                print(f"  {lang}: {count} slokas")
    
    print("\n" + "=" * 60)
    print("Summary:")
    grand_total = 0
    for lang, count in sorted(total_stats.items()):
        if count > 0:
            print(f"  {lang}: {count} files")
            grand_total += count
    print(f"  TOTAL: {grand_total} files")


if __name__ == '__main__':
    main()
