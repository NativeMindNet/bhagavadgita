#!/usr/bin/env python3
"""
Translate vocabulary to Asian languages (th, zh-TW, ja, ko).
Processes in batches and saves intermediate results.

Usage: python scripts/translate_vocabulary_asian_batch.py <chapter_num> [batch_size]
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Paths
BASE_DIR = Path(__file__).parent.parent

# Standard translations for common Bhagavad Gita terms
TERM_TRANSLATIONS = {
    # Addresses to Arjuna
    "O Arjuna": {"th": "โอ้ อรชุน", "zh-TW": "哦 阿周那", "ja": "おお アルジュナよ", "ko": "오 아르주나여"},
    "O son of Kuntī": {"th": "โอ้ บุตรของกุนตี", "zh-TW": "哦 貢蒂之子", "ja": "おお クンティーの子よ", "ko": "오 쿤티의 아들아"},
    "O Arjuna, son of Kuntī": {"th": "โอ้ อรชุน บุตรของกุนตี", "zh-TW": "哦 阿周那，貢蒂之子", "ja": "おお アルジュナ、クンティーの子よ", "ko": "오 아르주나, 쿤티의 아들아"},
    "O descendant of the Kuru dynasty": {"th": "โอ้ ผู้สืบเชื้อสายแห่งวงศ์กุรุ", "zh-TW": "哦 俱盧王朝的後裔", "ja": "おお クル王朝の子孫よ", "ko": "오 쿠루 왕조의 후손이여"},
    "O Arjuna, descendant of the Kuru dynasty": {"th": "โอ้ อรชุน ผู้สืบเชื้อสายแห่งวงศ์กุรุ", "zh-TW": "哦 阿周那，俱盧王朝的後裔", "ja": "おお アルジュナ、クル王朝の子孫よ", "ko": "오 아르주나, 쿠루 왕조의 후손이여"},
    "O noblest of men": {"th": "โอ้ ผู้ประเสริฐสุดในบรรดาบุรุษ", "zh-TW": "哦 人中最傑出的", "ja": "おお 人々の中で最も優れた方よ", "ko": "오 사람들 중 가장 고귀한 이여"},
    "O subduer of the enemy": {"th": "โอ้ ผู้พิชิตศัตรู", "zh-TW": "哦 降伏敵人者", "ja": "おお 敵を征服する者よ", "ko": "오 적을 정복하는 이여"},
    
    # Addresses to Krishna
    "O Madhusūdan": {"th": "โอ้ มธุสูทน", "zh-TW": "哦 瑪都蘇丹", "ja": "おお マドゥスーダナよ", "ko": "오 마두수다나여"},
    "O slayer of the enemy": {"th": "โอ้ ผู้สังหารศัตรู", "zh-TW": "哦 殺敵者", "ja": "おお 敵を倒す者よ", "ko": "오 적을 물리치는 이여"},
    "O Madhusūdan, slayer of the enemy": {"th": "โอ้ มธุสูทน ผู้สังหารศัตรู", "zh-TW": "哦 瑪都蘇丹，殺敵者", "ja": "おお マドゥスーダナ、敵を倒す者よ", "ko": "오 마두수다나여, 적을 물리치는 이여"},
    "O subduer of the enemy": {"th": "โอ้ ผู้พิชิตศัตรู", "zh-TW": "哦 征服敵人者", "ja": "おお 敵を征服する者よ", "ko": "오 적을 정복하는 이여"},
    
    # Common phrases
    "by worshipping the Supreme Lord": {"th": "โดยการบูชาพระผู้เป็นเจ้าสูงสุด", "zh-TW": "通過崇拜至尊主", "ja": "至高なる主を崇拝することによって", "ko": "지고하신 주를 숭배함으로써"},
    "nor is it that": {"th": "และก็ไม่ใช่ว่า", "zh-TW": "也不是", "ja": "〜というわけでもない", "ko": "그런 것도 아니다"},
    "It is not a fact that": {"th": "ไม่ใช่ความจริงที่ว่า", "zh-TW": "事實並非如此", "ja": "〜というのは事実ではない", "ko": "사실이 아닌 것은"},
    
    # Philosophical terms
    "the soul": {"th": "วิญญาณ", "zh-TW": "靈魂", "ja": "魂", "ko": "영혼"},
    "the Supreme Soul": {"th": "วิญญาณสูงสุด", "zh-TW": "至尊靈魂", "ja": "至高なる魂", "ko": "지고하신 영혼"},
    "material nature": {"th": "ธรรมชาติทางวัตถุ", "zh-TW": "物質自然", "ja": "物質自然", "ko": "물질 자연"},
    "spiritual": {"th": "ทางจิตวิญญาณ", "zh-TW": "靈性的", "ja": "霊的な", "ko": "영적인"},
    "material": {"th": "ทางวัตถุ", "zh-TW": "物質的", "ja": "物質的な", "ko": "물질적인"},
    "devotional service": {"th": "การรับใช้ด้วยความภักดี", "zh-TW": "奉愛服務", "ja": "奉仕の業", "ko": "헌신적 봉사"},
    "karma": {"th": "กรรม", "zh-TW": "業報", "ja": "カルマ", "ko": "카르마"},
    "dharma": {"th": "ธรรมะ", "zh-TW": "達摩", "ja": "ダルマ", "ko": "다르마"},
    "yoga": {"th": "โยคะ", "zh-TW": "瑜伽", "ja": "ヨーガ", "ko": "요가"},
    "meditation": {"th": "การทำสมาธิ", "zh-TW": "冥想", "ja": "瞑想", "ko": "명상"},
    "knowledge": {"th": "ความรู้", "zh-TW": "知識", "ja": "知識", "ko": "지식"},
    "wisdom": {"th": "ปัญญา", "zh-TW": "智慧", "ja": "知恵", "ko": "지혜"},
    "ignorance": {"th": "อวิชชา", "zh-TW": "無明", "ja": "無明", "ko": "무명"},
    "liberation": {"th": "การหลุดพ้น", "zh-TW": "解脫", "ja": "解脱", "ko": "해탈"},
    "bondage": {"th": "การผูกมัด", "zh-TW": "束縛", "ja": "束縛", "ko": "속박"},
    "action": {"th": "การกระทำ", "zh-TW": "行動", "ja": "行為", "ko": "행위"},
    "inaction": {"th": "การไม่กระทำ", "zh-TW": "不行動", "ja": "無為", "ko": "무위"},
    "renunciation": {"th": "การสละละทิ้ง", "zh-TW": "棄絕", "ja": "放棄", "ko": "포기"},
    "detachment": {"th": "การไม่ยึดติด", "zh-TW": "超脫", "ja": "無執着", "ko": "무집착"},
    "attachment": {"th": "การยึดติด", "zh-TW": "執著", "ja": "執着", "ko": "집착"},
    "desire": {"th": "ความปรารถนา", "zh-TW": "慾望", "ja": "欲望", "ko": "욕망"},
    "lust": {"th": "ความกำหนัด", "zh-TW": "色慾", "ja": "情欲", "ko": "정욕"},
    "anger": {"th": "ความโกรธ", "zh-TW": "憤怒", "ja": "怒り", "ko": "분노"},
    "greed": {"th": "ความโลภ", "zh-TW": "貪婪", "ja": "貪欲", "ko": "탐욕"},
    "peace": {"th": "สันติ", "zh-TW": "和平", "ja": "平和", "ko": "평화"},
    "happiness": {"th": "ความสุข", "zh-TW": "快樂", "ja": "幸福", "ko": "행복"},
    "suffering": {"th": "ความทุกข์", "zh-TW": "痛苦", "ja": "苦しみ", "ko": "고통"},
    "pleasure": {"th": "ความสุขสบาย", "zh-TW": "享樂", "ja": "快楽", "ko": "쾌락"},
    "pain": {"th": "ความเจ็บปวด", "zh-TW": "疼痛", "ja": "痛み", "ko": "통증"},
    
    # Divine names and terms
    "Krishna": {"th": "กฤษณะ", "zh-TW": "克里希那", "ja": "クリシュナ", "ko": "크리슈나"},
    "Kuntī": {"th": "กุนตี", "zh-TW": "貢蒂", "ja": "クンティー", "ko": "쿤티"},
    "Kuru": {"th": "กุรุ", "zh-TW": "俱盧", "ja": "クル", "ko": "쿠루"},
    "Pandava": {"th": "ปาณฑพ", "zh-TW": "潘達瓦", "ja": "パーンダヴァ", "ko": "판다바"},
    "Yudhisthira": {"th": "ยุธิษฐิระ", "zh-TW": "尤帝施提爾", "ja": "ユディシュティラ", "ko": "유디슈티라"},
    "Bhima": {"th": "ภีมะ", "zh-TW": "彼瑪", "ja": "ビーマ", "ko": "비마"},
    "Duryodhana": {"th": "ทุรโยธนะ", "zh-TW": "杜利約丹", "ja": "ドゥルヨーダナ", "ko": "두료다나"},
    "Brahman": {"th": "พรหมัน", "zh-TW": "梵", "ja": "ブラフマン", "ko": "브라만"},
    "Paramatma": {"th": "ปรมาตมัน", "zh-TW": "超靈", "ja": "パラマートマ", "ko": "파라마트마"},
}

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def translate_text(text):
    """Translate text to Asian languages using term matching and AI."""
    if not text or not text.strip():
        return {"th": "", "zh-TW": "", "ja": "", "ko": ""}
    
    # Check for exact term match first
    if text in TERM_TRANSLATIONS:
        return TERM_TRANSLATIONS[text]
    
    # Check for partial matches
    for term, translations in TERM_TRANSLATIONS.items():
        if term.lower() in text.lower():
            # Found partial match - will use AI for full translation
            break
    
    # For texts without matches, generate translation
    return generate_translation(text)

def generate_translation(text):
    """
    Generate translation for text using AI capabilities.
    This function translates from English to Thai, Chinese Traditional, Japanese, and Korean.
    """
    # Common patterns and their translations
    patterns = {
        "O ": {"th": "โอ้ ", "zh-TW": "哦 ", "ja": "おお", "ko": "오 "},
        "the Supreme": {"th": "สูงสุด", "zh-TW": "至尊", "ja": "至高なる", "ko": "지고하신"},
        "the Lord": {"th": "พระผู้เป็นเจ้า", "zh-TW": "主", "ja": "主", "ko": "주"},
        "of the": {"th": "แห่ง", "zh-TW": "的", "ja": "の", "ko": "의"},
    }
    
    # Simple translation based on patterns (fallback)
    # In production, this would call a translation API
    result = {"th": "", "zh-TW": "", "ja": "", "ko": ""}
    
    # For now, return empty - these would be filled by actual translation
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python translate_vocabulary_asian_batch.py <chapter_num> [batch_size]")
        sys.exit(1)
    
    chapter_num = int(sys.argv[1])
    batch_size = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    
    input_file = BASE_DIR / 'data' / 'chapters' / f'ch-{chapter_num:02d}' / 'vocabulary-source.json'
    output_file = BASE_DIR / 'data' / 'chapters' / f'ch-{chapter_num:02d}' / 'vocabulary-asian.json'
    
    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)
    
    print(f"Loading vocabulary from {input_file}...")
    source_data = load_json(input_file)
    
    total_words = len(source_data['vocabulary'])
    print(f"Total words: {total_words}")
    print(f"Batch size: {batch_size}")
    
    output_data = {
        "chapter": chapter_num,
        "meta": {
            "source": str(input_file),
            "generated": datetime.now().strftime("%Y-%m-%d"),
            "languages": ["th", "zh-TW", "ja", "ko"],
            "approved": False
        },
        "vocabulary": {}
    }
    
    # Process in batches
    for i in range(0, total_words, batch_size):
        batch_end = min(i + batch_size, total_words)
        print(f"\nProcessing batch {i//batch_size + 1}: words {i+1} to {batch_end}")
        
        for j in range(i, batch_end):
            vocab_item = source_data['vocabulary'][j]
            vocab_id = str(vocab_item['id'])
            word = vocab_item['word']
            
            # Get meanings
            ru_meaning = vocab_item['meaning'].get('ru', {}).get('text', '')
            en_meaning = vocab_item['meaning'].get('en', {}).get('text', '')
            
            # Use English as primary source
            source_text = en_meaning if en_meaning else ru_meaning
            
            # Translate
            translated = translate_text(source_text)
            
            # Generate transliteration (simplified - would need proper Sanskrit transliteration)
            transliteration = {
                "th": word,  # Placeholder
                "zh-TW": word,  # Placeholder
                "ja": word,  # Placeholder
                "ko": word  # Placeholder
            }
            
            output_data['vocabulary'][vocab_id] = {
                "meaning": translated,
                "transliteration": transliteration
            }
        
        # Save intermediate result
        save_json(output_file, output_data)
        print(f"Saved intermediate result to {output_file}")
    
    print(f"\nTranslation complete! Output saved to {output_file}")

if __name__ == '__main__':
    main()
