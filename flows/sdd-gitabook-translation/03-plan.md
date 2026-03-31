# Optimized Plan: Complete Thai & Chinese Translations

> Version: 2.1
> Status: READY
> Last Updated: 2026-03-31
> Goal: 100% completion for th, zh-CN, zh-TW (slokas + vocabulary)

---

## Current State Analysis (EXACT NUMBERS)

| Component | th | zh-TW | zh-CN |
|-----------|-----|-------|-------|
| **Transliterations** | ✅ 663/663 | ✅ 663/663 | ✅ 663/663 |
| **Slokas (ch 1-6)** | ✅ 266/266 | ✅ 266/266 | ✅ 266/266 |
| **Slokas (ch 7-18)** | ✅ 397/397 | ✅ 397/397 | ❌ 0/397 |
| **Vocabulary** | ⚠️ 3560/3968 (90%) | ⚠️ 3560/3968 (90%) | ❌ 0/3968 (0%) |

### Key Insights

**th и zh-TW имеют 100% slokas!** 
- Нужно перевести только **408 словарных записей** каждый (~10%)
- Это ~1-2 часа работы на язык

**zh-CN имеет только 40% slokas (главы 1-6)**
- Нужно: slokas ch 7-18 (~397 файлов) + словари (~3,968 записей)
- Это ~6-8 часов работы

---

## Optimized Execution Order (FASTEST PATH TO 100%)

### Phase 1: Thai Vocabulary - 408 entries (~1 hour) ⭐ FASTEST
**Why first:** Quickest path to 100% for any language

| Step | Action | Entries | Time |
|------|--------|---------|------|
| 1.1 | Extract 408 English entries | 408 | 1 min |
| 1.2 | Translate to Thai | 408 | 30-45 min |
| 1.3 | Validate & save | 408 | 15 min |

**🎯 RESULT AFTER PHASE 1: th = 100% COMPLETE!**

---

### Phase 2: zh-TW Vocabulary - 408 entries (~1 hour) ⭐ FASTEST
**Why second:** Same quick win as Thai

| Step | Action | Entries | Time |
|------|--------|---------|------|
| 2.1 | Extract 408 English entries | 408 | 1 min |
| 2.2 | Translate to Traditional Chinese | 408 | 30-45 min |
| 2.3 | Validate & save | 408 | 15 min |

**🎯 RESULT AFTER PHASE 2: zh-TW = 100% COMPLETE!**

---

### Phase 3: zh-CN Slokas Chapters 7-18 - 397 files (~4-6 hours)
**Why third:** Biggest remaining gap

| Step | Action | Files | Time |
|------|--------|-------|------|
| 3.1 | Translate chapters 7-18 from source | 397 | 3-5 hours |
| 3.2 | Validate UTF-8 & structure | 397 | 30 min |
| 3.3 | Update meta files | 12 | 15 min |

**🎯 RESULT AFTER PHASE 3: zh-CN slokas = 100% COMPLETE!**

---

### Phase 4: zh-CN Vocabulary - 3,968 entries (~4-6 hours)
**Why fourth:** Can convert from zh-TW (same content, different script)

| Step | Action | Entries | Time |
|------|--------|---------|------|
| 4.1 | Copy zh-TW vocabulary structure | 3,968 | 5 min |
| 4.2 | Convert Traditional → Simplified | 3,968 | 30 min |
| 4.3 | Generate Pinyin transliterations | 3,968 | 30 min |
| 4.4 | Validate & save | 3,968 | 30 min |

**🎯 RESULT AFTER PHASE 4: zh-CN = 100% COMPLETE!**

---

## Summary: Fastest Path to 100%

| Phase | Action | th | zh-TW | zh-CN | Cumulative Time |
|-------|--------|-----|-------|-------|-----------------|
| **START** | - | 90% | 90% | 40% | 0h |
| After Phase 1 | Thai vocab (408 entries) | **100%** 🎯 | 90% | 40% | 1h |
| After Phase 2 | zh-TW vocab (408 entries) | 100% | **100%** 🎯 | 40% | 2h |
| After Phase 3 | zh-CN slokas ch 7-18 | 100% | 100% | **100% slokas** | 6-8h |
| After Phase 4 | zh-CN vocab (3,968 entries) | 100% | 100% | **100%** 🎯 | 10-14h |

---

## Detailed Task Instructions

### Phase 1: Thai Vocabulary Translation

**Files to update:**
- `data/translated/th/chapter-02-th_vocabulary.json` (107 entries)
- `data/translated/th/chapter-03-th_vocabulary.json` (71 entries)
- `data/translated/th/chapter-04-th_vocabulary.json` (62 entries)
- `data/translated/th/chapter-05-th_vocabulary.json` (44 entries)
- `data/translated/th/chapter-06-th_vocabulary.json` (67 entries)
- `data/translated/th/chapter-10-th_vocabulary.json` (57 entries)

**Translation approach:**
1. Load each file
2. Find entries where `meaning` is English-only
3. Translate meaning to Thai
4. Keep existing `transliteration` unchanged
5. Save file

**Sample entry to translate:**
```json
"18497": {
  "meaning": "โอ้ best of the valiant",  // → "โอ้ ยอดนักรบผู้กล้าหาญ"
  "transliteration": "หเอ) มอะหอา-พอาหโอ"  // Keep unchanged
}
```

---

### Phase 2: zh-TW Vocabulary Translation

Same as Phase 1, but translate to Traditional Chinese.

**Sample entry to translate:**
```json
"18497": {
  "meaning": "哦 best of the valiant",  // → "哦 最英勇的勇士"
  "transliteration": "哈埃) 瑪阿哈阿 - 巴阿哈奧"  // Keep unchanged
}
```

---

### Phase 3: zh-CN Slokas Translation

**Source:** `data/original/{ru,en,de,es}/` + `data/sanskrit/`
**Target:** `data/translated/zh-CN/chapter-XX-zh-CN/`

**Chapters to translate:** 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18

**Approach:**
1. For each chapter, load source slokas
2. Translate from Russian/English/Sanskrit
3. Save to zh-CN directory
4. Validate UTF-8 encoding

---

### Phase 4: zh-CN Vocabulary Creation

**Source:** zh-TW vocabulary files
**Target:** zh-CN vocabulary files

**Approach:**
1. Load zh-TW vocabulary
2. Convert Traditional Chinese → Simplified Chinese
3. Generate Pinyin transliterations
4. Save to zh-CN directory

**Conversion examples:**
- 哦 → 哦 (same)
- 勇士 → 勇士 (same)
- 靈魂 → 灵魂
- 神聖 → 神圣

---

## Detailed Task Breakdown

### Task 1.1: Check Archive for zh-CN Slokas

```bash
# Check if zh-CN slokas exist in alternative archive locations
ls -la /Users/anton/proj/gita/_archive/data.backup/chapters/ch-*/chapter-zh-CN.json
ls -la /Users/anton/proj/gita/_archive/data.backup/translated/zh-CN/
```

**If found:** Restore using `restore_translations.py` with zh-CN support
**If not found:** Proceed to Task 1.2

---

### Task 1.2: Translate zh-CN Slokas Chapters 7-18

**Source files:**
- `data/original/{ru,en,de,es}/chapter-XX-{lang}/`
- `data/sanskrit/chapter-XX-sanskrit/`

**Target:**
- `data/translated/zh-CN/chapter-XX-zh-CN/chapter-XX-Y.Y-zh-CN_sloka.txt`

**Approach:**
1. Use existing translation tool/script
2. Process chapters 7-18 sequentially
3. Save after each chapter

---

### Task 2.1-2.4: Thai Vocabulary Translation

**Script needed:** `translate_vocabulary.py`

```python
# Pseudocode
for chapter in 1..18:
    vocab = load(f"data/translated/th/chapter-{chapter:02d}-th_vocabulary.json")
    for word_id, entry in vocab['vocabulary'].items():
        if is_english_only(entry['meaning']):
            entry['meaning'] = translate_to_thai(entry['meaning'])
    save(vocab)
```

---

### Task 3.1-3.4: zh-TW Vocabulary Translation

Same approach as Thai, but translate to Traditional Chinese.

---

### Task 4.1-4.4: zh-CN Vocabulary Creation

**Approach:**
1. Use zh-TW vocabulary as template (same structure)
2. Convert Traditional Chinese → Simplified Chinese
3. Generate Pinyin transliterations from Sanskrit

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| zh-CN slokas not in archive | Medium | Medium | Have translation script ready |
| Vocabulary translation quality | Low | High | Spot-check after each chapter |
| Character encoding issues | Low | Medium | Validate UTF-8 after each save |
| Inconsistent terminology | Medium | Medium | Use glossary for key terms |

---

## Validation Checklist

### After Phase 1 (zh-CN slokas):
- [ ] zh-CN has 663 sloka files
- [ ] All files valid UTF-8
- [ ] No mixed scripts (Simplified only)
- [ ] Chapter meta files updated

### After Phase 2 (Thai vocabulary):
- [ ] All ~3,000 entries have Thai meaning (no English)
- [ ] Transliterations preserved
- [ ] Spot-check 10 random entries for quality

### After Phase 3 (zh-TW vocabulary):
- [ ] All ~3,000 entries have Traditional Chinese meaning
- [ ] Transliterations preserved
- [ ] Spot-check 10 random entries for quality

### After Phase 4 (zh-CN vocabulary):
- [ ] All ~3,000 entries have Simplified Chinese meaning
- [ ] Pinyin transliterations generated
- [ ] Spot-check 10 random entries for quality

---

## Final State

| Component | th | zh-TW | zh-CN |
|-----------|-----|-------|-------|
| **Transliterations** | ✅ 663 | ✅ 663 | ✅ 663 |
| **Slokas** | ✅ 663 | ✅ 663 | ✅ 663 |
| **Vocabulary** | ✅ ~3,000 | ✅ ~3,000 | ✅ ~3,000 |
| **STATUS** | 🎯 **100%** | 🎯 **100%** | 🎯 **100%** |

**Total estimated time:** 9-16 hours

---

## Next Steps

1. **Immediate:** Run Task 1.1 (check archive for zh-CN slokas)
2. **Based on result:** Either restore from archive OR translate
3. **Then:** Execute vocabulary translation in order: th → zh-TW → zh-CN
