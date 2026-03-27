# Implementation Plan: Bhagavad Gita JSON Translations

> Version: 1.0
> Status: APPROVED
> Last Updated: 2026-03-26
> Specifications: [02-specifications.md](02-specifications.md)

## Summary

Реализация в 3 фазы:
1. **Setup** — создание структуры и JSON Schema
2. **Conversion** — конвертация CSV → JSON (18 файлов)
3. **Translation** — перевод на 4 языка (ko, th, zh-CN, zh-TW)

## Task Breakdown

### Phase 1: Setup

#### Task 1.1: Create Directory Structure
- **Description**: Создать директории для JSON файлов
- **Commands**:
  ```bash
  mkdir -p data/schema data/chapters data/meta
  ```
- **Dependencies**: None
- **Verification**: Директории существуют
- **Complexity**: Low

#### Task 1.2: Create JSON Schema
- **Description**: Создать файл валидации chapter.schema.json
- **Files**:
  - `data/schema/chapter.schema.json` - Create
- **Dependencies**: Task 1.1
- **Verification**: Schema валидна (jsonschema validate)
- **Complexity**: Low

#### Task 1.3: Create Languages Metadata
- **Description**: Создать файл метаданных языков
- **Files**:
  - `data/meta/languages.json` - Create
- **Dependencies**: Task 1.1
- **Verification**: JSON валиден
- **Complexity**: Low

---

### Phase 2: CSV → JSON Conversion

#### Task 2.1: Write Conversion Script
- **Description**: Python скрипт для конвертации CSV в JSON
- **Files**:
  - `scripts/convert_csv_to_json.py` - Create
- **Dependencies**: Task 1.2
- **Verification**: Script runs without errors
- **Complexity**: Medium

**Script Logic:**
```
1. Load db_books.csv, db_chapters.csv
2. Filter: only BookId in [1, 2, 11, 14] (SM/ШМ)
3. Load Gita_Slokas.csv, Gita_Vocabularies.csv
4. For each chapter 1-18:
   a. Collect slokas from base book (BookId=1)
   b. Add translations from other SM books
   c. Add vocabulary
   d. Save as chapter-XX.json
```

#### Task 2.2: Run Conversion
- **Description**: Выполнить конвертацию всех 18 глав
- **Commands**:
  ```bash
  python scripts/convert_csv_to_json.py
  ```
- **Dependencies**: Task 2.1
- **Verification**: 18 JSON files created in data/chapters/
- **Complexity**: Low

#### Task 2.3: Validate JSON Files
- **Description**: Проверить все файлы против JSON Schema
- **Commands**:
  ```bash
  for f in data/chapters/*.json; do
    jsonschema -i "$f" data/schema/chapter.schema.json
  done
  ```
- **Dependencies**: Task 2.2
- **Verification**: All files pass validation
- **Complexity**: Low

#### Task 2.4: Commit Phase 2
- **Description**: Закоммитить результаты конвертации
- **Dependencies**: Task 2.3
- **Verification**: Git status clean
- **Complexity**: Low

---

### Phase 3: Translation (4 languages × 18 chapters)

#### Task 3.0: Translation Process (Repeat for each chapter)

Для каждой главы (1-18):

##### Task 3.X.1: Generate Translation Prompt
- **Description**: Сформировать prompt для Claude с шлоками главы
- **Input**: `data/chapters/chapter-XX.json`
- **Output**: Formatted prompt with RU → EN → DE/ES → Sanskrit

##### Task 3.X.2: Execute Translation
- **Description**: Перевести главу на ko, th, zh-CN, zh-TW
- **Method**: Claude dialog (manual)
- **Output**: JSON with translations

##### Task 3.X.3: Update Chapter JSON
- **Description**: Добавить переводы в JSON файл
- **Files**:
  - `data/chapters/chapter-XX.json` - Modify
- **Verification**: JSON valid, new languages present with `approved: false`

---

### Phase 3 Detailed: Chapter-by-Chapter

| Chapter | Slokas | Status | Translated |
|---------|--------|--------|------------|
| 1 | 37 | PENDING | |
| 2 | 72 | PENDING | |
| 3 | 43 | PENDING | |
| 4 | 42 | PENDING | |
| 5 | 27 | PENDING | |
| 6 | 45 | PENDING | |
| 7 | 30 | PENDING | |
| 8 | 27 | PENDING | |
| 9 | 34 | PENDING | |
| 10 | 40 | PENDING | |
| 11 | 52 | PENDING | |
| 12 | 16 | PENDING | |
| 13 | 31 | PENDING | |
| 14 | 24 | PENDING | |
| 15 | 20 | PENDING | |
| 16 | 21 | PENDING | |
| 17 | 27 | PENDING | |
| 18 | 75 | PENDING | |

**Total: 663 slokas × 4 languages = 2,652 translations**

---

## Dependency Graph

```
Phase 1: Setup
Task 1.1 ─┬─→ Task 1.2 ─┐
          └─→ Task 1.3 ─┤
                        │
Phase 2: Conversion     │
                        ▼
               Task 2.1 ─→ Task 2.2 ─→ Task 2.3 ─→ Task 2.4
                                                      │
Phase 3: Translation                                  │
                                                      ▼
               ┌─────────────────────────────────────────┐
               │  For each chapter 1-18:                 │
               │  Task 3.X.1 → Task 3.X.2 → Task 3.X.3   │
               └─────────────────────────────────────────┘
```

## File Change Summary

| File | Action | Reason |
|------|--------|--------|
| `data/schema/chapter.schema.json` | Create | JSON validation |
| `data/meta/languages.json` | Create | Language metadata |
| `data/chapters/chapter-01.json` | Create | Chapter 1 content |
| `data/chapters/chapter-02.json` | Create | Chapter 2 content |
| ... | Create | ... |
| `data/chapters/chapter-18.json` | Create | Chapter 18 content |
| `scripts/convert_csv_to_json.py` | Create | Conversion script |

**Total new files: 22** (1 schema + 1 meta + 18 chapters + 1 script + 1 dir structure)

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| CSV encoding issues | Medium | Medium | Use UTF-8-BOM, test first |
| Translation quality | Medium | High | approved: false flag, manual review later |
| Large chapter timeout | Low | Medium | Split into smaller batches if needed |
| Missing data in CSV | Low | Low | Log warnings, skip empty |

## Rollback Strategy

If implementation fails:

1. Phase 2: Delete `data/` directory, re-run conversion
2. Phase 3: Restore chapter JSON from git, re-translate

## Checkpoints

### After Phase 1:
- [x] Directories created
- [x] Schema file valid
- [x] Meta file created

### After Phase 2:
- [x] 18 JSON files exist
- [x] All files pass schema validation
- [x] Sloka count matches (~663 total)
- [x] All 4 languages present (ru, en, de, es)

### After Phase 3 (per chapter):
- [ ] 4 new languages added (ko, th, zh-CN, zh-TW)
- [ ] All new translations have `approved: false`
- [ ] JSON still valid

## Open Implementation Questions

- [x] ~~Batch size for translation~~ → By chapter (18 batches)
- [ ] Need pinyin/romanization for Chinese? → Decide during translation

## Execution Order

```
1. [NOW]      Plan approval
2. [Task 1.*] Setup (5 min)
3. [Task 2.*] Conversion script + run (30 min)
4. [Task 3.*] Translation (18 chapters, ~2-3 hours total)
   - Chapter 1 → verify quality
   - If OK → continue chapters 2-18
```

---

## Approval

- [x] Reviewed by: User
- [x] Approved on: 2026-03-26
- [x] Notes: Ready to implement
