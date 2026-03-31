#!/usr/bin/env python3
"""
Generate transliterations for Chapter 1 slokas in 12 target languages.
Uses Sanskrit text as source and converts to native scripts.
"""

import os
import re
from pathlib import Path

# Base directories
SANSKRIT_DIR = Path("/Users/anton/proj/gita/data/sanskrit/chapter-01-sanskrit")
TRANSLATED_BASE = Path("/Users/anton/proj/gita/data/translated")

# Target languages with their native script names
LANGUAGES = {
    'th': 'Thai',
    'zh-CN': 'Simplified Chinese',
    'zh-TW': 'Traditional Chinese',
    'ko': 'Korean',
    'ja': 'Japanese',
    'el': 'Greek',
    'ka': 'Georgian',
    'hy': 'Armenian',
    'he': 'Hebrew',
    'ar': 'Arabic',
    'tr': 'Turkish (IAST Latin)',
    'sw': 'Swahili (IAST Latin)',
}

# IAST to Latin mapping for tr and sw (same base)
IAST_LATIN = {
    'ā': 'ā', 'ī': 'ī', 'ū': 'ū', 'ṛ': 'ṛ', 'ṝ': 'ṝ', 'ḷ': 'ḷ', 'ḹ': 'ḹ',
    'ṭ': 'ṭ', 'ṭh': 'ṭh', 'ḍ': 'ḍ', 'ḍh': 'ḍh', 'ṇ': 'ṇ',
    'ś': 'ś', 'ṣ': 'ṣ', 'ṣh': 'ṣh',
    'ṃ': 'ṃ', 'ḥ': 'ḥ', 'ṅ': 'ṅ', 'ñ': 'ñ',
}

def get_sloka_files():
    """Get all sloka files from sanskrit directory, excluding meta."""
    files = []
    for f in sorted(SANSKRIT_DIR.glob("chapter-01-*.txt")):
        if 'meta' not in f.name and 'sloka' in f.name:
            files.append(f)
    return files

def read_sanskrit_text(filepath):
    """Read Sanskrit sloka text from file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read().strip()

def sanskrit_to_thai(text):
    """Convert Sanskrit to Thai script using standard transliteration rules."""
    # Mapping for Thai script (approximate phonetic transliteration)
    mappings = [
        ('अ', 'อ'), ('आ', 'อา'), ('इ', 'อิ'), ('ई', 'อี'), ('उ', 'อุ'), ('ऊ', 'อู'),
        ('ऋ', 'ฤ'), ('ए', 'เอ'), ('ऐ', 'ไอ'), ('ओ', 'โอ'), ('औ', 'เอา'),
        ('क', 'ก'), ('ख', 'ข'), ('ग', 'ค'), ('घ', 'ฆ'), ('ङ', 'ง'),
        ('च', 'จ'), ('छ', 'ฉ'), ('ज', 'ช'), ('झ', 'ฌ'), ('ञ', 'ญ'),
        ('ट', 'ฏ'), ('ठ', 'ฐ'), ('ड', 'ฑ'), ('ढ', 'ฒ'), ('ण', 'ณ'),
        ('त', 'ต'), ('थ', 'ถ'), ('द', 'ท'), ('ध', 'ธ'), ('न', 'น'),
        ('प', 'ป'), ('फ', 'ผ'), ('ब', 'พ'), ('भ', 'ภ'), ('म', 'ม'),
        ('य', 'ย'), ('र', 'ร'), ('ल', 'ล'), ('व', 'ว'),
        ('श', 'ศ'), ('ष', 'ษ'), ('स', 'ส'), ('ह', 'ห'),
        ('ळ', 'ฬ'), ('क्ष', 'กษ'), ('त्र', 'ตร'), ('ज्ञ', 'ชญ'),
        ('ं', 'ง'), ('ः', 'หะ'), ('।', ' '), ('॥', ' '),
        ('्', ''),  # virama - remove
    ]
    result = text
    for sanskrit, thai in mappings:
        result = result.replace(sanskrit, thai)
    return result

def sanskrit_to_chinese_simplified(text):
    """Convert Sanskrit to Simplified Chinese using phonetic transliteration."""
    # Standard Chinese transliteration for Sanskrit Buddhist texts
    mappings = [
        ('धृतराष्ट्र', '提头赖吒'), ('उवाच', '乌瓦恰'),
        ('धर्मक्षेत्रे', '达摩刹怛罗'), ('कुरुक्षेत्रे', '俱卢刹怛罗'),
        ('समवेता', '三末达'), ('युयुत्सवः', '育育楚瓦'),
        ('मामकाः', '摩摩迦'), ('पाण्डवाश्चैव', '般度瓦切瓦'),
        ('किमकुर्वत', '基姆古尔瓦特'), ('सञ्जय', '珊阇耶'),
        ('सञ्जय', '珊阇耶'), ('दृष्ट्वा', '德里斯特瓦'),
        ('तु', '图'), ('पाण्डवानीकं', '般度瓦尼卡姆'),
        ('व्यूढं', '维尤达姆'), ('दुर्योधनस्तदा', '杜尔约达纳斯塔达'),
        ('आचार्यमुपसङ्गम्य', '阿查尔亚姆乌帕桑加米亚'),
        ('राजा', '拉贾'), ('वचनमब्रवीत्', '瓦查纳姆阿布拉维特'),
        ('अत्र', '阿特拉'), ('शूरा', '舒拉'),
        ('महेष्वासा', '马赫什瓦萨'), ('भीमार्जुनसमा', '比马尔朱纳萨马'),
        ('युधि', '尤迪'), ('युयुधानो', '尤尤达诺'),
        ('विराटश्च', '维拉塔什查'), ('द्रुपदश्च', '德鲁帕达什查'),
        ('महारथः', '马哈拉塔'), ('धृष्टकेतुश्चेकितानः', '德里斯塔克图什切基塔纳'),
        ('काशिराजश्च', '卡希拉贾什查'), ('वीर्यवान्', '维里亚万'),
        ('पुरुजित्कुन्तिभोजश्च', '普鲁吉特昆蒂博贾什查'),
        ('शैब्यश्च', '夏比亚什查'), ('नरपुङ्गवः', '纳拉彭加瓦'),
        ('युधामन्युश्च', '尤达曼尤什查'), ('विक्रान्त', '维克兰塔'),
        ('उत्तमौजाश्च', '乌塔莫贾什查'), ('वीर्यवान्', '维里亚万'),
        ('सौभद्रो', '绍巴德罗'), ('द्रौपदेयाश्च', '德罗帕德亚什查'),
        ('सर्व', '萨尔瓦'), ('एव', '埃瓦'),
        ('महारथाः', '马哈拉塔'),
        ('॥', ''),
    ]
    result = text
    for sanskrit, chinese in mappings:
        result = result.replace(sanskrit, chinese)
    # Fallback: character-by-character phonetic
    if result == text:
        # Basic phonetic mapping
        char_map = {
            'अ': '阿', 'आ': '阿', 'इ': '伊', 'ई': '伊', 'उ': '乌', 'ऊ': '乌',
            'ऋ': '利', 'ए': '埃', 'ओ': '奥',
            'क': '卡', 'ख': '卡', 'ग': '嘎', 'घ': '嘎', 'ङ': '昂',
            'च': '查', 'छ': '查', 'ज': '贾', 'झ': '贾', 'ञ': '尼亚',
            'ट': '塔', 'ठ': '塔', 'ड': '达', 'ढ': '达', 'ण': '纳',
            'त': '塔', 'थ': '塔', 'द': '达', 'ध': '达', 'न': '纳',
            'प': '帕', 'फ': '帕', 'ब': '巴', 'भ': '巴', 'म': '马',
            'य': '亚', 'र': '拉', 'ल': '拉', 'व': '瓦',
            'श': '沙', 'ष': '沙', 'स': '萨', 'ह': '哈',
            'ं': '姆', 'ः': '哈', '।': ' ', '॥': ' ', '्': '',
        }
        result = ''.join(char_map.get(c, c) for c in text)
    return result

def sanskrit_to_chinese_traditional(text):
    """Convert Sanskrit to Traditional Chinese using phonetic transliteration."""
    # Traditional Chinese uses same phonetics but traditional characters
    simplified = sanskrit_to_chinese_simplified(text)
    # Convert simplified to traditional
    trad_map = {
        '马': '馬', '达': '達', '拉': '拉', '查': '查', '贾': '賈',
        '纳': '納', '塔': '塔', '瓦': '瓦', '萨': '薩', '尔': '爾',
        '约': '約', '尔': '爾', '干': '幹', '于': '於', '么': '麼',
    }
    result = simplified
    for simp, trad in trad_map.items():
        result = result.replace(simp, trad)
    return result

def sanskrit_to_korean(text):
    """Convert Sanskrit to Korean Hangul using standard transliteration."""
    # Standard Korean transliteration for Sanskrit
    mappings = [
        ('धृतराष्ट्र', '드리타라슈트라'), ('उवाच', '우바차'),
        ('धर्मक्षेत्रे', '다르마크셰트레'), ('कुरुक्षेत्रे', '쿠루크셰트레'),
        ('समवेता', '사마베타'), ('युयुत्सवः', '유유추바'),
        ('मामकाः', '마마카'), ('पाण्डवाश्चैव', '판다바슈차이바'),
        ('किमकुर्वत', '킴쿠르바타'), ('सञ्जय', '산자야'),
        ('दृष्ट्वा', '드리슈트바'), ('तु', '투'),
        ('पाण्डवानीकं', '판다바니캄'), ('व्यूढं', '뷰담'),
        ('दुर्योधनस्तदा', '두료다나스타다'),
        ('आचार्यमुपसङ्गम्य', '아차르야무파상감야'),
        ('राजा', '라자'), ('वचनमब्रवीत्', '바차남아브라비트'),
        ('अत्र', '아트라'), ('शूरा', '슈라'),
        ('महेष्वासा', '마헤슈바사'), ('भीमार्जुनसमा', '비마르주나사마'),
        ('युधि', '유디'), ('युयुधानो', '유유다노'),
        ('विराटश्च', '비라타슈차'), ('द्रुपदश्च', '드루파다슈차'),
        ('महारथः', '마하라타'), ('धृष्टकेतुश्चेकितानः', '드리슈타케투슈체키타나'),
        ('काशिराजश्च', '카시라자슈차'), ('वीर्यवान्', '비랴완'),
        ('पुरुजित्कुन्तिभोजश्च', '푸루지트쿤티보자슈차'),
        ('शैब्यश्च', '샤이비아슈차'), ('नरपुङ्गवः', '나라푼가바'),
        ('युधामन्युश्च', '유다만유슈차'), ('विक्रान्त', '비크란타'),
        ('उत्तमौजाश्च', '우타모자슈차'), ('सौभद्रो', '사우바드로'),
        ('द्रौपदेयाश्च', '드라우파데야슈차'), ('सर्व', '사르바'),
        ('एव', '에바'), ('महारथाः', '마하라타'),
        ('॥', ''), ('।', ' '), ('ं', 'ᆫ'), ('ः', '하'),
    ]
    result = text
    for sanskrit, korean in mappings:
        result = result.replace(sanskrit, korean)
    return result

def sanskrit_to_japanese(text):
    """Convert Sanskrit to Japanese Katakana using standard transliteration."""
    # Standard Japanese Katakana transliteration for Sanskrit Buddhist texts
    mappings = [
        ('धृतराष्ट्र', 'ドリタラシュトラ'), ('उवाच', 'ウヴァーチャ'),
        ('धर्मक्षेत्रे', 'ダルマクシェートレ'), ('कुरुक्षेत्रे', 'クルクシェートレ'),
        ('समवेता', 'サマヴェータ'), ('युयुत्सवः', 'ユユツヴァ'),
        ('मामकाः', 'マーマカー'), ('पाण्डवाश्चैव', 'パーンダヴァーシュチャイヴァ'),
        ('किमकुर्वत', 'キムクルヴァタ'), ('सञ्जय', 'サンジャヤ'),
        ('दृष्ट्वा', 'ドゥリシュトゥヴァー'), ('तु', 'トゥ'),
        ('पाण्डवानीकं', 'パーンダヴァーニークム'), ('व्यूढं', 'ビューダム'),
        ('दुर्योधनस्तदा', 'ドゥルヨーダナスタダー'),
        ('आचार्यमुपसङ्गम्य', 'アーチャールヤムパサンギャムヤ'),
        ('राजा', 'ラージャ'), ('वचनमब्रवीत्', 'ヴァチャナマブラヴィート'),
        ('अत्र', 'アトラ'), ('शूरा', 'シューラー'),
        ('महेष्वासा', 'マヘーシュヴァーサー'), ('भीमार्जुनसमा', 'ビーマールジュナサマー'),
        ('युधि', 'ユディ'), ('युयुधानो', 'ユユダーノ'),
        ('विराटश्च', 'ヴィラータシュチャ'), ('द्रुपदश्च', 'ドルパダシュチャ'),
        ('महारथः', 'マハーラタ'), ('धृष्टकेतुश्चेकितानः', 'ドゥリシュタケトゥシュチェキターナ'),
        ('काशिराजश्च', 'カーシラージャシュチャ'), ('वीर्यवान्', 'ヴィールヤヴァーン'),
        ('पुरुजित्कुन्तिभोजश्च', 'プルジットクンティボージャシュチャ'),
        ('शैब्यश्च', 'シャイビアシュチャ'), ('नरपुङ्गवः', 'ナラプンガヴァ'),
        ('युधामन्युश्च', 'ユダーマニユシュチャ'), ('विक्रान्त', 'ヴィクラーンタ'),
        ('उत्तमौजाश्च', 'ウッタモージャシュチャ'), ('सौभद्रो', 'サウバドロ'),
        ('द्रौपदेयाश्च', 'ドラウパデヤーシュチャ'), ('सर्व', 'サルヴァ'),
        ('एव', 'エヴァ'), ('महारथाः', 'マハーラター'),
        ('॥', ''), ('।', ' '), ('ं', 'ーン'), ('ः', 'ハ'),
    ]
    result = text
    for sanskrit, japanese in mappings:
        result = result.replace(sanskrit, japanese)
    return result

def sanskrit_to_greek(text):
    """Convert Sanskrit to Greek script using phonetic transliteration."""
    # Greek transliteration mapping
    mappings = [
        ('अ', 'α'), ('आ', 'α'), ('इ', 'ι'), ('ई', 'ι'), ('उ', 'υ'), ('ऊ', 'υ'),
        ('ऋ', 'ρι'), ('ए', 'ε'), ('ऐ', 'αι'), ('ओ', 'ο'), ('औ', 'αυ'),
        ('क', 'κ'), ('ख', 'χ'), ('ग', 'γ'), ('घ', 'γχ'), ('ङ', 'γγ'),
        ('च', 'τσ'), ('छ', 'τσχ'), ('ज', 'τζ'), ('झ', 'τζχ'), ('ञ', 'νι'),
        ('ट', 'τ'), ('ठ', 'θ'), ('ड', 'δ'), ('ढ', 'δχ'), ('ण', 'ν'),
        ('त', 'τ'), ('थ', 'θ'), ('द', 'δ'), ('ध', 'δχ'), ('न', 'ν'),
        ('प', 'π'), ('फ', 'φ'), ('ब', 'μπ'), ('भ', 'μπχ'), ('म', 'μ'),
        ('य', 'γ'), ('र', 'ρ'), ('ल', 'λ'), ('व', 'β'),
        ('श', 'σ'), ('ष', 'σ'), ('स', 'σ'), ('ह', 'χ'),
        ('ळ', 'λ'), ('ा', 'ά'), ('ी', 'ί'), ('ू', 'ύ'),
        ('ं', 'ν'), ('ः', 'ς'), ('।', ' '), ('॥', ' '),
        ('्', ''),
    ]
    result = text
    for sanskrit, greek in mappings:
        result = result.replace(sanskrit, greek)
    return result

def sanskrit_to_georgian(text):
    """Convert Sanskrit to Georgian script using phonetic transliteration."""
    # Georgian transliteration mapping
    mappings = [
        ('अ', 'ა'), ('आ', 'ა'), ('इ', 'ი'), ('ई', 'ი'), ('उ', 'უ'), ('ऊ', 'უ'),
        ('ऋ', 'რი'), ('ए', 'ე'), ('ऐ', 'აი'), ('ओ', 'ო'), ('औ', 'აუ'),
        ('क', 'კ'), ('ख', 'ხ'), ('ग', 'გ'), ('घ', 'ღ'), ('ङ', 'ნგ'),
        ('च', 'ჩ'), ('छ', 'ცხ'), ('ज', 'ჯ'), ('झ', 'ძხ'), ('ञ', 'ნი'),
        ('ट', 'ტ'), ('ठ', 'თ'), ('ड', 'დ'), ('ढ', 'დხ'), ('ण', 'ნ'),
        ('त', 'ტ'), ('थ', 'თ'), ('द', 'დ'), ('ध', 'დხ'), ('न', 'ნ'),
        ('प', 'პ'), ('फ', 'ფ'), ('ब', 'ბ'), ('भ', 'ბხ'), ('म', 'მ'),
        ('य', 'ი'), ('र', 'რ'), ('ल', 'ლ'), ('व', 'ვ'),
        ('श', 'შ'), ('ष', 'შ'), ('स', 'ს'), ('ह', 'ჰ'),
        ('ळ', 'ლ'), ('ा', 'ა'), ('ी', 'ი'), ('ू', 'უ'),
        ('ं', 'ნ'), ('ः', 'ჰ'), ('।', ' '), ('॥', ' '),
        ('्', ''),
    ]
    result = text
    for sanskrit, georgian in mappings:
        result = result.replace(sanskrit, georgian)
    return result

def sanskrit_to_armenian(text):
    """Convert Sanskrit to Armenian script using phonetic transliteration."""
    # Armenian transliteration mapping
    mappings = [
        ('अ', 'ա'), ('आ', 'ա'), ('इ', 'ի'), ('ई', 'ի'), ('उ', 'ու'), ('ऊ', 'ու'),
        ('ऋ', 'րի'), ('ए', 'ե'), ('ऐ', 'այ'), ('ओ', 'ո'), ('औ', 'աու'),
        ('क', 'կ'), ('ख', 'խ'), ('ग', 'գ'), ('घ', 'ղ'), ('ङ', 'նգ'),
        ('च', 'չ'), ('छ', 'ցխ'), ('ज', 'ջ'), ('झ', 'ջխ'), ('ञ', 'նյ'),
        ('ट', 'տ'), ('ठ', 'թ'), ('ड', 'դ'), ('ढ', 'դխ'), ('ण', 'ն'),
        ('त', 'տ'), ('थ', 'թ'), ('द', 'դ'), ('ध', 'դխ'), ('न', 'ն'),
        ('प', 'պ'), ('फ', 'փ'), ('ब', 'բ'), ('भ', 'փ'), ('म', 'մ'),
        ('य', 'յ'), ('र', 'ր'), ('ल', 'լ'), ('व', 'վ'),
        ('श', 'շ'), ('ष', 'շ'), ('स', 'ս'), ('ह', 'հ'),
        ('ळ', 'լ'), ('ा', 'ա'), ('ी', 'ի'), ('ू', 'ու'),
        ('ं', 'ն'), ('ः', 'հ'), ('।', ' '), ('॥', ' '),
        ('्', ''),
    ]
    result = text
    for sanskrit, armenian in mappings:
        result = result.replace(sanskrit, armenian)
    return result

def sanskrit_to_hebrew(text):
    """Convert Sanskrit to Hebrew script using phonetic transliteration."""
    # Hebrew transliteration mapping (right-to-left)
    mappings = [
        ('अ', 'אַ'), ('आ', 'אַ'), ('इ', 'אִי'), ('ई', 'אִי'), ('उ', 'אוּ'), ('ऊ', 'אוּ'),
        ('ऋ', 'רִי'), ('ए', 'אֵ'), ('ऐ', 'אַי'), ('ओ', 'אוֹ'), ('औ', 'אַו'),
        ('क', 'כּ'), ('ख', 'כ'), ('ג', 'גּ'), ('ग', 'ג'), ('घ', 'גח'), ('ङ', 'נג'),
        ('च', 'צ'), ('छ', 'צח'), ('ज', 'ג׳'), ('झ', 'ג׳ח'), ('ञ', 'ני'),
        ('ट', 'ט'), ('ठ', 'ת'), ('ड', 'ד'), ('ढ', 'דח'), ('ण', 'נ'),
        ('त', 'ט'), ('थ', 'ת'), ('द', 'ד'), ('ध', 'דח'), ('נ', 'נ'),
        ('פ', 'פּ'), ('फ', 'פ'), ('ב', 'בּ'), ('भ', 'בח'), ('מ', 'מ'),
        ('य', 'י'), ('ר', 'ר'), ('ל', 'ל'), ('ו', 'ו'),
        ('ש', 'ש'), ('ष', 'ש'), ('ס', 'ס'), ('ה', 'ה'),
        ('ळ', 'ל'), ('ा', 'ָ'), ('ी', 'ִי'), ('ू', 'וּ'),
        ('ं', 'ן'), ('ः', 'ה'), ('।', ' '), ('॥', ' '),
        ('्', ''),
    ]
    result = text
    for sanskrit, hebrew in mappings:
        result = result.replace(sanskrit, hebrew)
    return result

def sanskrit_to_arabic(text):
    """Convert Sanskrit to Arabic script using phonetic transliteration."""
    # Arabic transliteration mapping (right-to-left)
    mappings = [
        ('अ', 'أَ'), ('आ', 'آ'), ('इ', 'إِ'), ('ई', 'إِي'), ('उ', 'أُ'), ('ऊ', 'أُو'),
        ('ऋ', 'رِ'), ('ए', 'إِي'), ('ऐ', 'أَي'), ('ओ', 'أُو'), ('औ', 'أَو'),
        ('क', 'ك'), ('ख', 'خ'), ('ग', 'غ'), ('घ', 'غ'), ('ङ', 'نغ'),
        ('च', 'ج'), ('छ', 'ج'), ('ज', 'ج'), ('झ', 'ج'), ('ञ', 'ني'),
        ('ट', 'ط'), ('ठ', 'ت'), ('ड', 'د'), ('ढ', 'د'), ('ण', 'ن'),
        ('त', 'ت'), ('थ', 'ث'), ('द', 'د'), ('ध', 'ذ'), ('ن', 'ن'),
        ('प', 'ب'), ('फ', 'ف'), ('ब', 'ب'), ('भ', 'ب'), ('م', 'م'),
        ('य', 'ي'), ('ر', 'ر'), ('ل', 'ل'), ('و', 'و'),
        ('श', 'ش'), ('ष', 'ص'), ('س', 'س'), ('ه', 'ه'),
        ('ळ', 'ل'), ('ا', 'ا'), ('ी', 'ِي'), ('ू', 'ُو'),
        ('ं', 'نْ'), ('ः', 'هْ'), ('।', ' '), ('॥', ' '),
        ('्', ''),
    ]
    result = text
    for sanskrit, arabic in mappings:
        result = result.replace(sanskrit, arabic)
    return result

def sanskrit_to_iast_latin(text):
    """Convert Sanskrit Devanagari to IAST Latin script (for Turkish and Swahili)."""
    # First, preserve spaces and line breaks
    lines = text.split('\n')
    result_lines = []
    
    for line in lines:
        # Process each line, preserving word boundaries
        words = line.split(' ')
        iast_words = []
        for word in words:
            iast_word = convert_word_to_iast(word)
            if iast_word:
                iast_words.append(iast_word)
        result_lines.append(' '.join(iast_words))
    
    return '\n'.join(result_lines)

def convert_word_to_iast(word):
    """Convert a single Devanagari word to IAST Latin."""
    iast_map = {
        'अ': 'a', 'आ': 'ā', 'इ': 'i', 'ई': 'ī', 'उ': 'u', 'ऊ': 'ū',
        'ऋ': 'ṛ', 'ॠ': 'ṝ', 'ऌ': 'ḷ', 'ॡ': 'ḹ',
        'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au',
        'क': 'k', 'ख': 'kh', 'ग': 'g', 'घ': 'gh', 'ङ': 'ṅ',
        'च': 'c', 'छ': 'ch', 'ज': 'j', 'झ': 'jh', 'ञ': 'ñ',
        'ट': 'ṭ', 'ठ': 'ṭh', 'ड': 'ḍ', 'ढ': 'ḍh', 'ण': 'ṇ',
        'त': 't', 'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n',
        'प': 'p', 'फ': 'ph', 'ब': 'b', 'भ': 'bh', 'म': 'm',
        'य': 'y', 'र': 'r', 'ल': 'l', 'व': 'v',
        'श': 'ś', 'ष': 'ṣ', 'स': 's', 'ह': 'h',
        'ळ': 'ḷ', 'क्ष': 'kṣ', 'त्र': 'tr', 'ज्ञ': 'jñ',
        'ा': 'ā', 'ि': 'i', 'ी': 'ī', 'ु': 'u', 'ू': 'ū',
        'ृ': 'ṛ', 'ॄ': 'ṝ', 'ॢ': 'ḷ', 'ॣ': 'ḹ',
        'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au',
        'ं': 'ṃ', 'ः': 'ḥ', '्': '', '।': '', '॥': '',
        'ँ': 'm̐', '१': '1', '२': '2', '३': '3', '४': '4',
        '५': '5', '६': '6', '७': '7', '८': '8', '९': '9', '०': '0',
    }
    result = ''
    i = 0
    while i < len(word):
        # Check for multi-character mappings first (3 chars, then 2, then 1)
        found = False
        for length in [3, 2, 1]:
            if i + length <= len(word):
                chunk = word[i:i+length]
                if chunk in iast_map:
                    result += iast_map[chunk]
                    i += length
                    found = True
                    break
        if not found:
            i += 1
    return result.strip()

def generate_transliteration(sanskrit_text, lang):
    """Generate transliteration for a given language."""
    converters = {
        'th': sanskrit_to_thai,
        'zh-CN': sanskrit_to_chinese_simplified,
        'zh-TW': sanskrit_to_chinese_traditional,
        'ko': sanskrit_to_korean,
        'ja': sanskrit_to_japanese,
        'el': sanskrit_to_greek,
        'ka': sanskrit_to_georgian,
        'hy': sanskrit_to_armenian,
        'he': sanskrit_to_hebrew,
        'ar': sanskrit_to_arabic,
        'tr': sanskrit_to_iast_latin,
        'sw': sanskrit_to_iast_latin,
    }
    converter = converters.get(lang)
    if converter:
        return converter(sanskrit_text)
    return sanskrit_text

def process_sloka(sloka_file, lang):
    """Process a single sloka file for a given language."""
    # Read Sanskrit text
    sanskrit_text = read_sanskrit_text(sloka_file)
    
    # Generate transliteration
    translit_text = generate_transliteration(sanskrit_text, lang)
    
    # Determine output path
    sloka_name = sloka_file.stem  # e.g., chapter-01-1.1-sanskrit_sloka
    # Extract sloka number part (e.g., 1.1, 1.4-6)
    match = re.search(r'chapter-01-(\d+\.?\d*(?:-\d+)?)', sloka_name)
    if match:
        sloka_id = match.group(1)
    else:
        sloka_id = sloka_name.replace('chapter-01-', '').replace('-sanskrit_sloka', '')
    
    output_name = f"chapter-01-{sloka_id}-{lang}_translit.txt"
    output_dir = TRANSLATED_BASE / lang / f"chapter-01-{lang}"
    output_path = output_dir / output_name
    
    # Ensure directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Write transliteration file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(translit_text)
    
    return output_path, True

def main():
    """Main function to process all slokas for all languages."""
    sloka_files = get_sloka_files()
    print(f"Found {len(sloka_files)} sloka files to process")
    print(f"Processing for {len(LANGUAGES)} languages")
    print(f"Total files to generate: {len(sloka_files) * len(LANGUAGES)}")
    print()
    
    stats = {'success': 0, 'errors': 0}
    errors = []
    
    for lang in LANGUAGES:
        print(f"\n=== Processing {lang} ({LANGUAGES[lang]}) ===")
        lang_stats = {'success': 0, 'errors': 0}
        
        for sloka_file in sloka_files:
            try:
                output_path, success = process_sloka(sloka_file, lang)
                if success:
                    lang_stats['success'] += 1
                    stats['success'] += 1
                    print(f"  ✓ {output_path.name}")
                else:
                    lang_stats['errors'] += 1
                    stats['errors'] += 1
                    errors.append((str(sloka_file), lang, "Conversion failed"))
            except Exception as e:
                lang_stats['errors'] += 1
                stats['errors'] += 1
                errors.append((str(sloka_file), lang, str(e)))
                print(f"  ✗ {sloka_file.name}: {e}")
        
        print(f"  Lang stats: {lang_stats['success']} success, {lang_stats['errors']} errors")
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total files generated: {stats['success']}")
    print(f"Total errors: {stats['errors']}")
    
    if errors:
        print("\nErrors:")
        for sloka, lang, error in errors:
            print(f"  - {sloka} ({lang}): {error}")
    
    return stats

if __name__ == '__main__':
    main()
