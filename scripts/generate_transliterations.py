#!/usr/bin/env python3
"""
Generate transliterations for GitaBook slokas in 12 target languages.

This script reads Sanskrit source files (in Devanagari script) and generates
transliterations in the native scripts of each target language.

Uses indic-transliteration library for Indic scripts and custom mappings
for non-Indic scripts.

Target languages and their scripts:
- ja (Japanese) - Katakana (phonetic approximation)
- ko (Korean) - Hangul (phonetic approximation)
- th (Thai) - Thai script (via indic-transliteration)
- zh-CN (Simplified Chinese) - Hanzi + Pinyin (phonetic approximation)
- zh-TW (Traditional Chinese) - Hanzi Traditional
- el (Greek) - Greek alphabet (phonetic approximation)
- ka (Georgian) - Georgian script (phonetic approximation)
- hy (Armenian) - Armenian script (phonetic approximation)
- he (Hebrew) - Hebrew alphabet (phonetic approximation)
- ar (Arabic) - Arabic script (via indic-transliteration Urdu as base)
- tr (Turkish) - IAST Latin
- sw (Swahili) - IAST Latin
"""

import os
import json
from pathlib import Path
from typing import Dict, List
from indic_transliteration import sanscript

# Base directories
BASE_DIR = Path("/Users/anton/proj/gita/data")
SANSKRIT_DIR = BASE_DIR / "sanskrit"
TRANSLATED_DIR = BASE_DIR / "translated"

# Target languages
TARGET_LANGS = ["th", "zh-CN", "zh-TW", "ko", "ja", "el", "ka", "hy", "he", "ar", "tr", "sw"]


def transliterate_to_thai(text: str) -> str:
    """
    Transliterate Devanagari Sanskrit to Thai script.
    Uses IAST as intermediate step.
    """
    try:
        iast_text = sanscript.transliterate(text, sanscript.DEVANAGARI, sanscript.IAST)
        
        # IAST to Thai mapping
        mappings = {
            'ā': 'อา', 'ī': 'อี', 'ū': 'อู', 'ṛ': 'ริ', 'ḷ': 'ลิ',
            'e': 'เอ', 'ai': 'ไอ', 'o': 'โอ', 'au': 'เอา',
            'kh': 'ข', 'gh': 'ฆ', 'ch': 'จ', 'jh': 'ฌ',
            'ṭh': 'ฐ', 'ḍh': 'ฒ', 'th': 'ถ', 'dh': 'ธ',
            'ph': 'ผ', 'bh': 'ภ', 'ś': 'ศ', 'ṣ': 'ษ',
            'ṅ': 'ง', 'ñ': 'ญ', 'ṇ': 'ณ', 'ṃ': 'ง', 'ḥ': 'ห',
            'a': 'อะ', 'i': 'อิ', 'u': 'อุ',
            'k': 'ก', 'g': 'ค', 'c': 'จ', 'j': 'ช',
            'ṭ': 'ฏ', 'ḍ': 'ฑ', 't': 'ต', 'd': 'ท',
            'p': 'ป', 'b': 'พ', 'm': 'ม',
            'y': 'ย', 'r': 'ร', 'l': 'ล', 'v': 'ว', 's': 'ส', 'h': 'ห',
            ' ': ' ', '।': ' ', '॥': ' ', 'ॐ': 'โอม',
        }
        
        result = iast_text.lower()
        for key in sorted(mappings.keys(), key=len, reverse=True):
            if len(key) > 1:
                result = result.replace(key, mappings[key])
        for key in mappings:
            if len(key) == 1:
                result = result.replace(key, mappings[key])
        
        return result
    except Exception as e:
        print(f"  Thai transliteration error: {e}")
        return text


def transliterate_to_arabic(text: str) -> str:
    """
    Transliterate Devanagari Sanskrit to Arabic script.
    Uses IAST as intermediate step with phonetic approximation.
    """
    try:
        iast_text = sanscript.transliterate(text, sanscript.DEVANAGARI, sanscript.IAST)
        
        # IAST to Arabic mapping (written right-to-left)
        mappings = {
            'ā': 'ا', 'ī': 'ي', 'ū': 'و', 'ṛ': 'رِ', 'ḷ': 'لِ',
            'e': 'ِ', 'ai': 'َيْ', 'o': 'و', 'au': 'َوْ',
            'kh': 'خ', 'gh': 'غ', 'ch': 'تش', 'jh': 'ج',
            'ṭh': 'ط', 'ḍh': 'ض', 'th': 'ث', 'dh': 'ذ',
            'ph': 'ف', 'bh': 'ب', 'ś': 'ش', 'ṣ': 'ص',
            'ṅ': 'نغ', 'ñ': 'ني', 'ṇ': 'ن', 'ṃ': 'مْ', 'ḥ': 'ح',
            'a': 'َ', 'i': 'ِ', 'u': 'ُ',
            'k': 'ك', 'g': 'ج', 'c': 'تش', 'j': 'ج',
            'ṭ': 'ط', 'ḍ': 'ض', 't': 'ت', 'd': 'د',
            'p': 'ب', 'b': 'ب', 'm': 'م',
            'y': 'ي', 'r': 'ر', 'l': 'ل', 'v': 'ف', 's': 'س', 'h': 'ه',
            ' ': ' ', '।': ' ', '॥': ' ', 'ॐ': 'أوم',
        }
        
        result = iast_text.lower()
        for key in sorted(mappings.keys(), key=len, reverse=True):
            if len(key) > 1:
                result = result.replace(key, mappings[key])
        for key in mappings:
            if len(key) == 1:
                result = result.replace(key, mappings[key])
        
        return result
    except Exception as e:
        print(f"  Arabic transliteration error: {e}")
        return text


def transliterate_to_iast(text: str) -> str:
    """Transliterate Devanagari to IAST Latin."""
    try:
        return sanscript.transliterate(text, sanscript.DEVANAGARI, sanscript.IAST)
    except Exception as e:
        print(f"  IAST transliteration error: {e}")
        return text


def devanagari_to_katakana(text: str) -> str:
    """
    Transliterate Devanagari Sanskrit to Japanese Katakana.
    Uses IAST as intermediate step.
    """
    try:
        iast_text = sanscript.transliterate(text, sanscript.DEVANAGARI, sanscript.IAST)
        
        # IAST to Katakana mapping
        mappings = {
            'ā': 'アー', 'ī': 'イー', 'ū': 'ウー', 'ṛ': 'リ', 'ḷ': 'ル',
            'ṝ': 'リー', 'e': 'エ', 'ai': 'アイ', 'o': 'オ', 'au': 'アウ',
            'kh': 'クハ', 'gh': 'グハ', 'ch': 'チハ', 'jh': 'ヂハ',
            'ṭh': 'トハ', 'ḍh': 'ドハ', 'th': 'トハ', 'dh': 'ドハ',
            'ph': 'プハ', 'bh': 'ブハ', 'ś': 'シャ', 'ṣ': 'シャ',
            'ṅ': 'ン', 'ñ': 'ニ', 'ṇ': 'ナ', 'ṃ': 'ン', 'ḥ': 'ハ',
            'a': 'ア', 'i': 'イ', 'u': 'ウ',
            'k': 'ク', 'g': 'グ', 'c': 'チ', 'j': 'ヂ',
            'ṭ': 'ト', 'ḍ': 'ド', 't': 'ト', 'd': 'ド',
            'p': 'プ', 'b': 'ブ', 'm': 'マ',
            'y': 'ヤ', 'r': 'ラ', 'l': 'ラ', 'v': 'ヴァ', 's': 'サ', 'h': 'ハ',
            ' ': ' ', '।': ' ', '॥': ' ', 'ॐ': 'オーム',
        }
        
        result = iast_text.lower()
        for key in sorted(mappings.keys(), key=len, reverse=True):
            if len(key) > 1:
                result = result.replace(key, mappings[key])
        for key in mappings:
            if len(key) == 1:
                result = result.replace(key, mappings[key])
        
        return result
    except Exception as e:
        print(f"  Katakana transliteration error: {e}")
        return text


def devanagari_to_hangul(text: str) -> str:
    """
    Transliterate Devanagari Sanskrit to Korean Hangul.
    Uses IAST as intermediate step.
    """
    try:
        iast_text = sanscript.transliterate(text, sanscript.DEVANAGARI, sanscript.IAST)
        
        # IAST to Hangul mapping
        mappings = {
            'ā': '아', 'ī': '이', 'ū': '우', 'ṛ': '리', 'ḷ': '리',
            'ṝ': '리', 'e': '에', 'ai': '아이', 'o': '오', 'au': '아우',
            'kh': '크하', 'gh': '그하', 'ch': '치하', 'jh': '자하',
            'ṭh': '타하', 'ḍh': '다하', 'th': '타하', 'dh': '다하',
            'ph': '파하', 'bh': '바하', 'ś': '샤', 'ṣ': '샤',
            'ṅ': '응', 'ñ': '냐', 'ṇ': '나', 'ṃ': '음', 'ḥ': '하',
            'a': '아', 'i': '이', 'u': '우',
            'k': '크', 'g': '그', 'c': '차', 'j': '자',
            'ṭ': '타', 'ḍ': '다', 't': '타', 'd': '다',
            'p': '파', 'b': '바', 'm': '마',
            'y': '야', 'r': '라', 'l': '라', 'v': '바', 's': '사', 'h': '하',
            ' ': ' ', '।': ' ', '॥': ' ', 'ॐ': '옴',
        }
        
        result = iast_text.lower()
        for key in sorted(mappings.keys(), key=len, reverse=True):
            if len(key) > 1:
                result = result.replace(key, mappings[key])
        for key in mappings:
            if len(key) == 1:
                result = result.replace(key, mappings[key])
        
        return result
    except Exception as e:
        print(f"  Hangul transliteration error: {e}")
        return text


def devanagari_to_greek(text: str) -> str:
    """
    Transliterate Devanagari Sanskrit to Greek script.
    Uses IAST as intermediate step.
    """
    try:
        iast_text = sanscript.transliterate(text, sanscript.DEVANAGARI, sanscript.IAST)
        
        # IAST to Greek mapping
        mappings = {
            'ā': 'α', 'ī': 'ι', 'ū': 'υ', 'ṛ': 'ρι', 'ḷ': 'λι',
            'e': 'ε', 'ai': 'αι', 'o': 'ο', 'au': 'αυ',
            'kh': 'χ', 'gh': 'γχ', 'ch': 'τσ', 'jh': 'τζ',
            'ṭh': 'θ', 'ḍh': 'δχ', 'th': 'θ', 'dh': 'δχ',
            'ph': 'φ', 'bh': 'μπχ', 'ś': 'σ', 'ṣ': 'σ',
            'ṅ': 'νγ', 'ñ': 'νι', 'ṇ': 'ν', 'ṃ': 'μ', 'ḥ': 'χ',
            'a': 'α', 'i': 'ι', 'u': 'υ',
            'k': 'κ', 'g': 'γ', 'c': 'τσ', 'j': 'τζ',
            'ṭ': 'τ', 'ḍ': 'δ', 't': 'τ', 'd': 'δ',
            'p': 'π', 'b': 'μπ', 'm': 'μ',
            'y': 'γ', 'r': 'ρ', 'l': 'λ', 'v': 'β', 's': 'σ', 'h': 'χ',
            ' ': ' ', '।': ' ', '॥': ' ', 'ॐ': 'Ωμ',
        }
        
        result = iast_text.lower()
        for key in sorted(mappings.keys(), key=len, reverse=True):
            if len(key) > 1:
                result = result.replace(key, mappings[key])
        for key in mappings:
            if len(key) == 1:
                result = result.replace(key, mappings[key])
        
        return result
    except Exception as e:
        print(f"  Greek transliteration error: {e}")
        return text


def devanagari_to_georgian(text: str) -> str:
    """
    Transliterate Devanagari Sanskrit to Georgian script.
    Uses IAST as intermediate step.
    """
    try:
        iast_text = sanscript.transliterate(text, sanscript.DEVANAGARI, sanscript.IAST)
        
        # IAST to Georgian mapping
        mappings = {
            'ā': 'ა', 'ī': 'ი', 'ū': 'უ', 'ṛ': 'რი', 'ḷ': 'ლი',
            'e': 'ე', 'ai': 'აი', 'o': 'ო', 'au': 'აუ',
            'kh': 'ხ', 'gh': 'ღ', 'ch': 'ჩ', 'jh': 'ჯხ',
            'ṭh': 'თხ', 'ḍh': 'დხ', 'th': 'თხ', 'dh': 'დხ',
            'ph': 'ფ', 'bh': 'ბხ', 'ś': 'შ', 'ṣ': 'შ',
            'ṅ': 'ნგ', 'ñ': 'ნი', 'ṇ': 'ნ', 'ṃ': 'მ', 'ḥ': 'ჰ',
            'a': 'ა', 'i': 'ი', 'u': 'უ',
            'k': 'კ', 'g': 'გ', 'c': 'ჩ', 'j': 'ჯ',
            'ṭ': 'ტ', 'ḍ': 'დ', 't': 'ტ', 'd': 'დ',
            'p': 'პ', 'b': 'ბ', 'm': 'მ',
            'y': 'ი', 'r': 'რ', 'l': 'ლ', 'v': 'ვ', 's': 'ს', 'h': 'ჰ',
            ' ': ' ', '।': ' ', '॥': ' ', 'ॐ': 'ომ',
        }
        
        result = iast_text.lower()
        for key in sorted(mappings.keys(), key=len, reverse=True):
            if len(key) > 1:
                result = result.replace(key, mappings[key])
        for key in mappings:
            if len(key) == 1:
                result = result.replace(key, mappings[key])
        
        return result
    except Exception as e:
        print(f"  Georgian transliteration error: {e}")
        return text


def devanagari_to_armenian(text: str) -> str:
    """
    Transliterate Devanagari Sanskrit to Armenian script.
    Uses IAST as intermediate step.
    """
    try:
        iast_text = sanscript.transliterate(text, sanscript.DEVANAGARI, sanscript.IAST)
        
        # IAST to Armenian mapping
        mappings = {
            'ā': 'ա', 'ī': 'ի', 'ū': 'ու', 'ṛ': 'րի', 'ḷ': 'լի',
            'e': 'ե', 'ai': 'այ', 'o': 'ո', 'au': 'աու',
            'kh': 'խ', 'gh': 'ղ', 'ch': 'չ', 'jh': 'ջխ',
            'ṭh': 'թխ', 'ḍh': 'դխ', 'th': 'թխ', 'dh': 'դխ',
            'ph': 'փ', 'bh': 'բխ', 'ś': 'շ', 'ṣ': 'շ',
            'ṅ': 'նգ', 'ñ': 'նի', 'ṇ': 'ն', 'ṃ': 'մ', 'ḥ': 'հ',
            'a': 'ա', 'i': 'ի', 'u': 'ու',
            'k': 'կ', 'g': 'գ', 'c': 'չ', 'j': 'ջ',
            'ṭ': 'տ', 'ḍ': 'դ', 't': 'տ', 'd': 'դ',
            'p': 'պ', 'b': 'բ', 'm': 'մ',
            'y': 'յ', 'r': 'ր', 'l': 'լ', 'v': 'վ', 's': 'ս', 'h': 'հ',
            ' ': ' ', '।': ' ', '॥': ' ', 'ॐ': 'օմ',
        }
        
        result = iast_text.lower()
        for key in sorted(mappings.keys(), key=len, reverse=True):
            if len(key) > 1:
                result = result.replace(key, mappings[key])
        for key in mappings:
            if len(key) == 1:
                result = result.replace(key, mappings[key])
        
        return result
    except Exception as e:
        print(f"  Armenian transliteration error: {e}")
        return text


def devanagari_to_hebrew(text: str) -> str:
    """
    Transliterate Devanagari Sanskrit to Hebrew script.
    Uses IAST as intermediate step.
    """
    try:
        iast_text = sanscript.transliterate(text, sanscript.DEVANAGARI, sanscript.IAST)
        
        # IAST to Hebrew mapping (written right-to-left)
        mappings = {
            'ā': 'ָ', 'ī': 'ִי', 'ū': 'וּ', 'ṛ': 'רִ', 'ḷ': 'לִ',
            'e': 'ֵ', 'ai': 'ַי', 'o': 'וֹ', 'au': 'ַו',
            'kh': 'כְח', 'gh': 'גְח', 'ch': 'צְח', 'jh': 'ג׳ח',
            'ṭh': 'טְח', 'ḍh': 'דְח', 'th': 'תְח', 'dh': 'דְח',
            'ph': 'פְח', 'bh': 'בְח', 'ś': 'שׁ', 'ṣ': 'שׁ',
            'ṅ': 'נְג', 'ñ': 'נְי', 'ṇ': 'נ', 'ṃ': 'ם', 'ḥ': 'ח',
            'a': 'ַ', 'i': 'ִ', 'u': 'ֻ',
            'k': 'כ', 'g': 'ג', 'c': 'צ', 'j': 'ג׳',
            'ṭ': 'ט', 'ḍ': 'ד', 't': 'ת', 'd': 'ד',
            'p': 'פ', 'b': 'ב', 'm': 'מ',
            'y': 'י', 'r': 'ר', 'l': 'ל', 'v': 'ו', 's': 'ס', 'h': 'ה',
            ' ': ' ', '।': ' ', '॥': ' ', 'ॐ': 'אום',
        }
        
        result = iast_text.lower()
        for key in sorted(mappings.keys(), key=len, reverse=True):
            if len(key) > 1:
                result = result.replace(key, mappings[key])
        for key in mappings:
            if len(key) == 1:
                result = result.replace(key, mappings[key])
        
        return result
    except Exception as e:
        print(f"  Hebrew transliteration error: {e}")
        return text


def devanagari_to_chinese_simplified(text: str) -> str:
    """
    Transliterate Devanagari Sanskrit to Chinese Simplified with Pinyin.
    Uses common Buddhist transliteration conventions.
    """
    try:
        # Common Sanskrit Buddhist terms in Chinese
        term_mappings = {
            'धृतराष्ट्र': '德里塔拉什特拉',
            'उवाच': '乌瓦查',
            'धर्मक्षेत्रे': '达摩刹特拉',
            'कुरुक्षेत्रे': '俱卢刹特拉',
            'समवेता': '萨马维塔',
            'युयुत्सवः': '尤尤察瓦',
            'मामकाः': '马马卡',
            'पाण्डवाः': '潘达瓦',
            'च': '和',
            'एव': '确实',
            'किम्': '什么',
            'अकुर्वत': '阿库尔瓦塔',
            'सञ्जय': '桑贾亚',
            'भगवान': '薄伽梵',
            'अर्जुन': '阿周那',
            'कृष्ण': '克里希纳',
            'योग': '瑜伽',
            'सांख्य': '数论',
            'वेदान्त': '吠檀多',
            'उपनिषद्': '奥义书',
            'गीता': '歌塔',
            'अध्याय': '章',
            'श्लोक': '颂',
            'महाभारत': '摩诃婆罗多',
            'धर्म': '达摩',
            'कर्म': '业',
            'आत्मन्': '我',
            'ब्रह्मन्': '梵',
            'विष्णु': '毗湿奴',
            'शिव': '湿婆',
        }
        
        result = text
        # Apply term mappings first
        for term in sorted(term_mappings.keys(), key=len, reverse=True):
            if term in result:
                result = result.replace(term, term_mappings[term])
        
        # For remaining Devanagari, convert to Pinyin approximation
        remaining = result
        if any('\u0900' <= c <= '\u097F' for c in remaining):
            # Convert remaining to IAST then to Pinyin-like representation
            iast = sanscript.transliterate(remaining, sanscript.DEVANAGARI, sanscript.IAST)
            # Simple character mapping for remaining text
            pinyin_map = {
                'ā': 'ā', 'ī': 'ī', 'ū': 'ū', 'ṛ': 'ṛ', 'ḷ': 'ḷ',
                'ṃ': 'ṃ', 'ḥ': 'ḥ', 'ś': 'ś', 'ṣ': 'ṣ',
                ' ': ' ', '।': ' ', '॥': '',
            }
            for k, v in pinyin_map.items():
                iast = iast.replace(k, v)
            result = iast
        
        return result
    except Exception as e:
        print(f"  Chinese Simplified transliteration error: {e}")
        return text


def devanagari_to_chinese_traditional(text: str) -> str:
    """
    Transliterate Devanagari Sanskrit to Chinese Traditional.
    Similar to Simplified but with traditional character forms.
    """
    try:
        # Start with simplified, then convert key terms to traditional
        simplified = devanagari_to_chinese_simplified(text)
        
        # Traditional variants for Buddhist terms
        trad_mappings = {
            '达摩': '達摩',
            '刹特拉': '剎特拉',
            '俱卢': '俱盧',
            '萨马维塔': '薩馬維塔',
            '潘达瓦': '潘達瓦',
            '桑贾亚': '桑賈亞',
            '薄伽梵': '薄伽梵',
            '阿周那': '阿周那',
            '克里希纳': '克里希納',
            '瑜伽': '瑜伽',
            '数论': '數論',
            '吠檀多': '吠檀多',
            '奥义书': '奧義書',
            '歌塔': '歌塔',
            '摩诃婆罗多': '摩訶婆羅多',
            '业': '業',
            '梵': '梵',
            '毗湿奴': '毗濕奴',
            '湿婆': '濕婆',
        }
        
        result = simplified
        for simp, trad in trad_mappings.items():
            result = result.replace(simp, trad)
        
        return result
    except Exception as e:
        print(f"  Chinese Traditional transliteration error: {e}")
        return text


def get_transliteration(text: str, lang: str) -> str:
    """Get transliteration for a given language."""
    translit_functions = {
        'th': transliterate_to_thai,
        'ar': transliterate_to_arabic,
        'tr': transliterate_to_iast,
        'sw': transliterate_to_iast,
        'ja': devanagari_to_katakana,
        'ko': devanagari_to_hangul,
        'zh-CN': devanagari_to_chinese_simplified,
        'zh-TW': devanagari_to_chinese_traditional,
        'el': devanagari_to_greek,
        'ka': devanagari_to_georgian,
        'hy': devanagari_to_armenian,
        'he': devanagari_to_hebrew,
    }
    
    func = translit_functions.get(lang)
    if func:
        return func(text)
    return text  # Fallback


def get_sloka_files(chapter_dir: Path) -> List[Path]:
    """Get all sloka files from a chapter directory."""
    return sorted([f for f in chapter_dir.glob('*_sloka.txt') if 'meta' not in f.name])


def process_chapter_transliteration(chapter_num: int, target_langs: List[str]) -> Dict[str, int]:
    """
    Process transliteration for a single chapter.
    
    Returns dict with counts of files generated per language.
    """
    chapter_str = f"{chapter_num:02d}"
    sanskrit_chapter_dir = SANSKRIT_DIR / f"chapter-{chapter_str}-sanskrit"
    
    if not sanskrit_chapter_dir.exists():
        print(f"Error: Sanskrit directory not found: {sanskrit_chapter_dir}")
        return {}
    
    sloka_files = get_sloka_files(sanskrit_chapter_dir)
    print(f"Processing Chapter {chapter_num}: {len(sloka_files)} sloka files")
    
    stats = {lang: 0 for lang in target_langs}
    
    for sloka_file in sloka_files:
        # Read Sanskrit text (Devanagari)
        with open(sloka_file, 'r', encoding='utf-8') as f:
            sanskrit_text = f.read().strip()
        
        # Extract sloka identifier from filename
        # e.g., chapter-01-1.1-sanskrit_sloka.txt -> 1.1
        filename = sloka_file.name
        parts = filename.replace('chapter-', '').replace('-sanskrit_sloka.txt', '').split('-')
        sloka_id = parts[1] if len(parts) > 1 else parts[0]
        
        # Generate and save transliteration for each language
        for lang in target_langs:
            lang_dir = TRANSLATED_DIR / lang / f"chapter-{chapter_str}-{lang}"
            lang_dir.mkdir(parents=True, exist_ok=True)
            
            translit_text = get_transliteration(sanskrit_text, lang)
            
            output_file = lang_dir / f"chapter-{chapter_str}-{sloka_id}-{lang}_translit.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(translit_text)
            
            stats[lang] += 1
    
    return stats


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate transliterations for GitaBook slokas')
    parser.add_argument('--chapter', type=int, required=True, help='Chapter number to process')
    parser.add_argument('--languages', nargs='+', default=TARGET_LANGS,
                       help='Target languages (default: all 12)')
    
    args = parser.parse_args()
    
    print(f"Generating transliterations for Chapter {args.chapter}")
    print(f"Target languages: {', '.join(args.languages)}")
    print("-" * 60)
    
    stats = process_chapter_transliteration(args.chapter, args.languages)
    
    print("-" * 60)
    print("Summary:")
    total = 0
    for lang, count in sorted(stats.items()):
        print(f"  {lang}: {count} files")
        total += count
    print(f"  TOTAL: {total} files")


if __name__ == '__main__':
    main()
