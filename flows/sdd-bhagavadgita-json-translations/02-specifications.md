# Specifications: Bhagavad Gita JSON Translations

> Version: 1.1
> Status: APPROVED
> Last Updated: 2026-03-26
> Requirements: [01-requirements.md](01-requirements.md)

## Overview

Конвертация CSV данных Бхагавад-гиты в структурированные JSON файлы по главам с последующим добавлением переводов на азиатские языки.

## Affected Systems

| System | Impact | Notes |
|--------|--------|-------|
| `/legacy/csv/Books/` | Read | Источник данных |
| `/data/chapters/` | Create | 18 JSON файлов |
| `/data/schema/` | Create | JSON Schema для валидации |

## Architecture

### File Structure

```
data/
├── schema/
│   └── chapter.schema.json      # JSON Schema
├── chapters/
│   ├── chapter-01.json
│   ├── chapter-02.json
│   ├── ...
│   └── chapter-18.json
└── meta/
    └── languages.json           # Метаданные языков
```

### Data Flow

```
Phase 1: Conversion
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Gita_Slokas.csv │────►│  Python Script   │────►│ chapter-XX.json  │
│  Vocabularies.csv│     │  (convert.py)    │     │  (18 files)      │
│  db_chapters.csv │     └──────────────────┘     └──────────────────┘
└──────────────────┘

Phase 2: Translation
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ chapter-XX.json  │────►│  Claude Dialog   │────►│ chapter-XX.json  │
│  (existing)      │     │  (manual)        │     │  (+ new langs)   │
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

## JSON Schema

### Chapter Schema (`chapter.schema.json`)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "chapter.schema.json",
  "title": "Bhagavad Gita Chapter",
  "type": "object",
  "required": ["chapter", "title", "slokas"],
  "properties": {
    "chapter": {
      "type": "integer",
      "minimum": 1,
      "maximum": 18
    },
    "title": {
      "$ref": "#/$defs/multilingualText"
    },
    "slokas": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/sloka"
      }
    },
    "meta": {
      "type": "object",
      "properties": {
        "totalSlokas": { "type": "integer" },
        "lastUpdated": { "type": "string", "format": "date-time" },
        "version": { "type": "string" }
      }
    }
  },
  "$defs": {
    "translatedText": {
      "type": "object",
      "required": ["text", "approved"],
      "properties": {
        "text": { "type": "string" },
        "approved": { "type": "boolean" }
      }
    },
    "multilingualText": {
      "type": "object",
      "properties": {
        "sanskrit": { "type": "string" },
        "transliteration": { "type": "string" },
        "ru": { "$ref": "#/$defs/translatedText" },
        "en": { "$ref": "#/$defs/translatedText" },
        "de": { "$ref": "#/$defs/translatedText" },
        "es": { "$ref": "#/$defs/translatedText" },
        "ko": { "$ref": "#/$defs/translatedText" },
        "th": { "$ref": "#/$defs/translatedText" },
        "zh-CN": { "$ref": "#/$defs/translatedText" },
        "zh-TW": { "$ref": "#/$defs/translatedText" }
      },
      "additionalProperties": {
        "$ref": "#/$defs/translatedText"
      }
    },
    "vocabularyItem": {
      "type": "object",
      "required": ["word", "transliteration", "meaning"],
      "properties": {
        "word": { "type": "string" },
        "transliteration": { "type": "string" },
        "meaning": { "$ref": "#/$defs/multilingualText" },
        "order": { "type": "integer" }
      }
    },
    "sloka": {
      "type": "object",
      "required": ["number", "order", "sanskrit", "transliteration", "translations"],
      "properties": {
        "number": {
          "type": "string",
          "pattern": "^\\d+\\.\\d+(-\\d+)?$"
        },
        "order": { "type": "integer" },
        "sanskrit": { "type": "string" },
        "transliteration": { "type": "string" },
        "translations": { "$ref": "#/$defs/multilingualText" },
        "comment": { "$ref": "#/$defs/multilingualText" },
        "vocabulary": {
          "type": "array",
          "items": { "$ref": "#/$defs/vocabularyItem" }
        },
        "audio": {
          "type": "object",
          "properties": {
            "recitation": { "type": "string" },
            "sanskrit": { "type": "string" }
          }
        }
      }
    }
  }
}
```

### Example Chapter JSON

```json
{
  "chapter": 1,
  "title": {
    "sanskrit": "अर्जुनविषादयोग",
    "transliteration": "arjuna-viṣāda-yoga",
    "ru": { "text": "Скорбь Арджуны", "approved": true },
    "en": { "text": "Arjuna's Grief", "approved": true },
    "de": { "text": "Arjunas Kummer", "approved": true },
    "es": { "text": "La aflicción de Arjuna", "approved": true },
    "ko": { "text": "아르주나의 슬픔", "approved": false },
    "th": { "text": "ความทุกข์ของอรชุน", "approved": false },
    "zh-CN": { "text": "阿周那的悲伤", "approved": false },
    "zh-TW": { "text": "阿周那的悲傷", "approved": false }
  },
  "meta": {
    "totalSlokas": 37,
    "lastUpdated": "2026-03-26T12:00:00Z",
    "version": "1.0"
  },
  "slokas": [
    {
      "number": "1.1",
      "order": 1,
      "sanskrit": "धृतराष्ट्र उवाच ।\nधर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः ।\nमामकाः पाण्डवाश्चैव किमकुर्वत सञ्जय ॥१॥",
      "transliteration": "dhṛtarāṣṭra uvāca\ndharma-kṣetre kuru-kṣetre samavetā yuyutsavaḥ\nmāmakāḥ pāṇḍavāś caiva kim akurvata sañjaya",
      "translations": {
        "ru": {
          "text": "Дхритараштра сказал: Санджая! Что произошло, когда мои сыновья и сыновья Панду сошлись для битвы на священной земле Курукшетры?",
          "approved": true
        },
        "en": {
          "text": "Dhritarashtra said: O Sanjaya, what happened when my sons and the sons of Pandu assembled on the sacred field of Kurukshetra, eager to fight?",
          "approved": true
        }
      },
      "comment": {
        "ru": {
          "text": "Комментарий к шлоке...",
          "approved": true
        }
      },
      "vocabulary": [
        {
          "word": "धृतराष्ट्र",
          "transliteration": "dhṛtarāṣṭra",
          "meaning": {
            "ru": { "text": "Дхритараштра (имя царя)", "approved": true }
          },
          "order": 1
        },
        {
          "word": "उवाच",
          "transliteration": "uvāca",
          "meaning": {
            "ru": { "text": "сказал", "approved": true }
          },
          "order": 2
        }
      ],
      "audio": {
        "recitation": "/Files/76f01c2e659c424aa116a22f54800028.mp3",
        "sanskrit": "/Files/3b9b7603ba184a65836fd841bee30f8e.mp3"
      }
    }
  ]
}
```

## Conversion Script Specification

### Input Files

| File | Delimiter | Encoding | Key Fields |
|------|-----------|----------|------------|
| `Gita_Slokas.csv` | `;` | UTF-8-BOM | Id, ChapterId, Name, Text, Transcription, Translation, Comment, Order, Audio, AudioSanskrit |
| `Gita_Vocabularies.csv` | `;` | UTF-8-BOM | Id, SlokaId, Text, Translation |
| `db_chapters.csv` | `,` | UTF-8-BOM | Id, BookId, Name, Order |
| `db_books.csv` | `,` | UTF-8-BOM | Id, LanguageId, Name, Initials |

### Conversion Logic

```python
# Псевдокод
def convert():
    # 1. Загрузить метаданные
    books = load_csv('db_books.csv')
    chapters = load_csv('db_chapters.csv')

    # 2. Фильтр: только книги SM/ШМ (Шридхар Махарадж)
    SM_BOOK_IDS = [1, 2, 11, 14]  # ru, en, de, es
    sm_books = filter(books, id in SM_BOOK_IDS)

    # 3. Определить "базовую" книгу (BookId=1, русский)
    base_book_id = 1
    base_chapters = filter(chapters, book_id=base_book_id)

    # 3. Для каждой главы 1-18
    for chapter_order in range(1, 19):
        chapter_data = {
            "chapter": chapter_order,
            "title": build_multilingual_title(chapter_order),
            "slokas": [],
            "meta": {...}
        }

        # 4. Загрузить шлоки для этой главы
        chapter_id = get_chapter_id(base_book_id, chapter_order)
        slokas = filter(all_slokas, chapter_id=chapter_id)

        for sloka in slokas:
            # 5. Собрать переводы из других книг
            translations = collect_translations(sloka.number, all_books)

            # 6. Загрузить vocabulary
            vocabulary = filter(all_vocab, sloka_id=sloka.id)

            chapter_data["slokas"].append({
                "number": sloka.name,
                "order": sloka.order,
                "sanskrit": sloka.text,
                "transliteration": sloka.transcription,
                "translations": translations,
                "comment": {...},
                "vocabulary": vocabulary,
                "audio": {...}
            })

        # 7. Сохранить JSON
        save_json(f"chapter-{chapter_order:02d}.json", chapter_data)
```

### Language Mapping

**В скоупе только автор SM/ШМ (Шридхар Махарадж):**

| BookId | LanguageId | Language Code | Initials | In Scope |
|--------|------------|---------------|----------|----------|
| 1 | 2 | ru | ШМ | YES |
| 2 | 1 | en | SM | YES |
| 11 | 3 | de | SM | YES |
| 14 | 5 | es | SM | YES |
| 5 | 1 | en | VC | NO (другой автор) |
| 8 | 1 | en | SP | NO (другой автор) |

**SM = SCSM = ШМ = ШЧСМ** — Sri Chaitanya Saraswat Math / Шри Чайтанья Сарасват Матх

Одна книга в 4 переводах на разные языки.

## Translation Process Specification

### Input Format for Claude

```
═══════════════════════════════════════════════════════════════
ГЛАВА {N}, ШЛОКА {number}
═══════════════════════════════════════════════════════════════

═══ ОСНОВНЫЕ ИСТОЧНИКИ СМЫСЛА ═══

[RU] {russian_translation}

[EN] {english_translation}

═══ ДОПОЛНИТЕЛЬНЫЙ КОНТЕКСТ ═══

[DE] {german_translation}

[ES] {spanish_translation}

═══ САНСКРИТ (только для уточнения терминов) ═══

Деванагари: {sanskrit_text}
Транслитерация: {transliteration}

───────────────────────────────────────────────────────────────
ЗАДАНИЕ: Переведи на ko, th, zh-CN, zh-TW
Смысл бери из RU/EN. Санскрит — только для точности терминов.
───────────────────────────────────────────────────────────────
```

### Output Format from Claude

```json
{
  "ko": "드리타라슈트라가 말했다: 오 산자야, 쿠루크셰트라의 성스러운 전장에서...",
  "th": "ธฤตราษฏร์กล่าวว่า: โอ้ สัญชัย เมื่อลูกชายของข้าและลูกชายของปาณฑุ...",
  "zh-CN": "持国王说：桑伽耶啊，当我的儿子们和般度的儿子们聚集在俱卢之野...",
  "zh-TW": "持國王說：桑伽耶啊，當我的兒子們和般度的兒子們聚集在俱盧之野..."
}
```

### Batch Size

- **Per request:** 1 глава (~30-75 шлок)
- **Total requests:** 18 (по одному на главу)
- **Languages per request:** 4 (ko, th, zh-CN, zh-TW)

## Edge Cases

| Case | Trigger | Handling |
|------|---------|----------|
| Multiline Sanskrit | Text contains `\n` | Preserve newlines in JSON |
| Missing translation | NULL in CSV | Omit language from translations object |
| Compound verse numbers | "1.4-6" | Store as string, not parsed |
| Empty comment | NULL or empty | Omit comment field |
| Special characters | Diacritics in transliteration | UTF-8 encoding |
| German multiline chapters | Chapter names with newlines | Clean/normalize |

## Error Handling

| Error | Cause | Response |
|-------|-------|----------|
| Invalid UTF-8 | Corrupted CSV | Skip row, log warning |
| Missing ChapterId | Orphan sloka | Skip row, log error |
| Duplicate sloka number | Data inconsistency | Use first occurrence |
| JSON validation fail | Schema mismatch | Fix and re-validate |

## Testing Strategy

### Validation Tests

- [ ] All 18 JSON files created
- [ ] Each file passes JSON Schema validation
- [ ] Total sloka count matches source (~663)
- [ ] All existing translations preserved
- [ ] Audio paths correct format

### Manual Verification

- [ ] Spot-check 3 random slokas per chapter
- [ ] Verify Sanskrit rendering in browser
- [ ] Check vocabulary order matches source
- [ ] Validate multilingual display

## Dependencies

### Requires
- Python 3.8+ with `json`, `csv` modules
- Source CSV files in `/legacy/csv/Books/`

### Blocks
- Mobile app JSON loading
- Translation workflow

## Migration / Rollout

### Phase 1: Conversion
1. Run conversion script
2. Validate all 18 JSON files
3. Commit to repository

### Phase 2: Translation (Automated)
1. Command: `/translate.sanscrit [output_file]`
2. Agent extracts chapter data (slokas + vocabulary)
3. Agent translates to ko, th, zh-CN, zh-TW, ja
4. Agent adds transliteration (th, zh, ko, ja scripts)
5. Agent saves result immediately
6. Continue to next chapter after successful save

---

## Automated Translation Command

**Command**: `/translate.sanscrit [output_file_path]`

See: `.qwen/commands/translate.sanscrit.md` for full documentation.

**Sequential Execution**:
- Chapter N+1 waits for Chapter N to complete
- Results saved before next agent starts
- No manual intervention required

---

## Approval

- [x] Reviewed by: User
- [x] Approved on: 2026-03-26
- [x] Notes: Только книги SM/SCSM/ШМ/ШЧСМ (BookId: 1, 2, 11, 14). Automated translation via /translate.sanscrit command.
