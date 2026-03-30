# Implementation Plan: Gitabook Translations Combined

> Version: 2.0
> Status: NEEDS RE-APPROVAL
> Last Updated: 2026-03-27
> Specifications: [02-specifications.md](02-specifications.md)

## Overview

План реализации объединённого перевода глав и vocabulary на расширенный список языков.

**Порядок перевода**: с последних глав к первым (ch-18 → ch-01)

## Phase Summary

| Phase | Description | Tasks | Status |
|-------|-------------|-------|--------|
| 0 | Backup & Preparation | 2 | ✅ Complete |
| 1 | Restructure Folders | 4 | ✅ Complete |
| 2 | Asian Translations (ch-07 to ch-18) | 2 | ✅ Complete |
| 3 | Other Translations (ch-07 to ch-18) | 1 | ✅ Complete |
| **5** | **Missing Ch 1-6 Translations** | **3** | **Pending** |
| 4 | Validation & Cleanup | 3 | Pending |

**Total Tasks**: 15

## Current Data Gaps (Analysis 2026-03-27)

| File Type | ch-01 - ch-06 | ch-07 - ch-18 |
|-----------|---------------|---------------|
| chapter-asian.json | ✅ 6 files | ✅ 12 files |
| chapter-other.json | ❌ **MISSING** | ✅ 12 files |
| vocabulary-asian.json | ❌ **MISSING** | ✅ 12 files |
| vocabulary-other.json | ❌ **MISSING** | ✅ 12 files |

---

## Phase 0: Backup & Preparation ✅ COMPLETE

### Task 0.1: Backup Original Data ✅

**Action**: Create backup of current data

```bash
cp -r data/chapters/original data/chapters/original.bak
cp -r data/vocabulary/original data/vocabulary/original.bak
```

**Output**: Backup directories created

---

### Task 0.2: Verify Source Data Integrity ✅

**Action**: Validate all 18 chapter and vocabulary JSON files

**Checks**:
- [x] 18 chapter files exist
- [x] 18 vocabulary files exist
- [x] All files valid JSON
- [x] All files have expected structure

---

## Phase 1: Restructure Folders ✅ COMPLETE

### Task 1.1: Create Chapter Directories ✅

**Action**: Create 18 chapter bundle directories

```bash
for i in $(seq -w 1 18); do
  mkdir -p data/chapters/ch-$i
done
```

**Output**: 18 directories created

---

### Task 1.2: Copy Source Files ✅

**Action**: Copy chapter sources to new structure

```bash
for i in $(seq -w 1 18); do
  cp data/chapters/original/chapter-$i.json data/chapters/ch-$i/chapter-source.json
done
```

**Output**: 18 chapter-source.json files

---

### Task 1.3: Copy Vocabulary Files ✅

**Action**: Copy vocabulary to chapter bundles

```bash
for i in $(seq -w 1 18); do
  cp data/vocabulary/original/vocab_$i.json data/chapters/ch-$i/vocabulary-source.json
done
```

**Output**: 18 vocabulary-source.json files

---

### Task 1.4: Extract Existing Asian Translations (Ch 1-6) ✅

**Action**: For chapters 1-6, extract existing ko, th, zh-TW translations

**Process**:
1. Read current chapter-XX.json files
2. Extract Asian language translations (if present)
3. Create `chapter-asian.json` for each chapter

**Note**: Chapters 1-6 already have some Asian translations from previous work

---

## Phase 2: Asian Translations (ch-07 to ch-18) ✅ COMPLETE

### Task 2.1: Translate Chapters + Vocabulary (Asian) ✅

**Action**: Use `/translate.sanscrit` for chapters 7-18

**Target languages**: th, zh-TW, ja, ko

**Output**:
- 12 x chapter-asian.json (ch-07 to ch-18)
- 12 x vocabulary-asian.json (ch-07 to ch-18)

---

### Task 2.2: Merge Existing Translations (Ch 1-6) ✅

**Action**: For chapters 1-6, chapter-asian.json already exists with ko, th, zh-TW, ja

**Note**: Chapter translations done, but vocabulary-asian.json NOT created

---

## Phase 3: Other Translations (ch-07 to ch-18) ✅ COMPLETE

### Task 3.1: Translate Chapters + Vocabulary (Other) ✅

**Action**: Translated chapters 7-18 to he, ar, tr, sw

**Output**:
- 12 x chapter-other.json (ch-07 to ch-18)
- 12 x vocabulary-other.json (ch-07 to ch-18)

---

## Phase 5: Missing Ch 1-6 Translations ⏳ PENDING

> **IMPORTANT**: This phase was added to complete missing data for chapters 1-6

### Task 5.1: Vocabulary Asian (Ch 1-6)

**Action**: Create vocabulary-asian.json for chapters 1-6

**Target languages**: th, zh-TW, ja, ko

**Process** (SEQUENTIAL - one chapter at a time):
```bash
/translate.sanscrit data/chapters/ch-01/vocabulary-source.json \
  data/chapters/ch-01/vocabulary-asian.json --languages=th,zh-TW,ja,ko

/translate.sanscrit data/chapters/ch-02/vocabulary-source.json \
  data/chapters/ch-02/vocabulary-asian.json --languages=th,zh-TW,ja,ko

/translate.sanscrit data/chapters/ch-03/vocabulary-source.json \
  data/chapters/ch-03/vocabulary-asian.json --languages=th,zh-TW,ja,ko

/translate.sanscrit data/chapters/ch-04/vocabulary-source.json \
  data/chapters/ch-04/vocabulary-asian.json --languages=th,zh-TW,ja,ko

/translate.sanscrit data/chapters/ch-05/vocabulary-source.json \
  data/chapters/ch-05/vocabulary-asian.json --languages=th,zh-TW,ja,ko

/translate.sanscrit data/chapters/ch-06/vocabulary-source.json \
  data/chapters/ch-06/vocabulary-asian.json --languages=th,zh-TW,ja,ko
```

**Output**: 6 x vocabulary-asian.json

---

### Task 5.2: Chapter Other (Ch 1-6)

**Action**: Create chapter-other.json for chapters 1-6

**Target languages**: he, ar, tr, sw

**Process** (SEQUENTIAL - one chapter at a time):
```bash
/translate.sanscrit data/chapters/ch-01/chapter-source.json \
  data/chapters/ch-01/chapter-other.json --languages=he,ar,tr,sw

/translate.sanscrit data/chapters/ch-02/chapter-source.json \
  data/chapters/ch-02/chapter-other.json --languages=he,ar,tr,sw

/translate.sanscrit data/chapters/ch-03/chapter-source.json \
  data/chapters/ch-03/chapter-other.json --languages=he,ar,tr,sw

/translate.sanscrit data/chapters/ch-04/chapter-source.json \
  data/chapters/ch-04/chapter-other.json --languages=he,ar,tr,sw

/translate.sanscrit data/chapters/ch-05/chapter-source.json \
  data/chapters/ch-05/chapter-other.json --languages=he,ar,tr,sw

/translate.sanscrit data/chapters/ch-06/chapter-source.json \
  data/chapters/ch-06/chapter-other.json --languages=he,ar,tr,sw
```

**Output**: 6 x chapter-other.json

---

### Task 5.3: Vocabulary Other (Ch 1-6)

**Action**: Create vocabulary-other.json for chapters 1-6

**Target languages**: he, ar, tr, sw

**Process** (SEQUENTIAL - one chapter at a time):
```bash
/translate.sanscrit data/chapters/ch-01/vocabulary-source.json \
  data/chapters/ch-01/vocabulary-other.json --languages=he,ar,tr,sw

/translate.sanscrit data/chapters/ch-02/vocabulary-source.json \
  data/chapters/ch-02/vocabulary-other.json --languages=he,ar,tr,sw

/translate.sanscrit data/chapters/ch-03/vocabulary-source.json \
  data/chapters/ch-03/vocabulary-other.json --languages=he,ar,tr,sw

/translate.sanscrit data/chapters/ch-04/vocabulary-source.json \
  data/chapters/ch-04/vocabulary-other.json --languages=he,ar,tr,sw

/translate.sanscrit data/chapters/ch-05/vocabulary-source.json \
  data/chapters/ch-05/vocabulary-other.json --languages=he,ar,tr,sw

/translate.sanscrit data/chapters/ch-06/vocabulary-source.json \
  data/chapters/ch-06/vocabulary-other.json --languages=he,ar,tr,sw
```

**Output**: 6 x vocabulary-other.json

---

## Phase 4: Validation & Cleanup ⏳ PENDING

### Task 4.1: Validate All Translation Files

**Action**: Run JSON schema validation

**Checks**:
- [ ] All 18 chapter-asian.json valid
- [ ] All 18 chapter-other.json valid
- [ ] All 18 vocabulary-asian.json valid
- [ ] All 18 vocabulary-other.json valid
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
Phase 0 ──► Phase 1 ──► Phase 2 ──┬──► Phase 5 ──► Phase 4
                        Phase 3 ──┘
```

- Phase 5 depends on Phases 2 and 3 being complete
- Phase 4 requires Phase 5 complete

## Execution Order for Phase 5

Recommended order to minimize context switching:

1. **Task 5.1** - All 6 vocabulary-asian (th, zh-TW, ja, ko)
2. **Task 5.2** - All 6 chapter-other (he, ar, tr, sw)
3. **Task 5.3** - All 6 vocabulary-other (he, ar, tr, sw)

Total: 18 translation operations

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Data loss | Backup in Phase 0 |
| Translation errors | Spot-check in Phase 4 |
| Missing files | Validation in Phase 4 |

## Success Criteria

- [x] All 18 chapters restructured
- [x] Asian chapter translations complete (th, zh-TW, ja, ko) - ch-07 to ch-18
- [x] Other chapter translations complete (he, ar, tr, sw) - ch-07 to ch-18
- [ ] **Asian vocabulary complete for ALL 18 chapters**
- [ ] **Other translations complete for ALL 18 chapters**
- [ ] All new translations marked `approved: false`
- [ ] Old directory structure removed

---

## Approval

- [x] Reviewed by: User
- [x] Approved on: 2026-03-27
- [x] Notes: Plan approved
- [ ] **Re-approval needed for Phase 5 additions**
