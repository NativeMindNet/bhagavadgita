#!/usr/bin/env python3
"""
Combined Translation Script for Chapter Slokas + Vocabulary.

Translates:
- Chapter slokas (RU/EN/DE/ES) → ko, th, zh-CN, zh-TW, ja
- Vocabulary meanings (RU/EN) → ko, th, zh-CN, zh-TW, ja
- Vocabulary transliteration → th, zh-CN, zh-TW, ko, ja

Outputs:
- data/chapters/chapter-XX-asian-translations.json (slokas overlay)
- data/vocabulary/vocab_XX.json (updated with translations + transliteration)
"""

import json
import os
from pathlib import Path
from datetime import datetime

# Paths
BASE_DIR = Path(__file__).parent.parent
CHAPTERS_DIR = BASE_DIR / 'data' / 'chapters'
VOCAB_DIR = BASE_DIR / 'data' / 'vocabulary'
OUTPUT_DIR = BASE_DIR / 'data' / 'translations'

def load_json(filepath):
    """Load JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    """Save JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def extract_chapter_for_translation(chapter_num):
    """Extract chapter slokas and vocabulary for translation."""
    
    # Load chapter
    chapter_file = CHAPTERS_DIR / f'chapter-{chapter_num:02d}.json'
    chapter = load_json(chapter_file)
    
    # Load vocabulary
    vocab_file = VOCAB_DIR / f'vocab_{chapter_num:02d}.json'
    vocab = load_json(vocab_file)
    
    # Extract chapter title
    title_data = {
        "sanskrit": chapter['title'].get('sanskrit', ''),
        "transliteration": chapter['title'].get('transliteration', ''),
        "ru": chapter['title'].get('ru', {}).get('text', ''),
        "en": chapter['title'].get('en', {}).get('text', ''),
        "de": chapter['title'].get('de', {}).get('text', ''),
        "es": chapter['title'].get('es', {}).get('text', '')
    }
    
    # Extract slokas
    slokas = []
    for sloka in chapter['slokas']:
        sloka_data = {
            "number": sloka['number'],
            "order": sloka['order'],
            "sanskrit": sloka.get('sanskrit', ''),
            "transliteration": sloka.get('transliteration', ''),
            "translations": {},
            "comment": sloka.get('comment', {}),
            "vocabulary": sloka.get('vocabulary', [])
        }
        
        # Extract existing translations
        for lang in ['ru', 'en', 'de', 'es']:
            if lang in sloka.get('translations', {}):
                sloka_data['translations'][lang] = sloka['translations'][lang].get('text', '')
        
        slokas.append(sloka_data)
    
    # Extract vocabulary
    vocab_list = []
    for v in vocab['vocabulary']:
        vocab_data = {
            "id": v['id'],
            "slokaId": v['slokaId'],
            "word": v['word'],
            "transliteration": v.get('transliteration', {}),
            "meaning": {}
        }
        
        # Extract existing meanings
        for lang in ['ru', 'en']:
            if lang in v.get('meaning', {}):
                vocab_data['meaning'][lang] = v['meaning'][lang].get('text', '')
        
        vocab_list.append(vocab_data)
    
    return {
        "chapter": chapter_num,
        "title": title_data,
        "slokas": slokas,
        "vocabulary": vocab_list,
        "meta": {
            "totalSlokas": len(slokas),
            "totalWords": len(vocab_list)
        }
    }

def format_translation_prompt(batch_data):
    """Format translation prompt for Claude."""
    
    chapter_num = batch_data['chapter']
    
    prompt = f"""═══════════════════════════════════════════════════════════════
CHAPTER {chapter_num} TRANSLATION BATCH
═══════════════════════════════════════════════════════════════

TARGET LANGUAGES: Korean (ko), Thai (th), Chinese Simplified (zh-CN), 
                  Chinese Traditional (zh-TW), Japanese (ja)

═══════════════════════════════════════════════════════════════
PART 1: CHAPTER TITLE
═══════════════════════════════════════════════════════════════

[RU] {batch_data['title']['ru']}
[EN] {batch_data['title']['en']}
[DE] {batch_data['title']['de']}
[ES] {batch_data['title']['es']}

Translate title to: ko, th, zh-CN, zh-TW, ja

═══════════════════════════════════════════════════════════════
PART 2: SLOKAS ({len(batch_data['slokas'])} slokas)
═══════════════════════════════════════════════════════════════

For each sloka, translate the text to ko, th, zh-CN, zh-TW, ja.
Use RU/EN as primary sources. DE/ES for additional context.

"""
    
    # Add first 5 slokas as examples (to avoid huge prompt)
    for sloka in batch_data['slokas'][:5]:
        prompt += f"""
---
Sloka {sloka['number']}:
[RU] {sloka['translations'].get('ru', '')[:200]}
[EN] {sloka['translations'].get('en', '')[:200]}
"""
    
    if len(batch_data['slokas']) > 5:
        prompt += f"\n... ({len(batch_data['slokas']) - 5} more slokas)\n"
    
    prompt += f"""
═══════════════════════════════════════════════════════════════
PART 3: VOCABULARY ({len(batch_data['vocabulary'])} words)
═══════════════════════════════════════════════════════════════

For each vocabulary word:
1. Translate meaning to ko, th, zh-CN, zh-TW, ja
2. Add transliteration in target scripts:
   - Thai: Thai script transliteration
   - Chinese: Pinyin
   - Korean: Hangul transliteration
   - Japanese: Romaji + Kana

Sample vocabulary:
"""
    
    # Add first 10 vocabulary words as examples
    for v in batch_data['vocabulary'][:10]:
        prompt += f"""
Word: {v['word']}
[RU] {v['meaning'].get('ru', '')}
[EN] {v['meaning'].get('en', '')}
"""
    
    if len(batch_data['vocabulary']) > 10:
        prompt += f"\n... ({len(batch_data['vocabulary']) - 10} more words)\n"
    
    prompt += """
═══════════════════════════════════════════════════════════════
OUTPUT FORMAT:

Return JSON in this format:
{
  "chapterTitle": {
    "ko": "...",
    "th": "...",
    "zh-CN": "...",
    "zh-TW": "...",
    "ja": "..."
  },
  "slokas": {
    "1.1": {
      "ko": "...",
      "th": "...",
      "zh-CN": "...",
      "zh-TW": "...",
      "ja": "..."
    },
    ...
  },
  "vocabulary": {
    "1": {
      "meaning": {
        "ko": "...",
        "th": "...",
        "zh-CN": "...",
        "zh-TW": "...",
        "ja": "..."
      },
      "transliteration": {
        "th": "...",
        "zh-CN": "...",
        "ko": "...",
        "ja": "..."
      }
    },
    ...
  }
}
═══════════════════════════════════════════════════════════════
"""
    
    return prompt

def save_translations(chapter_num, translations, batch_data):
    """Save translations to output files."""
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Save chapter translation overlay
    chapter_overlay = {
        "chapter": chapter_num,
        "meta": {
            "lastUpdated": datetime.now().isoformat(),
            "version": "1.0",
            "source": "SM/SCSM/ШМ/ШЧСМ",
            "languages": ["ko", "th", "zh-CN", "zh-TW", "ja"]
        },
        "title": translations.get('chapterTitle', {}),
        "slokas": []
    }
    
    # Map sloka translations
    sloka_trans = translations.get('slokas', {})
    for sloka in batch_data['slokas']:
        sloka_num = sloka['number']
        trans = sloka_trans.get(sloka_num, {})
        
        overlay_sloka = {
            "number": sloka_num,
            "order": sloka['order'],
            "translations": {}
        }
        
        for lang in ['ko', 'th', 'zh-CN', 'zh-TW', 'ja']:
            if lang in trans:
                overlay_sloka['translations'][lang] = {
                    "text": trans[lang],
                    "approved": False
                }
        
        chapter_overlay['slokas'].append(overlay_sloka)
    
    chapter_overlay_file = CHAPTERS_DIR / f'chapter-{chapter_num:02d}-asian-translations.json'
    save_json(chapter_overlay_file, chapter_overlay)
    print(f"  Saved: {chapter_overlay_file}")
    
    # 2. Update vocabulary file
    vocab_file = VOCAB_DIR / f'vocab_{chapter_num:02d}.json'
    vocab = load_json(vocab_file)
    
    vocab_trans = translations.get('vocabulary', {})
    for v in vocab['vocabulary']:
        vocab_id = str(v['id'])
        trans = vocab_trans.get(vocab_id, {})
        
        # Update meaning
        for lang in ['ko', 'th', 'zh-CN', 'zh-TW', 'ja']:
            if lang in trans.get('meaning', {}):
                v['meaning'][lang] = {
                    "text": trans['meaning'][lang],
                    "approved": False
                }
        
        # Update transliteration
        if 'transliteration' in trans:
            for lang in ['th', 'zh-CN', 'zh-TW', 'ko', 'ja']:
                if lang in trans['transliteration']:
                    v['transliteration'][lang] = trans['transliteration'][lang]
    
    save_json(vocab_file, vocab)
    print(f"  Updated: {vocab_file}")

def translate_chapter(chapter_num):
    """Translate a single chapter with vocabulary."""
    
    print(f"\n{'='*60}")
    print(f"Translating Chapter {chapter_num}")
    print(f"{'='*60}")
    
    # Extract data
    print("  Extracting chapter data...")
    batch_data = extract_chapter_for_translation(chapter_num)
    print(f"  Slokas: {batch_data['meta']['totalSlokas']}")
    print(f"  Vocabulary: {batch_data['meta']['totalWords']}")
    
    # Format prompt
    print("  Formatting translation prompt...")
    prompt = format_translation_prompt(batch_data)
    
    # Save prompt for manual translation (or send to API)
    prompt_file = OUTPUT_DIR / f'chapter-{chapter_num:02d}-prompt.txt'
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt)
    print(f"  Saved prompt: {prompt_file}")
    
    # NOTE: In production, this would call Claude API
    # For now, we save the prompt for manual translation
    print(f"  → Translate using Claude and save to chapter-{chapter_num:02d}-translations.json")
    
    return batch_data

def main():
    """Main entry point."""
    print("="*60)
    print("Combined Translation Script")
    print("Chapter Slokas + Vocabulary")
    print("="*60)
    
    # Translate chapters 1-18
    for chapter_num in range(1, 19):
        translate_chapter(chapter_num)
    
    print("\n" + "="*60)
    print("Phase 3 Preparation Complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Review prompts in data/translations/")
    print("2. Translate using Claude (manual or API)")
    print("3. Save translations as chapter-XX-translations.json")
    print("4. Run: python scripts/apply_translations.py chapter-XX")

if __name__ == '__main__':
    main()
