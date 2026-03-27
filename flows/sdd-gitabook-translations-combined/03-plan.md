# Implementation Plan: Gitabook Translations Combined

> Version: 1.0
> Status: DRAFT
> Last Updated: 2026-03-27
> Specifications: [02-specifications.md](02-specifications.md)

## Overview

План реализации объединённого перевода глав и vocabulary на расширенный список языков.

## Phase Summary

| Phase | Description | Tasks | Status |
|-------|-------------|-------|--------|
| 0 | Backup & Preparation | 2 | Pending |
| 1 | Restructure Folders | 4 | Pending |
| 2 | Asian Translations | 2 | Pending |
| 3 | Other Translations | 2 | Pending |
| 4 | Validation & Cleanup | 3 | Pending |

**Total Tasks**: 13

## Phase 0: Backup & Preparation

### Task 0.1: Backup Original Data

**Action**: Create backup of current data

```bash
cp -r data/chapters/original data/chapters/original.bak
cp -r data/vocabulary/original data/vocabulary/original.bak
```

**Output**: Backup directories created

---

### Task 0.2: Verify Source Data Integrity

**Action**: Validate all 18 chapter and vocabulary JSON files

**Checks**:
- [ ] 18 chapter files exist
- [ ] 18 vocabulary files exist
- [ ] All files valid JSON
- [ ] All files have expected structure

---

## Phase 1: Restructure Folders

### Task 1.1: Create Chapter Directories

**Action**: Create 18 chapter bundle directories

```bash
for i in $(seq -w 1 18); do
  mkdir -p data/chapters/ch-$i
done
```

**Output**: 18 directories created

---

### Task 1.2: Copy Source Files

**Action**: Copy chapter sources to new structure

```bash
for i in $(seq -w 1 18); do
  cp data/chapters/original/chapter-$i.json data/chapters/ch-$i/source.json
done
```

**Output**: 18 source.json files

---

### Task 1.3: Copy Vocabulary Files

**Action**: Copy vocabulary to chapter bundles

```bash
for i in $(seq -w 1 18); do
  cp data/vocabulary/original/vocab_$i.json data/chapters/ch-$i/vocabulary.json
done
```

**Output**: 18 vocabulary.json files

---

### Task 1.4: Extract Existing Asian Translations (Ch 1-6)

**Action**: For chapters 1-6, extract existing ko, th, zh-CN, zh-TW translations

**Process**:
1. Read current chapter-XX.json files
2. Extract Asian language translations (if present)
3. Create `translations-asian.json` for each chapter

**Note**: Chapters 1-6 already have some Asian translations from previous work

---

## Phase 2: Asian Translations

### Task 2.1: Translate Chapters 7-18 (Asian)

**Action**: Use `/translate.sanscrit` for chapters 7-18

**Target languages**: th, zh-TW, ja, ko

**Process**:
```bash
# For each chapter 7-18
/translate.sanscrit data/chapters/ch-07 --target asian
/translate.sanscrit data/chapters/ch-08 --target asian
...
/translate.sanscrit data/chapters/ch-18 --target asian
```

**Output**: translations-asian.json for ch-07 through ch-18

---

### Task 2.2: Add Japanese (ja) to Chapters 1-6

**Action**: Chapters 1-6 missing Japanese, add it

**Target**: ja only

```bash
# For each chapter 1-6
/translate.sanscrit data/chapters/ch-01 --target ja
...
/translate.sanscrit data/chapters/ch-06 --target ja
```

**Output**: Updated translations-asian.json with ja added

---

## Phase 3: Other Translations

### Task 3.1: Translate All Chapters (Hebrew)

**Action**: Translate all 18 chapters to Hebrew

```bash
for ch in ch-{01..18}; do
  /translate.sanscrit data/chapters/$ch --target he
done
```

**Output**: translations-other.json with Hebrew

---

### Task 3.2: Translate All Chapters (Arabic, Turkish)

**Action**: Translate all 18 chapters to Arabic and Turkish

```bash
for ch in ch-{01..18}; do
  /translate.sanscrit data/chapters/$ch --target ar,tr
done
```

**Output**: Updated translations-other.json with ar, tr

---

## Phase 4: Validation & Cleanup

### Task 4.1: Validate All Translation Files

**Action**: Run JSON schema validation

**Checks**:
- [ ] All translations-asian.json valid
- [ ] All translations-other.json valid
- [ ] All vocabulary translations present
- [ ] No missing slokas

---

### Task 4.2: Spot-Check Translation Quality

**Action**: Manual review of sample translations

**Samples**:
- Chapter 1, Sloka 1 (opening)
- Chapter 2, Sloka 47 (famous karma yoga verse)
- Chapter 18, Sloka 66 (final teaching)

**Languages to check**: th, ja, he, ar

---

### Task 4.3: Cleanup Old Structure

**Action**: Remove deprecated directories

```bash
rm -rf data/chapters/original
rm -rf data/chapters/asian
rm -rf data/chapters/other
rm -rf data/vocabulary/
rm -rf data/translations/
```

**Safety**: Only after validation complete

---

## Task Dependencies

```
Phase 0 ──► Phase 1 ──► Phase 2 ──┬──► Phase 4
                        Phase 3 ──┘
```

- Phase 2 and 3 can run in parallel
- Phase 4 requires both Phase 2 and 3 complete

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Data loss | Backup in Phase 0 |
| Translation errors | Spot-check in Phase 4 |
| Missing files | Validation in Phase 4 |

## Success Criteria

- [ ] All 18 chapters restructured
- [ ] Asian translations complete (th, zh-TW, ja, ko)
- [ ] Other translations complete (he, ar, tr)
- [ ] All vocabulary translated with chapters
- [ ] All new translations marked `approved: false`
- [ ] Old directory structure removed

---

## Approval

- [ ] Reviewed by: User
- [ ] Approved on: [DATE]
- [ ] Notes: [NOTES]
