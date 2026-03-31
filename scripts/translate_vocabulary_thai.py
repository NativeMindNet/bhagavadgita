#!/usr/bin/env python3
"""
Translate Thai vocabulary entries from English to Thai.

This script identifies English-only vocabulary entries and translates them to Thai.
"""

import json
from pathlib import Path
from typing import Dict, List

# Directories
TRANSLATED_DIR = Path("/Users/anton/proj/gita/data/translated")

# Thai translation mappings for common Bhagavad Gita terms
THAI_TRANSLATIONS = {
    # Common phrases
    "O ": "โอ้ ",
    "oh ": "โอ้ ",
    "the ": "",
    "of ": "แห่ง ",
    "in ": "ใน ",
    "with ": "ด้วย ",
    "by ": "โดย ",
    "from ": "จาก ",
    "to ": "สู่ ",
    "and ": "และ ",
    "or ": "หรือ ",
    "is ": "คือ ",
    "are ": "คือ ",
    "was ": "คือ ",
    "were ": "คือ ",
    "be ": "เป็น ",
    "been ": "เป็น ",
    "being ": "การเป็น ",
    "have ": "มี ",
    "has ": "มี ",
    "had ": "มี ",
    "do ": "ทำ ",
    "does ": "ทำ ",
    "did ": "ทำ ",
    "will ": "จะ ",
    "would ": "จะ ",
    "could ": "สามารถ ",
    "should ": "ควร ",
    "may ": "อาจ ",
    "might ": "อาจ ",
    "must ": "ต้อง ",
    "can ": "สามารถ ",
    
    # Key terms
    "valiant": "นักรบผู้กล้าหาญ",
    "brave": "ผู้กล้าหาญ",
    "warrior": "นักรบ",
    "hero": "วีรบุรุษ",
    "king": "กษัตริย์",
    "lord": "พระผู้เป็นเจ้า",
    "master": "อาจารย์",
    "teacher": "ครู",
    "disciple": "ศิษย์",
    "student": "นักเรียน",
    "devotee": "ผู้ศรัทธา",
    "yogi": "นักโยคะ",
    "sage": "นักปราชญ์",
    "seer": "ผู้หยั่งรู้",
    "soul": "วิญญาณ",
    "self": "ตัวตน",
    "spirit": "จิตวิญญาณ",
    "mind": "จิตใจ",
    "heart": "หัวใจ",
    "body": "ร่างกาย",
    "action": "การกระทำ",
    "work": "งาน",
    "duty": "หน้าที่",
    "dharma": "ธรรมะ",
    "karma": "กรรม",
    "yoga": "โยคะ",
    "knowledge": "ความรู้",
    "wisdom": "ปัญญา",
    "devotion": "ความศรัทธา",
    "meditation": "การทำสมาธิ",
    "concentration": "สมาธิ",
    "detachment": "ความไม่ยึดติด",
    "renunciation": "การละทิ้ง",
    "liberation": "การหลุดพ้น",
    "salvation": "ความรอด",
    "enlightenment": "การตรัสรู้",
    "consciousness": "จิตสำนึก",
    "awareness": "สติ",
    "perception": "การรับรู้",
    "sense": "ประสาทสัมผัส",
    "object": "วัตถุ",
    "world": "โลก",
    "universe": "จักรวาล",
    "nature": "ธรรมชาติ",
    "material": "วัตถุ",
    "spiritual": "จิตวิญญาณ",
    "divine": "ศักดิ์สิทธิ์",
    "sacred": "ศักดิ์สิทธิ์",
    "holy": "บริสุทธิ์",
    "pure": "บริสุทธิ์",
    "supreme": "สูงสุด",
    "eternal": "นิรันดร์",
    "imperishable": "ไม่เสื่อมสลาย",
    "indestructible": "ทำลายไม่ได้",
    "immortal": "อมตะ",
    "death": "ความตาย",
    "birth": "การเกิด",
    "life": "ชีวิต",
    "existence": "การมีอยู่",
    "reality": "ความจริง",
    "truth": "สัจธรรม",
    "illusion": "มายา",
    "delusion": "ความหลงผิด",
    "ignorance": "อวิชชา",
    "desire": "ความปรารถนา",
    "attachment": "ความยึดติด",
    "aversion": "ความเกลียดชัง",
    "anger": "ความโกรธ",
    "greed": "ความโลภ",
    "lust": "กิเลส",
    "pride": "ความเย่อหยิ่ง",
    "envy": "ความอิจฉา",
    "fear": "ความกลัว",
    "sorrow": "ความโศกเศร้า",
    "joy": "ความสุข",
    "peace": "สันติ",
    "bliss": "ความปีติ",
    "happiness": "ความสุข",
    "pleasure": "ความเพลิดเพลิน",
    "pain": "ความเจ็บปวด",
    "suffering": "ความทุกข์",
    "enjoyment": "ความเพลิดเพลิน",
    "experience": "ประสบการณ์",
    "state": "สถานะ",
    "condition": "สภาพ",
    "quality": "คุณสมบัติ",
    "mode": "โหมด",
    "guna": "คุณะ",
    "sattva": "สัตตะ",
    "rajas": "รชัส",
    "tamas": "ตมัส",
    "element": "ธาตุ",
    "earth": "ดิน",
    "water": "น้ำ",
    "fire": "ไฟ",
    "air": "อากาศ",
    "ether": "อีเทอร์",
    "space": "อวกาศ",
    "time": "เวลา",
    "cause": "สาเหตุ",
    "effect": "ผลลัพธ์",
    "source": "แหล่งกำเนิด",
    "origin": "จุดเริ่มต้น",
    "end": "จุดจบ",
    "beginning": "จุดเริ่มต้น",
    "middle": "กลาง",
    "within": "ภายใน",
    "without": "ภายนอก",
    "inside": "ข้างใน",
    "outside": "ข้างนอก",
    "above": "เหนือ",
    "below": "ใต้",
    "beyond": "เหนือกว่า",
    "higher": "สูงกว่า",
    "lower": "ต่ำกว่า",
    "inner": "ภายใน",
    "outer": "ภายนอก",
    "subtle": "ละเอียด",
    "gross": "หยาบ",
    "manifest": "ปรากฏ",
    "unmanifest": "ไม่ปรากฏ",
    "visible": "มองเห็น",
    "invisible": "มองไม่เห็น",
    "known": "ที่รู้จัก",
    "unknown": "ที่ไม่รู้จัก",
    "attain": "บรรลุ",
    "reach": "ไปถึง",
    "achieve": "สำเร็จ",
    "obtain": "ได้รับ",
    "gain": "ได้รับ",
    "lose": "สูญเสีย",
    "find": "พบ",
    "seek": "แสวงหา",
    "search": "ค้นหา",
    "know": "รู้",
    "understand": "เข้าใจ",
    "realize": "ตระหนัก",
    "see": "เห็น",
    "perceive": "รับรู้",
    "experience": "ประสบการณ์",
    "enjoy": "เพลิดเพลิน",
    "suffer": "ทนทุกข์",
    "act": "กระทำ",
    "perform": "ปฏิบัติ",
    "do": "ทำ",
    "practice": "ปฏิบัติ",
    "worship": "บูชา",
    "serve": "รับใช้",
    "surrender": "ยอมจำนน",
    "dedicate": "อุทิศ",
    "offer": "ถวาย",
    "give": "ให้",
    "take": "เอา",
    "accept": "ยอมรับ",
    "reject": "ปฏิเสธ",
    "abandon": "ละทิ้ง",
    "renounce": "ละเลิก",
    "control": "ควบคุม",
    "restrain": "ระงับ",
    "conquer": "พิชิต",
    "overcome": "เอาชนะ",
    "defeat": "พ่ายแพ้",
    "win": "ชนะ",
    "lose": "แพ้",
    "fight": "ต่อสู้",
    "battle": "การต่อสู้",
    "war": "สงคราม",
    "enemy": "ศัตรู",
    "friend": "เพื่อน",
    "ally": "พันธมิตร",
    "companion": "สหาย",
    "guide": "ผู้นำทาง",
    "leader": "ผู้นำ",
    "follower": "ผู้ตาม",
    "master": "เจ้านาย",
    "servant": "ผู้รับใช้",
    "father": "บิดา",
    "mother": "มารดา",
    "son": "บุตร",
    "daughter": "ธิดา",
    "family": "ครอบครัว",
    "dynasty": "ราชวงศ์",
    "lineage": "เชื้อสาย",
    "tradition": "ประเพณี",
    "scripture": "คัมภีร์",
    "veda": "พระเวท",
    "upanishad": "อุปนิษัท",
    "gita": "คีตา",
    "chapter": "บท",
    "verse": "โศลก",
    "word": "คำ",
    "meaning": "ความหมาย",
    "purpose": "วัตถุประสงค์",
    "goal": "เป้าหมาย",
    "path": "หนทาง",
    "way": "ทาง",
    "method": "วิธีการ",
    "process": "กระบวนการ",
    "system": "ระบบ",
    "science": "วิทยาศาสตร์",
    "art": "ศิลปะ",
    "skill": "ทักษะ",
    "power": "พลัง",
    "strength": "ความแข็งแกร่ง",
    "energy": "พลังงาน",
    "force": "แรง",
    "light": "แสงสว่าง",
    "darkness": "ความมืด",
    "sun": "ดวงอาทิตย์",
    "moon": "ดวงจันทร์",
    "star": "ดวงดาว",
    "heaven": "สวรรค์",
    "earth": "โลก",
    "hell": "นรก",
    "plane": "ระดับ",
    "realm": "อาณาจักร",
    "region": "ภูมิภาค",
    "place": "สถานที่",
    "abode": "ที่อยู่",
    "home": "บ้าน",
    "dwelling": "ที่พำนัก",
    "residence": "ที่อยู่อาศัย",
    "position": "ตำแหน่ง",
    "status": "สถานะ",
    "rank": "อันดับ",
    "level": "ระดับ",
    "stage": "ขั้น",
    "step": "ขั้นตอน",
    "degree": "ระดับ",
    "extent": "ขอบเขต",
    "measure": "มาตรการ",
    "limit": "ขีดจำกัด",
    "boundary": "ขอบเขต",
    "end": "จุดจบ",
    "completion": "เสร็จสมบูรณ์",
    "perfection": "ความสมบูรณ์แบบ",
    "fulfillment": "ความสมบูรณ์",
    "satisfaction": "ความพึงพอใจ",
    "contentment": "ความพอใจ",
    "gratification": "ความพึงพอใจ",
    "pleasure": "ความเพลิดเพลิน",
    "delight": "ความยินดี",
    "happiness": "ความสุข",
    "bliss": "ความปีติ",
    "ecstasy": "ความปิติยินดี",
    "love": "ความรัก",
    "compassion": "ความเมตตา",
    "kindness": "ความเมตตา",
    "mercy": "ความเมตตา",
    "grace": "พระคุณ",
    "blessing": "พร",
    "gift": "ของขวัญ",
    "boon": "พร",
    "favor": "ความโปรดปราน",
    "benefit": "ประโยชน์",
    "good": "ดี",
    "evil": "ชั่วร้าย",
    "right": "ถูกต้อง",
    "wrong": "ผิด",
    "virtue": "คุณธรรม",
    "sin": "บาป",
    "merit": "บุญ",
    "demerit": "บาป",
    "reward": "รางวัล",
    "punishment": "การลงโทษ",
    "consequence": "ผลลัพธ์",
    "result": "ผล",
    "fruit": "ผล",
    "outcome": "ผลลัพธ์",
    "effect": "ผลกระทบ",
    "impact": "ผลกระทบ",
    "influence": "อิทธิพล",
    "power": "อำนาจ",
    "authority": "อำนาจ",
    "control": "การควบคุม",
    "dominion": "อำนาจ",
    "sovereignty": "อำนาจอธิปไตย",
    "rule": "กฎ",
    "law": "กฎหมาย",
    "order": "คำสั่ง",
    "command": "คำสั่ง",
    "instruction": "คำแนะนำ",
    "teaching": "คำสอน",
    "lesson": "บทเรียน",
    "message": "ข้อความ",
    "word": "คำพูด",
    "speech": "คำพูด",
    "sound": "เสียง",
    "name": "ชื่อ",
    "form": "รูปแบบ",
    "shape": "รูปร่าง",
    "appearance": "ลักษณะที่ปรากฏ",
    "quality": "คุณภาพ",
    "attribute": "คุณลักษณะ",
    "property": "คุณสมบัติ",
    "characteristic": "ลักษณะ",
    "feature": "คุณสมบัติ",
    "aspect": "แง่มุม",
    "part": "ส่วน",
    "portion": "ส่วน",
    "fragment": "เศษ",
    "piece": "ชิ้น",
    "unit": "หน่วย",
    "element": "องค์ประกอบ",
    "component": "ส่วนประกอบ",
    "factor": "ปัจจัย",
    "cause": "สาเหตุ",
    "reason": "เหตุผล",
    "purpose": "วัตถุประสงค์",
    "aim": "เป้าหมาย",
    "objective": "วัตถุประสงค์",
    "target": "เป้าหมาย",
    "end": "จุดหมาย",
    "goal": "เป้าหมาย",
    "destination": "จุดหมายปลายทาง",
    "path": "เส้นทาง",
    "route": "เส้นทาง",
    "journey": "การเดินทาง",
    "travel": "การเดินทาง",
    "movement": "การเคลื่อนไหว",
    "motion": "การเคลื่อนไหว",
    "action": "การกระทำ",
    "activity": "กิจกรรม",
    "operation": "การดำเนินงาน",
    "function": "หน้าที่",
    "work": "งาน",
    "labor": "แรงงาน",
    "effort": "ความพยายาม",
    "endeavor": "ความพยายาม",
    "attempt": "ความพยายาม",
    "trial": "การทดลอง",
    "test": "การทดสอบ",
    "examination": "การตรวจสอบ",
    "inspection": "การตรวจสอบ",
    "observation": "การสังเกต",
    "study": "การศึกษา",
    "research": "การวิจัย",
    "investigation": "การสอบสวน",
    "inquiry": "การสอบถาม",
    "question": "คำถาม",
    "answer": "คำตอบ",
    "solution": "วิธีแก้",
    "resolution": "มติ",
    "decision": "การตัดสินใจ",
    "choice": "ทางเลือก",
    "option": "ตัวเลือก",
    "alternative": "ทางเลือก",
    "possibility": "ความเป็นไปได้",
    "probability": "ความน่าจะเป็น",
    "certainty": "ความแน่นอน",
    "uncertainty": "ความไม่แน่นอน",
    "doubt": "ความสงสัย",
    "faith": "ศรัทธา",
    "belief": "ความเชื่อ",
    "trust": "ความไว้วางใจ",
    "confidence": "ความมั่นใจ",
    "hope": "ความหวัง",
    "expectation": "ความคาดหวัง",
    "desire": "ความปรารถนา",
    "wish": "ความปรารถนา",
    "want": "ต้องการ",
    "need": "ต้องการ",
    "requirement": "ความต้องการ",
    "necessity": "ความจำเป็น",
    "obligation": "ภาระผูกพัน",
    "duty": "หน้าที่",
    "responsibility": "ความรับผิดชอบ",
    "accountability": "ความรับผิดชอบ",
    "liability": "ความรับผิด",
    "guilt": "ความผิด",
    "innocence": "ความบริสุทธิ์",
    "purity": "ความบริสุทธิ์",
    "cleanliness": "ความสะอาด",
    "hygiene": "สุขอนามัย",
    "health": "สุขภาพ",
    "wellness": "สุขภาพที่ดี",
    "fitness": "ความฟิต",
    "strength": "ความแข็งแรง",
    "vitality": "ความมีชีวิตชีวา",
    "vigor": "ความกระฉับกระเฉง",
    "energy": "พลังงาน",
    "power": "พลัง",
    "force": "แรง",
    "might": "พลัง",
    "potency": "ศักยภาพ",
    "capacity": "ความจุ",
    "ability": "ความสามารถ",
    "capability": "ความสามารถ",
    "skill": "ทักษะ",
    "talent": "ความสามารถ",
    "gift": "ของขวัญ",
    "endowment": "พรสวรรค์",
    "blessing": "พร",
    "grace": "พระคุณ",
    "mercy": "ความเมตตา",
    "compassion": "ความเมตตา",
    "kindness": "ความเมตตา",
    "gentleness": "ความอ่อนโยน",
    "tenderness": "ความอ่อนโยน",
    "softness": "ความนุ่มนวล",
    "hardness": "ความแข็ง",
    "roughness": "ความขรุขระ",
    "smoothness": "ความเรียบ",
    "balance": "ความสมดุล",
    "equilibrium": "ความสมดุล",
    "harmony": "ความสามัคคี",
    "unity": "ความสามัคคี",
    "oneness": "ความเป็นหนึ่ง",
    "wholeness": "ความสมบูรณ์",
    "completeness": "ความสมบูรณ์",
    "perfection": "ความสมบูรณ์แบบ",
    "flawlessness": "ความไร้ที่ติ",
    "excellence": "ความเป็นเลิศ",
    "superiority": "ความเหนือกว่า",
    "supremacy": "ความเป็นสูงสุด",
    "paramountcy": "ความเป็นสูงสุด",
    "preeminence": "ความเป็นเลิศ",
    "distinction": "ความแตกต่าง",
    "uniqueness": "ความเป็นเอกลักษณ์",
    "specialness": "ความพิเศษ",
    "rarity": "ความหายาก",
    "scarcity": "ความขาดแคลน",
    "abundance": "ความอุดมสมบูรณ์",
    "plenty": "มากมาย",
    "fullness": "ความเต็ม",
    "completeness": "ความสมบูรณ์",
    "totality": "ความสมบูรณ์",
    "entirety": "ทั้งหมด",
    "whole": "ทั้งหมด",
    "all": "ทั้งหมด",
    "everything": "ทุกอย่าง",
    "nothing": "ไม่มีอะไร",
    "something": "บางอย่าง",
    "anything": "อะไรก็ได้",
    "someone": "บางคน",
    "no one": "ไม่มีใคร",
    "everyone": "ทุกคน",
    "anyone": "ใครก็ได้",
    "somebody": "บางคน",
    "nobody": "ไม่มีใคร",
    "everybody": "ทุกคน",
    "anybody": "ใครก็ได้",
}

# More specific Thai translations for common English phrases in vocabulary
PHRASE_TRANSLATIONS = {
    "best of the valiant": "ยอดนักรบผู้กล้าหาญที่สุด",
    "son of Kuru": "บุตรแห่งกุรุ",
    "son of Kunti": "บุตรแห่งกุนตี",
    "O son of": "โอ้ บุตรแห่ง",
    "O best of": "โอ้ ยอดเยี่ยมแห่ง",
    "the Supreme Lord": "พระผู้เป็นเจ้าสูงสุด",
    "the Supreme Personality": "พระบุคคลสูงสุด",
    "the Supreme Person": "พระบุคคลสูงสุด",
    "the Supreme Soul": "วิญญาณสูงสุด",
    "the Supersoul": "วิญญาณสูงสุด",
    "the individual soul": "วิญญาณแต่ละดวง",
    "the living entity": "สิ่งมีชีวิต",
    "the living being": "สิ่งมีชีวิต",
    "the embodied soul": "วิญญาณที่มีร่างกาย",
    "the embodied being": "สิ่งมีชีวิตที่มีร่างกาย",
    "the body": "ร่างกาย",
    "the mind": "จิตใจ",
    "the senses": "ประสาทสัมผัส",
    "the sense objects": "วัตถุแห่งประสาทสัมผัส",
    "the material world": "โลกวัตถุ",
    "the spiritual world": "โลกจิตวิญญาณ",
    "the material energy": "พลังงานวัตถุ",
    "the spiritual energy": "พลังงานจิตวิญญาณ",
    "the external energy": "พลังงานภายนอก",
    "the internal energy": "พลังงานภายใน",
    "the marginal energy": "พลังงานชายขอบ",
    "the illusory energy": "พลังงานมายา",
    "the deluding energy": "พลังงานที่ทำให้หลงผิด",
    "the modes of nature": "คุณะแห่งธรรมชาติ",
    "the three modes": "คุณะทั้งสาม",
    "the mode of goodness": "คุณะแห่งความดี",
    "the mode of passion": "คุณะแห่งความหลงใหล",
    "the mode of ignorance": "คุณะแห่งความไม่รู้",
    "the path of": "หนทางแห่ง",
    "the way of": "หนทางแห่ง",
    "the process of": "กระบวนการแห่ง",
    "the science of": "วิทยาศาสตร์แห่ง",
    "the art of": "ศิลปะแห่ง",
    "the yoga of": "โยคะแห่ง",
    "the knowledge of": "ความรู้แห่ง",
    "the wisdom of": "ปัญญาแห่ง",
    "the realization of": "การตระหนักแห่ง",
    "the understanding of": "ความเข้าใจแห่ง",
    "the practice of": "การปฏิบัติแห่ง",
    "the performance of": "การปฏิบัติแห่ง",
    "the offering of": "การถวายแห่ง",
    "the sacrifice of": "การเสียสละแห่ง",
    "the renunciation of": "การละทิ้งแห่ง",
    "the detachment from": "ความไม่ยึดติดจาก",
    "the attachment to": "ความยึดติดกับ",
    "the desire for": "ความปรารถนาเพื่อ",
    "the love for": "ความรักเพื่อ",
    "the devotion to": "ความศรัทธาเพื่อ",
    "the surrender to": "การยอมจำนนต่อ",
    "the service of": "การรับใช้แห่ง",
    "the worship of": "การบูชาแห่ง",
    "the meditation on": "การทำสมาธิบน",
    "the concentration on": "สมาธิบน",
    "the contemplation on": "การไตร่ตรองบน",
    "the remembrance of": "การระลึกถึง",
    "the chanting of": "การสวดมนต์แห่ง",
    "the hearing of": "การฟังแห่ง",
    "the speaking of": "การพูดแห่ง",
    "the seeing of": "การเห็นแห่ง",
    "the tasting of": "การลิ้มรสแห่ง",
    "the touching of": "การสัมผัสแห่ง",
    "the smelling of": "การดมกลิ่นแห่ง",
    "attaining to": "บรรลุถึง",
    "reaching to": "ไปถึง",
    "achieving": "บรรลุ",
    "obtaining": "ได้รับ",
    "gaining": "ได้รับ",
    "losing": "สูญเสีย",
    "finding": "พบ",
    "seeking": "แสวงหา",
    "searching for": "ค้นหา",
    "knowing": "รู้",
    "understanding": "เข้าใจ",
    "realizing": "ตระหนัก",
    "seeing": "เห็น",
    "perceiving": "รับรู้",
    "experiencing": "ประสบ",
    "enjoying": "เพลิดเพลิน",
    "suffering": "ทนทุกข์",
    "acting": "กระทำ",
    "performing": "ปฏิบัติ",
    "doing": "ทำ",
    "practicing": "ปฏิบัติ",
    "worshiping": "บูชา",
    "serving": "รับใช้",
    "surrendering": "ยอมจำนน",
    "dedicating": "อุทิศ",
    "offering": "ถวาย",
    "giving": "ให้",
    "taking": "เอา",
    "accepting": "ยอมรับ",
    "rejecting": "ปฏิเสธ",
    "abandoning": "ละทิ้ง",
    "renouncing": "ละเลิก",
    "controlling": "ควบคุม",
    "restraining": "ระงับ",
    "conquering": "พิชิต",
    "overcoming": "เอาชนะ",
    "defeating": "พ่ายแพ้",
    "winning": "ชนะ",
    "losing": "แพ้",
    "fighting": "ต่อสู้",
    "battling": "ต่อสู้",
    "with mind detached": "ด้วยจิตใจที่ไม่ยึดติด",
    "with devotion": "ด้วยความศรัทธา",
    "with love": "ด้วยความรัก",
    "with compassion": "ด้วยความเมตตา",
    "with kindness": "ด้วยความเมตตา",
    "with wisdom": "ด้วยปัญญา",
    "with knowledge": "ด้วยความรู้",
    "with understanding": "ด้วยความเข้าใจ",
    "with faith": "ด้วยศรัทธา",
    "with trust": "ด้วยความไว้วางใจ",
    "with confidence": "ด้วยความมั่นใจ",
    "with hope": "ด้วยความหวัง",
    "with desire": "ด้วยความปรารถนา",
    "without desire": "โดยไม่มีความปรารถนา",
    "without attachment": "โดยไม่มีความยึดติด",
    "without ego": "โดยไม่มีความยึดมั่นในตัวตน",
    "without pride": "โดยไม่มีความเย่อหยิ่ง",
    "without anger": "โดยไม่มีความโกรธ",
    "without greed": "โดยไม่มีความโลภ",
    "without lust": "โดยไม่มีความกิเลส",
    "without fear": "โดยไม่มีความกลัว",
    "without sorrow": "โดยไม่มีความโศกเศร้า",
    "free from": "ปราศจาก",
    "devoid of": "ปราศจาก",
    "full of": "เต็มไปด้วย",
    "filled with": "เต็มไปด้วย",
    "endowed with": "ประกอบด้วย",
    "blessed with": "ได้รับพรด้วย",
    "graced with": "ได้รับพระคุณด้วย",
    "known as": "รู้จักกันในชื่อ",
    "called": "เรียกว่า",
    "named": "ชื่อว่า",
    "termed": "เรียกว่า",
    "described as": "อธิบายว่าเป็น",
    "considered as": "ถือว่าเป็น",
    "regarded as": "ถือว่าเป็น",
    "seen as": "เห็นว่าเป็น",
    "understood as": "เข้าใจว่าเป็น",
    "realized as": "ตระหนักว่าเป็น",
    "to be": "ที่จะเป็น",
    "to have": "ที่จะมี",
    "to do": "ที่จะทำ",
    "to act": "ที่จะกระทำ",
    "to perform": "ที่จะปฏิบัติ",
    "to achieve": "ที่จะบรรลุ",
    "to attain": "ที่จะบรรลุ",
    "to reach": "ที่จะไปถึง",
    "to obtain": "ที่จะได้รับ",
    "to gain": "ที่จะได้รับ",
    "to lose": "ที่จะสูญเสีย",
    "to find": "ที่จะพบ",
    "to seek": "ที่จะแสวงหา",
    "to know": "ที่จะรู้",
    "to understand": "ที่จะเข้าใจ",
    "to realize": "ที่จะตระหนัก",
    "to see": "ที่จะเห็น",
    "to perceive": "ที่จะรับรู้",
    "to experience": "ที่จะประสบ",
    "to enjoy": "ที่จะเพลิดเพลิน",
    "to suffer": "ที่จะทนทุกข์",
    "to worship": "ที่จะบูชา",
    "to serve": "ที่จะรับใช้",
    "to surrender": "ที่จะยอมจำนน",
    "to dedicate": "ที่จะอุทิศ",
    "to offer": "ที่จะถวาย",
    "to give": "ที่จะให้",
    "to take": "ที่จะเอา",
    "to accept": "ที่จะยอมรับ",
    "to reject": "ที่จะปฏิเสธ",
    "to abandon": "ที่จะละทิ้ง",
    "to renounce": "ที่จะละเลิก",
    "to control": "ที่จะควบคุม",
    "to restrain": "ที่จะระงับ",
    "to conquer": "ที่จะพิชิต",
    "to overcome": "ที่จะเอาชนะ",
}


def translate_to_thai(text: str) -> str:
    """
    Translate English text to Thai.
    This is a simple rule-based translator for Bhagavad Gita vocabulary.
    """
    result = text
    
    # First, try phrase-level translations
    for phrase, translation in PHRASE_TRANSLATIONS.items():
        if phrase.lower() in result.lower():
            # Preserve capitalization of first letter
            if result[0].isupper():
                result = result.replace(phrase, translation, 1)
            else:
                result = result.replace(phrase.lower(), translation, 1)
    
    # Then word-level translations
    words = result.split()
    translated_words = []
    
    for word in words:
        # Preserve punctuation
        clean_word = word.strip('(),.!?;:"\'')
        punctuation = word[len(clean_word):] if len(word) > len(clean_word) else ''
        prefix = word[:len(word)-len(clean_word)-len(punctuation)] if len(word) > len(clean_word)+len(punctuation) else ''
        
        # Try to translate
        if clean_word.lower() in THAI_TRANSLATIONS:
            translated = THAI_TRANSLATIONS[clean_word.lower()]
            translated_words.append(prefix + translated + punctuation)
        else:
            # Keep original if no translation found
            translated_words.append(word)
    
    result = ' '.join(translated_words)
    
    # Clean up extra spaces
    result = ' '.join(result.split())
    
    return result


def analyze_vocabulary(lang: str, chapter: int) -> Dict:
    """Analyze vocabulary file for a language and chapter."""
    chapter_str = f"{chapter:02d}"
    vocab_file = TRANSLATED_DIR / lang / f"chapter-{chapter_str}-{lang}_vocabulary.json"
    
    if not vocab_file.exists():
        return {'error': 'File not found'}
    
    with open(vocab_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    vocabulary = data.get('vocabulary', {})
    total = len(vocabulary)
    english_only = 0
    has_native = 0
    entries_to_translate = []
    
    for word_id, entry in vocabulary.items():
        meaning = entry.get('meaning', '')
        
        # Check if English-only (ASCII)
        try:
            meaning.encode('ascii')
            english_only += 1
            entries_to_translate.append(word_id)
        except UnicodeEncodeError:
            has_native += 1
    
    return {
        'total': total,
        'english_only': english_only,
        'has_native': has_native,
        'entries_to_translate': entries_to_translate
    }


def translate_chapter_vocabulary(chapter: int, dry_run: bool = True) -> Dict:
    """Translate English-only vocabulary entries for a chapter."""
    chapter_str = f"{chapter:02d}"
    lang = 'th'
    vocab_file = TRANSLATED_DIR / lang / f"chapter-{chapter_str}-{lang}_vocabulary.json"
    
    if not vocab_file.exists():
        return {'error': 'File not found'}
    
    with open(vocab_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    vocabulary = data.get('vocabulary', {})
    translated_count = 0
    skipped_count = 0
    
    for word_id, entry in vocabulary.items():
        meaning = entry.get('meaning', '')
        
        # Check if English-only
        try:
            meaning.encode('ascii')
            # Translate
            thai_meaning = translate_to_thai(meaning)
            entry['meaning'] = thai_meaning
            translated_count += 1
            
            if not dry_run:
                print(f"  {word_id}: {meaning[:40]}... → {thai_meaning[:40]}...")
        except UnicodeEncodeError:
            # Already has Thai, skip
            skipped_count += 1
    
    if not dry_run:
        # Save updated vocabulary
        with open(vocab_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    return {
        'chapter': chapter,
        'translated': translated_count,
        'skipped': skipped_count,
        'total': translated_count + skipped_count
    }


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Translate Thai vocabulary')
    parser.add_argument('--chapter', type=int, help='Specific chapter (1-18)')
    parser.add_argument('--execute', action='store_true', 
                       help='Execute translation (default: analyze only)')
    
    args = parser.parse_args()
    
    chapters = range(1, 19)
    if args.chapter:
        chapters = [args.chapter]
    
    print("Thai Vocabulary Translation")
    print("=" * 60)
    
    if not args.execute:
        # Analysis mode
        total_entries = 0
        total_english = 0
        
        for chapter in chapters:
            stats = analyze_vocabulary('th', chapter)
            if 'error' not in stats:
                print(f"Chapter {chapter:2d}: {stats['total']:4d} entries, "
                      f"{stats['english_only']:4d} to translate, "
                      f"{stats['has_native']:4d} already Thai")
                total_entries += stats['total']
                total_english += stats['english_only']
        
        print("=" * 60)
        print(f"TOTAL: {total_entries} entries, {total_english} need translation")
        print("\nRun with --execute to perform translation")
    else:
        # Translation mode
        print("Executing translation...")
        print("=" * 60)
        
        total_translated = 0
        total_skipped = 0
        
        for chapter in chapters:
            print(f"\nChapter {chapter}:")
            result = translate_chapter_vocabulary(chapter, dry_run=False)
            if 'error' not in result:
                print(f"  Translated: {result['translated']}, Skipped: {result['skipped']}")
                total_translated += result['translated']
                total_skipped += result['skipped']
        
        print("\n" + "=" * 60)
        print(f"COMPLETE: Translated {total_translated} entries, skipped {total_skipped}")


if __name__ == '__main__':
    main()
