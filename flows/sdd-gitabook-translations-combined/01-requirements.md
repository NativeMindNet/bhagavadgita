# Requirements: Gitabook Translations Combined

> Version: 1.0
> Status: DRAFT
> Last Updated: 2026-03-27
> Source: Merged from sdd-gitabook-translation-chapters-json + sdd-gitabook-translation-vocabulary-json

## Problem Statement

Текущий статус:
- Шлоки конвертированы в JSON (18 файлов в `data/chapters/original/`)
- Vocabulary конвертирован в JSON (18 файлов в `data/vocabulary/original/`)
- Переведены главы 1-6 на: ko, th, zh-CN, zh-TW
- Vocabulary не переведён

Нужно:
1. Оптимизировать структуру папок для совместной обработки глава+vocabulary
2. Добавить переводы на расширенный список языков
3. Автоматизировать процесс перевода через `/translate.sanscrit`

## User Stories

### Primary

**As a** разработчик
**I want** единую структуру для главы+vocabulary
**So that** переводить оба компонента в одном контексте для консистентности терминов

**As a** пользователь из Азии
**I want** читать Гиту на своем родном языке (тайский, китайский, японский, корейский)
**So that** понимать священный текст без языкового барьера

**As a** пользователь из Ближнего Востока
**I want** читать Гиту на иврите, арабском, турецком
**So that** изучать священный текст на своем языке

## Target Languages (Updated)

### Asian Languages

| Code | Language | Native Name | Script | Status |
|------|----------|-------------|--------|--------|
| th | Thai | ภาษาไทย | Thai | Ch 1-6 done |
| zh-TW | Chinese Traditional | 繁體中文 | Han | Ch 1-6 done |
| ja | Japanese | 日本語 | Kanji/Kana | Pending |
| ko | Korean | 한국어 | Hangul | Ch 1-6 done |

### Other Languages

| Code | Language | Native Name | Script | Status |
|------|----------|-------------|--------|--------|
| he | Hebrew | עברית | Hebrew | Pending |
| ar | Arabic | العربية | Arabic | Pending |
| tr | Turkish | Türkçe | Latin | Pending |
| sw | Swahili | Kiswahili | Latin | Pending |

### Existing Languages (Already in original)

| Code | Language | Status |
|------|----------|--------|
| ru | Russian | Complete |
| en | English | Complete |
| de | German | Complete |
| es | Spanish | Complete |

## Optimized Folder Structure

### Current Structure (Suboptimal)

```
data/
├── chapters/
│   ├── original/          # chapter-01.json ... chapter-18.json
│   ├── asian/             # Empty folders
│   └── other/
└── vocabulary/
    ├── original/          # vocab_01.json ... vocab_18.json
    ├── asian/             # Empty
    └── other/             # Empty
```

### Proposed Structure (Chapter-centric)

```
data/
├── schema/
│   ├── chapter.schema.json
│   └── vocabulary.schema.json
├── meta/
│   └── languages.json
└── translations/
    ├── source/                    # Original data (read-only)
    │   ├── chapter-01.json
    │   ├── vocab-01.json
    │   ├── chapter-02.json
    │   ├── vocab-02.json
    │   └── ...
    ├── asian/                     # Asian translations
    │   ├── chapter-01-asian.json
    │   ├── vocab-01-asian.json
    │   └── ...
    └── other/                     # Hebrew, Arabic, Turkish
        ├── chapter-01-other.json
        ├── vocab-01-other.json
        └── ...
```

### Alternative: Per-Chapter Bundles (Recommended)

```
data/
├── schema/
├── meta/
└── chapters/
    ├── ch-01/
    │   ├── source.json           # Chapter slokas (RU/EN/DE/ES)
    │   ├── vocabulary.json       # Vocabulary (RU/EN)
    │   ├── translations-asian.json
    │   └── translations-other.json
    ├── ch-02/
    │   ├── source.json
    │   ├── vocabulary.json
    │   ├── translations-asian.json
    │   └── translations-other.json
    └── ...
```

**Advantages:**
- All chapter data in one place
- Easy to pass chapter+vocabulary to translation agent
- Clear separation of source vs translations
- No need to cross-reference files

## Scope

### In Scope

1. **Restructure folders** to per-chapter bundles
2. **Translate chapters 7-18** to: ko, th, zh-TW, ja
3. **Add new languages**: he, ar, tr
4. **Translate vocabulary** alongside chapters
5. **Use `/translate.sanscrit`** for automated translation

### What Gets Translated

| Component | Description |
|-----------|-------------|
| **Chapter title** | Название главы на каждом языке |
| **Sloka text** | Перевод текста шлоки |
| **Comment** | Комментарий духовного учителя (Шридхара Махараджа) |
| **Vocabulary meaning** | Значение санскритского слова |
| **Vocabulary transliteration** | Фонетическая транскрипция на письме целевого языка |

### Transliteration Requirement

Санскритские слова должны иметь правильную фонетическую транскрипцию на каждом языке:

| Language | Script | Example: dhṛtarāṣṭra |
|----------|--------|---------------------|
| Thai | Thai | ธฤตราษฏร |
| Chinese | Hanzi | 德瑞塔拉什特拉 |
| Japanese | Katakana | ドゥリタラーシュトラ |
| Korean | Hangul | 드리타라슈트라 |
| Hebrew | Hebrew | דְּרִיטַרָאשְׁטְרַה |
| Arabic | Arabic | دريتاراشترا |
| Turkish | Latin | Dhritaraştra |
| Swahili | Latin | Dhritarashtra |

### Out of Scope

- zh-CN (Simplified Chinese) - focus on zh-TW (Traditional)
- Audio files
- Interactive editor
- Modifications to original chapter-XX.json files

## Translation Workflow

### Command

```
/translate.sanscrit
```

### Input Per Chapter

For each chapter, the agent receives:
1. Chapter slokas (source.json or original)
2. Chapter vocabulary (vocabulary.json or vocab-XX.json)
3. Target language(s)

### Output Per Chapter

1. `translations-asian.json` - ko, th, zh-TW, ja translations
2. `translations-other.json` - he, ar, tr translations
3. Updated vocabulary with translations

### Source Priority

1. **Russian (ru)** — primary source for meaning
2. **English (en)** — secondary source
3. **German (de), Spanish (es)** — additional context
4. **Sanskrit** — ONLY for term accuracy, not for understanding

## Acceptance Criteria

### Must Have

1. **Given** current folder structure
   **When** restructuring completes
   **Then** all 18 chapters organized in chapter-centric bundles

2. **Given** chapter with vocabulary
   **When** /translate.sanscrit runs
   **Then** both chapter AND vocabulary translated together

3. **Given** Asian translation task
   **When** translation completes
   **Then** outputs: th, zh-TW, ja, ko translations

4. **Given** Other languages task
   **When** translation completes
   **Then** outputs: he, ar, tr translations

5. **Given** translated content
   **When** saved
   **Then** marked with `approved: false`

6. **Given** sloka with comment
   **When** translation runs
   **Then** comment (духовного учителя) переведён вместе со шлокой

7. **Given** vocabulary word
   **When** translation runs
   **Then** meaning переведён + phonetic transliteration на письме целевого языка

### Should Have

- Validation against JSON Schema
- Progress tracking per chapter

### Won't Have (This Iteration)

- zh-CN (Simplified Chinese)
- Audio generation
- Manual approval workflow

## Constraints

- **Encoding**: UTF-8 for all files
- **Validation**: JSON Schema for structure
- **Size**: Keep individual files < 500KB
- **Compatibility**: JSON readable in browsers and mobile apps

## Open Questions

- [x] ~~Folder structure~~ → Per-chapter bundles recommended
- [x] ~~Target languages~~ → Asian: th, zh-TW, ja, ko; Other: he, ar, tr
- [ ] Should we keep both zh-CN and zh-TW or just zh-TW?
- [ ] Hebrew/Arabic: right-to-left rendering considerations?

## Dependencies

- Source data: `/data/chapters/original/`, `/data/vocabulary/original/`
- Translation command: `/translate.sanscrit`
- Related flows: `sdd-gitabook-translation-chapters-json`, `sdd-gitabook-translation-vocabulary-json`

## References

- Original chapters flow: `flows/sdd-gitabook-translation-chapters-json/`
- Original vocabulary flow: `flows/sdd-gitabook-translation-vocabulary-json/`
- Translation command: `.qwen/commands/translate.sanscrit.md`

---

## Approval

- [ ] Reviewed by: User
- [ ] Approved on: [DATE]
- [ ] Notes: [NOTES]
