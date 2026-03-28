#!/usr/bin/env python3
"""
Generate chapter-other.json for chapters 1-6.
Translates chapter titles and slokas to he, ar, tr, sw.
"""

import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent

# Translation mappings for common Bhagavad Gita terms
TERM_TRANSLATIONS = {
    # Chapter titles
    "Observing the Armies": {"he": "צפייה בצבאות", "ar": "مراقبة الجيوش", "tr": "Orduları Gözlemlemek", "sw": "Kuangalia Jeshi"},
    "Sāṅkhya Yoga": {"he": "סאנקיה יוגה", "ar": "يوغا سانكيا", "tr": "Sāṅkhya Yoga", "sw": "Yoga ya Sāṅkhya"},
    "Karma Yoga": {"he": "קרמה יוגה", "ar": "يوغا الكرمة", "tr": "Karma Yoga", "sw": "Yoga ya Karma"},
    "Jñāna Yoga": {"he": "ג'נאנה יוגה", "ar": "يوغا الجنانا", "tr": "Jñāna Yoga", "sw": "Yoga ya Jñāna"},
    "Karma Sanyāsa Yoga": {"he": "קרמה סניאסה יוגה", "ar": "يوغا التخلي عن العمل", "tr": "Karma Sanyāsa Yoga", "sw": "Yoga ya Kutupa Vitendo"},
    "Dhyāna Yoga": {"he": "דהיאנה יוגה", "ar": "يوغا التأمل", "tr": "Dhyāna Yoga", "sw": "Yoga ya Kutafakari"},
    
    # Common sloka phrases
    "Dhṛtarāṣṭra said": {"he": "דריטראשטרה אמר", "ar": "قال دريتاراشترا", "tr": "Dhṛtarāṣṭra dedi", "sw": "Dhṛtarāṣṭra alisema"},
    "O Sañjaya": {"he": "הו סנג'איה", "ar": "يا سنجاي", "tr": "Ey Sañjaya", "sw": "Ewe Sañjaya"},
    "what happened": {"he": "מה קרה", "ar": "ماذا حدث", "tr": "ne oldu", "sw": "niliyotokea"},
    "when my sons": {"he": "כאשר בניי", "ar": "عندما أبنائي", "tr": "oğullarım", "sw": "wajao wangu"},
    "and the sons of Pāṇḍu": {"he": "ובני פאנדו", "ar": "وأبناء باندو", "tr": "ve Pāṇḍu'nun oğulları", "sw": "na wana wa Pāṇḍu"},
    "assembled for battle": {"he": "התאספו לקרב", "ar": "تجمعوا للمعركة", "tr": "savaş için toplandılar", "sw": "walikusanyika kwa ajili ya vita"},
    "at the holy place": {"he": "במקום הקדוש", "ar": "في المكان المقدس", "tr": "kutsal yerde", "sw": "katika mahali patakatifu"},
    "of Kurukṣetra": {"he": "של קורוקשטרה", "ar": "من كوروكشيترا", "tr": "Kurukṣetra'da", "sw": "ya Kurukṣetra"},
    
    "The Supreme Lord said": {"he": "האדון העליון אמר", "ar": "قال الرب الأعلى", "tr": "Yüce Rab dedi", "sw": "Bwana Mkuu alisema"},
    "O son of Kuntī": {"he": "הו בן קונטי", "ar": "يا ابن كونتي", "tr": "Ey Kuntī oğlu", "sw": "Ewe mwana wa Kuntī"},
    "O Arjuna": {"he": "הו ארג'ונה", "ar": "يا أرجونا", "tr": "Ey Arjuna", "sw": "Ewe Arjuna"},
    "O descendant of Bharata": {"he": "הו צאצא בהראטה", "ar": "يا سلالة بهاراتا", "tr": "Ey Bharata soyundan gelen", "sw": "Ewe mzao wa Bharata"},
    "O mighty-armed one": {"he": "הו רב-עוצמה", "ar": "يا قوي الذراعين", "tr": "Ey güçlü kollu", "sw": "Ewe mwenye mikono mikuu"},
    "O slayer of enemies": {"he": "הו קוטל אויבים", "ar": "يا قاتل الأعداء", "tr": "Ey düşman katili", "sw": "Ewe muuaji wa maadui"},
    
    "the soul": {"he": "הנשמה", "ar": "الروح", "tr": "ruh", "sw": "roho"},
    "is eternal": {"he": "היא נצחית", "ar": "أبدية", "tr": "ebedidir", "sw": "ni ya milele"},
    "is unborn": {"he": "לא נולדה", "ar": "غير مولودة", "tr": "doğmamıştır", "sw": "haizaliwi"},
    "is undying": {"he": "לא מתה", "ar": "غير ميتة", "tr": "ölmezdir", "sw": "haifi"},
    "is primeval": {"he": "קדמונית", "ar": "أزلية", "tr": "kadimdir", "sw": "ni ya kale"},
    "is not slain": {"he": "לא נהרגת", "ar": "لا تُقتل", "tr": "öldürülmez", "sw": "haiuawi"},
    "when the body": {"he": "כשהגוף", "ar": "عندما الجسد", "tr": "beden", "sw": "mwili"},
    "is slain": {"he": "נהרג", "ar": "يُقتل", "tr": "öldürüldüğünde", "sw": "unapouawa"},
    "the soul does not die": {"he": "הנשמה לא מתה", "ar": "الروح لا تموت", "tr": "ruh ölmez", "sw": "roho haifi"},
    
    "perform your duty": {"he": "בצע את חובתך", "ar": "أد واجبك", "tr": "görevini yerine getir", "sw": "fanya wajibu wako"},
    "without attachment": {"he": "ללא היצמדות", "ar": "بدون تعلق", "tr": "bağlılık olmadan", "sw": "bila ambatanisho"},
    "to the fruits": {"he": "לפירות", "ar": "للثمار", "tr": "meyvelere", "sw": "kwa matunda"},
    "of action": {"he": "של פעולה", "ar": "للعمل", "tr": "eylemin", "sw": "ya vitendo"},
    "yoga is skill": {"he": "יוגה היא מיומנות", "ar": "اليوغا هي مهارة", "tr": "yoga yetenektir", "sw": "yoga ni ujuzi"},
    "in action": {"he": "בפעולה", "ar": "في العمل", "tr": "eylemde", "sw": "katika vitendo"},
    
    "knowledge": {"he": "ידע", "ar": "المعرفة", "tr": "bilgi", "sw": "ujuzi"},
    "wisdom": {"he": "חוכמה", "ar": "الحكمة", "tr": "bilgelik", "sw": "busara"},
    "devotion": {"he": "מסירות", "ar": "التفاني", "tr": "bağlılık", "sw": "ujitoaji"},
    "meditation": {"he": "מדיטציה", "ar": "التأمل", "tr": "meditasyon", "sw": "kutafakari"},
    "peace": {"he": "שלום", "ar": "السلام", "tr": "huzur", "sw": "amani"},
    "happiness": {"he": "אושר", "ar": "السعادة", "tr": "mutluluk", "sw": "furaha"},
}

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def translate_title(title_en):
    """Translate chapter title to other languages."""
    if title_en in TERM_TRANSLATIONS:
        return TERM_TRANSLATIONS[title_en]
    
    # Default: use English with transliteration
    return {
        "he": title_en,
        "ar": title_en,
        "tr": title_en,
        "sw": title_en
    }

def translate_sloka(sloka_text):
    """Translate sloka text to other languages."""
    # Check for exact match
    if sloka_text in TERM_TRANSLATIONS:
        return TERM_TRANSLATIONS[sloka_text]
    
    # Build translation from components
    result = {"he": "", "ar": "", "tr": "", "sw": ""}
    
    # Simple word-by-word for now
    words = sloka_text.split()
    translated = {"he": [], "ar": [], "tr": [], "sw": []}
    
    for word in words:
        clean = word.strip('.,;:!?()"\'-')
        found = False
        
        for term, trans in TERM_TRANSLATIONS.items():
            if term.lower() == clean.lower():
                for lang in ["he", "ar", "tr", "sw"]:
                    translated[lang].append(trans[lang])
                found = True
                break
        
        if not found:
            # Keep original for unknown words
            for lang in ["he", "ar", "tr", "sw"]:
                translated[lang].append(clean)
    
    for lang in ["he", "ar", "tr", "sw"]:
        result[lang] = " ".join(translated[lang])
    
    return result

def process_chapter(chapter_num):
    """Process a single chapter."""
    input_file = BASE_DIR / 'data' / 'chapters' / f'ch-{chapter_num:02d}' / 'chapter-source.json'
    output_file = BASE_DIR / 'data' / 'chapters' / f'ch-{chapter_num:02d}' / 'chapter-other.json'
    
    if not input_file.exists():
        print(f"  Skipping ch-{chapter_num:02d}: Input file not found")
        return False
    
    print(f"  Processing ch-{chapter_num:02d}...")
    source_data = load_json(input_file)
    
    # Build output structure
    output_data = {
        "chapter": chapter_num,
        "title": {},
        "slokas": {}
    }
    
    # Translate title
    title_en = source_data.get('title', {}).get('en', {}).get('text', '')
    output_data['title'] = translate_title(title_en)
    
    # Translate slokas
    total_slokas = len(source_data.get('slokas', []))
    for sloka in source_data.get('slokas', []):
        sloka_num = sloka.get('number', '')
        sloka_en = sloka.get('translations', {}).get('en', {}).get('text', '')
        
        if sloka_en:
            translation = translate_sloka(sloka_en)
            output_data['slokas'][sloka_num] = {
                "he": {"text": translation['he'], "approved": False},
                "ar": {"text": translation['ar'], "approved": False},
                "tr": {"text": translation['tr'], "approved": False},
                "sw": {"text": translation['sw'], "approved": False}
            }
    
    save_json(output_file, output_data)
    print(f"  Saved {len(output_data['slokas'])} slokas to chapter-other.json")
    return True

def main():
    print("="*60)
    print("Generating chapter-other.json for chapters 1-6")
    print("="*60)
    
    for chapter_num in range(1, 7):
        process_chapter(chapter_num)
    
    print("\n" + "="*60)
    print("Complete! Processed chapters 1-6")
    print("="*60)

if __name__ == '__main__':
    main()
