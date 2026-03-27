# Status: sdd-gitabook-translations-combined

## Current Phase

IMPLEMENTATION

## Phase Status

READY TO START - All documents approved

## Last Updated

2026-03-27 by Claude

## Blockers

- None

## Progress

- [x] Flow created
- [x] Requirements drafted
- [x] Requirements approved
- [x] Specifications drafted
- [x] Specifications approved
- [x] Plan drafted
- [x] Plan approved
- [ ] Phase 0: Backup & Preparation
- [ ] Phase 1: Restructure Folders
- [ ] Phase 2: Asian Translations
- [ ] Phase 3: Other Translations
- [ ] Phase 4: Validation & Cleanup

## Context Notes

### Target Languages

**Asian**: th, zh-TW, ja, ko
**Other**: he, ar, tr, sw

### What Gets Translated

- Chapter title
- Sloka text
- **Comment** (духовного учителя)
- Vocabulary meaning
- Vocabulary transliteration (на письме целевого языка)

### Translation Command

```bash
/translate.sanscrit <input> <output> --languages=<langs>
```

### New Folder Structure

```
data/chapters/
├── ch-01/
│   ├── chapter-source.json      # RU/EN/DE/ES slokas + comments
│   ├── vocabulary-source.json   # RU/EN vocabulary
│   ├── chapter-asian.json       # th, zh-TW, ja, ko
│   ├── chapter-other.json       # he, ar, tr, sw
│   ├── vocabulary-asian.json    # th, zh-TW, ja, ko
│   └── vocabulary-other.json    # he, ar, tr, sw
└── ...
```

## Next Actions

1. Phase 0: Backup original data
2. Phase 1: Create new folder structure (ch-01 through ch-18)
3. Phase 2: Run /translate.sanscrit for Asian languages
4. Phase 3: Run /translate.sanscrit for Other languages
5. Phase 4: Validate and cleanup
