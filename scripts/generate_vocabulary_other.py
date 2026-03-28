#!/usr/bin/env python3
"""
Generate vocabulary-other.json for chapters 1-6.
Translates vocabulary meanings to he, ar, tr, sw.
"""

import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent

# Translation mappings for common Bhagavad Gita terms
TERM_TRANSLATIONS = {
    # Addresses
    "O Arjuna, son of Kuntī": {"he": "הו ארג'ונה בני קונטי", "ar": "يا أرجونا ابن كونتي", "tr": "Ey Arjuna, Kuntī oğlu", "sw": "Ewe Arjuna, mwana wa Kuntī"},
    "O Arjuna": {"he": "הו ארג'ונה", "ar": "يا أرجونا", "tr": "Ey Arjuna", "sw": "Ewe Arjuna"},
    "O son of Kuntī": {"he": "הו בן קונטי", "ar": "يا ابن كونتي", "tr": "Ey Kuntī oğlu", "sw": "Ewe mwana wa Kuntī"},
    "O descendant of the Kuru dynasty": {"he": "הו צאצא שושלת קורו", "ar": "يا سلالة أسرة كورو", "tr": "Ey Kuru hanedanının soyundan gelen", "sw": "Ewe mzao wa nasaba ya Kuru"},
    "O Madhusūdan, slayer of the enemy": {"he": "הו מדהוסודן קוטל האויב", "ar": "يا مادوسودان قاتل العدو", "tr": "Ey Madhusūdan, düşman katili", "sw": "Ewe Madhusūdan, muuaji wa adui"},
    "O subduer of the enemy": {"he": "הו כובש האויב", "ar": "يا قاهر العدو", "tr": "Ey düşmanı boyunduruk altına alan", "sw": "Ewe mshindi wa adui"},
    "O noblest of men": {"he": "הו האציל שבאנשים", "ar": "يا noblest of الرجال", "tr": "Ey insanların en soylusu", "sw": "Ewe bora zaidi ya wanadamu"},
    "O slayer of the enemy": {"he": "הו קוטל האויב", "ar": "يا قاتل العدو", "tr": "Ey düşman katili", "sw": "Ewe muuaji wa adui"},
    
    # Common phrases
    "by worshipping the Supreme Lord": {"he": "על ידי סגידה לאדון העליון", "ar": "من خلال عبادة الرب الأعلى", "tr": "Yüce Rab'be tapınarak", "sw": "kwa kuabudu Bwana Mkuu"},
    "nor is it that": {"he": "וגם לא זה", "ar": "ولا ذلك", "tr": "ne de bu", "sw": "wala sio kwamba"},
    "It is not a fact that": {"he": "זו לא עובדה ש", "ar": "ليست حقيقة أن", "tr": "şu bir gerçek değil ki", "sw": "sio kweli kwamba"},
    "actions of the senses": {"he": "פעולות החושים", "ar": "أعمال الحواس", "tr": "duyuların eylemleri", "sw": "matendo ya hisia"},
    "engaging with material sense objects": {"he": "מעורבות עם אובייקטים חושיים חומריים", "ar": "الانخراط مع الأشياء الحسية المادية", "tr": "maddi duyusal nesnelerle meşgul olmak", "sw": "kushiriki na vitu vya hisia vya kimwili"},
    "These come and go": {"he": "אלה באים והולכים", "ar": "هذه تأتي وتذهب", "tr": "bunlar gelir ve gider", "sw": "hizi huja na kuondoka"},
    "of the various purposes fulfilled": {"he": "של המטרות השונות שהושלמו", "ar": "من الأغراض المختلفة المحققة", "tr": "çeşitli amaçların yerine getirilmesi", "sw": "ya madhumuni mbalimbali yaliyotimizwa"},
    "I have revealed to you": {"he": "גיליתי לך", "ar": "لقد كشفت لك", "tr": "sana vahyettim", "sw": "nimekufunulia"},
    "failure in the beginning": {"he": "כישלון בהתחלה", "ar": "الفشل في البداية", "tr": "başlangıçta başarısızlık", "sw": "ushindani mwanzoni"},
    "it remains steady": {"he": "זה נשאר יציב", "ar": "يبقى ثابتاً", "tr": "sabit kalır", "sw": "inabaki thabiti"},
    "its water never crossing the shore": {"he": "מימיו לעולם לא חוצים את החוף", "ar": "مياهه لا تعبر الشاطئ أبداً", "tr": "suyu asla kıyıyı geçmez", "sw": "maji yake hayavuki pwani kamwe"},
    "or the living": {"he": "או החיים", "ar": "أو الأحياء", "tr": "veya yaşayanlar", "sw": "au walio hai"},
    "non-performance of your prescribed duties": {"he": "אי-ביצוע חובותיך הקבועות", "ar": "عدم أداء واجباتك المفروضة", "tr": "belirlenen görevlerini yerine getirmeme", "sw": "kutofanya majukumu yako yaliyoamriwa"},
    "and the cause of infamy": {"he": "והסיבה לקלון", "ar": "وسبب العار", "tr": "ve rezillik nedeni", "sw": "na chanzo cha aibu"},
    "on the ocean": {"he": "על האוקיינוס", "ar": "على المحيط", "tr": "okyanusta", "sw": "kwenye bahari"},
    "even at the time of death": {"he": "אפילו בזמן המוות", "ar": "حتى في وقت الموت", "tr": "ölüm anında bile", "sw": "hata wakati wa kifo"},
    "subject to destruction": {"he": "כפוף להשמדה", "ar": "عرضة للتدمير", "tr": "yıkıma tabi", "sw": "kujerushiwa kwa uharibifu"},
    "Such a conclusion": {"he": "מסקנה כזו", "ar": "مثل هذا الاستنتاج", "tr": "böyle bir sonuç", "sw": "hitimisho kama hilo"},
    "One whose mind is undisturbed": {"he": "מי שדעתו לא מופרעת", "ar": "من لم ينزعج عقله", "tr": "zihni huzursuz olmayan", "sw": "Ambaye akili yake haisumbuki"},
    "it is inappropriate to grieve": {"he": "לא מתאים להתאבל", "ar": "من غير المناسب الحزن", "tr": "yas tutmak uygun değil", "sw": "si vya kufaa kusikitika"},
    "better course of action": {"he": "דרך פעולה טובה יותר", "ar": "مسار عمل أفضل", "tr": "daha iyi eylem yolu", "sw": "njia bora ya vitendo"},
    "for the inevitable": {"he": "עבור הבלתי נמנע", "ar": "للحتمي", "tr": "kaçınılmaz olan için", "sw": "kwa ajili ya yasiyoepukika"},
    "and immeasurable": {"he": "ובלתי ניתן למדידה", "ar": "ولا يمكن قياسه", "tr": "ve ölçülemez", "sw": "na hupimiki"},
    "due to his extremely subtle nature": {"he": "בגלל טבעו העדין ביותר", "ar": "بسبب طبيعته الدقيقة للغاية", "tr": "son derece ince doğası nedeniyle", "sw": "kwa sababu ya asili yake nyembamba sana"},
    "as an open door to heaven": {"he": "כדלת פתוחה לגן עדן", "ar": "كباب مفتوح للجنة", "tr": "cennete açılan açık bir kapı gibi", "sw": "kama mlango wazi wa mbingu"},
    "wealth and coveted enjoyable objects": {"he": "עושר וחפצים מהנים נחשקים", "ar": "الثروة والأشياء الممتعة المرغوبة", "tr": "zenginlik ve arzulanan zevk nesneleri", "sw": "utajiri na vitu vinavyotamanika vya furaha"},
    "it is an obstacle": {"he": "זהו מכשול", "ar": "إنه عائق", "tr": "bu bir engeldir", "sw": "ni kizuizi"},
    "to the attainment of heaven": {"he": "להשגת גן עדן", "ar": "للحصول على الجنة", "tr": "cennete ulaşmaya", "sw": "kufikia mbingu"},
    "of that person bereft of self-control": {"he": "של אותו אדם חסר שליטה עצמית", "ar": "ذلك الشخص المحروم من ضبط النفس", "tr": "öz kontrolünden yoksun kişinin", "sw": "wa yule mtu asiye na udhibiti wa nafsi"},
    "and the situation after death": {"he": "והמצב אחרי המוות", "ar": "والوضع بعد الموت", "tr": "ve ölümden sonraki durum", "sw": "na hali baada ya kifo"},
    "is again unknown": {"he": "שוב לא ידוע", "ar": "مجهول مرة أخرى", "tr": "tekrar bilinmiyor", "sw": "tena haijulikani"},
    "imperceptible": {"he": "בלתי מורגש", "ar": "غير محسوس", "tr": "algılanamaz", "sw": "haisikiki"},
    "the situation before birth": {"he": "המצב לפני הלידה", "ar": "الوضع قبل الولادة", "tr": "doğumdan önceki durum", "sw": "hali kabla ya kuzaliwa"},
    "is unknown": {"he": "לא ידוע", "ar": "مجهول", "tr": "bilinmiyor", "sw": "haijulikani"},
    "of the irresolute": {"he": "של חסרי ההחלטה", "ar": "للتردد", "tr": "kararsız olanların", "sw": "wa wasio na azimio"},
    "those who nurture mundane desires": {"he": "אלה שמטפחים תשוקות חילוניות", "ar": "أولئك الذين يرعون الرغبات الدنيوية", "tr": "dünyevi arzuları besleyenler", "sw": "wale wanaolisha tamaa za kidunia"},
    "The soul is indivisible": {"he": "הנשמה היא בלתי ניתנת לחלוקה", "ar": "الروح غير قابلة للتجزئة", "tr": "ruh bölünemez", "sw": "roho haigawanyiki"},
    "This soul is birthless": {"he": "נשמה זו היא ללא לידה", "ar": "هذه الروح غير مولودة", "tr": "Bu ruh doğmamıştır", "sw": "roho hii haizaliwi"},
    "It is everlasting": {"he": "היא נצחית", "ar": "هي أبدية", "tr": "O ebedidir", "sw": "ni ya milele"},
    "It is said to be": {"he": "נאמר שהיא", "ar": "يقال أنها", "tr": "şöyle söylenir", "sw": "inasemekwa kuwa"},
    "For such a person devoid of this intelligence": {"he": "עבור אדם כזה חסר אינטליגנציה זו", "ar": "لمثل هذا الشخص المحروم من هذه الذكاء", "tr": "Bu zekadan yoksun böyle bir kişi için", "sw": "kwa mtu kama huyo asiye na akili hii"},
    "for those unworthy of grief": {"he": "עבור אלה שאינם ראויים לצער", "ar": "لأولئك الذين لا يستحقون الحزن", "tr": "yas için layık olmayanlar için", "sw": "kwa wale wasiostahili kusikitika"},
    "his eyes brimming with tears": {"he": "עיניו מלאות דמעות", "ar": "عيناه مليئة بالدموع", "tr": "gözleri yaşlarla dolu", "sw": "macho yake yamejaa machozi"},
    "showing his distress": {"he": "מראה את מצוקתו", "ar": "يُظهر ضيقه", "tr": "sıkıntısını göstererek", "sw": "kuonyesha taabu yake"},
    "have been the object of great honour": {"he": "היו מושא לכבוד רב", "ar": "كانوا موضوع تكريم عظيم", "tr": "büyük onur konusu olmuş", "sw": "wamekuwa kitu cha heshima kubwa"},
    "out of fear": {"he": "מתוך פחד", "ar": "خوفاً", "tr": "korkudan", "sw": "kwa sababu ya hofu"},
    "and lead to enjoyment and opulence": {"he": "ומובילים להנאה ולעושר", "ar": "وتؤدي إلى المتعة والثراء", "tr": "ve zevk ve zenginliğe yol açar", "sw": "na kusababisha furaha na utajiri"},
    "Of those persons attached to enjoyment and opulence": {"he": "של אותם אנשים המחוברים להנאה ולעושר", "ar": "أولئك الأشخاص المرتبطين بالمتعة والثراء", "tr": "Zevk ve zenginliğe bağlı olan kişilerin", "sw": "Wa watu walioambatana na furaha na utajiri"},
    "meditation on the Lord": {"he": "מדיטציה על האדון", "ar": "التأمل في الرب", "tr": "Rab üzerine meditasyon", "sw": "kutafakari juu ya Bwana"},
    "purity of thought": {"he": "טוהר המחשבה", "ar": "نقاء الفكر", "tr": "düşünce saflığı", "sw": "usafi wa mawazo"},
    
    # Common terms
    "the soul": {"he": "הנשמה", "ar": "الروح", "tr": "ruh", "sw": "roho"},
    "the Supreme Soul": {"he": "הנשמה העליונה", "ar": "الروح الأعلى", "tr": "Yüce Ruh", "sw": "Roho Mkuu"},
    "material nature": {"he": "טבע חומרי", "ar": "الطبيعة المادية", "tr": "maddi doğa", "sw": "asili ya kimwili"},
    "spiritual": {"he": "רוחני", "ar": "روحي", "tr": "ruhani", "sw": "ya kiroho"},
    "material": {"he": "חומרי", "ar": "مادي", "tr": "maddi", "sw": "ya kimwili"},
    "devotional service": {"he": "שירות מסור", "ar": "الخدمة التفاني", "tr": "bağlılık hizmeti", "sw": "utumishi wa uaminifu"},
    "karma": {"he": "קרמה", "ar": "الكرمة", "tr": "karma", "sw": "karma"},
    "dharma": {"he": "דהרמה", "ar": "الدارما", "tr": "dharma", "sw": "dharma"},
    "yoga": {"he": "יוגה", "ar": "اليوغا", "tr": "yoga", "sw": "yoga"},
    "meditation": {"he": "מדיטציה", "ar": "التأمل", "tr": "meditasyon", "sw": "kutafakari"},
    "knowledge": {"he": "ידע", "ar": "المعرفة", "tr": "bilgi", "sw": "ujuzi"},
    "wisdom": {"he": "חוכמה", "ar": "الحكمة", "tr": "bilgelik", "sw": "busara"},
    "ignorance": {"he": "בורות", "ar": "الجهل", "tr": "cehalet", "sw": "ujinga"},
    "liberation": {"he": "שחרור", "ar": "التحرر", "tr": "kurtuluş", "sw": "ukombozi"},
    "bondage": {"he": "שיעבוד", "ar": "العبودية", "tr": "kölelik", "sw": "utumwa"},
    "action": {"he": "פעולה", "ar": "العمل", "tr": "eylem", "sw": "kitendo"},
    "inaction": {"he": "חוסר פעולה", "ar": "عدم العمل", "tr": "eylemsizlik", "sw": "kutotenda"},
    "renunciation": {"he": "ויתור", "ar": "الزهد", "tr": "feragat", "sw": "kujitoa"},
    "detachment": {"he": "ניתוק", "ar": "اللامبالاة", "tr": "bağlılık olmama", "sw": "kutokuwa na ambatanisho"},
    "attachment": {"he": "היצמדות", "ar": "التعلق", "tr": "bağlılık", "sw": "ambatanisho"},
    "desire": {"he": "תשוקה", "ar": "الرغبة", "tr": "arzu", "sw": "tamaa"},
    "lust": {"he": "תאווה", "ar": "الشهوة", "tr": "şehvet", "sw": "shahawa"},
    "anger": {"he": "כעס", "ar": "الغضب", "tr": "öfke", "sw": "hasira"},
    "greed": {"he": "חמדנות", "ar": "الطمع", "tr": "açgözlülük", "sw": "kuzu"},
    "peace": {"he": "שלום", "ar": "السلام", "tr": "huzur", "sw": "amani"},
    "happiness": {"he": "אושר", "ar": "السعادة", "tr": "mutluluk", "sw": "furaha"},
    "suffering": {"he": "סבל", "ar": "المعاناة", "tr": "acı", "sw": "mateso"},
    "pleasure": {"he": "הנאה", "ar": "المتعة", "tr": "zevk", "sw": "furaha"},
    "pain": {"he": "כאב", "ar": "الألم", "tr": "acı", "sw": "maumivu"},
}

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def translate_meaning(text):
    """Translate English text to he, ar, tr, sw."""
    if not text or not text.strip():
        return {"he": "", "ar": "", "tr": "", "sw": ""}
    
    # Check for exact match
    if text in TERM_TRANSLATIONS:
        return TERM_TRANSLATIONS[text]
    
    # Build translation from components
    result = {"he": "", "ar": "", "tr": "", "sw": ""}
    words = text.split()
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
    input_file = BASE_DIR / 'data' / 'chapters' / f'ch-{chapter_num:02d}' / 'vocabulary-source.json'
    output_file = BASE_DIR / 'data' / 'chapters' / f'ch-{chapter_num:02d}' / 'vocabulary-other.json'
    
    if not input_file.exists():
        print(f"  Skipping ch-{chapter_num:02d}: Input file not found")
        return False
    
    print(f"  Processing ch-{chapter_num:02d}...")
    source_data = load_json(input_file)
    
    output_data = {
        "chapter": chapter_num,
        "meta": {
            "source": str(input_file),
            "generated": datetime.now().strftime("%Y-%m-%d"),
            "languages": ["he", "ar", "tr", "sw"],
            "approved": False
        },
        "vocabulary": {}
    }
    
    total_words = len(source_data['vocabulary'])
    for i, vocab_item in enumerate(source_data['vocabulary']):
        vocab_id = str(vocab_item['id'])
        word = vocab_item['word']
        
        en_meaning = vocab_item['meaning'].get('en', {}).get('text', '')
        
        translated_meaning = translate_meaning(en_meaning)
        
        output_data['vocabulary'][vocab_id] = {
            "meaning": translated_meaning
        }
    
    save_json(output_file, output_data)
    print(f"  Saved {total_words} words to vocabulary-other.json")
    return True

def main():
    print("="*60)
    print("Generating vocabulary-other.json for chapters 1-6")
    print("="*60)
    
    for chapter_num in range(1, 7):
        process_chapter(chapter_num)
    
    print("\n" + "="*60)
    print("Complete! Processed chapters 1-6")
    print("="*60)

if __name__ == '__main__':
    main()
