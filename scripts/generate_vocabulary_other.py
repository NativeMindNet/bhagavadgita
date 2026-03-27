#!/usr/bin/env python3
"""Generate vocabulary-other.json for Chapter 18 with HE/AR/TR/SW translations."""

import json
from datetime import datetime

# Translation mappings for common terms
TERM_TRANSLATIONS = {
    "O best of the Bhāratas": {
        "he": "הו הטוב שבבهارתות",
        "ar": "يا أفضل البهاراتاس",
        "tr": "Ey Bhāratas'ın en iyisi",
        "sw": "Ewe bora wa Bhāratas"
    },
    "O Lord of all senses": {
        "he": "הו אדון כל החושים",
        "ar": "يا رب كل الحواس",
        "tr": "Ey tüm duyuların efendisi",
        "sw": "Ewe Bwana wa hisia zote"
    },
    "O son of Kuntī": {
        "he": "הו בן קונטי",
        "ar": "يا ابن كونتي",
        "tr": "Ey Kunti oğlu",
        "sw": "Ewe mwana wa Kunti"
    },
    "O slayer of the Keśi demon": {
        "he": "הו הורג השד קשי",
        "ar": "يا قاتل الشيطان كيشي",
        "tr": "Ey Keşi iblisini öldüren",
        "sw": "Ewe muuaji wa shetani Keśi"
    },
    "O vanquisher of the enemy": {
        "he": "הו מנצח האויב",
        "ar": "يا قاهر العدو",
        "tr": "Ey düşmanı yenen",
        "sw": "Ewe mshindi wa adui"
    },
    "O best of men": {
        "he": "הו הטוב שבאנשים",
        "ar": "يا أفضل الرجال",
        "tr": "Ey erkeklerin en iyisi",
        "sw": "Ewe bora wa wanaume"
    },
    "amongst the humans, etc": {
        "he": "בקרב בני האדם וכדומה",
        "ar": "بين البشر، إلخ",
        "tr": "insanlar arasında, vb.",
        "sw": "kati ya wanadamu, n.k."
    },
    "sings the glories of": {
        "he": "משבח את תהילת",
        "ar": "يسبح أمجاد",
        "tr": "önünü över",
        "sw": "huimba sifa za"
    },
    "it is said": {
        "he": "נאמר",
        "ar": "قيل",
        "tr": "söylenir",
        "sw": "imesemwa"
    },
    "(1) The basis, the body": {
        "he": "(1) הבסיס, הגוף",
        "ar": "(1) الأساس، الجسد",
        "tr": "(1) Temel, beden",
        "sw": "(1) Msingi, mwili"
    },
    "as fire is covered": {
        "he": "כמו שאש מכוסה",
        "ar": "كما النار مغطاة",
        "tr": "ateşin örtülü olduğu gibi",
        "sw": "kama moto umefunikwa"
    },
    "and in the beginning": {
        "he": "ובהתחלה",
        "ar": "وفي البداية",
        "tr": "ve başlangıçta",
        "sw": "na mwanzoni"
    },
    "in the beginning": {
        "he": "בהתחלה",
        "ar": "في البداية",
        "tr": "başlangıçta",
        "sw": "mwanzoni"
    },
    "out of pride": {
        "he": "מתוך גאווה",
        "ar": "من الغرور",
        "tr": "gururdan",
        "sw": "kwa kiburi"
    },
    "ignorance and delusion": {
        "he": "בורות ואשליה",
        "ar": "الجهل والوهم",
        "tr": "cehalet ve yanılsama",
        "sw": "ujinga na udanganyifu"
    },
    "due to impure intelligence": {
        "he": "בגלל אינטליגנציה לא טהורה",
        "ar": "بسبب الذكاء غير النقي",
        "tr": "saf olmayan zeka nedeniyle",
        "sw": "kwa sababu ya akili isiyo safi"
    },
    "and in the end": {
        "he": "ובסוף",
        "ar": "وفي النهاية",
        "tr": "ve sonunda",
        "sw": "na mwishoni"
    },
    "and others (generally the mīmāṁsakas)": {
        "he": "ואחרים (בדרך כלל המימאמסאקים)",
        "ar": "وآخرون (عموماً الميمامساكاس)",
        "tr": "ve diğerleri (genellikle mīmāṁsakas)",
        "sw": "na wengine (kwa kawaida mīmāṁsakas)"
    },
    "unbiased by likes and dislikes": {
        "he": "ללא משוא פנים של חיבה ושנאה",
        "ar": "دون تحيز من المحبة والكراهية",
        "tr": "sevgi ve nefretten önyargısız",
        "sw": "bila upendeleo wa upendo na chuki"
    },
    "One with the wisdom of detachment": {
        "he": "אחד עם חכמת ההתנתקות",
        "ar": "واحد مع حكمة عدم التعلق",
        "tr": "detachment bilgeliği ile bir",
        "sw": "mmoja na hekima ya kutokushikamana"
    },
    "to one devoid of self-sacrifice": {
        "he": "למי שאין לו הקרבה עצמית",
        "ar": "لمن يفتقر إلى التضحية الذاتية",
        "tr": "özgeciliği olmayan birine",
        "sw": "kwa asiye na kujitoa"
    },
    "not seeking the truth – without spiritual or scriptural conception": {
        "he": "לא מחפש את האמת - ללא תפיסה רוחנית או כתבי קודש",
        "ar": "لا يبحث عن الحقيقة - بدون تصور روحي أو كتابي",
        "tr": "gerçeği aramayan - ruhani veya kutsal yazı kavramı olmadan",
        "sw": "asiyetafuta ukweli - bila dhana ya kiroho au ya maandiko"
    },
    "and the fifth factor": {
        "he": "והגורם החמישי",
        "ar": "والعامل الخامس",
        "tr": "ve beşinci faktör",
        "sw": "na sababu ya tano"
    },
    "nor to one who is averse to My service": {
        "he": "ולא למי שסולד מעבודתי",
        "ar": "ولا لمن يكره خدمتي",
        "tr": "hizmetimden tiksinen birine de",
        "sw": "wala kwa anayechukia huduma yangu"
    },
    "and bondage and liberation": {
        "he": "וכבילה ושחרור",
        "ar": "والقيد والتحرر",
        "tr": "ve bağlanma ve özgürlük",
        "sw": "na kufungwa na ukombolewa"
    },
    "danger and safety": {
        "he": "סכנה וביטחון",
        "ar": "الخطر والأمان",
        "tr": "tehlike ve güvenlik",
        "sw": "hatari na usalama"
    },
    "in the world": {
        "he": "בעולם",
        "ar": "في العالم",
        "tr": "dünyada",
        "sw": "duniani"
    },
    "living beings (considering My superior potency to be in everything)": {
        "he": "יצורים חיים (מחשיב את העליונות שלי כנמצאת בכל)",
        "ar": "الكائنات الحية (اعتبار قوتي العليا في كل شيء)",
        "tr": "canlı varlıklar (üstün gücümün her şeyde olduğunu düşünerek)",
        "sw": "viumbe hai (kukua nguvu yangu ya juu iko katika kila kitu)"
    },
    "Brahma, the Absolute": {
        "he": "ברהמה, המוחלט",
        "ar": "براهما، المطلق",
        "tr": "Brahma, Mutlak",
        "sw": "Brahma, Uhalisi"
    },
    "duties of the brāhmaṇs": {
        "he": "חובות הברהמינים",
        "ar": "واجبات البراهمة",
        "tr": "Brahmanaların görevleri",
        "sw": "majukumu ya Brahmanas"
    },
    "renunciation": {
        "he": "ויתור",
        "ar": "التخلي",
        "tr": "vazgeçiş",
        "sw": "kuachilia"
    },
    "detachment": {
        "he": "התנתקות",
        "ar": "عدم التعلق",
        "tr": "bağlılık olmama",
        "sw": "kutokushikamana"
    },
    "action": {
        "he": "פעולה",
        "ar": "العمل",
        "tr": "eylem",
        "sw": "kitendo"
    },
    "knowledge": {
        "he": "ידע",
        "ar": "المعرفة",
        "tr": "bilgi",
        "sw": "elimu"
    },
    "the knower": {
        "he": "היודע",
        "ar": "العارف",
        "tr": "bilen",
        "sw": "mwenye kujua"
    },
    "the object of knowledge": {
        "he": "מושא הידע",
        "ar": "موضوع المعرفة",
        "tr": "bilginin nesnesi",
        "sw": "kitu cha elimu"
    },
    "the doer": {
        "he": "הפועל",
        "ar": "الفاعل",
        "tr": "fail",
        "sw": "mtenda"
    },
    "the instrument": {
        "he": "הכלי",
        "ar": "الأداة",
        "tr": "araç",
        "sw": "kifaa"
    },
    "the senses": {
        "he": "החושים",
        "ar": "الحواس",
        "tr": "duyular",
        "sw": "hisia"
    },
    "the body": {
        "he": "הגוף",
        "ar": "الجسد",
        "tr": "beden",
        "sw": "mwili"
    },
    "the soul": {
        "he": "הנשמה",
        "ar": "الروح",
        "tr": "ruh",
        "sw": "roho"
    },
    "the Supreme Soul": {
        "he": "הנשמה העליונה",
        "ar": "الروح الأعلى",
        "tr": "Yüce Ruh",
        "sw": "Roho Mkuu"
    },
    "goodness": {
        "he": "טוב",
        "ar": "الخيرية",
        "tr": "iyilik",
        "sw": "wema"
    },
    "passion": {
        "he": "רגש/תשוקה",
        "ar": "العاطفة",
        "tr": "tutku",
        "sw": "hisia"
    },
    "ignorance": {
        "he": "בערות",
        "ar": "الجهل",
        "tr": "cehalet",
        "sw": "ujinga"
    },
    "happiness": {
        "he": "אושר",
        "ar": "السعادة",
        "tr": "mutluluk",
        "sw": "furaha"
    },
    "duty": {
        "he": "חובה",
        "ar": "الواجب",
        "tr": "görev",
        "sw": "jukumu"
    },
    "nature": {
        "he": "טבע",
        "ar": "الطبيعة",
        "tr": "doğa",
        "sw": "asili"
    },
    "faith": {
        "he": "אמונה",
        "ar": "الإيمان",
        "tr": "inanç",
        "sw": "imani"
    },
    "sacrifice": {
        "he": "קרבן",
        "ar": "التضحية",
        "tr": "kurban",
        "sw": "sadaka"
    },
    "charity": {
        "he": "צדקה",
        "ar": "الصدقة",
        "tr": "sadaka",
        "sw": "hisani"
    },
    "austerity": {
        "he": "סיגוף",
        "ar": "الزهد",
        "tr": "çile",
        "sw": "ukalipu"
    },
    "peace": {
        "he": "שלווה",
        "ar": "السلام",
        "tr": "huzur",
        "sw": "amani"
    },
    "self-control": {
        "he": "איפוק/שליטה עצמית",
        "ar": "ضبط النفس",
        "tr": "öz denetim",
        "sw": "kujidhibiti"
    },
    "purity": {
        "he": "טוהר",
        "ar": "النقاء",
        "tr": "saflık",
        "sw": "usafi"
    },
    "patience": {
        "he": "סבלנות",
        "ar": "الصبر",
        "tr": "sabır",
        "sw": "uvumilivu"
    },
    "honesty": {
        "he": "יושר",
        "ar": "الاستقامة",
        "tr": "dürüstlük",
        "sw": "uadilifu"
    },
    "wisdom": {
        "he": "חכמה",
        "ar": "الحكمة",
        "tr": "bilgelik",
        "sw": "hekima"
    },
    "understanding": {
        "he": "הבנה",
        "ar": "الفهم",
        "tr": "anlayış",
        "sw": "uelewa"
    },
    "belief in God": {
        "he": "אמונה באלוהים",
        "ar": "الإيمان بالله",
        "tr": "Tanrı'ya inanç",
        "sw": "imani kwa Mungu"
    },
    "courage": {
        "he": "גבורה",
        "ar": "الشجاعة",
        "tr": "cesaret",
        "sw": "ushujaa"
    },
    "splendor": {
        "he": "הדר",
        "ar": "المجد",
        "tr": "görkem",
        "sw": "utukufu"
    },
    "determination": {
        "he": "נחישות",
        "ar": "العزيمة",
        "tr": "kararlılık",
        "sw": "azimio"
    },
    "resourcefulness": {
        "he": "זריזות/תושייה",
        "ar": "النشاط",
        "tr": "çeviklik",
        "sw": "chapukazi"
    },
    "not fleeing in battle": {
        "he": "לא לברוח בקרב",
        "ar": "عدم الهروب في المعركة",
        "tr": "savaşta kaçmama",
        "sw": "kutokukimbia vitani"
    },
    "generosity": {
        "he": "נדיבות",
        "ar": "الكرم",
        "tr": "cömertlik",
        "sw": "ukarimu"
    },
    "leadership ability": {
        "he": "יכולת הנהגה",
        "ar": "القدرة على القيادة",
        "tr": "liderlik yeteneği",
        "sw": "uwezo wa kuongoza"
    },
    "agriculture": {
        "he": "חקלאות",
        "ar": "الزراعة",
        "tr": "tarım",
        "sw": "kilimo"
    },
    "cow protection": {
        "he": "הגנת בקר",
        "ar": "حماية الماشية",
        "tr": "sığır koruma",
        "sw": "kulinda mifugo"
    },
    "trade": {
        "he": "מסחר",
        "ar": "التجارة",
        "tr": "ticaret",
        "sw": "biashara"
    },
    "service work": {
        "he": "עבודת שירות",
        "ar": "عمل الخدمة",
        "tr": "hizmet işi",
        "sw": "kazi ya huduma"
    },
    "perfection": {
        "he": "שלמות",
        "ar": "الكمال",
        "tr": "mükemmellik",
        "sw": "ukamilifu"
    },
    "God": {
        "he": "אלוהים",
        "ar": "الله",
        "tr": "Tanrı",
        "sw": "Mungu"
    },
    "devotion": {
        "he": "מסירות",
        "ar": "التفاني",
        "tr": "adanmışlık",
        "sw": "ibada"
    },
    "grace": {
        "he": "חסד",
        "ar": "النعمة",
        "tr": "lütuf",
        "sw": "neema"
    },
    "eternal": {
        "he": "נצחי",
        "ar": "الأبدي",
        "tr": "ebedi",
        "sw": "milele"
    },
    "meditation": {
        "he": "מדיטציה",
        "ar": "التأمل",
        "tr": "meditasyon",
        "sw": "meditetesheni"
    },
    "non-violence": {
        "he": "אי-אלימות",
        "ar": "عدم العنف",
        "tr": "şiddetsizlik",
        "sw": "kutokukwa na vurugu"
    },
    "anger": {
        "he": "כעס",
        "ar": "الغضب",
        "tr": "öfke",
        "sw": "hasira"
    },
    "desire": {
        "he": "תשוקה",
        "ar": "الرغبة",
        "tr": "arzu",
        "sw": "tamaa"
    },
    "greed": {
        "he": "חמדנות",
        "ar": "الجشع",
        "tr": "açgözlülük",
        "sw": "uchoyo"
    },
    "ego": {
        "he": "אגו",
        "ar": "الأنا",
        "tr": "ego",
        "sw": "ego"
    },
    "delusion": {
        "he": "אשליה",
        "ar": "الوهم",
        "tr": "yanılsama",
        "sw": "udanganyifu"
    },
    "sleep": {
        "he": "שינה",
        "ar": "النوم",
        "tr": "uyku",
        "sw": "usingizi"
    },
    "fear": {
        "he": "פחד",
        "ar": "الخوف",
        "tr": "korku",
        "sw": "woga"
    },
    "grief": {
        "he": "אבל/צער",
        "ar": "الحزن",
        "tr": "keder",
        "sw": "huzuni"
    },
    "despair": {
        "he": "ייאוש",
        "ar": "اليأس",
        "tr": "umutsuzluk",
        "sw": "kukata tamaa"
    },
    "arrogance": {
        "he": "שחצנות",
        "ar": "الغطرسة",
        "tr": "kibir",
        "sw": "kiburi"
    },
    "intelligence": {
        "he": "שכל/אינטליגנציה",
        "ar": "العقل",
        "tr": "akıl",
        "sw": "akili"
    },
    "righteous": {
        "he": "צדיקים",
        "ar": "الصالحين",
        "tr": "salih",
        "sw": "wanyofu"
    },
    "sin": {
        "he": "חטא",
        "ar": "الخطيئة",
        "tr": "günah",
        "sw": "dhambi"
    },
    "liberation": {
        "he": "שחרור",
        "ar": "التحرر",
        "tr": "özgürlük",
        "sw": "uhuru"
    },
    "Supreme Lord": {
        "he": "האל העליון",
        "ar": "الرب الأعلى",
        "tr": "Yüce Rab",
        "sw": "Bwana Mkuu"
    },
    "O son of Kunti": {
        "he": "הו בן קונטי",
        "ar": "يا ابن كونتي",
        "tr": "Ey Kunti oğlu",
        "sw": "Ewe mwana wa Kunti"
    },
    "O mighty-armed one": {
        "he": "הו רב-עוצמה",
        "ar": "يا قوي الذراع",
        "tr": "Ey güçlü kollu",
        "sw": "Ewe mwenye mikono yenye nguvu"
    },
    "O conqueror of wealth": {
        "he": "הו כובש העושר",
        "ar": "يا قاهر الثروة",
        "tr": "Ey servetin fatihi",
        "sw": "Ewe mshindi wa utajiri"
    },
    "O best of the Bhāratas": {
        "he": "הו הטוב שבבهارתות",
        "ar": "يا أفضل البهاراتاس",
        "tr": "Ey Bhāratas'ın en iyisi",
        "sw": "Ewe bora wa Bhāratas"
    },
    "O Arjuna": {
        "he": "הו ארג'ונה",
        "ar": "يا أرجونا",
        "tr": "Ey Arjuna",
        "sw": "Ewe Arjuna"
    },
    "Sanjaya said": {
        "he": "סנג'איה אמר",
        "ar": "قال سنجايا",
        "tr": "Sanjaya dedi",
        "sw": "Sanjaya alisema"
    },
    "Arjuna said": {
        "he": "ארג'ונה אמר",
        "ar": "قال أرجونا",
        "tr": "Arjuna dedi",
        "sw": "Arjuna alisema"
    },
    "The Supreme Lord said": {
        "he": "האל העליון אמר",
        "ar": "قال الرب الأعلى",
        "tr": "Yüce Rab dedi",
        "sw": "Bwana Mkuu alisema"
    }
}

def get_translation(meaning_en, lang):
    """Get translation for a given English meaning."""
    if not meaning_en or meaning_en.strip() == "":
        return ""
    
    # Check exact match
    if meaning_en in TERM_TRANSLATIONS:
        return TERM_TRANSLATIONS[meaning_en].get(lang, meaning_en)
    
    # Check partial match (case-insensitive)
    meaning_lower = meaning_en.lower()
    for key, translations in TERM_TRANSLATIONS.items():
        if key.lower() in meaning_lower or meaning_lower in key.lower():
            return translations.get(lang, meaning_en)
    
    # Default: return English with note
    return meaning_en

def get_transliteration(word, lang):
    """Generate transliteration for a Sanskrit word based on language."""
    if not word:
        return ""
    
    # Clean the word
    clean_word = word.replace("(he) ", "").replace("(manuṣyādiṣu)", "").strip()
    
    if lang == "he":
        # Hebrew transliteration (simplified)
        return clean_word  # Keep Latin script for Sanskrit terms
    elif lang == "ar":
        # Arabic transliteration (simplified)
        return f"({clean_word})"
    elif lang == "tr":
        # Turkish uses Latin script
        return f"({clean_word})"
    elif lang == "sw":
        # Swahili uses Latin script
        return f"({clean_word})"
    
    return clean_word

def main():
    # Read source vocabulary
    with open("/Users/anton/proj/gita/data/chapters/ch-18/vocabulary-source.json", "r", encoding="utf-8") as f:
        source_data = json.load(f)
    
    # Build output vocabulary
    output_vocab = {}
    
    for entry in source_data.get("vocabulary", []):
        word_id = str(entry.get("id", ""))
        if not word_id:
            continue
        
        # Get English meaning
        meaning_en = entry.get("meaning", {}).get("en", {}).get("text", "")
        
        # Generate translations
        meaning_translations = {}
        transliterations = {}
        
        for lang in ["he", "ar", "tr", "sw"]:
            meaning_translations[lang] = get_translation(meaning_en, lang)
            transliterations[lang] = get_transliteration(entry.get("word", ""), lang)
        
        output_vocab[word_id] = {
            "meaning": meaning_translations,
            "transliteration": transliterations
        }
    
    # Build output structure
    output_data = {
        "chapter": 18,
        "meta": {
            "source": "/Users/anton/proj/gita/data/chapters/ch-18/vocabulary-source.json",
            "generated": datetime.now().strftime("%Y-%m-%d"),
            "languages": ["he", "ar", "tr", "sw"],
            "approved": False
        },
        "vocabulary": output_vocab
    }
    
    # Write output
    with open("/Users/anton/proj/gita/data/chapters/ch-18/vocabulary-other.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"Generated vocabulary-other.json with {len(output_vocab)} entries")

if __name__ == "__main__":
    main()
