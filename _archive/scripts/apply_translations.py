#!/usr/bin/env python3
"""
Apply translations to chapter and vocabulary files.

Usage: python scripts/apply_translations.py <chapter_num>

Example: python scripts/apply_translations.py 1
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Paths
BASE_DIR = Path(__file__).parent.parent
CHAPTERS_DIR = BASE_DIR / 'data' / 'chapters'
VOCAB_DIR = BASE_DIR / 'data' / 'vocabulary'
TRANSLATIONS_DIR = BASE_DIR / 'data' / 'translations'

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def apply_translations(chapter_num):
    """Apply translations for a chapter."""
    
    print(f"\n{'='*60}")
    print(f"Applying translations for Chapter {chapter_num}")
    print(f"{'='*60}")
    
    # Load translation file
    translation_file = TRANSLATIONS_DIR / f'chapter-{chapter_num:02d}-translations.json'
    if not translation_file.exists():
        print(f"ERROR: Translation file not found: {translation_file}")
        print(f"Please translate the prompt first and save as {translation_file.name}")
        return False
    
    translations = load_json(translation_file)
    print(f"  Loaded translations from {translation_file.name}")
    
    # 1. Update chapter asian translations overlay
    chapter_overlay_file = CHAPTERS_DIR / f'chapter-{chapter_num:02d}-asian-translations.json'
    
    if chapter_overlay_file.exists():
        chapter_overlay = load_json(chapter_overlay_file)
    else:
        chapter_overlay = {
            "chapter": chapter_num,
            "meta": {
                "lastUpdated": datetime.now().isoformat(),
                "version": "1.0",
                "source": "SM/SCSM/ШМ/ШЧСМ",
                "languages": ["ko", "th", "zh-CN", "zh-TW", "ja"]
            },
            "title": {},
            "slokas": []
        }
    
    # Update title
    if 'chapterTitle' in translations:
        chapter_overlay['title'] = {}
        for lang in ['ko', 'th', 'zh-CN', 'zh-TW', 'ja']:
            if lang in translations['chapterTitle']:
                chapter_overlay['title'][lang] = {
                    "text": translations['chapterTitle'][lang],
                    "approved": False
                }
    
    # Update slokas
    sloka_trans = translations.get('slokas', {})
    for sloka_num, trans in sloka_trans.items():
        # Find or create sloka entry
        sloka_entry = next((s for s in chapter_overlay['slokas'] if s['number'] == sloka_num), None)
        
        if not sloka_entry:
            sloka_entry = {
                "number": sloka_num,
                "order": 0,
                "translations": {}
            }
            chapter_overlay['slokas'].append(sloka_entry)
        
        # Add translations
        for lang in ['ko', 'th', 'zh-CN', 'zh-TW', 'ja']:
            if lang in trans:
                sloka_entry['translations'][lang] = {
                    "text": trans[lang],
                    "approved": False
                }
    
    save_json(chapter_overlay_file, chapter_overlay)
    print(f"  Updated: {chapter_overlay_file}")
    
    # 2. Update vocabulary file
    vocab_file = VOCAB_DIR / f'vocab_{chapter_num:02d}.json'
    if not vocab_file.exists():
        print(f"ERROR: Vocabulary file not found: {vocab_file}")
        return False
    
    vocab = load_json(vocab_file)
    
    vocab_trans = translations.get('vocabulary', {})
    updated_count = 0
    
    for v in vocab['vocabulary']:
        vocab_id = str(v['id'])
        trans = vocab_trans.get(vocab_id, {})
        
        # Update meaning
        if 'meaning' in trans:
            for lang in ['ko', 'th', 'zh-CN', 'zh-TW', 'ja']:
                if lang in trans['meaning']:
                    v['meaning'][lang] = {
                        "text": trans['meaning'][lang],
                        "approved": False
                    }
                    updated_count += 1
        
        # Update transliteration
        if 'transliteration' in trans:
            for lang in ['th', 'zh-CN', 'zh-TW', 'ko', 'ja']:
                if lang in trans['transliteration']:
                    v['transliteration'][lang] = trans['transliteration'][lang]
    
    save_json(vocab_file, vocab)
    print(f"  Updated: {vocab_file} ({updated_count} translations added)")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Chapter {chapter_num} Translation Complete!")
    print(f"{'='*60}")
    print(f"  Title translations: 5 languages")
    print(f"  Sloka translations: {len(sloka_trans)} slokas × 5 languages")
    print(f"  Vocabulary translations: {updated_count} words × 5 languages")
    print(f"  Transliteration: Thai, Chinese, Korean, Japanese")
    print(f"\n  All translations marked as 'approved: false' - review required")
    
    return True

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python scripts/apply_translations.py <chapter_num>")
        print("Example: python scripts/apply_translations.py 1")
        sys.exit(1)
    
    chapter_num = int(sys.argv[1])
    apply_translations(chapter_num)
