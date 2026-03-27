# 02. Specification

## Overview

This specification defines the technical design for generating Bhagavat-gita books in Chinese, Thai, and Hebrew from existing JSON source data.

## Data Sources

### Source Files

| Source | Path Pattern | Content |
|--------|--------------|---------|
| Original Chapters | `/data/chapters/original/chapter-{01-18}.json` | Sanskrit slokas, transliteration, translations (ru, en, de, es, ko, th, zh-CN, zh-TW) |
| Asian Translations | `/data/chapters/asian/chapter-{01-18}-asian-translations.json` | Consolidated Asian translations (ko, th, zh-CN, zh-TW) |
| Vocabulary | `/data/chapters/ch-{01-18}/vocabulary-source.json` | Word-by-word meanings (en approved, others pending) |
| Chapter Meta | `/data/chapters/ch-{01-18}/chapter-source.json` | Chapter titles, metadata, sloka details |

### Data Structure

**Chapter JSON** (`original/chapter-XX.json`):
```json
{
  "chapter": 1,
  "title": {
    "sanskrit": "",
    "transliteration": "",
    "ru": {"text": "...", "approved": true},
    "en": {"text": "...", "approved": true},
    "zh-CN": {"text": "...", "approved": false},
    "th": {"text": "...", "approved": false}
  },
  "meta": {
    "totalSlokas": 37,
    "version": "1.1"
  },
  "slokas": [...]
}
```

**Sloka Structure**:
```json
{
  "number": "1.1",
  "order": 1,
  "sanskrit": "धृतराष्ट्र उवाच ।...",
  "transliteration": "дхр̣тара̄ш̣т̣ра ува̄ча...",
  "translations": {
    "zh-CN": {"text": "...", "approved": false},
    "th": {"text": "...", "approved": false}
  },
  "vocabulary": [...]
}
```

## Output Specification

### Directory Structure

```
/data/chapters/generated/
├── chinese/
│   ├── README.md           # Book cover & table of contents
│   ├── chapter-01.md       # Chapter 1: 观军
│   ├── chapter-02.md
│   │   ...
│   ├── chapter-18.md
│   ├── glossary.md         # 词汇表
│   └── comments.md         # 注释 - 待翻译内容
├── thai/
│   ├── README.md
│   ├── chapter-01.md       # บทที่ 1: การสังเกตกองทัพ
│   │   ...
│   ├── glossary.md         # ศัพท์บัญญัติ
│   └── comments.md         # หมายเหตุ - เนื้อหาที่รอการแปล
└── hebrew/
    ├── README.md           # ספר ברהמא וידה
    ├── chapter-01.md       # פרק 1: ⚠️ awaiting translation
    │   ...
    ├── glossary.md         # ⚠️ awaiting translation
    └── comments.md         # הערות - תרגום חסר
```

### Markdown Template

**Chapter File Template**:
```markdown
# Глава {N}: {Title in Target Language}

{Meta: total slokas, version}

---

## Стих {sloka-number}

### Санскрит
```sanskrit
{sanskrit text}
```

### Перевод
> {translation text}
> 
> ⚠️ **Ожидает перевода** (if not available)

### Комментарий
{commentary if available}

### Словарь
| Слово | Транслитерация | Значение |
|-------|---------------|----------|
| ... | ... | ... |

---
```

**Glossary Template**:
```markdown
# Словарь / Glossary

## A
| Term | Transliteration | Meaning (RU) | Meaning (EN) | Meaning (TARGET) |
|------|-----------------|--------------|--------------|------------------|
| ... | ... | ... | ... | ... |

### Notes
- ⚠️ Marked entries await translation
```

## Language-Specific Details

### Chinese (zh-CN)
- **Title**: 《博伽梵歌》
- **Chapter format**: 第 X 章：{title}
- **Glossary**: 词汇表
- **Comments**: 注释
- **Font direction**: LTR

### Thai (th)
- **Title**: ภควัทคีตา
- **Chapter format**: บทที่ X: {title}
- **Glossary**: ศัพท์บัญญัติ
- **Comments**: หมายเหตุ
- **Font direction**: LTR

### Hebrew (he)
- **Title**: בהגavad גיטה
- **Chapter format**: פרק X: {title}
- **Glossary**: אוצר מילים
- **Comments**: הערות
- **Font direction**: **RTL** (requires `<div dir="rtl">` or Markdown RTL support)
- **Status**: ⚠️ **All content awaits translation**

## Translation Status Matrix

| Language | Chapter Titles | Slokas | Vocabulary | Status |
|----------|---------------|--------|------------|--------|
| zh-CN | ✅ Available | ✅ Available | ⚠️ Partial | Ready |
| th | ✅ Available | ✅ Available | ⚠️ Partial | Ready |
| he | ❌ Missing | ❌ Missing | ❌ Missing | Awaiting |

## Processing Rules

### Rule 1: Translation Priority
1. Use `approved: true` translations when available
2. Fall back to `approved: false` if no approved version
3. Mark as "awaiting translation" if completely missing

### Rule 2: Untranslated Content
For any missing translation:
```markdown
> ⚠️ **Ожидает перевода** / Await translation
> 
> **English reference**: {english text}
```

### Rule 3: Hebrew Special Handling
Since Hebrew has no source data:
- Generate complete structure
- Include English reference for all content
- Add prominent notice on each page
- Create comprehensive "awaiting translation" list

### Rule 4: Vocabulary Aggregation
- Collect all unique vocabulary words across all chapters
- Include Sanskrit original
- Include transliteration
- Include all available translations
- Mark missing translations

## Quality Checks

- [ ] All 18 chapters present for each language
- [ ] Chapter titles match source data
- [ ] Sloka numbers sequential and complete
- [ ] Sanskrit text preserved without modification
- [ ] Untranslated content clearly marked
- [ ] Glossary alphabetically organized
- [ ] Comments section lists all missing translations
- [ ] Hebrew files include RTL direction markers

---

**Status**: Draft  
**Created**: 2026-03-27  
**Based on**: REQ-01
