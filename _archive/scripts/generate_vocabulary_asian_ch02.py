#!/usr/bin/env python3
"""
Generate vocabulary-asian.json for Chapter 2.
Translates vocabulary meanings from RU/EN to th, zh-TW, ja, ko.
Also generates transliterations.
"""

import json
from pathlib import Path
from datetime import datetime

# Paths
BASE_DIR = Path(__file__).parent.parent
INPUT_FILE = BASE_DIR / 'data' / 'chapters' / 'ch-02' / 'vocabulary-source.json'
OUTPUT_FILE = BASE_DIR / 'data' / 'chapters' / 'ch-02' / 'vocabulary-asian.json'

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Translation mappings for common Sanskrit terms and philosophical concepts
# These are standard translations used in Bhagavad Gita translations

COMMON_TERMS = {
    # Sanskrit terms that stay similar across languages
    "bhagavad": {"th": "พระภควาน", "zh-TW": "巴嘎萬", "ja": "バガヴァン", "ko": "바가반"},
    "ārādhane": {"th": "การบูชา", "zh-TW": "崇拜", "ja": "崇拝", "ko": "숭배"},
    "Supreme Lord": {"th": "พระผู้เป็นเจ้าสูงสุด", "zh-TW": "至尊主", "ja": "至高なる主", "ko": "지고하신 주"},
    "Arjuna": {"th": "อรชุน", "zh-TW": "阿周那", "ja": "アルジュナ", "ko": "아르주나"},
    "Kuntī": {"th": "กุนตี", "zh-TW": "貢蒂", "ja": "クンティー", "ko": "쿤티"},
    "kuru": {"th": "กุรุ", "zh-TW": "俱盧", "ja": "クル", "ko": "쿠루"},
    "nandana": {"th": "นันทน", "zh-TW": "難陀那", "ja": "ナンダナ", "ko": "난다나"},
    "he": {"th": "โอ้", "zh-TW": "哦", "ja": "おお", "ko": "오"},
    "O": {"th": "โอ้", "zh-TW": "哦", "ja": "おお", "ko": "오"},
    "son of": {"th": "บุตรของ", "zh-TW": "之子", "ja": "〜の子", "ko": "〜의 아들"},
    "worshipping": {"th": "การบูชา", "zh-TW": "崇拜", "ja": "崇拝すること", "ko": "숭배하는"},
    "by worshipping": {"th": "โดยการบูชา", "zh-TW": "通過崇拜", "ja": "崇拝することによって", "ko": "숭배함으로써"},
}

def translate_meaning(ru_text, en_text):
    """
    Translate meaning from RU/EN to th, zh-TW, ja, ko.
    Uses English as primary source, Russian for context.
    """
    # Use English as primary source
    source_text = en_text if en_text else ru_text
    
    if not source_text:
        return {
            "th": "",
            "zh-TW": "",
            "ja": "",
            "ko": ""
        }
    
    # Check for common terms first
    for term, translations in COMMON_TERMS.items():
        if term.lower() in source_text.lower():
            # Partial match - will be handled in full translation
            pass
    
    # Generate translations based on the source text
    # This is a simplified version - in production, this would call an API
    translations = generate_translations(source_text)
    
    return translations

def generate_translations(text):
    """Generate translations for a given text."""
    # This is a placeholder that would be replaced with actual translation logic
    # For now, return empty translations
    return {
        "th": "",
        "zh-TW": "",
        "ja": "",
        "ko": ""
    }

def generate_transliteration(word):
    """Generate transliteration for a Sanskrit word."""
    # This is a placeholder
    return {
        "th": "",
        "zh-TW": "",
        "ja": "",
        "ko": ""
    }

def main():
    print("Loading vocabulary source...")
    source_data = load_json(INPUT_FILE)
    
    print(f"Processing {len(source_data['vocabulary'])} words...")
    
    output_data = {
        "chapter": 2,
        "meta": {
            "source": str(INPUT_FILE),
            "generated": datetime.now().strftime("%Y-%m-%d"),
            "languages": ["th", "zh-TW", "ja", "ko"],
            "approved": False
        },
        "vocabulary": {}
    }
    
    for vocab_item in source_data['vocabulary']:
        vocab_id = str(vocab_item['id'])
        word = vocab_item['word']
        
        # Get Russian and English meanings
        ru_meaning = vocab_item['meaning'].get('ru', {}).get('text', '')
        en_meaning = vocab_item['meaning'].get('en', {}).get('text', '')
        
        # Generate translations
        translated_meaning = translate_meaning(ru_meaning, en_meaning)
        
        # Generate transliteration
        transliteration = generate_transliteration(word)
        
        output_data['vocabulary'][vocab_id] = {
            "meaning": translated_meaning,
            "transliteration": transliteration
        }
    
    print(f"Saving to {OUTPUT_FILE}...")
    save_json(OUTPUT_FILE, output_data)
    print("Done!")

if __name__ == '__main__':
    main()
