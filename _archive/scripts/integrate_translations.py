#!/usr/bin/env python3
"""
Integrate Asian language translations into chapter JSON files.
"""

import json
import sys

def integrate_translations(chapter_file, translations_file):
    # Load the chapter file
    with open(chapter_file, 'r', encoding='utf-8') as f:
        chapter = json.load(f)
    
    # Load the translations
    with open(translations_file, 'r', encoding='utf-8') as f:
        translations = json.load(f)
    
    # Update chapter title
    chapter['title']['ko'] = {"text": translations['chapterTitle']['ko'], "approved": False}
    chapter['title']['th'] = {"text": translations['chapterTitle']['th'], "approved": False}
    chapter['title']['zh-CN'] = {"text": translations['chapterTitle']['zh-CN'], "approved": False}
    chapter['title']['zh-TW'] = {"text": translations['chapterTitle']['zh-TW'], "approved": False}
    
    # Create a mapping of sloka number to sloka object
    sloka_map = {sloka['number']: sloka for sloka in chapter['slokas']}
    
    # Integrate translations for each sloka
    for sloka_number, trans in translations['slokas'].items():
        if sloka_number in sloka_map:
            sloka = sloka_map[sloka_number]
            
            # Add translations for each language
            for lang_code in ['ko', 'th', 'zh-CN', 'zh-TW']:
                if lang_code not in sloka['translations']:
                    sloka['translations'][lang_code] = {
                        "text": trans[lang_code],
                        "approved": False
                    }
        else:
            print(f"Warning: Sloka {sloka_number} not found in chapter file")
    
    # Update meta
    chapter['meta']['lastUpdated'] = "2026-03-26T12:00:00Z"
    chapter['meta']['version'] = "1.1"
    
    # Save the updated chapter
    with open(chapter_file, 'w', encoding='utf-8') as f:
        json.dump(chapter, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully integrated translations into {chapter_file}")
    
    # Count added translations
    new_langs = 4
    total_slokas = len(translations['slokas'])
    print(f"Added {new_langs} languages to {total_slokas} slokas")
    print(f"Total new translations: {new_langs * total_slokas}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python integrate_translations.py <chapter.json> <translations.json>")
        sys.exit(1)
    
    integrate_translations(sys.argv[1], sys.argv[2])
