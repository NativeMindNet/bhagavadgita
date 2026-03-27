# Implementation Plan: Gitabook Translation Vocabulary JSON

> Version: 1.0
> Status: APPROVED
> Last Updated: 2026-03-26
> Specifications: [02-specifications.md](02-specifications.md)

## Summary

Реализация в 3 фазы:
1. **Setup** — создание структуры директорий и JSON Schema
2. **Conversion** — конвертация CSV → JSON (18 файлов vocabulary)
3. **Translation** — комбинированный перевод глав + словаря (ko, th, zh-CN, zh-TW, ja)

## Task Breakdown

### Phase 1: Setup

#### Task 1.1: Create Directory Structure
- **Description**: Создать директорию для vocabulary JSON файлов
- **Commands**:
  ```bash
  mkdir -p data/vocabulary
  ```
- **Dependencies**: None
- **Verification**: Директория существует
- **Complexity**: Low

#### Task 1.2: Create JSON Schema
- **Description**: Создать файл валидации vocabulary.schema.json
- **Files**:
  - `data/schema/vocabulary.schema.json` - Create
- **Dependencies**: Task 1.1
- **Verification**: Schema валидна (jsonschema validate)
- **Complexity**: Low

---

### Phase 2: CSV → JSON Conversion

#### Task 2.1: Write Conversion Script
- **Description**: Python скрипт для конвертации CSV vocabulary в JSON
- **Files**:
  - `scripts/convert_vocabulary_to_json.py` - Create
- **Dependencies**: Task 1.2
- **Verification**: Script runs without errors
- **Complexity**: Medium

**Script Logic:**
```
1. Load Gita_Vocabularies.csv (delimiter: ;)
2. Load Gita_Slokas.csv to map SlokaId → ChapterId
3. For each chapter 1-18:
   a. Filter vocabulary for chapter
   b. Create JSON structure with ru/en meanings
   c. Save as vocab_XX.json
```

#### Task 2.2: Run Conversion
- **Description**: Выполнить конвертацию всех 18 файлов vocabulary
- **Commands**:
  ```bash
  python scripts/convert_vocabulary_to_json.py
  ```
- **Dependencies**: Task 2.1
- **Verification**: 18 JSON files created in data/vocabulary/
- **Complexity**: Low

#### Task 2.3: Validate JSON Files
- **Description**: Проверить все файлы против JSON Schema
- **Commands**:
  ```bash
  for f in data/vocabulary/*.json; do
    jsonschema -i "$f" data/schema/vocabulary.schema.json
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

### Phase 3: Combined Translation (Automated via Agent)

#### Task 3.0: Translation Process (Automated for each chapter)

Для каждой главы (1-18):

##### Task 3.X.1: Extract Chapter + Vocabulary
- **Description**: Извлечь шлоки и словарь для главы
- **Input**: `data/chapters/chapter-XX.json`, `data/vocabulary/vocab_XX.json`
- **Output**: Combined translation prompt

##### Task 3.X.2: Execute Translation via Agent
- **Description**: Запустить агента для перевода на ko, th, zh-CN, zh-TW, ja
- **Method**: Sequential agent execution per chapter
- **Output**: JSON with translations + transliteration

##### Task 3.X.3: Save Translations Immediately
- **Description**: Сохранить переводы в файлы сразу после обработки агентом
- **Files**:
  - `data/chapters/chapter-XX-asian-translations.json` - Create/Update
  - `data/vocabulary/vocab_XX.json` - Modify (add asian languages + transliteration)
- **Verification**: JSON valid, new languages present with `approved: false`

##### Task 3.X.4: Validate & Continue
- **Description**: Валидировать результат и продолжить со следующей главой
- **Blocking**: Next chapter translation waits for current chapter to complete

---

### Phase 3 Detailed: Chapter-by-Chapter (Automated)

| Chapter | Slokas | Vocabulary | Status |
|---------|--------|------------|--------|
| 1 | 37 | 498 | PENDING |
| 2 | 72 | 858 | PENDING |
| 3 | 43 | 512 | PENDING |
| 4 | 42 | 502 | PENDING |
| 5 | 27 | 365 | PENDING |
| 6 | 45 | 548 | PENDING |
| 7 | 30 | 403 | PENDING |
| 8 | 27 | 365 | PENDING |
| 9 | 34 | 408 | PENDING |
| 10 | 40 | 454 | PENDING |
| 11 | 52 | 683 | PENDING |
| 12 | 16 | 235 | PENDING |
| 13 | 31 | 411 | PENDING |
| 14 | 24 | 327 | PENDING |
| 15 | 20 | 303 | PENDING |
| 16 | 21 | 320 | PENDING |
| 17 | 27 | 335 | PENDING |
| 18 | 75 | 840 | PENDING |

**Total: ~663 slokas + ~7,767 vocabulary words × 5 languages = ~42,150 translations**

---

## Automated Translation Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  FOR each chapter 1-18 (SEQUENTIAL):                        │
├─────────────────────────────────────────────────────────────┤
│  1. Extract chapter data (slokas + vocabulary)              │
│  2. Launch translation agent                                │
│  3. Agent translates to ko, th, zh-CN, zh-TW, ja            │
│  4. Agent adds transliteration (th, zh, ko, ja scripts)     │
│  5. Save results IMMEDIATELY:                               │
│     - chapter-XX-asian-translations.json                    │
│     - vocab_XX.json (updated)                               │
│  6. Validate JSON                                           │
│  7. CONTINUE to next chapter only after success             │
└─────────────────────────────────────────────────────────────┘
```

**Key Requirements:**
- **Sequential execution**: Chapter N+1 waits for Chapter N to complete
- **Immediate save**: Results saved before next agent starts
- **No manual intervention**: Fully automated pipeline
- **Error handling**: If chapter fails, log error and continue

## File Change Summary

| File | Action | Reason |
|------|--------|--------|
| `data/vocabulary/` | Create dir | Vocabulary storage |
| `data/schema/vocabulary.schema.json` | Create | JSON validation |
| `data/vocabulary/vocab_01.json` | Create | Chapter 1 vocabulary |
| `data/vocabulary/vocab_02.json` | Create | Chapter 2 vocabulary |
| ... | Create | ... |
| `data/vocabulary/vocab_18.json` | Create | Chapter 18 vocabulary |
| `scripts/convert_vocabulary_to_json.py` | Create | Conversion script |
| `scripts/translate_chapter_with_vocabulary.py` | Create | Translation script |
| `data/chapters/chapter-XX-asian-translations.json` | Create | Translation overlay (18 files) |

**Total new files: 40+** (1 schema + 18 vocabulary + 18 translation overlays + 2 scripts + 1 dir)

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| CSV encoding issues | Medium | Medium | Use UTF-8-BOM, test first |
| SlokaId mapping fail | Low | High | Validate mapping before conversion |
| Translation quality | Medium | High | `approved: false` flag, manual review |
| Large context timeout | Low | Medium | Split vocabulary if needed |
| Terminology mismatch | Medium | Medium | Combined context prevents this |

## Rollback Strategy

If implementation fails:

1. Phase 2: Delete `data/vocabulary/` directory, re-run conversion
2. Phase 3: Restore vocabulary JSON from git, re-translate

## Checkpoints

### After Phase 1:
- [ ] Directory `data/vocabulary/` created
- [ ] Schema file valid

### After Phase 2:
- [ ] 18 vocabulary JSON files exist
- [ ] All files pass schema validation
- [ ] Word count matches source CSV (~935 total)
- [ ] RU/EN meanings present

### After Phase 3 (per chapter):
- [ ] 5 new languages added (ko, th, zh-CN, zh-TW, ja)
- [ ] All new translations have `approved: false`
- [ ] JSON still valid
- [ ] Terminology consistent between slokas and vocabulary

## Open Implementation Questions

- [x] ~~Batch size for translation~~ → By chapter (18 batches, combined with vocabulary)
- [x] ~~Where to store asian translations~~ → `chapter-XX-asian-translations.json`
- [ ] Need pinyin/romanization for Chinese vocabulary? → Decide during translation

## Execution Order

```
1. [NOW]       Plan approval
2. [Task 1.*]  Setup (5 min)
3. [Task 2.*]  Conversion script + run (30 min)
4. [Task 3.*]  Translation (18 chapters, ~3-4 hours total)
   - Chapter 1 → verify quality + terminology consistency
   - If OK → continue chapters 2-18
```

---

## Approval

- [x] Reviewed by: User
- [x] Approved on: 2026-03-26
- [x] Notes: Ready to implement. Combined chapter+vocabulary translation for consistency.
