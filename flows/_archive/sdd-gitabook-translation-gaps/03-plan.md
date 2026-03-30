# Implementation Plan: Gitabook Translation V2

> Version: 1.0
> Status: DRAFT
> Last Updated: 2026-03-28
> Specifications: [02-specifications.md](02-specifications.md)

## Overview

План выполнения переводов с использованием `/translate.sanscrit`.

**Ограничение:** Только контентная работа, без написания кода/скриптов.

## Phase Summary

| Phase | Description | Operations |
|-------|-------------|------------|
| 1 | Add ja to chapters 1-6 | 6 |
| 2 | Add zh-CN to chapters 7-18 | 12 |
| 3 | Re-translate chapter-other 1-6 | 6 |
| 4 | Translate ШМ comments | 2 |
| 5 | Translate SM comments | 2 |
| **Total** | | **28** |

---

## Phase 1: Add Japanese (ja) to Chapters 1-6

### Task 1.1-1.6: Translate and merge ja

**Process for each chapter (1-6):**

```bash
# Step 1: Translate to ja only
/translate.sanscrit data/chapters/ch-XX/chapter-source.json \
  data/chapters/ch-XX/chapter-ja-temp.json \
  --languages=ja

# Step 2: Manually merge ja into chapter-asian.json
# (Add "ja" key to title and each sloka)

# Step 3: Delete temp file
```

**Commands:**

| Ch | Command |
|----|---------|
| 01 | `/translate.sanscrit data/chapters/ch-01/chapter-source.json data/chapters/ch-01/chapter-ja-temp.json --languages=ja` |
| 02 | `/translate.sanscrit data/chapters/ch-02/chapter-source.json data/chapters/ch-02/chapter-ja-temp.json --languages=ja` |
| 03 | `/translate.sanscrit data/chapters/ch-03/chapter-source.json data/chapters/ch-03/chapter-ja-temp.json --languages=ja` |
| 04 | `/translate.sanscrit data/chapters/ch-04/chapter-source.json data/chapters/ch-04/chapter-ja-temp.json --languages=ja` |
| 05 | `/translate.sanscrit data/chapters/ch-05/chapter-source.json data/chapters/ch-05/chapter-ja-temp.json --languages=ja` |
| 06 | `/translate.sanscrit data/chapters/ch-06/chapter-source.json data/chapters/ch-06/chapter-ja-temp.json --languages=ja` |

---

## Phase 2: Add Simplified Chinese (zh-CN) to Chapters 7-18

### Task 2.1-2.12: Translate and merge zh-CN

**Commands:**

| Ch | Command |
|----|---------|
| 07 | `/translate.sanscrit data/chapters/ch-07/chapter-source.json data/chapters/ch-07/chapter-zhcn-temp.json --languages=zh-CN` |
| 08 | `/translate.sanscrit data/chapters/ch-08/chapter-source.json data/chapters/ch-08/chapter-zhcn-temp.json --languages=zh-CN` |
| 09 | `/translate.sanscrit data/chapters/ch-09/chapter-source.json data/chapters/ch-09/chapter-zhcn-temp.json --languages=zh-CN` |
| 10 | `/translate.sanscrit data/chapters/ch-10/chapter-source.json data/chapters/ch-10/chapter-zhcn-temp.json --languages=zh-CN` |
| 11 | `/translate.sanscrit data/chapters/ch-11/chapter-source.json data/chapters/ch-11/chapter-zhcn-temp.json --languages=zh-CN` |
| 12 | `/translate.sanscrit data/chapters/ch-12/chapter-source.json data/chapters/ch-12/chapter-zhcn-temp.json --languages=zh-CN` |
| 13 | `/translate.sanscrit data/chapters/ch-13/chapter-source.json data/chapters/ch-13/chapter-zhcn-temp.json --languages=zh-CN` |
| 14 | `/translate.sanscrit data/chapters/ch-14/chapter-source.json data/chapters/ch-14/chapter-zhcn-temp.json --languages=zh-CN` |
| 15 | `/translate.sanscrit data/chapters/ch-15/chapter-source.json data/chapters/ch-15/chapter-zhcn-temp.json --languages=zh-CN` |
| 16 | `/translate.sanscrit data/chapters/ch-16/chapter-source.json data/chapters/ch-16/chapter-zhcn-temp.json --languages=zh-CN` |
| 17 | `/translate.sanscrit data/chapters/ch-17/chapter-source.json data/chapters/ch-17/chapter-zhcn-temp.json --languages=zh-CN` |
| 18 | `/translate.sanscrit data/chapters/ch-18/chapter-source.json data/chapters/ch-18/chapter-zhcn-temp.json --languages=zh-CN` |

---

## Phase 3: Re-translate Chapters 1-6 Other Languages

### Task 3.1-3.6: Full translation to he, ar, tr, sw

**Commands:**

| Ch | Command |
|----|---------|
| 01 | `/translate.sanscrit data/chapters/ch-01/chapter-source.json data/chapters/ch-01/chapter-other.json --languages=he,ar,tr,sw` |
| 02 | `/translate.sanscrit data/chapters/ch-02/chapter-source.json data/chapters/ch-02/chapter-other.json --languages=he,ar,tr,sw` |
| 03 | `/translate.sanscrit data/chapters/ch-03/chapter-source.json data/chapters/ch-03/chapter-other.json --languages=he,ar,tr,sw` |
| 04 | `/translate.sanscrit data/chapters/ch-04/chapter-source.json data/chapters/ch-04/chapter-other.json --languages=he,ar,tr,sw` |
| 05 | `/translate.sanscrit data/chapters/ch-05/chapter-source.json data/chapters/ch-05/chapter-other.json --languages=he,ar,tr,sw` |
| 06 | `/translate.sanscrit data/chapters/ch-06/chapter-source.json data/chapters/ch-06/chapter-other.json --languages=he,ar,tr,sw` |

---

## Phase 4: Translate ШМ Comments (12 comments)

### Task 4.0: Prepare comments source file

**Manual step:** Create `data/comments/shm-comments-source.json` with extracted comments from CSV.

**Format:**
```json
{
  "source": "ШМ",
  "comments": [
    {
      "chapter": 4,
      "sloka": "4.13",
      "ru": "* Эти четыре сословия: брахманы..."
    }
  ]
}
```

### Task 4.1: Translate to Asian languages

```bash
/translate.sanscrit data/comments/shm-comments-source.json \
  data/comments/shm-comments-asian.json \
  --languages=th,zh-CN,zh-TW,ja,ko
```

### Task 4.2: Translate to Other languages

```bash
/translate.sanscrit data/comments/shm-comments-source.json \
  data/comments/shm-comments-other.json \
  --languages=he,ar,tr,sw
```

### Task 4.3: Distribute to chapter directories

Copy translated comments to respective `ch-XX/comments-asian.json` and `comments-other.json`.

---

## Phase 5: Translate SM Comments (21 comments)

### Task 5.0: Prepare comments source file

**Manual step:** Create `data/comments/sm-comments-source.json` with extracted comments from CSV.

### Task 5.1: Translate to Asian languages

```bash
/translate.sanscrit data/comments/sm-comments-source.json \
  data/comments/sm-comments-asian.json \
  --languages=th,zh-CN,zh-TW,ja,ko
```

### Task 5.2: Translate to Other languages

```bash
/translate.sanscrit data/comments/sm-comments-source.json \
  data/comments/sm-comments-other.json \
  --languages=he,ar,tr,sw
```

### Task 5.3: Distribute to chapter directories

Copy translated comments to respective chapter directories.

---

## Execution Order

Recommended sequence:

1. **Phase 3** (chapter-other 1-6) - независимые, полная перезапись
2. **Phase 1** (ja for ch 1-6) - требует merge
3. **Phase 2** (zh-CN for ch 7-18) - требует merge
4. **Phase 4** (ШМ comments) - после подготовки source
5. **Phase 5** (SM comments) - после подготовки source

---

## Checklist

### Phase 1: ja for Ch 1-6
- [ ] Ch 01 translated + merged
- [ ] Ch 02 translated + merged
- [ ] Ch 03 translated + merged
- [ ] Ch 04 translated + merged
- [ ] Ch 05 translated + merged
- [ ] Ch 06 translated + merged

### Phase 2: zh-CN for Ch 7-18
- [ ] Ch 07 translated + merged
- [ ] Ch 08 translated + merged
- [ ] Ch 09 translated + merged
- [ ] Ch 10 translated + merged
- [ ] Ch 11 translated + merged
- [ ] Ch 12 translated + merged
- [ ] Ch 13 translated + merged
- [ ] Ch 14 translated + merged
- [ ] Ch 15 translated + merged
- [ ] Ch 16 translated + merged
- [ ] Ch 17 translated + merged
- [ ] Ch 18 translated + merged

### Phase 3: Other for Ch 1-6
- [ ] Ch 01 translated
- [ ] Ch 02 translated
- [ ] Ch 03 translated
- [ ] Ch 04 translated
- [ ] Ch 05 translated
- [ ] Ch 06 translated

### Phase 4: ШМ Comments
- [ ] Source file prepared
- [ ] Asian translated
- [ ] Other translated
- [ ] Distributed to chapters

### Phase 5: SM Comments
- [ ] Source file prepared
- [ ] Asian translated
- [ ] Other translated
- [ ] Distributed to chapters

---

## Approval

- [x] Reviewed by: User
- [x] Approved on: 2026-03-28
- [x] Notes: Plan approved, ready for implementation
