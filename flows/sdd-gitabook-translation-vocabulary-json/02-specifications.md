# Specifications: Gitabook Translation Vocabulary JSON

> Version: 0.1 (Draft)
> Status: IN PROGRESS
> Last Updated: 2026-03-26
> Requirements: [01-requirements.md](01-requirements.md)

## Overview

Конвертация vocabulary из legacy CSV в отдельные JSON файлы для каждой главы с добавлением переводов на 5 азиатских языков.

## Affected Systems

| System | Impact | Notes |
|--------|--------|-------|
| `/legacy/csv/books/Gita_Vocabularies.csv` | Read | Источник данных |
| `/data/vocabulary/` | Create | 18 JSON файлов (vocab_01.json - vocab_18.json) |
| `/data/schema/vocabulary.schema.json` | Create | JSON Schema для валидации |

## Architecture

### File Structure

```
data/
├── schema/
│   ├── chapter.schema.json           # Chapter JSON Schema
│   └── vocabulary.schema.json        # Vocabulary JSON Schema
├── chapters/
│   ├── chapter-01.json               # Main chapter (RU/EN/DE/ES only)
│   ├── chapter-01-asian-translations.json  # Asian translations (ko/th/zh/ja)
│   ├── chapter-02.json
│   ├── chapter-02-asian-translations.json
│   └── ...
└── vocabulary/
    ├── vocab_01.json                 # Chapter 1 vocabulary (all languages)
    ├── vocab_02.json                 # Chapter 2 vocabulary (all languages)
    └── ...
```

### Separation of Concerns

**chapter-XX.json** (Main file):
- Contains: Sanskrit, transliteration, RU/EN/DE/ES translations, vocabulary (RU/EN only)
- Purpose: Primary source, stable, reviewed translations
- Updated: During CSV conversion phase

**chapter-XX-asian-translations.json** (Translation overlay):
- Contains: ONLY ko, th, zh-CN, zh-TW, ja translations
- Purpose: Separate layer for Asian translations
- Updated: During translation phase
- **Does NOT modify original chapter-XX.json**

**vocab_XX.json** (Vocabulary):
- Contains: All vocabulary for chapter with all languages
- Purpose: Word-by-word study
- Updated: During vocabulary translation phase

### Data Flow

```
Phase 1: Conversion
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Gita_Slokas.csv │────►│  Python Script   │────►│ chapter-XX.json  │
│  Gita_Vocab.csv  │     │  (convert.py)    │     │ vocab_XX.json    │
└──────────────────┘     └──────────────────┘     └──────────────────┘

Phase 2: Translation (Combined Chapter + Vocabulary)
┌──────────────────────────────────────┐     ┌──────────────────┐
│  chapter-XX.json + vocab_XX.json     │────►│  Claude Dialog   │
│  (combined in single context)        │     │  (translate)     │
└──────────────────────────────────────┘     └──────────────────┘
                                                   │
                                                   ▼
                                          ┌──────────────────┐
                                          │ chapter-XX-asian-│
                                          │ translations.json│
                                          │ + vocab_XX.json  │
                                          │ (with new langs) │
                                          └──────────────────┘
```

### Combined Translation Context

For efficient translation, each chapter batch includes:

```
═══════════════════════════════════════════════════════════════
CHAPTER {N} TRANSLATION BATCH
═══════════════════════════════════════════════════════════════

Part 1: Chapter Title & Slokas (~30-75 slokas)
──────────────────────────────────────────────
[Chapter title in RU/EN/DE/ES]
[Sloka 1: RU/EN/DE/ES + Sanskrit]
[Sloka 2: RU/EN/DE/ES + Sanskrit]
...

Part 2: Vocabulary for Chapter {N} (~50-150 words)
──────────────────────────────────────────────
[Word 1: дхр̣тара̄ш̣т̣рах̣ ува̄ча → "Дхр̣тара̄ш̣т̣ра сказал"]
[Word 2: дхарма-кш̣етре → "на священной земле Курукш̣етры"]
...

TASK: Translate ALL to ko, th, zh-CN, zh-TW, ja
Use RU/EN for meaning. Sanskrit for term accuracy.
```

**Benefits:**
1. **Context consistency**: Translator sees both slokas and vocabulary together
2. **Terminology consistency**: Same terms translated identically in slokas and vocabulary
3. **Efficiency**: Single API call per chapter instead of two separate batches
4. **Quality**: Vocabulary translations match sloka translations

## JSON Structure

### Vocabulary File Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "vocabulary.schema.json",
  "title": "Bhagavad Gita Vocabulary",
  "type": "object",
  "required": ["chapter", "vocabulary"],
  "properties": {
    "chapter": {
      "type": "integer",
      "minimum": 1,
      "maximum": 18
    },
    "meta": {
      "type": "object",
      "properties": {
        "totalWords": { "type": "integer" },
        "lastUpdated": { "type": "string", "format": "date-time" },
        "version": { "type": "string" },
        "source": { "type": "string", "const": "SM/SCSM/ШМ/ШЧСМ" },
        "sources": {
          "type": "object",
          "properties": {
            "russian": { "type": "string" },
            "english": { "type": "string" }
          }
        }
      }
    },
    "vocabulary": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/vocabularyEntry"
      }
    }
  },
  "$defs": {
    "vocabularyEntry": {
      "type": "object",
      "required": ["id", "slokaId", "word", "transliteration", "meaning"],
      "properties": {
        "id": { "type": "integer" },
        "slokaId": { "type": "integer" },
        "word": { "type": "string", "description": "Sanskrit word (Cyrillic or IAST)" },
        "transliteration": {
          "type": "object",
          "required": ["cyrillic", "iast"],
          "properties": {
            "cyrillic": { "type": "string" },
            "iast": { "type": "string" },
            "th": { "type": "string", "description": "Thai transliteration" },
            "zh-CN": { "type": "string", "description": "Chinese Pinyin" },
            "zh-TW": { "type": "string", "description": "Chinese Pinyin (Traditional)" },
            "ko": { "type": "string", "description": "Korean Hangul transliteration" },
            "ja": { "type": "string", "description": "Japanese Romaji/Kana" }
          }
        },
        "meaning": {
          "type": "object",
          "required": ["ru"],
          "properties": {
            "ru": { "$ref": "#/$defs/translation" },
            "en": { "$ref": "#/$defs/translation" },
            "th": { "$ref": "#/$defs/translation" },
            "zh-CN": { "$ref": "#/$defs/translation" },
            "zh-TW": { "$ref": "#/$defs/translation" },
            "ko": { "$ref": "#/$defs/translation" },
            "ja": { "$ref": "#/$defs/translation" }
          }
        },
        "order": { "type": "integer" }
      }
    },
    "translation": {
      "type": "object",
      "required": ["text", "approved"],
      "properties": {
        "text": { "type": "string" },
        "approved": { "type": "boolean", "default": false }
      }
    }
  }
}
```

### Example Vocabulary Entry

```json
{
  "id": 1,
  "slokaId": 1,
  "word": "дхр̣тара̄ш̣т̣рах̣ ува̄ча",
  "transliteration": "dhṛtarāṣṭraḥ uvāca",
  "meaning": {
    "ru": {
      "text": "Дхр̣тара̄ш̣т̣ра сказал",
      "approved": true
    },
    "en": {
      "text": "Dhritarashtra said",
      "approved": true
    },
    "th": {
      "text": "ธฤตราษฏระกล่าว",
      "approved": false
    },
    "zh-CN": {
      "text": "持国说",
      "approved": false
    },
    "zh-TW": {
      "text": "持國說",
      "approved": false
    },
    "ko": {
      "text": "드리타라슈트라가 말했다",
      "approved": false
    },
    "ja": {
      "text": "ドリタラシュトラが言った",
      "approved": false
    }
  },
  "order": 1
}
```

## Conversion Logic

```python
# Псевдокод конвертации
def convert_vocabulary():
    # 1. Загрузить CSV
    vocab_data = load_csv('Gita_Vocabularies.csv', delimiter=';')
    
    # 2. Сгруппировать по главам
    # Нужно загрузить slokas чтобы определить chapter для каждого slokaId
    slokas = load_csv('Gita_Slokas.csv', delimiter=';')
    sloka_to_chapter = {s['Id']: s['ChapterId'] for s in slokas}
    
    # 3. Для каждой главы 1-18
    for chapter_num in range(1, 19):
        vocab_entry = {
            "chapter": chapter_num,
            "meta": {
                "totalWords": 0,
                "lastUpdated": datetime.now().isoformat(),
                "version": "1.0",
                "source": "SM/SCSM/ШМ/ШЧСМ"
            },
            "vocabulary": []
        }
        
        # 4. Фильтр vocabulary для этой главы
        chapter_vocab = [
            v for v in vocab_data 
            if sloka_to_chapter.get(v['SlokaId']) == chapter_num
        ]
        
        for v in chapter_vocab:
            # 5. Перевести meaning на 5 языков
            translations = translate_meaning(v['Translation'])
            
            vocab_entry["vocabulary"].append({
                "id": v['Id'],
                "slokaId": v['SlokaId'],
                "word": v['Text'],  # Сохраняем legacy формат (кириллица)
                "transliteration": convert_to_iast(v['Text']),
                "meaning": {
                    "ru": {"text": v['Translation'], "approved": True},
                    "en": {"text": translations['en'], "approved": True},
                    "th": {"text": translations['th'], "approved": False},
                    "zh-CN": {"text": translations['zh-CN'], "approved": False},
                    "zh-TW": {"text": translations['zh-TW'], "approved": False},
                    "ko": {"text": translations['ko'], "approved": False},
                    "ja": {"text": translations['ja'], "approved": False}
                },
                "order": extract_order(v)
            })
        
        # 6. Сохранить JSON
        save_json(f'vocab_{chapter_num:02d}.json', vocab_entry)
```

## Translation Process Specification

### Input Format for Translation

```
═══════════════════════════════════════════════════════════════
VOCABULARY TRANSLATION BATCH - CHAPTER {N}
═══════════════════════════════════════════════════════════════

═══ SOURCE PRIORITY ═══

[RU] {russian_meaning}  ← PRIMARY

[EN] {english_meaning}  ← SECONDARY

[DE] {german_meaning}   ← CONTEXT (if available)

[ES] {spanish_meaning}  ← CONTEXT (if available)

═══ SANSKRIT REFERENCE ═══

Word: {cyrillic_transliteration}
IAST: {iast_transliteration}

───────────────────────────────────────────────────────────────
TASK: Translate meaning to th, zh-CN, zh-TW, ko, ja
Use RU/EN for meaning. Sanskrit for term accuracy only.
───────────────────────────────────────────────────────────────
```

### Output Format

```json
{
  "th": "ความหมายภาษาไทย...",
  "zh-CN": "中文含义...",
  "zh-TW": "中文含義...",
  "ko": "한국어 의미...",
  "ja": "日本語の意味..."
}
```

## Edge Cases

| Case | Trigger | Handling |
|------|---------|----------|
| Compound words | Word contains hyphen/space | Translate as single unit |
| Multi-word entries | "дхр̣тара̄ш̣т̣рах̣ ува̄ча" | Translate complete phrase |
| Missing English | No EN translation in source | Use RU only |
| Ambiguous meaning | Multiple possible translations | Use context from parent sloka |

## Error Handling

| Error | Cause | Response |
|-------|-------|----------|
| Invalid UTF-8 | Corrupted CSV | Skip row, log warning |
| Missing SlokaId | Orphan vocabulary | Skip row, log error |
| Translation fail | API timeout | Retry 3 times, then skip |
| JSON validation fail | Schema mismatch | Fix and re-validate |

## Testing Strategy

### Validation Tests

- [ ] All 18 vocabulary JSON files created
- [ ] Each file passes JSON Schema validation
- [ ] Total word count matches source CSV
- [ ] All 5 target languages present in each entry
- [ ] Transliteration preserved in legacy format

### Manual Verification

- [ ] Spot-check 5 random words per chapter
- [ ] Verify translation quality for each language
- [ ] Validate Sanskrit term accuracy

## Dependencies

### Requires
- Python 3.8+ with `json`, `csv` modules
- Source CSV files in `/legacy/csv/books/`
- Translation API (Claude)

### Blocks
- Mobile app vocabulary display
- Multi-language word-by-word study feature

## Migration / Rollout

### Phase 1: Conversion
1. Run conversion script
2. Validate all 18 JSON files
3. Commit to repository

### Phase 2: Translation (per chapter)
1. Load chapter vocabulary JSON
2. Generate translation prompts
3. Execute translations
4. Update JSON with new translations (`approved: false`)
5. Commit updated JSON

---

## Approval

- [ ] Reviewed by: User
- [ ] Approved on: [DATE]
- [ ] Notes: [NOTES]
