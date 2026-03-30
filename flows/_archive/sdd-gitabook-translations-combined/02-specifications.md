# Specifications: Gitabook Translations Combined

> Version: 1.0
> Status: APPROVED
> Last Updated: 2026-03-27
> Requirements: [01-requirements.md](01-requirements.md)

## Overview

Объединённая спецификация для перевода глав и vocabulary Бхагавад-гиты на расширенный список языков с оптимизированной структурой папок.

## Translation Scope

### What Gets Translated

| Component | Description | Example |
|-----------|-------------|---------|
| **Chapter title** | Название главы | "Скорбь Арджуны" → "아르주나의 슬픔" |
| **Sloka text** | Перевод шлоки | Основной текст стиха |
| **Comment** | Комментарий духовного учителя | Пояснения Шридхара Махараджа |
| **Vocabulary meaning** | Значение санскритского слова | "сказал", "священная земля" |
| **Vocabulary transliteration** | Фонетическая транскрипция на языке перевода | dhṛtarāṣṭra → 드리타라슈트라 (ko) |

### Transliteration Rules

Санскритские слова транскрибируются на письмо целевого языка:

| Language | Script | Example: dhṛtarāṣṭra |
|----------|--------|---------------------|
| th (Thai) | Thai script | ธฤตราษฏร |
| zh-TW (Chinese) | Hanzi + Pinyin | 德瑞塔拉什特拉 (Dé ruì tǎ lā shí tè lā) |
| ja (Japanese) | Katakana | ドゥリタラーシュトラ |
| ko (Korean) | Hangul | 드리타라슈트라 |
| he (Hebrew) | Hebrew script | דְּרִיטַרָאשְׁטְרַה |
| ar (Arabic) | Arabic script | دريتاراشترا |
| tr (Turkish) | Latin | Dhritaraştra |
| sw (Swahili) | Latin | Dhritarashtra |

**Важно**: Транскрипция должна отражать правильное произношение санскритского слова на целевом языке, а не просто латинскую транслитерацию.

## Affected Systems

| System | Impact | Notes |
|--------|--------|-------|
| `data/chapters/original/` | Read | Источник глав (18 JSON) |
| `data/vocabulary/original/` | Read | Источник vocabulary (18 JSON) |
| `data/chapters/` | Restructure | Новая структура по главам |
| `data/translations/` | Delete | Удалить (временные промпты) |

## Architecture

### Final Folder Structure

```
data/
├── schema/
│   ├── chapter.schema.json
│   └── vocabulary.schema.json
├── meta/
│   └── languages.json
└── chapters/
    ├── ch-01/
    │   ├── chapter-source.json      # RU/EN/DE/ES slokas + comments
    │   ├── vocabulary-source.json   # RU/EN vocabulary
    │   ├── chapter-asian.json       # th, zh-TW, ja, ko (slokas + comments)
    │   ├── chapter-other.json       # he, ar, tr, sw (slokas + comments)
    │   ├── vocabulary-asian.json    # th, zh-TW, ja, ko (meanings + transliterations)
    │   └── vocabulary-other.json    # he, ar, tr, sw (meanings + transliterations)
    ├── ch-02/
    │   └── ...
    └── ch-18/
        └── ...
```

### File Contents

#### chapter-source.json (Read-only)

```json
{
  "chapter": 1,
  "title": {
    "sanskrit": "अर्जुनविषादयोग",
    "transliteration": "arjuna-viṣāda-yoga",
    "ru": "Скорбь Арджуны",
    "en": "Arjuna's Grief",
    "de": "Arjunas Kummer",
    "es": "La aflicción de Arjuna"
  },
  "meta": {
    "totalSlokas": 37,
    "version": "1.0"
  },
  "slokas": [
    {
      "number": "1.1",
      "order": 1,
      "sanskrit": "धृतराष्ट्र उवाच...",
      "transliteration": "dhṛtarāṣṭra uvāca...",
      "translations": {
        "ru": { "text": "...", "approved": true },
        "en": { "text": "...", "approved": true }
      },
      "comment": {
        "ru": { "text": "...", "approved": true },
        "en": { "text": "...", "approved": true }
      }
    }
  ]
}
```

#### vocabulary-source.json (Per chapter)

```json
{
  "chapter": 1,
  "meta": {
    "totalWords": 498,
    "sources": {
      "ru": "BookId 1 (ШМ)",
      "en": "BookId 2 (SM)"
    }
  },
  "vocabulary": [
    {
      "id": 1,
      "slokaNumber": "1.1",
      "word": "धृतराष्ट्र",
      "transliteration": {
        "cyrillic": "дхр̣тара̄ш̣т̣ра",
        "iast": "dhṛtarāṣṭra"
      },
      "meaning": {
        "ru": { "text": "Дхритараштра", "approved": true },
        "en": { "text": "Dhritarashtra", "approved": true }
      }
    }
  ]
}
```

#### chapter-asian.json

```json
{
  "chapter": 1,
  "generated": "2026-03-27T12:00:00Z",
  "command": "/translate.sanscrit",
  "title": {
    "th": "ความทุกข์ของอรชุน",
    "zh-TW": "阿周那的悲傷",
    "ja": "アルジュナの悲嘆",
    "ko": "아르주나의 슬픔"
  },
  "slokas": [
    {
      "number": "1.1",
      "translations": {
        "th": { "text": "...", "approved": false },
        "zh-TW": { "text": "...", "approved": false },
        "ja": { "text": "...", "approved": false },
        "ko": { "text": "...", "approved": false }
      },
      "comment": {
        "th": { "text": "...", "approved": false },
        "zh-TW": { "text": "...", "approved": false },
        "ja": { "text": "...", "approved": false },
        "ko": { "text": "...", "approved": false }
      }
    }
  ]
}
```

#### vocabulary-asian.json

```json
{
  "chapter": 1,
  "generated": "2026-03-27T12:00:00Z",
  "command": "/translate.sanscrit",
  "vocabulary": [
    {
      "slokaNumber": "1.1",
      "word": "dhṛtarāṣṭra",
      "meaning": {
        "th": { "text": "...", "approved": false },
        "zh-TW": { "text": "...", "approved": false },
        "ja": { "text": "...", "approved": false },
        "ko": { "text": "...", "approved": false }
      },
      "transliteration": {
        "th": "ทฤตราษฏระ",
        "zh-TW": "德瑞塔拉什特拉",
        "ja": "ドゥリタラーシュトラ",
        "ko": "드리타라슈트라"
      }
    }
  ]
}
```

#### chapter-other.json

```json
{
  "chapter": 1,
  "generated": "2026-03-27T12:00:00Z",
  "command": "/translate.sanscrit",
  "title": {
    "he": "צערו של ארג'ונה",
    "ar": "حزن أرجونا",
    "tr": "Arjuna'nın Kederi",
    "sw": "Huzuni ya Arjuna"
  },
  "slokas": [
    {
      "number": "1.1",
      "translations": {
        "he": { "text": "...", "approved": false },
        "ar": { "text": "...", "approved": false },
        "tr": { "text": "...", "approved": false },
        "sw": { "text": "...", "approved": false }
      },
      "comment": {
        "he": { "text": "...", "approved": false },
        "ar": { "text": "...", "approved": false },
        "tr": { "text": "...", "approved": false },
        "sw": { "text": "...", "approved": false }
      }
    }
  ]
}
```

#### vocabulary-other.json

```json
{
  "chapter": 1,
  "generated": "2026-03-27T12:00:00Z",
  "command": "/translate.sanscrit",
  "vocabulary": [
    {
      "slokaNumber": "1.1",
      "word": "dhṛtarāṣṭra",
      "meaning": {
        "he": { "text": "דְּרִיטַרָאשְׁטְרַה (שם המלך)", "approved": false },
        "ar": { "text": "دريتاراشترا (اسم الملك)", "approved": false },
        "tr": { "text": "Dhritaraştra (kralın adı)", "approved": false },
        "sw": { "text": "Dhritarashtra (jina la mfalme)", "approved": false }
      },
      "transliteration": {
        "he": "דְּרִיטַרָאשְׁטְרַה",
        "ar": "دريتاراشترا",
        "tr": "Dhritaraştra",
        "sw": "Dhritarashtra"
      }
    }
  ]
}
```

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     RESTRUCTURE PHASE                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  data/chapters/original/chapter-01.json ──► ch-01/chapter-source.json
│  data/vocabulary/original/vocab_01.json ──► ch-01/vocabulary-source.json
│                                                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     TRANSLATION PHASE                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ch-01/chapter-source.json    ──┐                           │
│  ch-01/vocabulary-source.json ──┼──► /translate.sanscrit    │
│                                 │           │                │
│                                 │           ▼                │
│                                 │    ┌──────────────┐        │
│                                 │    │   Claude     │        │
│                                 │    │  Translator  │        │
│                                 │    └──────┬───────┘        │
│                                 │           │                │
│                                 ▼           ▼                │
│                          ┌─────────────────────────┐         │
│                          │ ch-01/chapter-asian.json│         │
│                          │ ch-01/chapter-other.json│         │
│                          │ ch-01/vocabulary-asian.json       │
│                          │ ch-01/vocabulary-other.json       │
│                          └─────────────────────────┘         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Translation Command Specification

### Command: `/translate.sanscrit`

**Input**: Chapter directory path (e.g., `data/chapters/ch-01/`)

**Process**:
1. Read `source.json` and `vocabulary.json`
2. Format combined translation prompt
3. Translate to target languages
4. Save `translations-asian.json` and/or `translations-other.json`

### Translation Prompt Template

```
═══════════════════════════════════════════════════════════════
CHAPTER {N}: {TITLE}
Total: {X} slokas, {Y} vocabulary words
═══════════════════════════════════════════════════════════════

──────────────────────────────────────────────────────────────
SLOKA {number}
──────────────────────────────────────────────────────────────

═══ PRIMARY SOURCES (use for meaning) ═══

[RU] {russian_translation}

[EN] {english_translation}

═══ COMMENT (Spiritual Teacher's Commentary) ═══

[RU] {russian_comment}

[EN] {english_comment}

═══ ADDITIONAL CONTEXT ═══

[DE] {german_translation}

[ES] {spanish_translation}

═══ SANSKRIT (for terminology only) ═══

देवनागरी: {sanskrit}
IAST: {transliteration}

═══ VOCABULARY FOR THIS SLOKA ═══

1. {word_iast} ({word_cyrillic}) → RU: {meaning_ru} | EN: {meaning_en}
2. {word_iast} ({word_cyrillic}) → RU: {meaning_ru} | EN: {meaning_en}
...

──────────────────────────────────────────────────────────────

[REPEAT FOR ALL SLOKAS]

═══════════════════════════════════════════════════════════════
TASK: Translate to {target_languages}

1. SLOKA TEXT: Translate the verse meaning (use RU/EN as source)
2. COMMENT: Translate the spiritual teacher's commentary
3. VOCABULARY:
   - Translate meanings (use RU/EN as source)
   - Create phonetic transliteration in target script
     Example: dhṛtarāṣṭra → 드리타라슈트라 (Korean)
     Example: dhṛtarāṣṭra → ドゥリタラーシュトラ (Japanese)
     Example: dhṛtarāṣṭra → ธฤตราษฏร (Thai)

Sanskrit is ONLY for terminology accuracy, NOT for understanding meaning.
═══════════════════════════════════════════════════════════════
```

### Target Language Groups

**Asian (translations-asian.json)**:
- th (Thai) - ภาษาไทย
- zh-TW (Chinese Traditional) - 繁體中文
- ja (Japanese) - 日本語
- ko (Korean) - 한국어

**Other (translations-other.json)**:
- he (Hebrew) - עברית
- ar (Arabic) - العربية
- tr (Turkish) - Türkçe
- sw (Swahili) - Kiswahili

## Migration Steps

### Step 1: Create New Structure

```bash
# For each chapter 01-18
mkdir -p data/chapters/ch-{01..18}

# Copy source files
cp data/chapters/original/chapter-01.json data/chapters/ch-01/chapter-source.json
cp data/vocabulary/original/vocab_01.json data/chapters/ch-01/vocabulary-source.json
# ... repeat for all chapters
```

### Step 2: Merge Existing Translations

For chapters 1-6 that already have Asian translations:
- Extract ko, th, zh-TW from current chapter files
- Move to `chapter-asian.json`

### Step 3: Run Translation

```bash
# Asian languages - chapters (all chapters)
for ch in ch-{01..18}; do
  /translate.sanscrit data/chapters/$ch/chapter-source.json \
    data/chapters/$ch/chapter-asian.json --languages=th,zh-TW,ja,ko
done

# Asian languages - vocabulary (all chapters)
for ch in ch-{01..18}; do
  /translate.sanscrit data/chapters/$ch/vocabulary-source.json \
    data/chapters/$ch/vocabulary-asian.json --languages=th,zh-TW,ja,ko
done

# Other languages - chapters (all chapters)
for ch in ch-{01..18}; do
  /translate.sanscrit data/chapters/$ch/chapter-source.json \
    data/chapters/$ch/chapter-other.json --languages=he,ar,tr,sw
done

# Other languages - vocabulary (all chapters)
for ch in ch-{01..18}; do
  /translate.sanscrit data/chapters/$ch/vocabulary-source.json \
    data/chapters/$ch/vocabulary-other.json --languages=he,ar,tr,sw
done
```

### Step 4: Cleanup

```bash
# Remove old structure
rm -rf data/chapters/original
rm -rf data/chapters/asian
rm -rf data/chapters/other
rm -rf data/vocabulary/
rm -rf data/translations/
```

## Edge Cases

| Case | Handling |
|------|----------|
| Existing translations (ch 1-6) | Preserve, don't re-translate |
| Missing comment | Omit comment field in translation |
| RTL languages (he, ar) | Add text direction hint in output |
| Multi-line Sanskrit | Preserve newlines |
| Compound verse numbers (1.4-6) | Keep as-is |

## Validation

### JSON Schema Validation

All output files validated against:
- `chapter.schema.json` for source files
- `vocabulary.schema.json` for vocabulary files
- New `translation.schema.json` for translation overlays

### Content Validation

- [ ] All 18 chapters restructured
- [ ] All vocabulary migrated
- [ ] Existing translations preserved
- [ ] New translations marked `approved: false`

## Testing Strategy

### Unit Tests

- [ ] Restructure script creates correct directories
- [ ] Source files copied correctly
- [ ] Vocabulary linked to correct chapter

### Integration Tests

- [ ] `/translate.sanscrit` processes ch-01 correctly
- [ ] Asian translations saved to correct file
- [ ] Other translations saved to correct file

### Manual Verification

- [ ] Spot-check 3 slokas from each language group
- [ ] Verify terminology consistency between sloka and vocabulary
- [ ] Check transliteration accuracy

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Data loss during restructure | High | Backup original/ folders first |
| Translation quality | Medium | Use RU/EN as primary source |
| RTL rendering issues | Low | Add dir="rtl" hints in JSON |

---

## Approval

- [x] Reviewed by: User
- [x] Approved on: 2026-03-27
- [x] Notes: Approved with comments translation and proper transliterations
