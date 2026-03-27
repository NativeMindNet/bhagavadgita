#!/usr/bin/env python3
"""
Automated Sequential Translation via Agent.

Translates all 18 chapters sequentially:
1. Extract chapter data
2. Launch translation agent for chapter
3. Save results immediately
4. Validate and continue to next chapter

Usage: python scripts/auto_translate_all.py
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Paths
BASE_DIR = Path(__file__).parent.parent
CHAPTERS_DIR = BASE_DIR / 'data' / 'chapters'
VOCAB_DIR = BASE_DIR / 'data' / 'vocabulary'
TRANSLATIONS_DIR = BASE_DIR / 'data' / 'translations'

# Ensure output directory exists
TRANSLATIONS_DIR.mkdir(parents=True, exist_ok=True)

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def extract_chapter_data(chapter_num):
    """Extract chapter slokas and vocabulary for translation."""
    
    # Load chapter
    chapter_file = CHAPTERS_DIR / f'chapter-{chapter_num:02d}.json'
    if not chapter_file.exists():
        print(f"  ERROR: Chapter file not found: {chapter_file}")
        return None
    chapter = load_json(chapter_file)
    
    # Load vocabulary
    vocab_file = VOCAB_DIR / f'vocab_{chapter_num:02d}.json'
    if not vocab_file.exists():
        print(f"  ERROR: Vocabulary file not found: {vocab_file}")
        return None
    vocab = load_json(vocab_file)
    
    # Extract title
    title_data = {
        "sanskrit": chapter['title'].get('sanskrit', ''),
        "transliteration": chapter['title'].get('transliteration', ''),
        "ru": chapter['title'].get('ru', {}).get('text', ''),
        "en": chapter['title'].get('en', {}).get('text', ''),
        "de": chapter['title'].get('de', {}).get('text', ''),
        "es": chapter['title'].get('es', {}).get('text', '')
    }
    
    # Extract slokas (limit to first 5 for agent context)
    slokas = []
    for sloka in chapter['slokas'][:5]:  # Sample for context
        sloka_data = {
            "number": sloka['number'],
            "sanskrit": sloka.get('sanskrit', '')[:100],
            "ru": sloka.get('translations', {}).get('ru', {}).get('text', '')[:200],
            "en": sloka.get('translations', {}).get('en', {}).get('text', '')[:200]
        }
        slokas.append(sloka_data)
    
    # Extract vocabulary (limit to first 20 for agent context)
    vocab_list = []
    for v in vocab['vocabulary'][:20]:  # Sample for context
        vocab_data = {
            "id": v['id'],
            "word": v['word'],
            "ru": v.get('meaning', {}).get('ru', {}).get('text', '')[:100],
            "en": v.get('meaning', {}).get('en', {}).get('text', '')[:100]
        }
        vocab_list.append(vocab_data)
    
    return {
        "chapter": chapter_num,
        "title": title_data,
        "slokas_sample": slokas,
        "vocabulary_sample": vocab_list,
        "meta": {
            "totalSlokas": len(chapter['slokas']),
            "totalWords": len(vocab['vocabulary'])
        }
    }

def translate_chapter_via_agent(chapter_num, chapter_data):
    """
    Launch agent to translate a chapter.
    Returns translations dict or None on failure.
    """
    
    print(f"\n{'='*60}")
    print(f"CHAPTER {chapter_num}: Launching Translation Agent")
    print(f"{'='*60}")
    print(f"  Slokas: {chapter_data['meta']['totalSlokas']}")
    print(f"  Vocabulary: {chapter_data['meta']['totalWords']}")
    
    # Create agent prompt
    prompt = f"""You are a professional translator specializing in religious and philosophical texts.

TASK: Translate Chapter {chapter_num} of the Bhagavad Gita into 5 Asian languages:
- Korean (ko)
- Thai (th)  
- Chinese Simplified (zh-CN)
- Chinese Traditional (zh-TW)
- Japanese (ja)

SOURCE PRIORITY:
1. Russian (ru) - primary source for meaning
2. English (en) - secondary source
3. German (de), Spanish (es) - additional context
4. Sanskrit - ONLY for term accuracy (names, places)

TRANSLATION REQUIREMENTS:

1. CHAPTER TITLE:
   - RU: {chapter_data['title']['ru']}
   - EN: {chapter_data['title']['en']}
   Translate to: ko, th, zh-CN, zh-TW, ja

2. SLOKAS ({chapter_data['meta']['totalSlokas']} total):
   Translate each sloka text to: ko, th, zh-CN, zh-TW, ja
   
3. VOCABULARY ({chapter_data['meta']['totalWords']} words):
   For each vocabulary word:
   a) Translate meaning to: ko, th, zh-CN, zh-TW, ja
   b) Add transliteration in target scripts:
      - Thai: Thai script
      - Chinese: Pinyin
      - Korean: Hangul
      - Japanese: Romaji + Kana

SAMPLE DATA (for context):

Chapter Title:
[RU] {chapter_data['title']['ru']}
[EN] {chapter_data['title']['en']}

Sample Slokas (first 5 of {chapter_data['meta']['totalSlokas']}):
{chr(10).join(f"- {s['number']}: [RU] {s['ru'][:100]}" for s in chapter_data['slokas_sample'][:3])}

Sample Vocabulary (first 20 of {chapter_data['meta']['totalWords']}):
{chr(10).join(f"- {v['word']}: [RU] {v['ru'][:80]}" for v in chapter_data['vocabulary_sample'][:5])}

OUTPUT FORMAT:

Return a JSON object with this exact structure:

```json
{{
  "chapterTitle": {{
    "ko": "...",
    "th": "...",
    "zh-CN": "...",
    "zh-TW": "...",
    "ja": "..."
  }},
  "slokas": {{
    "1.1": {{
      "ko": "...",
      "th": "...",
      "zh-CN": "...",
      "zh-TW": "...",
      "ja": "..."
    }},
    "1.2": {{ ... }},
    ...
  }},
  "vocabulary": {{
    "1": {{
      "meaning": {{
        "ko": "...",
        "th": "...",
        "zh-CN": "...",
        "zh-TW": "...",
        "ja": "..."
      }},
      "transliteration": {{
        "th": "...",
        "zh-CN": "...",
        "ko": "...",
        "ja": "..."
      }}
    }},
    ...
  }}
}}
```

IMPORTANT:
- Translate ALL {chapter_data['meta']['totalSlokas']} slokas
- Translate ALL {chapter_data['meta']['totalWords']} vocabulary words
- Use formal, reverent tone appropriate for sacred scripture
- Preserve proper nouns with appropriate transliteration
- Return ONLY the JSON object, no additional text
"""
    
    # Save prompt for reference
    prompt_file = TRANSLATIONS_DIR / f'chapter-{chapter_num:02d}-agent-prompt.txt'
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt)
    
    print(f"  Prompt saved: {prompt_file.name}")
    print(f"  → Launching agent...")
    
    # NOTE: In a real implementation, this would call an agent API
    # For this demo, we'll create a placeholder result
    # The actual agent call would be something like:
    # result = call_translation_agent(prompt)
    
    # For demonstration, return None to indicate manual translation needed
    print(f"  ⚠ AGENT INTEGRATION REQUIRED")
    print(f"  To complete translation, send prompt to translation agent API")
    print(f"  Save result as: chapter-{chapter_num:02d}-translations.json")
    
    return None

def save_translations(chapter_num, translations, chapter_data):
    """Save translations to output files."""
    
    if not translations:
        print(f"  SKIP: No translations to save")
        return False
    
    print(f"  Saving translations...")
    
    # 1. Save chapter translation overlay
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
    
    # Map title translations
    if 'chapterTitle' in translations:
        for lang in ['ko', 'th', 'zh-CN', 'zh-TW', 'ja']:
            if lang in translations['chapterTitle']:
                chapter_overlay['title'][lang] = {
                    "text": translations['chapterTitle'][lang],
                    "approved": False
                }
    
    # Map sloka translations
    sloka_trans = translations.get('slokas', {})
    for sloka_num, trans in sloka_trans.items():
        overlay_sloka = {
            "number": sloka_num,
            "order": 0,
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
    print(f"    Saved: {chapter_overlay_file.name}")
    
    # 2. Update vocabulary file
    vocab_file = VOCAB_DIR / f'vocab_{chapter_num:02d}.json'
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
    print(f"    Updated: {vocab_file.name} ({updated_count} translations)")
    
    return True

def validate_translations(chapter_num):
    """Validate translation files."""
    
    print(f"  Validating...")
    
    # Check chapter overlay
    chapter_overlay_file = CHAPTERS_DIR / f'chapter-{chapter_num:02d}-asian-translations.json'
    if chapter_overlay_file.exists():
        try:
            load_json(chapter_overlay_file)
            print(f"    ✓ Chapter overlay valid")
        except Exception as e:
            print(f"    ✗ Chapter overlay invalid: {e}")
            return False
    else:
        print(f"    ✗ Chapter overlay not found")
        return False
    
    # Check vocabulary
    vocab_file = VOCAB_DIR / f'vocab_{chapter_num:02d}.json'
    if vocab_file.exists():
        try:
            load_json(vocab_file)
            print(f"    ✓ Vocabulary valid")
        except Exception as e:
            print(f"    ✗ Vocabulary invalid: {e}")
            return False
    else:
        print(f"    ✗ Vocabulary not found")
        return False
    
    return True

def translate_all_chapters():
    """Translate all 18 chapters sequentially."""
    
    print("="*60)
    print("AUTOMATED SEQUENTIAL TRANSLATION")
    print("Bhagavad Gita Vocabulary + Slokas")
    print("="*60)
    
    results = {
        "started": datetime.now().isoformat(),
        "chapters": {},
        "completed": 0,
        "failed": 0
    }
    
    for chapter_num in range(1, 19):
        print(f"\n{'='*60}")
        print(f"CHAPTER {chapter_num}/18")
        print(f"{'='*60}")
        
        # Extract chapter data
        print("  Extracting chapter data...")
        chapter_data = extract_chapter_data(chapter_num)
        
        if not chapter_data:
            print(f"  ✗ FAILED: Could not extract chapter data")
            results["chapters"][chapter_num] = "FAILED: Extract"
            results["failed"] += 1
            continue
        
        # Translate via agent
        translations = translate_chapter_via_agent(chapter_num, chapter_data)
        
        if not translations:
            print(f"  ⚠ SKIPPED: Agent translation not available")
            results["chapters"][chapter_num] = "SKIPPED: No agent"
            # Continue to next chapter (in real implementation, would retry or fail)
            results["failed"] += 1
            continue
        
        # Save translations
        if not save_translations(chapter_num, translations, chapter_data):
            print(f"  ✗ FAILED: Could not save translations")
            results["chapters"][chapter_num] = "FAILED: Save"
            results["failed"] += 1
            continue
        
        # Validate
        if not validate_translations(chapter_num):
            print(f"  ✗ FAILED: Validation failed")
            results["chapters"][chapter_num] = "FAILED: Validation"
            results["failed"] += 1
            continue
        
        print(f"  ✓ COMPLETE")
        results["chapters"][chapter_num] = "SUCCESS"
        results["completed"] += 1
    
    # Summary
    results["completed_at"] = datetime.now().isoformat()
    
    print(f"\n{'='*60}")
    print("TRANSLATION COMPLETE")
    print(f"{'='*60}")
    print(f"  Completed: {results['completed']}/18 chapters")
    print(f"  Failed: {results['failed']}/18 chapters")
    print(f"  Started: {results['started']}")
    print(f"  Finished: {results['completed_at']}")
    
    # Save results
    results_file = TRANSLATIONS_DIR / 'translation-results.json'
    save_json(results_file, results)
    print(f"\n  Results saved: {results_file.name}")
    
    return results["completed"] == 18

if __name__ == '__main__':
    success = translate_all_chapters()
    sys.exit(0 if success else 1)
