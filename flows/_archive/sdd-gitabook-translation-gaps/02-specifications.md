# Specifications: Gitabook Translation V2

> Version: 1.0
> Status: DRAFT
> Last Updated: 2026-03-28
> Requirements: [01-requirements.md](01-requirements.md)

## Overview

Спецификация работ по завершению переводов глав и комментариев Бхагавад-гиты.

## 1. Chapter Translations

### 1.1 Add Japanese (ja) to Chapters 1-6

**Source files:**
```
data/chapters/ch-01/chapter-asian.json
data/chapters/ch-02/chapter-asian.json
data/chapters/ch-03/chapter-asian.json
data/chapters/ch-04/chapter-asian.json
data/chapters/ch-05/chapter-asian.json
data/chapters/ch-06/chapter-asian.json
```

**Current state:** ko, th, zh-CN, zh-TW (4 языка)

**Target state:** ko, th, zh-CN, zh-TW, **ja** (5 языков)

**Translation source:** Use existing English from `chapter-source.json`

**Format:**
```json
{
  "chapter": 1,
  "title": {
    "ko": "...",
    "th": "...",
    "zh-CN": "...",
    "zh-TW": "...",
    "ja": "NEW"  // <- добавить
  },
  "slokas": {
    "1.1": {
      "ko": {"text": "...", "approved": false},
      "th": {"text": "...", "approved": false},
      "zh-CN": {"text": "...", "approved": false},
      "zh-TW": {"text": "...", "approved": false},
      "ja": {"text": "NEW", "approved": false}  // <- добавить
    }
  }
}
```

---

### 1.2 Add Simplified Chinese (zh-CN) to Chapters 7-18

**Source files:**
```
data/chapters/ch-07/chapter-asian.json
...
data/chapters/ch-18/chapter-asian.json
```

**Current state:** th, zh-TW, ja, ko (4 языка)

**Target state:** th, zh-TW, ja, ko, **zh-CN** (5 языков)

**Translation source:** Use existing English from `chapter-source.json`

**Format:** Same as 1.1, add `zh-CN` key

---

### 1.3 Re-translate Chapters 1-6 for Other Languages

**Source files:**
```
data/chapters/ch-01/chapter-other.json
...
data/chapters/ch-06/chapter-other.json
```

**Current state:** Contains English text instead of translations

**Target state:** Real translations in he, ar, tr, sw

**Translation source:** Use existing English from `chapter-source.json`

**Format:**
```json
{
  "chapter": 1,
  "title": {
    "he": "צפייה בצבאות",
    "ar": "مراقبة الجيوش",
    "tr": "Orduları Gözlemlemek",
    "sw": "Kuangalia Jeshi"
  },
  "slokas": {
    "1.1": {
      "he": {"text": "REAL HEBREW", "approved": false},
      "ar": {"text": "REAL ARABIC", "approved": false},
      "tr": {"text": "REAL TURKISH", "approved": false},
      "sw": {"text": "REAL SWAHILI", "approved": false}
    }
  }
}
```

---

## 2. Comments Translation

### 2.1 Source Data

**File:** `legacy/csv/Books/Gita_Slokas.csv`

**Format:** CSV with `;` delimiter

**Relevant columns:**
- `ChapterId` - ID главы (1-18 для ШМ, 19-36 для SM)
- `Name` - номер шлоки (e.g., "1.1", "2.47")
- `Comment` - текст комментария

**Comments to extract:**

| Source | ChapterId Range | Language | Count |
|--------|-----------------|----------|-------|
| ШМ | 1-18 | RU | 12 |
| SM | 19-36 | EN | 21 |

**Mapping ChapterId to real chapter:**
- ШМ: ChapterId = real chapter (1→1, 2→2, etc.)
- SM: ChapterId - 18 = real chapter (19→1, 20→2, etc.)

---

### 2.2 Output Format

**Output files:**
```
data/chapters/ch-XX/comments-asian.json
data/chapters/ch-XX/comments-other.json
```

**Format:**
```json
{
  "chapter": 4,
  "source": "ШМ",
  "comments": [
    {
      "sloka": "4.13",
      "original": {
        "lang": "ru",
        "text": "* Эти четыре сословия..."
      },
      "translations": {
        "th": {"text": "...", "approved": false},
        "zh-CN": {"text": "...", "approved": false},
        "zh-TW": {"text": "...", "approved": false},
        "ja": {"text": "...", "approved": false},
        "ko": {"text": "...", "approved": false}
      }
    }
  ]
}
```

---

### 2.3 Comments List

**ШМ (Russian, 12 comments):**

| Ch | Sloka | Preview |
|----|-------|---------|
| 4 | 4.13 | Эти четыре сословия: брахманы — священнослужители... |
| 4 | 4.33 | Объяснение этого стиха Шрилой Шридхаром Махараджем... |
| 5 | 5.13 | Материальное тело имеет девять врат... |
| 10 | 10.7 | Стихи с восьмого по одиннадцатый этой главы... |
| 10 | 10.8 | Стихи с восьмого по одиннадцатый этой главы... |
| 10 | 10.9 | Господь Кришна говорит о всецело предавшихся... |
| 10 | 10.10 | Господь говорит: «Ближайшие из Моих слуг... |
| 10 | 10.11 | Первый из двух приведенных переводов... |
| 13 | 13.7 | Тонкие материальные элементы: ум, разум... |
| 13 | 13.13 | Брахман — всеохватывающий аспект Абсолюта... |
| 15 | 15.14 | Пища, которую пережевывают, рассасывают... |
| 18 | 18.66 | Здесь воспета слава сокровенного смысла... |

**SM (English, 21 comments):**

| Ch | Sloka | Preview |
|----|-------|---------|
| 2 | 2.25 | Birth, existence, growth, maturity... |
| 2 | 2.32 | One's natural duty or 'svadharma'... |
| 2 | 2.39 | It will be revealed that buddhi-yoga... |
| 2 | 2.40 | Mahābhay, the greatest fear... |
| 2 | 2.45 | The objective of the Vedas... |
| 3 | 3.13 | The remnants referred to here... |
| 3 | 3.35 | The eternal, superexcellent... |
| 4 | 4.23 | The actions of one practising... |
| 5 | 5.13 | The body of nine gates... |
| 7 | 7.4 | In this verse, it is expressed... |
| 8 | 8.17 | One yuga (age) in the time calculation... |
| 9 | 9.31 | The second interpretation... |
| 10 | 10.8 | Verses 8–11 are the four principal... |
| 10 | 10.9 | The Supreme Lord Kṛṣṇa is speaking... |
| 10 | 10.10 | The Lord says, "The highest group... |
| 10 | 10.11 | Of the two translations given above... |
| 12 | 12.3–4 | The Lord's statement, "The worshippers... |
| 15 | 15.1 | The roots of the tree of this world... |
| 15 | 15.2 | Within the expansive manifestation... |
| 18 | 18.64 | According to Śrīla Bhakti Vinod Ṭhākur... |
| 18 | 18.66 | Here, the glory of the hidden purpose... |

---

## 3. Translation Tool

**Command:** `/translate.sanskrit`

**Usage pattern:**
```
/translate.sanskrit [source_file] [output_file] --languages=[lang_codes]
```

**Important:** This is the ONLY tool allowed for translations. No code/scripts.

---

## 4. File Operations Summary

| Operation | Files | Action |
|-----------|-------|--------|
| Add ja to ch 1-6 | 6 | Merge new translations |
| Add zh-CN to ch 7-18 | 12 | Merge new translations |
| Replace ch-other 1-6 | 6 | Full re-translation |
| Create comments-asian | ~8 | New files |
| Create comments-other | ~8 | New files |

---

## 5. Validation Criteria

### Chapters
- [ ] All chapter-asian.json contain: ko, th, zh-CN, zh-TW, ja
- [ ] All chapter-other.json contain real translations (not English)
- [ ] All translations have `"approved": false`

### Comments
- [ ] All 33 comments extracted from CSV
- [ ] Asian translations: th, zh-CN, zh-TW, ja, ko
- [ ] Other translations: he, ar, tr, sw
- [ ] Original text preserved

---

## Approval

- [x] Reviewed by: User
- [x] Approved on: 2026-03-28
- [x] Notes: Specs confirmed
