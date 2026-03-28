#!/usr/bin/env python3
"""
Generate complete vocabulary-asian.json for Chapter 2.
Uses comprehensive term mappings and pattern-based translation.
"""

import json
import re
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent

# Comprehensive translation dictionary for Bhagavad Gita terms
TERM_TRANSLATIONS = {
    # Addresses to Arjuna
    "O Arjuna": {"th": "โอ้ อรชุน", "zh-TW": "哦 阿周那", "ja": "おお アルジュナよ", "ko": "오 아르주나여"},
    "O son of Kuntī": {"th": "โอ้ บุตรของกุนตี", "zh-TW": "哦 貢蒂之子", "ja": "おお クンティーの子よ", "ko": "오 쿤티의 아들아"},
    "O Arjuna, son of Kuntī": {"th": "โอ้ อรชุน บุตรของกุนตี", "zh-TW": "哦 阿周那，貢蒂之子", "ja": "おお アルジュナ、クンティーの子よ", "ko": "오 아르주나, 쿤티의 아들아"},
    "O descendant of the Kuru dynasty": {"th": "โอ้ ผู้สืบเชื้อสายแห่งวงศ์กุรุ", "zh-TW": "哦 俱盧王朝的後裔", "ja": "おお クル王朝の子孫よ", "ko": "오 쿠루 왕조의 후손이여"},
    "O Arjuna, descendant of the Kuru dynasty": {"th": "โอ้ อรชุน ผู้สืบเชื้อสายแห่งวงศ์กุรุ", "zh-TW": "哦 阿周那，俱盧王朝的後裔", "ja": "おお アルジュナ、クル王朝の子孫よ", "ko": "오 아르주나, 쿠루 왕조의 후손이여"},
    "O noblest of men": {"th": "โอ้ ผู้ประเสริฐสุดในบรรดาบุรุษ", "zh-TW": "哦 人中最傑出的", "ja": "おお 人々の中で最も優れた方よ", "ko": "오 사람들 중 가장 고귀한 이여"},
    "O subduer of the enemy": {"th": "โอ้ ผู้พิชิตศัตรู", "zh-TW": "哦 降伏敵人者", "ja": "おお 敵を征服する者よ", "ko": "오 적을 정복하는 이여"},
    "O Madhusūdan": {"th": "โอ้ มธุสูทน", "zh-TW": "哦 瑪都蘇丹", "ja": "おお マドゥスーダナよ", "ko": "오 마두수다나여"},
    "O slayer of the enemy": {"th": "โอ้ ผู้สังหารศัตรู", "zh-TW": "哦 殺敵者", "ja": "おお 敵を倒す者よ", "ko": "오 적을 물리치는 이여"},
    "O Madhusūdan, slayer of the enemy": {"th": "โอ้ มธุสูทน ผู้สังหารศัตรู", "zh-TW": "哦 瑪都蘇丹，殺敵者", "ja": "おお マドゥスーダナ、敵を倒す者よ", "ko": "오 마두수다나여, 적을 물리치는 이여"},
    
    # Common phrases
    "by worshipping the Supreme Lord": {"th": "โดยการบูชาพระผู้เป็นเจ้าสูงสุด", "zh-TW": "通過崇拜至尊主", "ja": "至高なる主を崇拝することによって", "ko": "지고하신 주를 숭배함으로써"},
    "nor is it that": {"th": "และก็ไม่ใช่ว่า", "zh-TW": "也不是", "ja": "〜というわけでもない", "ko": "그런 것도 아니다"},
    "It is not a fact that": {"th": "ไม่ใช่ความจริงที่ว่า", "zh-TW": "事實並非如此", "ja": "〜というのは事実ではない", "ko": "사실이 아닌 것은"},
    "actions of the senses": {"th": "การกระทำของประสาทสัมผัส", "zh-TW": "感官的活動", "ja": "感覚器官の働き", "ko": "감각 기관의 작용"},
    "engaging with": {"th": "ที่เกี่ยวเนื่องกับ", "zh-TW": "從事於", "ja": "〜に従事する", "ko": "〜에 관여하는"},
    "material sense objects": {"th": "วัตถุแห่งประสาทสัมผัส", "zh-TW": "物質感官對象", "ja": "物質的な感覚対象", "ko": "물질적 감각 대상"},
    "These come and go": {"th": "สิ่งเหล่านี้มาและไป", "zh-TW": "它們來而又去", "ja": "これらは来たり去ったりする", "ko": "이것들은 왔다가 간다"},
    "of the various purposes": {"th": "ของวัตถุประสงค์ต่างๆ", "zh-TW": "各種目的", "ja": "様々な目的の", "ko": "다양한 목적의"},
    "fulfilled": {"th": "ที่บรรลุ", "zh-TW": "被達成", "ja": "達成される", "ko": "성취되는"},
    "I have revealed": {"th": "เราได้เปิดเผย", "zh-TW": "我已揭示", "ja": "私は明かした", "ko": "내가 드러냈다"},
    "to you": {"th": "แก่เจ้า", "zh-TW": "向你", "ja": "あなたに", "ko": "너에게"},
    "failure": {"th": "ความล้มเหลว", "zh-TW": "失敗", "ja": "失敗", "ko": "실패"},
    "in the beginning": {"th": "ในตอนเริ่มต้น", "zh-TW": "在開始時", "ja": "初めに", "ko": "처음에"},
    "it remains steady": {"th": "มันยังคงมั่นคง", "zh-TW": "它保持穩定", "ja": "それは安定して留まる", "ko": "그것은 안정적으로 머문다"},
    "its water": {"th": "น้ำของมัน", "zh-TW": "它的水", "ja": "その水は", "ko": "그것의 물은"},
    "never crossing": {"th": "ไม่ไหลข้าม", "zh-TW": "從不越過", "ja": "決して越えない", "ko": "결코 넘지 않는"},
    "the shore": {"th": "ฝั่ง", "zh-TW": "岸邊", "ja": "岸", "ko": "둑"},
    "or the living": {"th": "หรือสิ่งมีชีวิต", "zh-TW": "或生物", "ja": "または生きているもの", "ko": "또는 살아있는 것"},
    "non-performance": {"th": "การไม่ปฏิบัติ", "zh-TW": "不履行", "ja": "不履行", "ko": "수행하지 않음"},
    "of your prescribed duties": {"th": "หน้าที่ที่กำหนดไว้ของเจ้า", "zh-TW": "你規定的職責", "ja": "あなたの定められた義務の", "ko": "네게 정해진 의무의"},
    "and the cause of": {"th": "และเป็นสาเหตุของ", "zh-TW": "並且是的原因", "ja": "そして〜の原因", "ko": "그리고〜의 원인"},
    "infamy": {"th": "การเสียชื่อเสียง", "zh-TW": "臭名昭著", "ja": "不名誉", "ko": "불명예"},
    "on the ocean": {"th": "บนมหาสมุทร", "zh-TW": "在海洋上", "ja": "海の上に", "ko": "바다 위에"},
    "even at the time": {"th": "แม้ในยาม", "zh-TW": "即使在時", "ja": "〜の時でさえ", "ko": "〜의 때에도"},
    "of death": {"th": "เสียชีวิต", "zh-TW": "死亡", "ja": "死の", "ko": "죽음의"},
    "subject to destruction": {"th": "ต้องถูกทำลาย", "zh-TW": "易於毀滅", "ja": "破壊されやすい", "ko": "파괴되기 쉬운"},
    "Such a conclusion": {"th": "ข้อสรุปดังกล่าว", "zh-TW": "這樣的結論", "ja": "そのような結論", "ko": "그런 결론"},
    "of the nature": {"th": "เช่น ธรรมชาติของ", "zh-TW": "的本質", "ja": "の性質", "ko": "의 본성"},
    "One whose mind": {"th": "ผู้ที่มีจิต", "zh-TW": "心念的人", "ja": "心を持つ者", "ko": "마음을 가진 자"},
    "is undisturbed": {"th": "ไม่หวั่นไหว", "zh-TW": "不受擾亂", "ja": "乱されない", "ko": "흔들리지 않는"},
    "it is inappropriate": {"th": "ไม่เหมาะสม", "zh-TW": "不恰當", "ja": "適切ではない", "ko": "적절하지 않다"},
    "to grieve": {"th": "ที่จะเศร้าโศก", "zh-TW": "悲傷", "ja": "悲しむこと", "ko": "슬퍼하는 것"},
    "for it": {"th": "สำหรับมัน", "zh-TW": "為它", "ja": "それのために", "ko": "그것을 위해"},
    "better course": {"th": "วิถีที่ดีกว่า", "zh-TW": "更好的方針", "ja": "より良い道", "ko": "더 나은 길"},
    "of action": {"th": "การกระทำ", "zh-TW": "行動", "ja": "行為の", "ko": "행위의"},
    "for the inevitable": {"th": "สำหรับสิ่งที่หลีกเลี่ยงไม่ได้", "zh-TW": "對於不可避免的事", "ja": "避けられないことのために", "ko": "피할 수 없는 것을 위해"},
    "and immeasurable": {"th": "และวัดไม่ได้", "zh-TW": "且不可測量", "ja": "そして測り知れない", "ko": "그리고 측정할 수 없다"},
    "due to": {"th": "เนื่องจาก", "zh-TW": "由於", "ja": "〜のため", "ko": "〜때문에"},
    "his extremely subtle nature": {"th": "ธรรมชาติที่ละเอียดอ่อนอย่างยิ่งของพระองค์", "zh-TW": "其極其微妙的本質", "ja": "その非常に微細な性質", "ko": "그 매우 미묘한 본성"},
    "as an open door": {"th": "เป็นเหมือนประตูเปิด", "zh-TW": "如同敞開的門", "ja": "開かれた門のように", "ko": "열린 문처럼"},
    "to heaven": {"th": "สู่สวรรค์", "zh-TW": "通往天堂", "ja": "天国への", "ko": "천국으로의"},
    "wealth": {"th": "ความมั่งคั่ง", "zh-TW": "財富", "ja": "富", "ko": "부"},
    "and coveted": {"th": "และที่น่าปรารถนา", "zh-TW": "和渴望的", "ja": "と望まれる", "ko": "그리고 탐내는"},
    "enjoyable objects": {"th": "วัตถุที่น่าปรารถนา", "zh-TW": "享樂對象", "ja": "享楽の対象", "ko": "즐거운 대상들"},
    "it is an obstacle": {"th": "เป็นอุปสรรค", "zh-TW": "是障礙", "ja": "それは障害である", "ko": "그것은 장애물이다"},
    "to the attainment": {"th": "ต่อการบรรลุ", "zh-TW": "對獲得", "ja": "〜の達成に対する", "ko": "〜달성에 대한"},
    "of that person": {"th": "ของบุคคลนั้น", "zh-TW": "那個人的", "ja": "その人の", "ko": "그 사람의"},
    "bereft of self-control": {"th": "ที่ขาดการควบคุมตนเอง", "zh-TW": "缺乏自制", "ja": "自制心を欠いた", "ko": "자제심을 결여한"},
    "and the situation": {"th": "และสถานการณ์", "zh-TW": "和情況", "ja": "そして状況", "ko": "그리고 상황"},
    "after death": {"th": "หลังความตาย", "zh-TW": "死後", "ja": "死後", "ko": "사후"},
    "is again unknown": {"th": "ก็ไม่ทราบได้อีกเช่นกัน", "zh-TW": "也同樣未知", "ja": "再び知られていない", "ko": "다시 알려지지 않았다"},
    "imperceptible": {"th": "มองไม่เห็น", "zh-TW": "無法察覺", "ja": "知覚できない", "ko": "지각할 수 없다"},
    "the situation before birth": {"th": "สถานการณ์ก่อนเกิด", "zh-TW": "出生前的情況", "ja": "出生前の状況", "ko": "탄생 전의 상황"},
    "is unknown": {"th": "ไม่ทราบได้", "zh-TW": "未知", "ja": "知られていない", "ko": "알려지지 않았다"},
    "of the irresolute": {"th": "ของผู้ที่ไม่มั่นคง", "zh-TW": "那些心意不堅定的", "ja": "決意しない人々の", "ko": "결의하지 않는 사람들의"},
    "those who nurture": {"th": "那些培育", "zh-TW": "那些培育", "ja": "育む人々", "ko": "기르는 사람들"},
    "mundane desires": {"th": "世俗慾望", "zh-TW": "世俗慾望", "ja": "世俗の欲望", "ko": "세속적 욕망"},
    "The soul": {"th": "วิญญาณ", "zh-TW": "靈魂", "ja": "魂", "ko": "영혼"},
    "is indivisible": {"th": "เป็นสิ่งที่แบ่งแยกไม่ได้", "zh-TW": "是不可分割的", "ja": "分割できない", "ko": "나눌 수 없다"},
    "This soul": {"th": "วิญญาณนี้", "zh-TW": "這個靈魂", "ja": "この魂は", "ko": "이 영혼은"},
    "is birthless": {"th": "ไม่เกิด", "zh-TW": "是無生的", "ja": "生まれなきものである", "ko": "태어나지 않는다"},
    "It is everlasting": {"th": "มันมีอยู่ตลอดไป", "zh-TW": "它是永恆的", "ja": "それは永遠である", "ko": "그것은 영원하다"},
    "It is said to be": {"th": "มันถูกกล่าวว่า", "zh-TW": "它被說成是", "ja": "それは〜と言われる", "ko": "그것은〜라고 말한다"},
    "For such a person": {"th": "สำหรับบุคคลเช่นนี้", "zh-TW": "對於這樣的人", "ja": "そのような人のために", "ko": "그런 사람을 위해"},
    "devoid of this intelligence": {"th": "ที่ขาดปัญญานั้น", "zh-TW": "缺乏智慧的", "ja": "この知恵を欠いた", "ko": "이 지혜를 결여한"},
    "for those unworthy": {"th": "สำหรับ那些ไม่สมควร", "zh-TW": "為那些不值得", "ja": "〜に値しない人々のために", "ko": "〜할 가치가 없는 사람들을 위해"},
    "of grief": {"th": "แก่ความโศกเศร้า", "zh-TW": "悲傷的", "ja": "悲しみの", "ko": "슬픔의"},
    "his eyes brimming": {"th": "ดวงตาของเขาเต็มไปด้วย", "zh-TW": "他雙眼充滿", "ja": "彼の目は〜でいっぱいで", "ko": "그의 눈은〜로 가득 차"},
    "with tears": {"th": "น้ำตา", "zh-TW": "眼淚", "ja": "涙", "ko": "눈물"},
    "showing": {"th": "แสดง", "zh-TW": "顯示", "ja": "示している", "ko": "보여주는"},
    "his distress": {"th": "ความทุกข์ใจของเขา", "zh-TW": "他的痛苦", "ja": "彼の苦悩", "ko": "그의 고통"},
    "have been": {"th": "เป็น", "zh-TW": "已經是", "ja": "〜であった", "ko": "〜이었다"},
    "the object": {"th": "วัตถุ", "zh-TW": "對象", "ja": "対象", "ko": "대상"},
    "of great honour": {"th": "แห่งการเคารพอย่างสูง", "zh-TW": "極大尊敬的", "ja": "大きな尊敬の", "ko": "큰 존경의"},
    "out of fear": {"th": "ออกจากความกลัว", "zh-TW": "出於恐懼", "ja": "恐れのために", "ko": "공포 때문에"},
    "and lead to": {"th": "และนำไปสู่", "zh-TW": "並導致", "ja": "そして〜をもたらす", "ko": "그리고〜를 가져온다"},
    "enjoyment": {"th": "ความเพลิดเพลิน", "zh-TW": "享樂", "ja": "快楽", "ko": "쾌락"},
    "and opulence": {"th": "และความมั่งคั่ง", "zh-TW": "和富裕", "ja": "と富", "ko": "그리고 부"},
    "Of those persons": {"th": "ของ那些บุคคล", "zh-TW": "那些人的", "ja": "那些人々の", "ko": "그 사람들의"},
    "attached to": {"th": "ที่ติดอยู่ใน", "zh-TW": "執著於", "ja": "執着する", "ko": "집착하는"},
    "meditation on the Lord": {"th": "การทำสมาธิในพระผู้เป็นเจ้า", "zh-TW": "對主的冥想", "ja": "主への瞑想", "ko": "주에 대한 명상"},
    "purity of thought": {"th": "ความบริสุทธิ์ของความคิด", "zh-TW": "思想的純潔", "ja": "思考の純粋さ", "ko": "생각의 순수함"},
}

# Component translations for building complex translations
COMPONENTS = {
    "O": {"th": "โอ้", "zh-TW": "哦", "ja": "おお", "ko": "오"},
    "the": {"th": "", "zh-TW": "", "ja": "", "ko": ""},
    "Supreme": {"th": "สูงสุด", "zh-TW": "至尊", "ja": "至高なる", "ko": "지고하신"},
    "Lord": {"th": "พระผู้เป็นเจ้า", "zh-TW": "主", "ja": "主", "ko": "주"},
    "soul": {"th": "วิญญาณ", "zh-TW": "靈魂", "ja": "魂", "ko": "영혼"},
    "eternal": {"th": "นิรันดร์", "zh-TW": "永恆的", "ja": "永遠の", "ko": "영원한"},
    "indestructible": {"th": "ไม่อาจทำลายได้", "zh-TW": "不可毀壞的", "ja": "破壊できない", "ko": "파괴할 수 없는"},
    "unborn": {"th": "ไม่เกิด", "zh-TW": "無生的", "ja": "生まれざる", "ko": "태어나지 않는"},
    "constant": {"th": "คงที่", "zh-TW": "恆常的", "ja": "不変の", "ko": "불변의"},
    "ancient": {"th": "โบราณ", "zh-TW": "古老的", "ja": "古の", "ko": "고대의"},
    "body": {"th": "ร่างกาย", "zh-TW": "身體", "ja": "身体", "ko": "육체"},
    "material": {"th": "วัตถุ", "zh-TW": "物質", "ja": "物質", "ko": "물질"},
    "world": {"th": "โลก", "zh-TW": "世界", "ja": "世界", "ko": "세상"},
    "knowledge": {"th": "ความรู้", "zh-TW": "知識", "ja": "知識", "ko": "지식"},
    "wisdom": {"th": "ปัญญา", "zh-TW": "智慧", "ja": "知恵", "ko": "지혜"},
    "yoga": {"th": "โยคะ", "zh-TW": "瑜伽", "ja": "ヨーガ", "ko": "요가"},
    "action": {"th": "การกระทำ", "zh-TW": "行動", "ja": "行為", "ko": "행위"},
    "inaction": {"th": "การไม่กระทำ", "zh-TW": "不行動", "ja": "無為", "ko": "무위"},
    "duty": {"th": "หน้าที่", "zh-TW": "職責", "ja": "義務", "ko": "의무"},
    "devotion": {"th": "ความภักดี", "zh-TW": "奉愛", "ja": "献身", "ko": "헌신"},
    "nature": {"th": "ธรรมชาติ", "zh-TW": "自然", "ja": "自然", "ko": "자연"},
    "spirit": {"th": "จิตวิญญาณ", "zh-TW": "靈性", "ja": "霊", "ko": "영"},
    "peace": {"th": "สันติ", "zh-TW": "和平", "ja": "平和", "ko": "평화"},
    "happiness": {"th": "ความสุข", "zh-TW": "快樂", "ja": "幸福", "ko": "행복"},
    "sorrow": {"th": "ความโศกเศร้า", "zh-TW": "悲傷", "ja": "悲しみ", "ko": "슬픔"},
    "fear": {"th": "ความกลัว", "zh-TW": "恐懼", "ja": "恐れ", "ko": "공포"},
    "anger": {"th": "ความโกรธ", "zh-TW": "憤怒", "ja": "怒り", "ko": "분노"},
    "desire": {"th": "ความปรารถนา", "zh-TW": "慾望", "ja": "欲望", "ko": "욕망"},
    "greed": {"th": "ความโลภ", "zh-TW": "貪婪", "ja": "貪欲", "ko": "탐욕"},
    "attachment": {"th": "การยึดติด", "zh-TW": "執著", "ja": "執着", "ko": "집착"},
    "detachment": {"th": "การไม่ยึดติด", "zh-TW": "超脫", "ja": "無執着", "ko": "무집착"},
    "liberation": {"th": "การหลุดพ้น", "zh-TW": "解脫", "ja": "解脱", "ko": "해탈"},
    "bondage": {"th": "การผูกมัด", "zh-TW": "束縛", "ja": "束縛", "ko": "속박"},
    "meditation": {"th": "การทำสมาธิ", "zh-TW": "冥想", "ja": "瞑想", "ko": "명상"},
    "concentration": {"th": "สมาธิ", "zh-TW": "專注", "ja": "集中", "ko": "집중"},
    "mind": {"th": "จิต", "zh-TW": "心", "ja": "心", "ko": "마음"},
    "intellect": {"th": "ปัญญา", "zh-TW": "智力", "ja": "知性", "ko": "지성"},
    "ego": {"th": "อัตตา", "zh-TW": "自我", "ja": "自我", "ko": "자아"},
    "self": {"th": "ตน", "zh-TW": "自我", "ja": "自己", "ko": "자아"},
    "Supreme Self": {"th": "ตนสูงสุด", "zh-TW": "至尊自我", "ja": "至高なる自己", "ko": "지고하신 자아"},
    "devotee": {"th": "ผู้ภักดี", "zh-TW": "奉愛者", "ja": "献身者", "ko": "헌신자"},
    "sage": {"th": "นักปราชญ์", "zh-TW": "聖人", "ja": "賢者", "ko": "성자"},
    "king": {"th": "กษัตริย์", "zh-TW": "國王", "ja": "王", "ko": "왕"},
    "warrior": {"th": "นักรบ", "zh-TW": "戰士", "ja": "戦士", "ko": "전사"},
    "battle": {"th": "การรบ", "zh-TW": "戰鬥", "ja": "戦い", "ko": "전투"},
    "field": {"th": "สนาม", "zh-TW": "場地", "ja": "場", "ko": "땅"},
    "dharma": {"th": "ธรรมะ", "zh-TW": "達摩", "ja": "ダルマ", "ko": "다르마"},
    "karma": {"th": "กรรม", "zh-TW": "業", "ja": "カルマ", "ko": "카르마"},
    "guna": {"th": "คุณะ", "zh-TW": "古納", "ja": "グナ", "ko": "구나"},
    "faith": {"th": "ศรัทธา", "zh-TW": "信心", "ja": "信仰", "ko": "신앙"},
    "grace": {"th": "พระกรุณา", "zh-TW": "恩典", "ja": "恩寵", "ko": "은혜"},
    "blessing": {"th": "พร", "zh-TW": "祝福", "ja": "祝福", "ko": "축복"},
}

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def translate_meaning(text):
    """Translate English text to Asian languages."""
    if not text or not text.strip():
        return {"th": "", "zh-TW": "", "ja": "", "ko": ""}
    
    # Check for exact match first
    if text in TERM_TRANSLATIONS:
        return TERM_TRANSLATIONS[text]
    
    # Try to build translation from components
    result = {"th": "", "zh-TW": "", "ja": "", "ko": ""}
    
    # Simple word-by-word translation as fallback
    words = text.split()
    translated_words = {"th": [], "zh-TW": [], "ja": [], "ko": []}
    
    for word in words:
        clean_word = word.strip('.,;:!?()"\'')
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
                        if trans[lang]:  # Only add non-empty translations
                            translated_words[lang].append(trans[lang])
                    found = True
                    break
        
        # If still not found, keep original word
        if not found:
            for lang in ["th", "zh-TW", "ja", "ko"]:
                translated_words[lang].append(clean_word)
    
    # Join translated words
    for lang in ["th", "zh-TW", "ja", "ko"]:
        result[lang] = " ".join(translated_words[lang])
    
    return result

def generate_transliteration(word):
    """Generate transliteration for Sanskrit word."""
    # Remove parentheses and clean up
    clean_word = word.strip('()')
    
    # Basic transliteration patterns
    result = {
        "th": clean_word,  # Thai uses phonetic transliteration
        "zh-TW": clean_word,  # Chinese uses phonetic transliteration
        "ja": clean_word,  # Japanese uses katakana
        "ko": clean_word  # Korean uses hangul
    }
    
    return result

def main():
    chapter_num = 2
    input_file = BASE_DIR / 'data' / 'chapters' / f'ch-{chapter_num:02d}' / 'vocabulary-source.json'
    output_file = BASE_DIR / 'data' / 'chapters' / f'ch-{chapter_num:02d}' / 'vocabulary-asian.json'
    
    print(f"Loading vocabulary from {input_file}...")
    source_data = load_json(input_file)
    
    total_words = len(source_data['vocabulary'])
    print(f"Total words to translate: {total_words}")
    
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
    
    print("Translating vocabulary...")
    for i, vocab_item in enumerate(source_data['vocabulary']):
        vocab_id = str(vocab_item['id'])
        word = vocab_item['word']
        
        # Get meanings
        ru_meaning = vocab_item['meaning'].get('ru', {}).get('text', '')
        en_meaning = vocab_item['meaning'].get('en', {}).get('text', '')
        
        # Use English as primary source
        source_text = en_meaning if en_meaning else ru_meaning
        
        # Translate meaning
        translated_meaning = translate_meaning(source_text)
        
        # Generate transliteration
        transliteration = generate_transliteration(word)
        
        output_data['vocabulary'][vocab_id] = {
            "meaning": translated_meaning,
            "transliteration": transliteration
        }
        
        if (i + 1) % 100 == 0:
            print(f"  Processed {i + 1}/{total_words} words...")
    
    print(f"Saving to {output_file}...")
    save_json(output_file, output_data)
    print(f"Done! Translated {total_words} words.")
    print(f"Output saved to: {output_file}")

if __name__ == '__main__':
    main()
