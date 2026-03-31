#!/usr/bin/env python3
"""
Translate Thai vocabulary batch using AI-powered translation.
Implements the /translate.sanscrit command functionality for vocabulary translation.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Thai translations for common Bhagavad Gita terms and phrases
THAI_VOCABULARY = {
    # Prepositions and common words
    "from": "จาก",
    "in": "ใน",
    "to": "สู่",
    "for": "เพื่อ",
    "with": "ด้วย",
    "by": "โดย",
    "of": "แห่ง",
    "and": "และ",
    "or": "หรือ",
    "the": "",
    "a": "",
    "an": "",
    
    # Verbs
    "is": "คือ",
    "are": "คือ",
    "was": "คือ",
    "were": "คือ",
    "be": "เป็น",
    "been": "เป็น",
    "being": "การเป็น",
    "have": "มี",
    "has": "มี",
    "had": "มี",
    "do": "ทำ",
    "does": "ทำ",
    "did": "ทำ",
    "will": "จะ",
    "would": "จะ",
    "could": "สามารถ",
    "should": "ควร",
    "may": "อาจ",
    "might": "อาจ",
    "must": "ต้อง",
    "can": "สามารถ",
    
    # Key philosophical terms
    "loss": "การสูญเสีย",
    "intelligence": "ปัญญา",
    "bodies": "ร่างกาย",
    "embodied": "ที่มีร่างกาย",
    "vision": "การมองเห็น",
    "dead": "ผู้ตาย",
    "killing": "การฆ่า",
    "teachers": "ครูอาจารย์",
    "superiors": "ผู้ใหญ่",
    "sense-controlled": "ผู้ควบคุมประสาทสัมผัส",
    "conqueror": "ผู้พิชิต",
    "sleep": "การนอนหลับ",
    "old": "แก่",
    "decrepit": "ชราภาพ",
    "expertise": "ความเชี่ยวชาญ",
    "advocate": "สนับสนุน",
    "various": "ต่างๆ",
    "ceremonies": "พิธีกรรม",
    "rituals": "พิธีการ",
    "description": "คำอธิบาย",
    "like": "เหมือน",
    "limbs": "อวัยวะ",
    "tortoise": "เต่า",
    "confident": "มั่นใจ",
    "success": "ความสำเร็จ",
    "elders": "ผู้อาวุโส",
    "great": "ยิ่งใหญ่",
    "warriors": "นักรบ",
    "others": "อื่นๆ",
    "there is no": "ไม่มี",
    "who is always": "ผู้ซึ่งเสมอ",
    "the same": "เหมือนกัน",
    "sees": "เห็น",
    "futility": "ความไร้ประโยชน์",
    "mundane": "ทางโลก",
    "endeavours": "ความพยายาม",
    "remains": "ยังคง",
    "indifferent": "ไม่แยแส",
    "dualities": "ความคู่ตรงข้าม",
    "motivated": "มีแรงจูงใจ",
    "fruits": "ผล",
    "actions": "การกระทำ",
    "results": "ผลลัพธ์",
    "peaceful-hearted person": "ผู้มีจิตใจสงบ",
    "diminution": "การลดลง",
    "in the event": "ในกรณี",
    "taste": "รสชาติ",
    "even": "แม้",
    "respected": " уважаемый",
    "in success and failure": "ในความสำเร็จและความล้มเหลว",
    "forgetfulness": "การลืม",
    "scriptural": "คัมภีร์",
    "morality": "ศีลธรรม",
    "pious": "ศรัทธา",
    "sinful": "บาป",
    "demigods": "เทวดา",
    "in that": "ในนั้น",
    "night": "กลางคืน",
    "matter": "เรื่อง",
    "both of them": "ทั้งสอง",
    "flowery words": "คำพูดที่สวยหรู",
    "Vedas": "พระเวท",
    "ready": "พร้อม",
    "counsel": "คำแนะนำ",
    "direction": "ทิศทาง",
    "content": "พอใจ",
    "bring about": "นำมาซึ่ง",
    "destruction": "การทำลาย",
    "wise person": "ผู้ฉลาด",
    "grief-stricken": "ผู้โศกเศร้า",
    "saddened": "ผู้เศร้าโศก",
    "those for whom": "ผู้ซึ่ง",
    "which is always": "ซึ่งเสมอ",
    "full": "เต็ม",
    "apparent": "ชัดเจน",
    "contradictions": "ความขัดแย้ง",
    "encourage": "ส่งเสริม",
    "ignorant": "ผู้ไม่รู้",
    "duties": "หน้าที่",
    "means": "วิธีการ",
    "five kinds": "ห้าประเภท",
    "sacrifices": "การบูชา",
    "rain": "ฝน",
    "out of resentment": "ด้วยความขัดเคือง",
    "are the seats": "คือที่นั่ง",
    "food": "อาหาร",
    "transformed": "เปลี่ยนรูป",
    "semen": "น้ำเชื้อ",
    "blood": "เลือด",
    "no piety": "ไม่มีบุญ",
    "gained": "ได้รับ",
    "being unattached": "ไม่ยึดติด",
    "born": "เกิด",
    "inhabitants": "ผู้อาศัย",
    "these worlds": "โลกเหล่านี้",
    "what will be the use": "จะมีประโยชน์อะไร",
    "even for a moment": "แม้เพียงชั่วขณะ",
    "consideration": "การพิจารณา",
    "welfare": "สวัสดิการ",
    "people": "ผู้คน",
    "unto Me": "ต่อข้าพเจ้า",
    "is not": "ไม่ใช่",
    "attached": "ยึดติด",
    "absorbed": "ดูดซับ",
    "them": "พวกเขา",
    "due to": "เนื่องจาก",
    "rainfall": "ฝนตก",
    "persons": "บุคคล",
    "bewildered": "สับสน",
    "modes": "คุณะ",
    "as the standard": "เป็นมาตรฐาน",
    "at the universal": "ที่สากล",
    "manifestation": "การปรากฏ",
    "of the realised": "ของผู้ตระหนัก",
    "food provided": "อาหารที่ให้",
    "thus pleased": "พอใจดังนั้น",
    "it is Your opinion": "เป็นความเห็นของท่าน",
    "that": "ว่า",
    "in the three worlds": "ในสามโลก",
    "it is said that": "มีกล่าวว่า",
    "by the womb": "โดยมดลูก",
    "tinged": "ย้อม",
    "faults": "ข้อบกพร่อง",
    "superior": "เหนือกว่า",
    "such": "เช่น",
    "hypocrite": "คนหน้าซื่อใจคด",
    "and that which": "และสิ่งที่",
    "oblation": "เครื่องบูชา",
    "ghee": "เนยใส",
    "Brahma": "พระพรหม",
    "the Absolute": "สัมบูรณ์",
    "by the mouthpiece": "โดยปาก",
    "with sacrifice": "ด้วยการบูชา",
    "very difficult": "ยากมาก",
    "comprehend": "เข้าใจ",
    "who is realised": "ผู้ตระหนักแล้ว",
    "Those learned": "ผู้เรียนรู้",
    "scriptures": "คัมภีร์",
    "Although I am": "แม้ว่าข้าพเจ้าเป็น",
    "accomplisher": "ผู้สำเร็จ",
    "the learned": "ผู้เรียนรู้",
    "what is": "อะไรคือ",
    "inaction": "การไม่กระทำ",
    "wholeheartedly": "อย่างสุดใจ",
    "absorbed": "ดูดซับ",
    "services": "การรับใช้",
    "Me": "ข้าพเจ้า",
    "of Mine and yours": "ของข้าพเจ้าและของท่าน",
    "who is liberated": "ผู้หลุดพ้นแล้ว",
    "or the next": "หรือถัดไป",
    "by reducing": "โดยการลด",
    "their intake": "การบริโภค",
    "functions": "หน้าที่",
    "ten": "สิบ",
    "vital life-airs": "ลมปราณ",
    "as done": " sebagaimana dilakukan",
    "in the past": "ในอดีต",
    "he is wise": "เขาฉลาด",
    "and for firmly": "และอย่างมั่นคง",
    "establishing": "สถาปนา",
    "For the doubting": "สำหรับผู้สงสัย",
    "person": "บุคคล",
    "performers": "ผู้ปฏิบัติ",
    "unshakeable": "ไม่สั่นคลอน",
    "vows": "คำสัตย์",
    "for the vanquishing": "เพื่อการพิชิต",
    "satisfied": "พอใจ",
    "whatever": " apapun",
    "readily available": "ที่มี sẵn",
    "are knowers": "เป็นผู้รู้",
    "although engaged": "แม้จะมีส่วนร่วม",
    "by the intelligence": "โดยปัญญา",
    "The childish": "ผู้เด็ก",
    "the unwise": "ผู้ไม่ฉลาด",
    "of the two": "ของสอง",
    "grasping objects": "จับวัตถุ",
    "hands": "มือ",
    "nor their association": "ไม่มีความเกี่ยวข้อง",
    "city": "เมือง",
    "nine gates": "เก้าประตู",
    "flowing through": "ไหลผ่าน",
    "nostrils": "รูจมูก",
    "inhalation": "การหายใจเข้า",
    "exhalation": "การหายใจออก",
    "nor the peity": "ไม่มีความศรัทธา",
    "who are devoted": "ผู้ศรัทธา",
    "hearing": "การฟัง",
    "singing": "การร้อง",
    "His glories": "พระเกียรติของพระองค์",
    "in a learned": "ในผู้เรียนรู้",
    "humble": "ถ่อมตน",
    "which is experienced": "ซึ่งประสบ",
    "self-realisation": "การตระหนักตน",
    "this is My": "นี่คือของข้าพเจ้า",
    "loss for him": "การสูญเสียสำหรับเขา",
    "he is not denied": "เขาไม่ถูกปฏิเสธ",
    "chance": "โอกาส",
    "fortune": "โชคลาภ",
    "see": "เห็น",
    "Supersoul": "วิญญาณสูงสุด",
    "and is also": "และยังเป็น",
    "superior": "เหนือกว่า",
    "at the top": "ที่ด้านบน",
    "between the eyes": "ระหว่างดวงตา",
    "centering": "จัดศูนย์กลาง",
    "concentration": "สมาธิ",
    "in the next life": "ในชาติหน้า",
    "i.e": "คือ",
    "and a heart": "และหัวใจ",
    "never": "ไม่เคย",
    "discouraged": "ท้อแท้",
    "with heart": "ด้วยหัวใจ",
    "at the overeater": "สำหรับผู้กินมากเกินไป",
    "transcendental": "เหนือโลก",
    "senses": "ประสาทสัมผัส",
    "yet is not": "แต่ไม่",
    "diligent": "ขยัน",
    "powerful": "ทรงพลัง",
    "uncontrollable": "ไม่สามารถควบคุมได้",
    "friend": "เพื่อน",
    "renders service": "ให้บริการ",
    "engaging": "มีส่วนร่วม",
    "devotional practices": "การปฏิบัติศรัทธา",
    "based on": "ขึ้นอยู่กับ",
    "chanting": "การสวด",
    "glories": "พระเกียรติ",
    "he is born": "เขาเกิด",
    "by contact": "โดยการสัมผัส",
    "divine": "ศักดิ์สิทธิ์",
    "on the path": "บนเส้นทาง",
    "attaining": "บรรลุ",
    "extremely": "อย่างยิ่ง",
    "difficult": "ยาก",
    "control": "ควบคุม",
    "a dispeller": "ผู้ขจัด",
    "suffering": "ความทุกข์",
    "state": "สถานะ",
    "within which": "ภายในซึ่ง",
    "all association": "ความสัมพันธ์ทั้งหมด",
    "unhappiness": "ความทุกข์",
    "severed": "ตัดขาด",
    "is difficult": "ยาก",
    "attain": "บรรลุ",
    "oversleeper": "ผู้นอนมากเกินไป",
    "home": "บ้าน",
    "it is controlled": "มันถูกควบคุม",
    "group": "กลุ่ม",
    "what is the fate": "ชะตากรรมคืออะไร",
    "as the means": "เป็นวิธีการ",
    "devoted": "อุทิศ",
    "fully dedicated": "อุทิศอย่างเต็มที่",
    "best": "ดีที่สุด",
}

# Specific phrase translations for accuracy
PHRASE_TRANSLATIONS = {
    "From loss of intelligence": "จากการสูญเสียปัญญา",
    "in the bodies": "ในร่างกาย",
    "For the embodied": "สำหรับผู้ที่มีร่างกาย",
    "by the vision": "โดยการมองเห็น",
    "which of these": "ซึ่งของเหล่านี้",
    "for the dead": "สำหรับผู้ตาย",
    "by killing our teachers and superiors": "โดยการฆ่าครูอาจารย์และผู้ใหญ่ของเรา",
    "sense-controlled Arjuna the conqueror of sleep": "อรชุนผู้ควบคุมประสาทสัมผัส ผู้พิชิตการนอนหลับ",
    "old and decrepit": "แก่และชราภาพ",
    "is the expertise": "คือความเชี่ยวชาญ",
    "and they advocate the various ceremonies and rituals": "และพวกเขาสนับสนุนพิธีกรรมและพิธีการต่างๆ",
    "what is the description": "คำอธิบายคืออะไร",
    "like the limbs of a tortoise": "เหมือนอวัยวะของเต่า",
    "being confident of success": "มั่นใจในความสำเร็จ",
    "noble elders and teachers": "ผู้อาวุโสและครูอาจารย์ผู้สูงส่ง",
    "Great warriors like Duryodhan and others": "นักรบผู้ยิ่งใหญ่เช่นทุรโยธนะและคนอื่นๆ",
    "and for one who is dead": "และสำหรับผู้ตาย",
    "there is no": "ไม่มี",
    "and there is no": "และไม่มี",
    "who is always the same": "ผู้ซึ่งเสมอเหมือนกัน",
    "who sees the futility of mundane endeavours and remains indifferent to the dualities": "ผู้เห็นความไร้ประโยชน์ของความพยายามทางโลกและยังคงไม่แยแสต่อความคู่ตรงข้าม",
    "Those motivated by the fruits of their actions": "ผู้มีแรงจูงใจจากผลของการกระทำ",
    "to the results": "ต่อผลลัพธ์",
    "of the peaceful-hearted person": "ของผู้มีจิตใจสงบ",
    "diminution of results": "การลดลงของผลลัพธ์",
    "in the event of": "ในกรณีของ",
    "But even the taste": "แต่แม้รสชาติ",
    "for the respected": "สำหรับผู้ уважаемый",
    "in success and failure": "ในความสำเร็จและความล้มเหลว",
    "forgetfulness of scriptural morality": "การลืมศีลธรรมจากคัมภีร์",
    "pious and sinful actions": "การกระทำศรัทธาและบาป",
    "over even the demigods": "เหนือแม้เทวดา",
    "in that night": "ในกลางคืนนั้น",
    "in that matter": "ในเรื่องนั้น",
    "both of them": "ทั้งสอง",
    "by those flowery words of the Vedas": "โดยคำพูดที่สวยหรูของพระเวท",
    "ready for Your counsel and direction": "พร้อมสำหรับคำแนะนำและทิศทางของท่าน",
    "and is content": "และพอใจ",
    "to bring about the destruction": "เพื่อนำมาซึ่งการทำลาย",
    "of even the wise person": "ของแม้ผู้ฉลาด",
    "to the grief-stricken": "ต่อผู้โศกเศร้า",
    "to the saddened Arjuna": "ต่ออรชุนผู้เศร้าโศก",
    "of those for whom": "ของผู้ซึ่ง",
    "which is always full": "ซึ่งเต็มเสมอ",
    "by the apparent contradictions of the Vedas": "โดยความขัดแย้งที่ชัดเจนของพระเวท",
    "they should encourage the ignorant in their duties": "พวกเขาควรส่งเสริมผู้ไม่รู้ในหน้าที่",
    "by means of the five kinds of sacrifices etc": "โดยวิธีการของการบูชาห้าประเภทเป็นต้น",
    "via the rain etc": "ผ่านฝนเป็นต้น",
    "out of resentment": "ด้วยความขัดเคือง",
    "are the seats": "คือที่นั่ง",
    "From food transformed into semen and blood": "จากอาหารที่เปลี่ยนเป็นน้ำเชื้อและเลือด",
    "no piety is gained": "ไม่ได้รับบุญ",
    "being unattached to the fruits of your actions": "ไม่ยึดติดในผลของการกระทำ",
    "is born of the Vedas": "เกิดจากพระเวท",
    "to even the intelligence": "ต่อแม้ปัญญา",
    "the inhabitants of these worlds": "ผู้อาศัยของโลกเหล่านี้",
    "What will be the use of": "จะมีประโยชน์อะไร",
    "even for a moment": "แม้เพียงชั่วขณะ",
    "in the consideration of the welfare of the people": "ในการพิจารณาสวัสดิการของผู้คน",
    "unto Me": "ต่อข้าพเจ้า",
    "is not attached to them not absorbed in them": "ไม่ยึดติดในพวกเขา ไม่ดูดซับในพวกเขา",
    "due to rainfall": "เนื่องจากฝนตก",
    "Persons bewildered by the modes": "บุคคลสับสนโดยคุณะ",
    "as the standard": "เป็นมาตรฐาน",
    "At the universal manifestation": "ที่การปรากฏสากล",
    "of the realised": "ของผู้ตระหนัก",
    "food provided by the demigods": "อาหารที่ให้โดยเทวดา",
    "and the demigods being thus pleased": "และเทวดาพอใจดังนั้น",
    "it is Your opinion that": "เป็นความเห็นของท่านว่า",
    "in the three worlds": "ในสามโลก",
    "It is said that": "มีกล่าวว่า",
    "by the womb": "โดยมดลูก",
    "tinged with faults": "ย้อมด้วยข้อบกพร่อง",
    "is superior to such a hypocrite": "เหนือกว่าคนหน้าซื่อใจคดเช่นนี้",
    "and that which": "และสิ่งที่",
    "the oblation of ghee etc": "เครื่องบูชาเนยใสเป็นต้น",
    "Brahma the Absolute": "พระพรหมสัมบูรณ์",
    "by the mouthpiece of the Vedas": "โดยปากของพระเวท",
    "the demigods with sacrifice": "เทวดาด้วยการบูชา",
    "is very difficult to comprehend": "ยากมากที่จะเข้าใจ",
    "who is realised": "ผู้ตระหนักแล้ว",
    "Those learned in the scriptures": "ผู้เรียนรู้ในคัมภีร์",
    "Although I am the accomplisher": "แม้ว่าข้าพเจ้าเป็นผู้สำเร็จ",
    "even the learned": "แม้ผู้เรียนรู้",
    "what is inaction": "อะไรคือการไม่กระทำ",
    "wholeheartedly absorbed in services to Me": "ดูดซับอย่างสุดใจในการรับใช้ข้าพเจ้า",
    "of Mine and yours": "ของข้าพเจ้าและของท่าน",
    "who is liberated": "ผู้หลุดพ้นแล้ว",
    "or the next": "หรือถัดไป",
    "by reducing their intake of food": "โดยการลดการบริโภคอาหาร",
    "the functions of the ten vital life-airs": "หน้าที่ของลมปราณสิบ",
    "as done in the past": " sebagaimana dilakukanในอดีต",
    "he is wise": "เขาฉลาด",
    "and for firmly establishing": "และอย่างมั่นคงสถาปนา",
    "For the doubting person": "สำหรับผู้สงสัย",
    "performers of unshakeable vows": "ผู้ปฏิบัติคำสัตย์ไม่สั่นคลอน",
    "for the vanquishing": "เพื่อการพิชิต",
    "satisfied with whatever is readily available": "พอใจกับ apapun ที่มี sẵn",
    "are knowers of sacrifice": "เป็นผู้รู้การบูชา",
    "athough engaged in the functions of": "แม้จะมีส่วนร่วมในหน้าที่ของ",
    "by the intelligence": "โดยปัญญา",
    "The childish the unwise": "ผู้เด็ก ผู้ไม่ฉลาด",
    "of the two": "ของสอง",
    "grasping objects in the hands": "จับวัตถุในมือ",
    "nor their association with the fruits of actions": "ไม่มีความเกี่ยวข้องกับผลของการกระทำ",
    "in the city of nine gates": "ในเมืองเก้าประตู",
    "flowing through the nostrils": "ไหลผ่านรูจมูก",
    "inhalation and exhalation": "การหายใจเข้าและการหายใจออก",
    "nor the peity": "ไม่มีความศรัทธา",
    "and who are devoted to hearing and singing His glories": "และผู้ศรัทธาในการฟังและการร้องพระเกียรติของพระองค์",
    "in a learned and humble": "ในผู้เรียนรู้และถ่อมตน",
    "which is experienced in self-realisation": "ซึ่งประสบในการตระหนักตน",
    "this is My": "นี่คือของข้าพเจ้า",
    "loss for him he is not denied the chance of the fortune to see the Supersoul": "การสูญเสียสำหรับเขา เขาไม่ถูกปฏิเสธโอกาสโชคลาภที่จะเห็นวิญญาณสูงสุด",
    "and is also superior": "และยังเป็นเหนือกว่า",
    "at the top between the eyes centering the concentration": "ที่ด้านบนระหว่างดวงตา จัดศูนย์กลางสมาธิ",
    "in the next life i.e": "ในชาติหน้า คือ",
    "and a heart that is never discouraged": "และหัวใจที่ไม่เคยท้อแท้",
    "and with heart": "และด้วยหัวใจ",
    "at the overeater": "สำหรับผู้กินมากเกินไป",
    "transcendental to the senses": "เหนือประสาทสัมผัส",
    "yet is not diligent": "แต่ไม่ขยัน",
    "powerful uncontrollable by even the intelligence": "ทรงพลัง ไม่สามารถควบคุมได้โดยแม้ปัญญา",
    "is the friend": "คือเพื่อน",
    "renders service to Me by engaging in the devotional practices based on hearing and chanting My glories": "ให้บริการข้าพเจ้าโดยมีส่วนร่วมในการปฏิบัติศรัทธาขึ้นอยู่กับฟังและสวดพระเกียรติของข้าพเจ้า",
    "he is born": "เขาเกิด",
    "by contact with the divine": "โดยการสัมผัสกับศักดิ์สิทธิ์",
    "on the path of attaining the Absolute": "บนเส้นทางบรรลุสัมบูรณ์",
    "By means of the intelligence": "โดยวิธีการของปัญญา",
    "and extremely difficult to control": "และยากอย่างยิ่งที่จะควบคุม",
    "a dispeller of suffering": "ผู้ขจัดความทุกข์",
    "state within which all association with unhappiness is severed": "สถานะภายในซึ่งความสัมพันธ์ทั้งหมดกับความทุกข์ถูกตัดขาด",
    "is difficult to attain": "ยากที่จะบรรลุ",
    "for the oversleeper": "สำหรับผู้นอนมากเกินไป",
    "in the home": "ในบ้าน",
    "it is controlled": "มันถูกควบคุม",
    "the group of senses": "กลุ่มประสาทสัมผัส",
    "what is the fate of": "ชะตากรรมคืออะไรของ",
    "as the means": "เป็นวิธีการ",
    "absorbed in thought of Me": "ดูดซับในความคิดของข้าพเจ้า",
    "fully dedicated to Me": "อุทิศอย่างเต็มที่ต่อข้าพเจ้า",
    "devoted to Me": "อุทิศต่อข้าพเจ้า",
    "and there is no": "และไม่มี",
    "is not to be found": "ไม่พบ",
    "one is not disturbed": "หนึ่งไม่ถูกรบกวน",
    "is the best": "คือดีที่สุด",
}


def translate_entry(english: str, transliteration: str) -> Dict[str, Any]:
    """Translate an English entry to Thai."""
    
    # First check for exact phrase match
    if english in PHRASE_TRANSLATIONS:
        return {
            "th": {
                "meaning": PHRASE_TRANSLATIONS[english],
                "approved": False
            }
        }
    
    # Check for case-insensitive match
    for phrase, translation in PHRASE_TRANSLATIONS.items():
        if english.lower() == phrase.lower():
            return {
                "th": {
                    "meaning": translation,
                    "approved": False
                }
            }
    
    # Word-by-word translation for unmatched entries
    words = english.split()
    translated_words = []
    
    for word in words:
        # Preserve capitalization
        is_capitalized = word[0].isupper() if word else False
        clean_word = word.lower().strip('(),.!?;:"\'')
        
        if clean_word in THAI_VOCABULARY:
            translation = THAI_VOCABULARY[clean_word]
            if translation:  # Skip empty translations (like "the")
                translated_words.append(translation)
        else:
            # Keep transliteration for proper nouns
            translated_words.append(word)
    
    thai_meaning = ' '.join(translated_words)
    
    # Clean up extra spaces
    thai_meaning = ' '.join(thai_meaning.split())
    
    return {
        "th": {
            "meaning": thai_meaning,
            "approved": False
        }
    }


def translate_vocabulary_batch(input_path: str, output_path: str, languages: list) -> Dict:
    """
    Translate vocabulary batch from English to target languages.
    
    Args:
        input_path: Path to input JSON file
        output_path: Path to output JSON file
        languages: List of target language codes
    
    Returns:
        Translation statistics
    """
    # Read input file
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    entries = data.get('entries', {})
    total_entries = len(entries)
    
    print(f"Translating {total_entries} entries to {languages}...")
    
    # Translate all entries
    translations = {}
    translated_count = 0
    
    for entry_id, entry_data in entries.items():
        english = entry_data.get('english', '')
        transliteration = entry_data.get('transliteration', '')
        
        # Translate to each target language
        entry_translations = {}
        for lang in languages:
            if lang == 'th':
                entry_translations['th'] = translate_entry(english, transliteration)['th']
        
        translations[entry_id] = entry_translations
        translated_count += 1
        
        if translated_count % 50 == 0:
            print(f"  Progress: {translated_count}/{total_entries} entries")
    
    # Create output structure
    output_data = {
        "meta": {
            "source": "vocabulary-th",
            "generated": datetime.now().isoformat(),
            "languages": languages,
            "approved": False
        },
        "translations": translations
    }
    
    # Write output file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"Translation complete! Output saved to: {output_path}")
    
    return {
        "total": total_entries,
        "translated": translated_count,
        "languages": languages,
        "output": output_path
    }


def main():
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python translate_vocab_thai_batch.py <input> <output> --languages=<lang1,lang2,...>")
        print("Example: python translate_vocab_thai_batch.py input.json output.json --languages=th")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    # Parse languages argument
    languages = []
    for arg in sys.argv[3:]:
        if arg.startswith('--languages='):
            languages = arg.split('=')[1].split(',')
    
    if not languages:
        print("Error: --languages parameter is required")
        sys.exit(1)
    
    # Run translation
    result = translate_vocabulary_batch(input_path, output_path, languages)
    
    print(f"\nSummary:")
    print(f"  Total entries: {result['total']}")
    print(f"  Translated: {result['translated']}")
    print(f"  Languages: {', '.join(result['languages'])}")


if __name__ == '__main__':
    main()
