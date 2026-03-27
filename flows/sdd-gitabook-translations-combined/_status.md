# Status: sdd-gitabook-translations-combined

## Current Phase

REQUIREMENTS

## Phase Status

DRAFT - Awaiting user review and approval

## Last Updated

2026-03-27 by Claude

## Blockers

- None

## Progress

- [x] Flow created
- [x] Requirements drafted (merged from chapters + vocabulary flows)
- [ ] Requirements approved
- [x] Specifications drafted
- [ ] Specifications approved
- [x] Plan drafted
- [ ] Plan approved
- [ ] Implementation started

## Context Notes

### What This Flow Does

Объединённый SDD для перевода глав + vocabulary:

1. **Оптимизация структуры папок**: Переход к per-chapter bundles
2. **Расширенный список языков**:
   - Asian: th, zh-TW, ja, ko
   - Other: he, ar, tr
3. **Совместный перевод**: Глава + vocabulary в одном контексте

### Source Flows

Merged from:
- `sdd-gitabook-translation-chapters-json` (chapters)
- `sdd-gitabook-translation-vocabulary-json` (vocabulary)

### Key Changes from Original Flows

1. **Removed zh-CN** - Focus on zh-TW (Traditional)
2. **Added new languages**: he (Hebrew), ar (Arabic), tr (Turkish)
3. **New folder structure**: Per-chapter bundles instead of separate directories
4. **Combined translation**: Chapter + vocabulary translated together

### Current Data State

| Data | Location | Count |
|------|----------|-------|
| Chapters (original) | `data/chapters/original/` | 18 |
| Vocabulary (original) | `data/vocabulary/original/` | 18 |
| Asian translations | `data/chapters/asian/` | Empty |
| Ch 1-6 (ko, th, zh-CN, zh-TW) | In original chapter files | Partial |

### Translation Command

```
/translate.sanscrit
```

## Next Actions

1. Review requirements document
2. Approve or request changes
3. Proceed to specifications approval
4. Proceed to plan approval
5. Start implementation
