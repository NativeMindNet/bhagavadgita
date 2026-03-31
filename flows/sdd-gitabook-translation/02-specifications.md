# Specifications: GitaBook Translation

> Version: 1.0
> Status: APPROVED
> Last Updated: 2026-03-31
> Requirements: [01-requirements.md](./01-requirements.md)

## Overview

Fill all translation gaps for 12 languages in `data/translated/` using `/translate.sanscrit` command. Process in 3 phases: transliterations first, then Asian languages, then remaining languages.

## Affected Systems

| System | Impact | Notes |
|--------|--------|-------|
| `data/translated/{lang}/` | Create/Modify | Add missing slokas and fix translits |
| `data/translated/{lang}/chapter-XX-{lang}/` | Modify | Add sloka and translit files |
| `data/translated/{lang}/chapter-XX-{lang}_meta.json` | Modify | Update statistics |

## Architecture

### Translation Flow

```
┌─────────────────────────────────────────────────────────────┐
│  FOR EACH: chapter in [1..18]                               │
│    FOR EACH: sloka in chapter.slokaList                     │
│                                                             │
│      ┌─────────────────────────────────────┐                │
│      │  1. LOAD SOURCE TEXTS               │                │
│      │     • ru: chapter-XX-{sloka}-ru_sloka.txt            │
│      │     • en: chapter-XX-{sloka}-en_sloka.txt            │
│      │     • de: chapter-XX-{sloka}-de_sloka.txt            │
│      │     • es: chapter-XX-{sloka}-es_sloka.txt            │
│      │     • sa: chapter-XX-{sloka}-sanskrit_sloka.txt      │
│      └──────────────┬──────────────────────┘                │
│                     ▼                                        │
│      ┌─────────────────────────────────────┐                │
│      │  2. CALL /translate.sanscrit        │                │
│      │     --languages={all target langs}  │                │
│      │     --type={translit|sloka}         │                │
│      └──────────────┬──────────────────────┘                │
│                     ▼                                        │
│      ┌─────────────────────────────────────┐                │
│      │  3. SAVE RESULTS                    │                │
│      │     • chapter-XX-{sloka}-{lang}_sloka.txt            │
│      │     • chapter-XX-{sloka}-{lang}_translit.txt         │
│      └─────────────────────────────────────┘                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Data Models

### Input: Source Texts

For each sloka, load from `data/original/` and `data/sanskrit/`:

| Source | Path |
|--------|------|
| Sanskrit | `data/sanskrit/chapter-{NN}-sanskrit/chapter-{NN}-{sloka}-sanskrit_sloka.txt` |
| Russian | `data/original/ru/chapter-{NN}-ru/chapter-{NN}-{sloka}-ru_sloka.txt` |
| English | `data/original/en/chapter-{NN}-en/chapter-{NN}-{sloka}-en_sloka.txt` |
| German | `data/original/de/chapter-{NN}-de/chapter-{NN}-{sloka}-de_sloka.txt` |
| Spanish | `data/original/es/chapter-{NN}-es/chapter-{NN}-{sloka}-es_sloka.txt` |

### Output: Translated Files

For each translated sloka:

| Type | Path |
|------|------|
| Sloka | `data/translated/{lang}/chapter-{NN}-{lang}/chapter-{NN}-{sloka}-{lang}_sloka.txt` |
| Translit | `data/translated/{lang}/chapter-{NN}-{lang}/chapter-{NN}-{sloka}-{lang}_translit.txt` |

### Transliteration Scripts

| Language | Script | Example |
|----------|--------|---------|
| ja | Katakana | ドゥリタラーシュトラ ウヴァーチャ |
| ko | Hangul | 드리타라시트라 우바차 |
| th | Thai | ธฤตราษฏระ อุวาจ |
| zh-CN | Hanzi (Pinyin) | 德里塔拉什特拉 (délǐtǎlāshítèlā) |
| zh-TW | Hanzi (Traditional) | 德里塔拉什特拉 |
| el | Greek | Δριταράστρα ουβάτσα |
| ka | Georgian | დჰრიტარაშტრა უვაჩა |
| hy | Armenian | Դdelays delays |
| he | Hebrew | דהריטאראשטרא אובאצ'א |
| ar | Arabic | دهريتاراشترا أوفاتشا |
| tr | IAST (Latin) | dhṛtarāṣṭra uvāca |
| sw | IAST (Latin) | dhṛtarāṣṭra uvāca |

## Behavior Specifications

### Happy Path

1. Load all 5 source texts for sloka X.Y
2. Call `/translate.sanscrit` with sources and target languages
3. Receive translations + native transliterations
4. Write files for each language
5. Repeat for next sloka

### Edge Cases

| Case | Trigger | Expected Behavior |
|------|---------|-------------------|
| Missing source | Source file doesn't exist | Skip sloka, log warning |
| Combined slokas | `1.4-6`, `1.8-9` format | Handle as single unit |
| RTL languages | he, ar | Ensure RTL text direction |
| Mixed script fix | th has Latin chars | Regenerate entire translation |

### Error Handling

| Error | Cause | Response |
|-------|-------|----------|
| Translation timeout | API delay | Retry up to 3 times |
| Invalid characters | Encoding issue | Log error, skip sloka |
| Partial result | Incomplete response | Retry translation |

## Batch Processing Strategy

### Вариант C: Сначала транслитерации, потом переводы

Разделяем на два типа задач:
- **Транслитерации** — быстрее (только конверсия скрипта)
- **Переводы** — медленнее (полный перевод текста)

```bash
/translate.sanscrit \
  data/original/ \
  data/translated/ \
  --chapter={NN} \
  --languages=th,zh-CN,zh-TW,ko,ja,el,ka,hy,he,ar,tr,sw \
  --type={translit|sloka}
```

### Execution Order

**Phase 1: Все транслитерации (18 calls)**

| Call | Chapter | Type | Languages |
|------|---------|------|-----------|
| 1-18 | 1-18 | translit | th,zh-CN,zh-TW,ko,ja,el,ka,hy,he,ar,tr,sw |

**После Phase 1:** 7,956 файлов `_translit.txt`

**Phase 2: Переводы для th, zh-CN, zh-TW, ko (12 calls)**

| Call | Chapter | Type | Languages |
|------|---------|------|-----------|
| 19-30 | 7-18 | sloka | th,zh-CN,zh-TW,ko |

**После Phase 2:** th, zh-CN, zh-TW, ko полностью готовы (663 slokas each)

**Phase 3: Переводы для остальных языков (18 calls)**

| Call | Chapter | Type | Languages |
|------|---------|------|-----------|
| 31-48 | 1-18 | sloka | ja,el,ka,hy,he,ar,tr,sw |

**После Phase 3:** Все 12 языков полностью готовы

### Summary

| Phase | Type | Chapters | Languages | Calls |
|-------|------|----------|-----------|-------|
| 1 | translit | 1-18 | all 12 | 18 |
| 2 | sloka | 7-18 | th,zh-CN,zh-TW,ko | 12 |
| 3 | sloka | 1-18 | ja,el,ka,hy,he,ar,tr,sw | 18 |
| **Total** | | | | **48** |

### Benefits

- **Быстрые первые результаты**: транслитерации появляются сразу
- **Приоритет Asian**: th, zh-CN, zh-TW, ko добиваются в Phase 2
- **Параллельность**: после Phase 1 можно проверять качество translits

## Validation

### Post-Translation Checks

For each translated chapter:

1. **File count**: `ls chapter-{NN}-{lang}/*_sloka.txt | wc -l` matches expected
2. **Translit count**: Same count for `*_translit.txt`
3. **Script check**: Translit uses correct native script (not Cyrillic)
4. **No mixed scripts**: Single script per file (except proper nouns)
5. **UTF-8 valid**: All files valid UTF-8

### Quality Spot Checks

After each language completes:
- Read sloka 1.1 - verify correct language
- Read sloka 10.10 - verify mid-book quality
- Read sloka 18.78 - verify final sloka

## Dependencies

### Requires

- Complete `data/original/` (ru, en, de, es) - ✓ exists
- Complete `data/sanskrit/` - ✓ exists
- `/translate.sanscrit` command - ✓ available

### Blocks

- Future vocabulary generation for translated languages

## Open Design Questions

- [x] Batch by chapter or individual sloka? → **By chapter**
- [x] Order of execution? → **Translits first, then slokas**
- [x] Optimization? → **Вариант C: translits → Asian slokas → other slokas**

---

## Approval

- [x] Approved on: 2026-03-31
