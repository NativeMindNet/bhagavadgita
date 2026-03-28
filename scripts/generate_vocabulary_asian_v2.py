#!/usr/bin/env python3
"""
Generate vocabulary-asian.json with proper transliterations.
Processes chapters 2-6.
"""

import json
import re
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent

# Sanskrit to target script transliteration mappings
SANSKRIT_TO_THAI = {
    'a': 'อะ', 'ā': 'อา', 'i': 'อิ', 'ī': 'อี', 'u': 'อุ', 'ū': 'อู',
    'ṛ': 'ริ', 'ṝ': 'รี', 'ḷ': 'ลิ', 'e': 'เอ', 'ai': 'ไอ', 'o': 'โอ', 'au': 'เอา',
    'k': 'ก', 'kh': 'ข', 'g': 'ค', 'gh': 'ฆ', 'ṅ': 'ง',
    'c': 'จ', 'ch': 'ฉ', 'j': 'ช', 'jh': 'ฌ', 'ñ': 'ญ',
    'ṭ': 'ฏ', 'ṭh': 'ฐ', 'ḍ': 'ฑ', 'ḍh': 'ฒ', 'ṇ': 'ณ',
    't': 'ต', 'th': 'ถ', 'd': 'ท', 'dh': 'ธ', 'n': 'น',
    'p': 'ป', 'ph': 'ผ', 'b': 'พ', 'bh': 'ภ', 'm': 'ม',
    'y': 'ย', 'r': 'ร', 'l': 'ล', 'v': 'ว', 'ś': 'ศ', 'ṣ': 'ษ', 's': 'ส', 'h': 'ห',
    "'": '์', 'ṃ': 'ง', 'ḥ': 'หะ',
}

SANSKRIT_TO_ZH_TW = {
    'a': '阿', 'ā': '阿', 'i': '伊', 'ī': '伊', 'u': '烏', 'ū': '烏',
    'ṛ': '利', 'e': '埃', 'ai': '艾', 'o': '奧', 'au': '奧',
    'k': '卡', 'kh': '卡', 'g': '嘎', 'gh': '嘎', 'ṅ': '昂',
    'c': '恰', 'ch': '恰', 'j': '佳', 'jh': '佳', 'ñ': '尼',
    'ṭ': '塔', 'ṭh': '塔', 'ḍ': '達', 'ḍh': '達', 'ṇ': '那',
    't': '塔', 'th': '塔', 'd': '達', 'dh': '達', 'n': '那',
    'p': '帕', 'ph': '帕', 'b': '巴', 'bh': '巴', 'm': '瑪',
    'y': '亞', 'r': '拉', 'l': '拉', 'v': '瓦', 'ś': '夏', 'ṣ': '夏', 's': '薩', 'h': '哈',
    "'": '', 'ṃ': '姆', 'ḥ': '哈',
}

SANSKRIT_TO_JA = {
    'a': 'ア', 'ā': 'アー', 'i': 'イ', 'ī': 'イー', 'u': 'ウ', 'ū': 'ウー',
    'ṛ': 'リ', 'e': 'エ', 'ai': 'アイ', 'o': 'オ', 'au': 'アウ',
    'k': 'ク', 'kh': 'ク', 'g': 'グ', 'gh': 'グ', 'ṅ': 'ン',
    'c': 'チャ', 'ch': 'チャ', 'j': 'ジャ', 'jh': 'ジャ', 'ñ': 'ニャ',
    'ṭ': 'タ', 'ṭh': 'タ', 'ḍ': 'ダ', 'ḍh': 'ダ', 'ṇ': 'ナ',
    't': 'タ', 'th': 'タ', 'd': 'ダ', 'dh': 'ダ', 'n': 'ナ',
    'p': 'パ', 'ph': 'パ', 'b': 'バ', 'bh': 'バ', 'm': 'マ',
    'y': 'ヤ', 'r': 'ラ', 'l': 'ラ', 'v': 'ヴァ', 'ś': 'シャ', 'ṣ': 'シャ', 's': 'サ', 'h': 'ハ',
    "'": 'ー', 'ṃ': 'ン', 'ḥ': 'ハ',
}

SANSKRIT_TO_KO = {
    'a': '아', 'ā': '아', 'i': '이', 'ī': '이', 'u': '우', 'ū': '우',
    'ṛ': '리', 'e': '에', 'ai': '아이', 'o': '오', 'au': '아우',
    'k': '크', 'kh': '크', 'g': '그', 'gh': '그', 'ṅ': '응',
    'c': '차', 'ch': '차', 'j': '자', 'jh': '자', 'ñ': '냐',
    'ṭ': '타', 'ṭh': '타', 'ḍ': '다', 'ḍh': '다', 'ṇ': '나',
    't': '타', 'th': '타', 'd': '다', 'dh': '다', 'n': '나',
    'p': '파', 'ph': '파', 'b': '바', 'bh': '바', 'm': '마',
    'y': '야', 'r': '라', 'l': '라', 'v': '바', 'ś': '샤', 'ṣ': '샤', 's': '사', 'h': '하',
    "'": '', 'ṃ': '음', 'ḥ': '하',
}

# Common term transliterations (pre-computed)
COMMON_TRANSLITERATIONS = {
    "he": {"th": "เห", "zh-TW": "嘿", "ja": "ヘー", "ko": "헤"},
    "kaunteya": {"th": "เกาุนเตยะ", "zh-TW": "考unteya", "ja": "カウンテーヤ", "ko": "카운테야"},
    "kuru-nandana": {"th": "กุรุนันทนะ", "zh-TW": "古魯南達那", "ja": "クルナンダナ", "ko": "쿠루난다나"},
    "madhusūdana": {"th": "มธุสูทน", "zh-TW": "瑪都蘇丹", "ja": "マドゥスーダナ", "ko": "마두수다나"},
    "arisūdana": {"th": "อริสูทน", "zh-TW": "阿利蘇丹", "ja": "アリスーダナ", "ko": "아리스다나"},
    "mahā-bāho": {"th": "มหาพาโห", "zh-TW": "瑪哈巴霍", "ja": "マハーバーホ", "ko": "마하바호"},
    "parantapa": {"th": "ปรันตปะ", "zh-TW": "帕蘭塔帕", "ja": "パランタパ", "ko": "파란타파"},
    "puruṣa-ṛṣabha": {"th": "ปุรุษะฤษภะ", "zh-TW": "普魯沙利沙巴", "ja": "プルシャリシャバ", "ko": "푸루샤리샤바"},
    "pārtha": {"th": "ปารถะ", "zh-TW": "帕爾塔", "ja": "パールタ", "ko": "팔타"},
    "mātrā-sparśāḥ": {"th": "มาตรา-สปะรशाห์", "zh-TW": "瑪特拉-斯帕爾沙", "ja": "マートラー・スパルシャー", "ko": "마트라-스파르샤"},
    "āgamāc-chānti": {"th": "อามา-ฉันติ", "zh-TW": "阿瑪-尚提", "ja": "アーガマッチャンティ", "ko": "아가마찬티"},
    "yatra": {"th": "ยัตระ", "zh-TW": "雅特拉", "ja": "ヤトラ", "ko": "야트라"},
    "arthaṣu": {"th": "อรรถะษุ", "zh-TW": "阿爾塔蘇", "ja": "アルタシュ", "ko": "아르타슈"},
    "uktam": {"th": "อุกฺตัม", "zh-TW": "烏克塔姆", "ja": "ウクタム", "ko": "우크탐"},
    "me": {"th": "เม", "zh-TW": "梅", "ja": "メー", "ko": "메"},
    "ādau": {"th": "อาทาวฺ", "zh-TW": "阿達武", "ja": "アーダヴ", "ko": "아다브"},
    "aviśyam": {"th": "อวิศฺยัม", "zh-TW": "阿維沙姆", "ja": "アヴィシャム", "ko": "아비샴"},
    "acalam": {"th": "อะจลัม", "zh-TW": "阿恰拉姆", "ja": "アチャラム", "ko": "아찰람"},
    "śritam": {"th": "ศฺริตะมฺ", "zh-TW": "什利塔姆", "ja": "シュリタム", "ko": "슈리탐"},
    "atha": {"th": "อะถะ", "zh-TW": "阿塔", "ja": "アタ", "ko": "아타"},
    "vā": {"th": "วา", "zh-TW": "瓦", "ja": "ヴァー", "ko": "바"},
    "sva-dharmam": {"th": "สวะ-ธรฺมัม", "zh-TW": "斯瓦-達爾瑪姆", "ja": "スヴァ・ダルマム", "ko": "스바・다르마ム"},
    "akurvāṇaḥ": {"th": "อะกฺรุวานะห์", "zh-TW": "阿庫爾瓦納赫", "ja": "アクルヴァーナハ", "ko": "아쿠르바나하"},
    "akīrteś": {"th": "อะกีรฺเตศฺ", "zh-TW": "阿基爾泰什", "ja": "アキールテーシュ", "ko": "아키르테시"},
    "ca": {"th": "จะ", "zh-TW": "恰", "ja": "チャ", "ko": "차"},
    "ambhasi": {"th": "อัมภสิ", "zh-TW": "安巴西", "ja": "アンバシ", "ko": "암바시"},
    "anta-kāle": {"th": "อันตะ-กาเล", "zh-TW": "安塔-卡莱", "ja": "アンタ・カーレ", "ko": "안타・칼레"},
    "vināśinam": {"th": "วินาศินัม", "zh-TW": "維納辛納姆", "ja": "ヴィナーシナム", "ko": "비나시남"},
    "eṣa": {"th": "เอษะ", "zh-TW": "埃沙", "ja": "エシャ", "ko": "에샤"},
    "abhiprāyaḥ": {"th": "อภิปรายะห์", "zh-TW": "阿比普拉亞赫", "ja": "アビプラヤーハ", "ko": "아비프라야하"},
    "yasya": {"th": "ยัสยะ", "zh-TW": "雅薩雅", "ja": "ヤサヤ", "ko": "야사야"},
    "manaḥ": {"th": "มะนะห์", "zh-TW": "馬納赫", "ja": "マナハ", "ko": "마나하"},
    "sthiram": {"th": "สฺถิรัม", "zh-TW": "斯蒂拉姆", "ja": "スティラム", "ko": "스티람"},
    "anuśocitum": {"th": "อะนุโศจิตุมฺ", "zh-TW": "阿努索奇特姆", "ja": "アヌソーチトゥム", "ko": "아누소치툼"},
    "arhasi": {"th": "อรฺหสิ", "zh-TW": "阿爾哈西", "ja": "アルハシ", "ko": "아르하시"},
    "śreyān": {"th": "ศฺเรยานฺ", "zh-TW": "什雷揚", "ja": "シュレヤーン", "ko": "슈레얀"},
    "sva-dharmo": {"th": "สวะ-ธรฺโม", "zh-TW": "斯瓦-達爾莫", "ja": "スヴァ・ダルモ", "ko": "스바・다르모"},
    "aparihāryārthe": {"th": "อะปะริหารฺยัรฺถะ", "zh-TW": "阿帕里哈爾亞爾塔", "ja": "アパリハールヤルタ", "ko": "아파리하르야르타"},
    "acintyo": {"th": "อะจินฺตฺโย", "zh-TW": "阿金提ョ", "ja": "アチンティョ", "ko": "아친티ョ"},
    "aprameyaś": {"th": "อะปฺระเมยศฺ", "zh-TW": "阿普拉梅亞什", "ja": "アプラメーヤシュ", "ko": "아프라메야슈"},
    "svarga": {"th": "สฺวர்கฺคะ", "zh-TW": "斯瓦格加", "ja": "スヴァッガ", "ko": "스바가"},
    "dvāram": {"th": "ทฺวารัม", "zh-TW": "德瓦拉姆", "ja": "ドヴァーラム", "ko": "드바람"},
    "artha": {"th": "อรรถะ", "zh-TW": "阿爾塔", "ja": "アルタ", "ko": "아르타"},
    "kāmān": {"th": "กามานฺ", "zh-TW": "卡曼", "ja": "カーマーン", "ko": "카만"},
    "svarga": {"th": "สฺวர்கฺคะ", "zh-TW": "斯瓦格加", "ja": "スヴァッガ", "ko": "스바가"},
    "vighnam": {"th": "วิฆฺนัม", "zh-TW": "維格納姆", "ja": "ヴィグナム", "ko": "비그남"},
    "ayata": {"th": "อะยะตะ", "zh-TW": "阿雅塔", "ja": "アヤタ", "ko": "아야타"},
    "indriyasya": {"th": "อินฺทฺริยสะยะ", "zh-TW": "因德里亞薩雅", "ja": "インドリヤサヤ", "ko": "인드리야사야"},
    "maraṇasya": {"th": "มะรฺณัสยะ", "zh-TW": "馬爾納薩雅", "ja": "マルナサヤ", "ko": "마르나사야"},
    "ata": {"th": "อะตะ", "zh-TW": "阿塔", "ja": "アタ", "ko": "아타"},
    "evam": {"th": "เอวัม", "zh-TW": "埃瓦姆", "ja": "エーヴァム", "ko": "에밤"},
    "janmanaḥ": {"th": "ชันฺมะนะห์", "zh-TW": "占馬納赫", "ja": "ジャンマナハ", "ko": "잠마나하"},
    "avyavasāyātmānām": {"th": "อะวิยฺวาสิตาตฺมานามฺ", "zh-TW": "阿維瓦西塔特馬納姆", "ja": "アヴィヴァーシタートマーム", "ko": "아비바시타트마암"},
    "acchedyo": {"th": "อะเฉทฺโย", "zh-TW": "阿切德โย", "ja": "アチェードョ", "ko": "아체드요"},
    "ayam": {"th": "ยัม", "zh-TW": "ยัม", "ja": "ヤム", "ko": "얌"},
    "na": {"th": "นะ", "zh-TW": "那", "ja": "ナ", "ko": "나"},
    "jāyate": {"th": "ชายะเต", "zh-TW": "恰雅泰", "ja": "ジャーヤテー", "ko": "자야테"},
    "nityaḥ": {"th": "นิตฺยะห์", "zh-TW": "尼提ョ赫", "ja": "ニティョハ", "ko": "니티ョ하"},
    "śāśvato": {"th": "ศฺวาศฺวะโต", "zh-TW": "什瓦什瓦托", "ja": "シュヴァーシュヴァト", "ko": "슈바슈바토"},
    "ucyate": {"th": "อุจฺยะเต", "zh-TW": "烏恰雅泰", "ja": "ウチャーテー", "ko": "우차테"},
    "naṣṭa": {"th": "นะษฺฏะ", "zh-TW": "納什塔", "ja": "ナシュタ", "ko": "나슈타"},
    "buddhīnām": {"th": "พุทธีนาามฺ", "zh-TW": "布迪納姆", "ja": "ブッディナーム", "ko": "부디나암"},
    "aśocyān": {"th": "อะโศจฺยานฺ", "zh-TW": "阿索吉安", "ja": "アソーチャン", "ko": "아소찬"},
    "bāṣpa": {"th": "บาษฺปะ", "zh-TW": "巴什帕", "ja": "バーシュパ", "ko": "바슈파"},
    "ākula": {"th": "อะากุละ", "zh-TW": "阿庫拉", "ja": "アクラ", "ko": "아클라"},
    "īkṣaṇam": {"th": "อีกฺษะณัม", "zh-TW": "イクシャ納姆", "ja": "イクシャナム", "ko": "이크샤남"},
    "pūjārhā": {"th": "ปูชฺยารฺหา", "zh-TW": "普賈爾哈", "ja": "プージャールハー", "ko": "푸자르하"},
    "bhayāt": {"th": "ภะยาตฺ", "zh-TW": "巴亞特", "ja": "バヤート", "ko": "바야트"},
    "bhoga": {"th": "โภคะ", "zh-TW": "博加", "ja": "ボーガ", "ko": "보가"},
    "aiśvarya": {"th": "ไอศฺวะรฺยะ", "zh-TW": "艾什瓦爾亞", "ja": "アイシュヴァリヤ", "ko": "아이슈바리야"},
    "prasaktānām": {"th": "ประสฺกฺตะ", "zh-TW": "普拉薩克塔", "ja": "プラサクターム", "ko": "프라삭타암"},
    "tayā": {"th": "ตะยฺยา", "zh-TW": "塔亞", "ja": "タイヤ", "ko": "타이야"},
    "hṛta": {"th": "หฺฤตะ", "zh-TW": "赫利塔", "ja": "フリタ", "ko": "흐리타"},
    "cetasām": {"th": "เจตสาามฺ", "zh-TW": "切塔薩姆", "ja": "チェータサーム", "ko": "체타사암"},
    "vīta": {"th": "วีตะ", "zh-TW": "維塔", "ja": "ヴィータ", "ko": "비타"},
    "rāga": {"th": "ราคะ", "zh-TW": "拉加", "ja": "ラーガ", "ko": "라가"},
    "bhaya": {"th": "ภะยะ", "zh-TW": "巴亞", "ja": "バヤ", "ko": "바야"},
    "krodha": {"th": "โกรธา", "zh-TW": "โกรธา", "ja": "クローダ", "ko": "크로다"},
}

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def transliterate_sanskrit(word, target_lang):
    """Transliterate Sanskrit word to target script."""
    # Clean the word
    clean_word = word.strip('()').lower()
    
    # Check for pre-computed transliteration
    for term, trans in COMMON_TRANSLITERATIONS.items():
        if term in clean_word:
            # Use pre-computed if available
            pass
    
    # Check if we have a direct match
    if clean_word in COMMON_TRANSLITERATIONS:
        return COMMON_TRANSLITERATIONS[clean_word][target_lang]
    
    # Select the appropriate mapping
    if target_lang == 'th':
        mapping = SANSKRIT_TO_THAI
    elif target_lang == 'zh-TW':
        mapping = SANSKRIT_TO_ZH_TW
    elif target_lang == 'ja':
        mapping = SANSKRIT_TO_JA
    elif target_lang == 'ko':
        mapping = SANSKRIT_TO_KO
    else:
        return clean_word
    
    # Simple character-by-character transliteration
    result = clean_word
    # Sort by length (longer patterns first)
    for src in sorted(mapping.keys(), key=len, reverse=True):
        result = result.replace(src, mapping[src])
    
    return result

def generate_transliteration(word):
    """Generate transliteration for all target languages."""
    return {
        "th": transliterate_sanskrit(word, 'th'),
        "zh-TW": transliterate_sanskrit(word, 'zh-TW'),
        "ja": transliterate_sanskrit(word, 'ja'),
        "ko": transliterate_sanskrit(word, 'ko')
    }

# Translation dictionary (same as before)
TERM_TRANSLATIONS = {
    "by worshipping the Supreme Lord": {"th": "โดยการบูชาพระผู้เป็นเจ้าสูงสุด", "zh-TW": "通過崇拜至尊主", "ja": "至高なる主を崇拝することによって", "ko": "지고하신 주를 숭배함으로써"},
    "O Arjuna, son of Kuntī": {"th": "โอ้ อรชุน บุตรของกุนตี", "zh-TW": "哦 阿周那，貢蒂之子", "ja": "おお アルジュナ、クンティーの子よ", "ko": "오 아르주나, 쿤티의 아들아"},
    "O Arjuna, descendant of the Kuru dynasty": {"th": "โอ้ อรชุน ผู้สืบเชื้อสายแห่งวงศ์กุรุ", "zh-TW": "哦 阿周那，俱盧王朝的後裔", "ja": "おお アルジュナ、クル王朝の子孫よ", "ko": "오 아르주나, 쿠루 왕조의 후손이여"},
    "O Madhusūdan, slayer of the enemy": {"th": "โอ้ มธุสูทน ผู้สังหารศัตรู", "zh-TW": "哦 瑪都蘇丹，殺敵者", "ja": "おお マドゥスーダナ、敵を倒す者よ", "ko": "오 마두수다나여, 적을 물리치는 이여"},
    "O subduer of the enemy": {"th": "โอ้ ผู้พิชิตศัตรู", "zh-TW": "哦 征服敵人者", "ja": "おお 敵を征服する者よ", "ko": "오 적을 정복하는 이여"},
    "O noblest of men": {"th": "โอ้ ผู้ประเสริฐสุดในบรรดาบุรุษ", "zh-TW": "哦 人中最傑出的", "ja": "おお 人々の中で最も優れた方よ", "ko": "오 사람들 중 가장 고귀한 이여"},
    "O son of Kuntī": {"th": "โอ้ บุตรของกุนตี", "zh-TW": "哦 貢蒂之子", "ja": "おお クンティーの子よ", "ko": "오 쿤티의 아들아"},
    "nor is it that": {"th": "และก็ไม่ใช่ว่า", "zh-TW": "也不是", "ja": "〜というわけでもない", "ko": "그런 것도 아니다"},
    "It is not a fact that": {"th": "ไม่ใช่ความจริงที่ว่า", "zh-TW": "事實並非如此", "ja": "〜というのは事実ではない", "ko": "사실이 아닌 것은"},
    "actions of the senses engaging with material sense objects": {"th": "การกระทำของประสาทสัมผัสที่เกี่ยวเนื่องกับวัตถุแห่งประสาทสัมผัส", "zh-TW": "感官與感官對象的接觸", "ja": "感覚器官が感覚対象と接触すること", "ko": "감각 기관이 감각 대상과 접촉하는 것"},
    "These come and go": {"th": "สิ่งเหล่านี้มาและไป", "zh-TW": "它們來而又去", "ja": "これらは来たり去ったりする", "ko": "이것들은 왔다가 간다"},
    "of the various purposes fulfilled": {"th": "ของวัตถุประสงค์ต่างๆ ที่บรรลุ", "zh-TW": "各種目的的達成", "ja": "様々な目的が達成されること", "ko": "다양한 목적의 성취"},
    "I have revealed to you": {"th": "เราได้เปิดเผยแก่เจ้าแล้ว", "zh-TW": "我已向你揭示", "ja": "私はあなたに明かした", "ko": "내가 너에게 드러냈다"},
    "failure in the beginning": {"th": "ความล้มเหลวในตอนเริ่มต้น", "zh-TW": "開始時的失敗", "ja": "初めにおける失敗", "ko": "처음의 실패"},
    "it remains steady, its water never crossing the shore": {"th": "มันยังคงมั่นคง น้ำไม่ไหลข้ามฝั่ง", "zh-TW": "它保持穩定，水不越過岸邊", "ja": "それは安定しており、水は岸を越えない", "ko": "그것은 안정적이고, 물은 둑을 넘지 않는다"},
    "or the living": {"th": "หรือสิ่งมีชีวิต", "zh-TW": "或生物", "ja": "または生物", "ko": "또는 생물"},
    "non-performance of your prescribed duties": {"th": "การไม่ปฏิบัติหน้าที่ที่กำหนดไว้ของเจ้า", "zh-TW": "你不履行規定的職責", "ja": "あなたの定められた義務を遂行しないこと", "ko": "네게 정해진 의무를 수행하지 않는 것"},
    "and the cause of infamy": {"th": "และเป็นสาเหตุของการเสียชื่อเสียง", "zh-TW": "並且是臭名昭著的原因", "ja": "そして不名誉の原因となる", "ko": "그리고 불명예의 원인이 된다"},
    "on the ocean": {"th": "บนมหาสมุทร", "zh-TW": "在海洋上", "ja": "海の上に", "ko": "바다 위에"},
    "even at the time of death": {"th": "แม้ในยามเสียชีวิต", "zh-TW": "即使在死亡之時", "ja": "死の時でさえ", "ko": "죽음의 때에도"},
    "subject to destruction": {"th": "ต้องถูกทำลาย", "zh-TW": "易於毀滅", "ja": "破壊されやすい", "ko": "파괴되기 쉬운"},
    "Such a conclusion, i.e., of the nature": {"th": "ข้อสรุปดังกล่าว เช่น ธรรมชาติของ", "zh-TW": "這樣的結論，即的本質", "ja": "そのような結論、すなわち〜の性質", "ko": "그런 결론, 즉〜의 본성"},
    "One whose mind is undisturbed": {"th": "ผู้ที่มีจิตไม่หวั่นไหว", "zh-TW": "心念不受擾亂的人", "ja": "心が乱されない人", "ko": "마음이 흔들리지 않는 사람"},
    "it is inappropriate to grieve for it": {"th": "ไม่เหมาะสมที่จะเศร้าโศกสำหรับมัน", "zh-TW": "為它悲傷是不恰當的", "ja": "それのために悲しむのは適切ではない", "ko": "그것을 위해 슬퍼하는 것은 적절하지 않다"},
    "better course of action": {"th": "วิถีการกระทำที่ดีกว่า", "zh-TW": "更好的行動方針", "ja": "より良い行為の道", "ko": "더 나은 행위의 길"},
    "for the inevitable": {"th": "สำหรับสิ่งที่หลีกเลี่ยงไม่ได้", "zh-TW": "對於不可避免的事", "ja": "避けられないことのために", "ko": "피할 수 없는 것을 위해"},
    "and immeasurable, due to his extremely subtle nature": {"th": "และวัดไม่ได้ เนื่องจากธรรมชาติที่ละเอียดอ่อนอย่างยิ่งของพระองค์", "zh-TW": "且不可測量，因其極其微妙的本質", "ja": "そして測り知れない、その非常に微細な性質のため", "ko": "그리고 측정할 수 없다, 그 매우 미묘한 본성 때문에"},
    "as an open door to heaven": {"th": "เป็นเหมือนประตูเปิดสู่สวรรค์", "zh-TW": "如同通往天堂的敞開之門", "ja": "天国への開かれた門のように", "ko": "천국으로 열리는 문처럼"},
    "wealth and coveted enjoyable objects": {"th": "ความมั่งคั่งและวัตถุที่น่าปรารถนา", "zh-TW": "財富和渴望的享樂對象", "ja": "富と望まれる享楽の対象", "ko": "부와 탐내는 즐거운 대상들"},
    "it is an obstacle to the attainment of heaven": {"th": "เป็นอุปสรรคต่อการบรรลุสวรรค์", "zh-TW": "是獲得天堂的障礙", "ja": "天国の達成に対する障害", "ko": "천국 달성에 대한 장애물"},
    "of that person bereft of self-control": {"th": "ของบุคคลที่ขาดการควบคุมตนเอง", "zh-TW": "那些缺乏自制的人", "ja": "自制心を欠いた人の", "ko": "자제심이 없는 사람의"},
    "and the situation after death is again unknown": {"th": "และสถานการณ์หลังความตายก็ไม่ทราบได้อีกเช่นกัน", "zh-TW": "死後的情況也同樣未知", "ja": "そして死後の状況もまた知られていない", "ko": "그리고 사후의 상황도 또한 알려지지 않았다"},
    "imperceptible due to its extremely subtle nature": {"th": "มองไม่เห็นเนื่องจากธรรมชาติที่ละเอียดอ่อนอย่างยิ่ง", "zh-TW": "因其極其微妙的本質而無法察覺", "ja": "その非常に微細な性質のため知覚できない", "ko": "그 매우 미묘한 본성 때문에 지각할 수 없다"},
    "the situation before birth is unknown": {"th": "สถานการณ์ก่อนเกิดไม่ทราบได้", "zh-TW": "出生前的情況未知", "ja": "出生前の状況は知られていない", "ko": "탄생 전의 상황은 알려지지 않았다"},
    "of the irresolute – those who nurture mundane desires": {"th": "ของผู้ที่ไม่มั่นคง —那些培育世俗慾望的人", "zh-TW": "那些心意不堅定的——培育世俗慾望的人", "ja": "決意しない人々—世俗の欲望を育む人々", "ko": "결의하지 않는 사람들—세속적 욕망을 기르는 사람들"},
    "The soul is indivisible": {"th": "วิญญาณเป็นสิ่งที่แบ่งแยกไม่ได้", "zh-TW": "靈魂是不可分割的", "ja": "魂は分割できない", "ko": "영혼은 나눌 수 없다"},
    "This soul is birthless": {"th": "วิญญาณนี้ไม่เกิด", "zh-TW": "這個靈魂是無生的", "ja": "この魂は生まれなきものである", "ko": "이 영혼은 태어나지 않는다"},
    "It is everlasting": {"th": "มันมีอยู่ตลอดไป", "zh-TW": "它是永恆的", "ja": "それは永遠である", "ko": "그것은 영원하다"},
    "It is said to be": {"th": "มันถูกกล่าวว่า", "zh-TW": "它被說成是", "ja": "それは〜と言われる", "ko": "그것은〜라고 말한다"},
    "For such a person devoid of this intelligence": {"th": "สำหรับบุคคลเช่นนี้ที่ขาดปัญญานั้น", "zh-TW": "對於這樣缺乏智慧的人", "ja": "この知恵を欠いた人のために", "ko": "이 지혜를 결여한 사람을 위해"},
    "for those unworthy of grief": {"th": "สำหรับ那些ไม่สมควรแก่ความโศกเศร้า", "zh-TW": "為那些不值得悲傷的", "ja": "悲しむに値しない人々のために", "ko": "슬퍼할 가치가 없는 사람들을 위해"},
    "his eyes brimming with tears, showing his distress": {"th": "ดวงตาของเขาเต็มไปด้วยน้ำตา แสดงความทุกข์ใจของเขา", "zh-TW": "他雙眼含淚，顯示他的痛苦", "ja": "彼の目は涙でいっぱいで、彼の苦悩を示している", "ko": "그의 눈은 눈물로 가득 차 있고, 그의 고통을 보여준다"},
    "have been the object of great honour": {"th": "เป็นวัตถุแห่งการเคารพอย่างสูง", "zh-TW": "受到極大的尊敬", "ja": "大きな尊敬の対象であった", "ko": "큰 존경의 대상이었다"},
    "out of fear": {"th": "ออกจากความกลัว", "zh-TW": "出於恐懼", "ja": "恐れのために", "ko": "공포 때문에"},
    "and lead to enjoyment and opulence": {"th": "และนำไปสู่ความเพลิดเพลินและความมั่งคั่ง", "zh-TW": "並導致享樂和富裕", "ja": "そして快楽と富をもたらす", "ko": "그리고 쾌락과 부를 가져온다"},
    "Of those persons attached to enjoyment and opulence": {"th": "ของ那些บุคคลที่ติดอยู่ในความเพลิดเพลินและความมั่งคั่ง", "zh-TW": "那些執著於享樂和富裕的人", "ja": "快楽と富に執着する人々の", "ko": "쾌락과 부에 집착하는 사람들의"},
    "meditation on the Lord, purity of thought": {"th": "การทำสมาธิในพระผู้เป็นเจ้า, ความบริสุทธิ์ของความคิด", "zh-TW": "對主的冥想，思想的純潔", "ja": "主への瞑想、思考の純粋さ", "ko": "주에 대한 명상, 생각의 순수함"},
}

COMPONENTS = {
    "O": {"th": "โอ้", "zh-TW": "哦", "ja": "おお", "ko": "오"},
    "soul": {"th": "วิญญาณ", "zh-TW": "靈魂", "ja": "魂", "ko": "영혼"},
    "eternal": {"th": "นิรันดร์", "zh-TW": "永恆的", "ja": "永遠の", "ko": "영원한"},
    "indestructible": {"th": "ไม่อาจทำลายได้", "zh-TW": "不可毀壞的", "ja": "破壊できない", "ko": "파괴할 수 없는"},
    "unborn": {"th": "ไม่เกิด", "zh-TW": "無生的", "ja": "生まれざる", "ko": "태어나지 않는"},
    "body": {"th": "ร่างกาย", "zh-TW": "身體", "ja": "身体", "ko": "육체"},
    "material": {"th": "วัตถุ", "zh-TW": "物質", "ja": "物質", "ko": "물질"},
    "knowledge": {"th": "ความรู้", "zh-TW": "知識", "ja": "知識", "ko": "지식"},
    "wisdom": {"th": "ปัญญา", "zh-TW": "智慧", "ja": "知恵", "ko": "지혜"},
    "yoga": {"th": "โยคะ", "zh-TW": "瑜伽", "ja": "ヨーガ", "ko": "요가"},
    "action": {"th": "การกระทำ", "zh-TW": "行動", "ja": "行為", "ko": "행위"},
    "duty": {"th": "หน้าที่", "zh-TW": "職責", "ja": "義務", "ko": "의무"},
    "devotion": {"th": "ความภักดี", "zh-TW": "奉愛", "ja": "献身", "ko": "헌신"},
    "nature": {"th": "ธรรมชาติ", "zh-TW": "自然", "ja": "自然", "ko": "자연"},
    "peace": {"th": "สันติ", "zh-TW": "和平", "ja": "平和", "ko": "평화"},
    "happiness": {"th": "ความสุข", "zh-TW": "快樂", "ja": "幸福", "ko": "행복"},
    "sorrow": {"th": "ความโศกเศร้า", "zh-TW": "悲傷", "ja": "悲しみ", "ko": "슬픔"},
    "fear": {"th": "ความกลัว", "zh-TW": "恐懼", "ja": "恐れ", "ko": "공포"},
    "anger": {"th": "ความโกรธ", "zh-TW": "憤怒", "ja": "怒り", "ko": "분노"},
    "desire": {"th": "ความปรารถนา", "zh-TW": "慾望", "ja": "欲望", "ko": "욕망"},
    "attachment": {"th": "การยึดติด", "zh-TW": "執著", "ja": "執着", "ko": "집착"},
    "liberation": {"th": "การหลุดพ้น", "zh-TW": "解脫", "ja": "解脱", "ko": "해탈"},
    "meditation": {"th": "การทำสมาธิ", "zh-TW": "冥想", "ja": "瞑想", "ko": "명상"},
    "mind": {"th": "จิต", "zh-TW": "心", "ja": "心", "ko": "마음"},
}

def translate_meaning(text):
    """Translate English text to Asian languages."""
    if not text or not text.strip():
        return {"th": "", "zh-TW": "", "ja": "", "ko": ""}
    
    # Check for exact match first
    if text in TERM_TRANSLATIONS:
        return TERM_TRANSLATIONS[text]
    
    # Build translation from components
    result = {"th": "", "zh-TW": "", "ja": "", "ko": ""}
    words = text.split()
    translated_words = {"th": [], "zh-TW": [], "ja": [], "ko": []}
    
    for word in words:
        clean_word = word.strip('.,;:!?()"\'-')
        found = False
        
        # Check term translations
        for term, trans in TERM_TRANSLATIONS.items():
            if term.lower() == clean_word.lower():
                for lang in ["th", "zh-TW", "ja", "ko"]:
                    translated_words[lang].append(trans[lang])
                found = True
                break
        
        # Check component translations
        if not found:
            for comp, trans in COMPONENTS.items():
                if comp.lower() == clean_word.lower():
                    for lang in ["th", "zh-TW", "ja", "ko"]:
                        if trans[lang]:
                            translated_words[lang].append(trans[lang])
                    found = True
                    break
        
        if not found:
            for lang in ["th", "zh-TW", "ja", "ko"]:
                translated_words[lang].append(clean_word)
    
    for lang in ["th", "zh-TW", "ja", "ko"]:
        result[lang] = " ".join(translated_words[lang])
    
    return result

def process_chapter(chapter_num):
    """Process a single chapter."""
    input_file = BASE_DIR / 'data' / 'chapters' / f'ch-{chapter_num:02d}' / 'vocabulary-source.json'
    output_file = BASE_DIR / 'data' / 'chapters' / f'ch-{chapter_num:02d}' / 'vocabulary-asian.json'
    
    if not input_file.exists():
        print(f"  Skipping ch-{chapter_num:02d}: Input file not found")
        return False
    
    print(f"  Loading vocabulary from ch-{chapter_num:02d}...")
    source_data = load_json(input_file)
    
    total_words = len(source_data['vocabulary'])
    
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
    
    for i, vocab_item in enumerate(source_data['vocabulary']):
        vocab_id = str(vocab_item['id'])
        word = vocab_item['word']
        
        ru_meaning = vocab_item['meaning'].get('ru', {}).get('text', '')
        en_meaning = vocab_item['meaning'].get('en', {}).get('text', '')
        source_text = en_meaning if en_meaning else ru_meaning
        
        translated_meaning = translate_meaning(source_text)
        transliteration = generate_transliteration(word)
        
        output_data['vocabulary'][vocab_id] = {
            "meaning": translated_meaning,
            "transliteration": transliteration
        }
    
    save_json(output_file, output_data)
    print(f"  Saved {total_words} words to vocabulary-asian.json")
    return True

def main():
    print("="*60)
    print("Generating vocabulary-asian.json for chapters 2-6")
    print("="*60)
    
    for chapter_num in range(2, 7):
        print(f"\nProcessing chapter {chapter_num}...")
        process_chapter(chapter_num)
    
    print("\n" + "="*60)
    print("Complete! Processed chapters 2-6")
    print("="*60)

if __name__ == '__main__':
    main()
