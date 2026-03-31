# Requirements: GitaBook Translation

> Version: 1.0
> Status: APPROVED
> Last Updated: 2026-03-31

## Problem Statement

The `data/translated/` folder contains 12 languages but most are incomplete or have incorrect content:
- **8 languages have ZERO content**: ar, el, he, hy, ja, ka, sw, tr
- **4 languages have partial content**: ko, th, zh-CN, zh-TW (only chapters 1-6 of 18)
- **All transliterations are wrong**: Using Cyrillic script instead of native scripts

## Gap Analysis

### File Counts

| Language | Expected Slokas | Actual Slokas | Translits | Gap |
|----------|-----------------|---------------|-----------|-----|
| ar (Arabic) | 663 | 0 | 0 | 100% missing |
| el (Greek) | 663 | 0 | 0 | 100% missing |
| he (Hebrew) | 663 | 0 | 0 | 100% missing |
| hy (Armenian) | 663 | 0 | 0 | 100% missing |
| ja (Japanese) | 663 | 0 | 0 | 100% missing |
| ka (Georgian) | 663 | 0 | 0 | 100% missing |
| ko (Korean) | 663 | 266 | 266 (wrong script) | 60% missing + translit fix |
| sw (Swahili) | 663 | 0 | 0 | 100% missing |
| th (Thai) | 663 | 266 | 266 (wrong script) | 60% missing + translit fix |
| tr (Turkish) | 663 | 0 | 0 | 100% missing |
| zh-CN (Simplified) | 663 | 266 | 266 (wrong script) | 60% missing + translit fix |
| zh-TW (Traditional) | 663 | 266 | 266 (wrong script) | 60% missing + translit fix |

### Chapter Coverage (languages with partial content)

| Chapter | Slokas | ko | th | zh-CN | zh-TW |
|---------|--------|----|----|-------|-------|
| 1 | 37 | ✓ | ✓ | ✓ | ✓ |
| 2 | 72 | ✓ | ✓ | ✓ | ✓ |
| 3 | 43 | ✓ | ✓ | ✓ | ✓ |
| 4 | 42 | ✓ | ✓ | ✓ | ✓ |
| 5 | 27 | ✓ | ✓ | ✓ | ✓ |
| 6 | 45 | ✓ | ✓ | ✓ | ✓ |
| 7-18 | 397 | ✗ | ✗ | ✗ | ✗ |

### Transliteration Issues

All existing translits use **Cyrillic** (Russian) script instead of native:

| Language | Current Script | Required Script |
|----------|----------------|-----------------|
| ja | - | Katakana (カタカナ) |
| ko | Cyrillic | Hangul (한글) |
| th | Cyrillic | Thai (ไทย) |
| zh-CN | Cyrillic | Hanzi Simplified (简体) |
| zh-TW | Cyrillic | Hanzi Traditional (繁體) |
| el | - | Greek (Ελληνικά) |
| ka | - | Georgian (ქართული) |
| hy | - | Armenian (Հայdelays) |
| he | - | Hebrew (עברית) |
| ar | - | Arabic (العربية) |
| tr | - | IAST (Latin) |
| sw | - | IAST (Latin) |

### Content Quality Issues

Thai sloka 1.1 has **mixed script error**:
```
กุรุกษetra  ← Latin "etra" instead of Thai "เตระ"
```

## User Stories

### Primary

**As a** GitaBook maintainer
**I want** complete translations for all 12 languages
**So that** readers can access Bhagavad Gita in their native language

### Secondary

**As a** reader of non-Latin script languages
**I want** transliterations in my native script
**So that** I can pronounce Sanskrit words correctly

## Acceptance Criteria

### Must Have

1. **Given** a translated language
   **When** checking file structure
   **Then** all 663 slokas exist with both `_sloka.txt` and `_translit.txt` files

2. **Given** a transliteration file
   **When** viewing content
   **Then** it uses the correct native script for that language

3. **Given** a sloka translation
   **When** viewing content
   **Then** text is entirely in the target language (no mixed scripts)

### Should Have

1. Translations verified for semantic accuracy
2. Meta files updated with correct statistics

### Won't Have (This Iteration)

1. Vocabulary files for translated languages
2. Comment files (spiritual teacher notes)
3. Quality review by native speakers

## Constraints

- **Tool**: Use `/translate.sanscrit` command for translations
- **Process**: Run sequentially, save after each completion
- **Source**: Translate from ru, en, de, es + sanskrit
- **Order**: Complete transliterations first, then translations

## Work Estimate

| Metric | Count |
|--------|-------|
| Total `/translate.sanscrit` calls | **48** |
| Translit files generated | 7,956 |
| Sloka files generated | 6,892 |
| **Total new files** | **14,848** |

## Priority Order (Вариант C)

**Phase 1: Все транслитерации** (быстрые результаты)
- Chapters 1-18, all 12 languages
- Fixes Cyrillic → native script for th, zh-CN, zh-TW, ko
- 18 calls

**Phase 2: Переводы th, zh-CN, zh-TW, ko** (добить)
- Chapters 7-18 only (missing)
- 4 languages become 100% complete
- 12 calls

**Phase 3: Переводы остальных**
- Chapters 1-18 for ja, el, ka, hy, he, ar, tr, sw
- 8 languages become 100% complete
- 18 calls

**Result:** All 12 languages × 18 chapters complete

## Open Questions

- [x] Which source language to translate from? → **ru, en, de, es + sanskrit**
- [x] How to handle mixed script errors? → **Regenerate entire sloka**
- [x] Optimization approach? → **Вариант C: translits first, then slokas**

## References

- Previous flow: `flows/sdd-gitabook-structure/`
- Languages config: `data/meta/languages.json`
- Chapter data: `data/meta/chapters.json`
- Translation command: `.claude/commands/translate.sanscrit.md`

---

## Approval

- [x] Approved on: 2026-03-31
