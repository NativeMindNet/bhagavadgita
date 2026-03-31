# Implementation Plan: GitaBook Translation

> Version: 1.0
> Status: DRAFT
> Last Updated: 2026-03-31
> Specifications: [02-specifications.md](./02-specifications.md)

## Summary

Fill translation gaps using `/translate.sanscrit` command in 3 phases:
1. All transliterations first (fast results)
2. Complete th, zh-CN, zh-TW, ko (priority Asian)
3. Add remaining 8 languages

Total: **48 calls**, **14,848 files** generated.

## Task Breakdown

### Phase 1: Транслитерации (18 calls)

Генерация `_translit.txt` для всех 12 языков, все 18 глав.

| Task | Command | Output Files |
|------|---------|--------------|
| 1.1 | `/translate.sanscrit ch01 --type=translit --languages=th,zh-CN,zh-TW,ko,ja,el,ka,hy,he,ar,tr,sw` | 37 × 12 = 444 |
| 1.2 | `/translate.sanscrit ch02 --type=translit --languages=...` | 72 × 12 = 864 |
| 1.3 | `/translate.sanscrit ch03 --type=translit --languages=...` | 43 × 12 = 516 |
| 1.4 | `/translate.sanscrit ch04 --type=translit --languages=...` | 42 × 12 = 504 |
| 1.5 | `/translate.sanscrit ch05 --type=translit --languages=...` | 27 × 12 = 324 |
| 1.6 | `/translate.sanscrit ch06 --type=translit --languages=...` | 45 × 12 = 540 |
| 1.7 | `/translate.sanscrit ch07 --type=translit --languages=...` | 30 × 12 = 360 |
| 1.8 | `/translate.sanscrit ch08 --type=translit --languages=...` | 27 × 12 = 324 |
| 1.9 | `/translate.sanscrit ch09 --type=translit --languages=...` | 34 × 12 = 408 |
| 1.10 | `/translate.sanscrit ch10 --type=translit --languages=...` | 40 × 12 = 480 |
| 1.11 | `/translate.sanscrit ch11 --type=translit --languages=...` | 52 × 12 = 624 |
| 1.12 | `/translate.sanscrit ch12 --type=translit --languages=...` | 16 × 12 = 192 |
| 1.13 | `/translate.sanscrit ch13 --type=translit --languages=...` | 31 × 12 = 372 |
| 1.14 | `/translate.sanscrit ch14 --type=translit --languages=...` | 24 × 12 = 288 |
| 1.15 | `/translate.sanscrit ch15 --type=translit --languages=...` | 20 × 12 = 240 |
| 1.16 | `/translate.sanscrit ch16 --type=translit --languages=...` | 21 × 12 = 252 |
| 1.17 | `/translate.sanscrit ch17 --type=translit --languages=...` | 27 × 12 = 324 |
| 1.18 | `/translate.sanscrit ch18 --type=translit --languages=...` | 75 × 12 = 900 |

**Phase 1 Total:** 663 × 12 = **7,956 `_translit.txt` files**

**Checkpoint:** Verify native scripts (Hangul for ko, Thai for th, etc.)

---

### Phase 2: Переводы th, zh-CN, zh-TW, ko (12 calls)

Генерация `_sloka.txt` для 4 азиатских языков, главы 7-18.

| Task | Command | Output Files |
|------|---------|--------------|
| 2.1 | `/translate.sanscrit ch07 --type=sloka --languages=th,zh-CN,zh-TW,ko` | 30 × 4 = 120 |
| 2.2 | `/translate.sanscrit ch08 --type=sloka --languages=th,zh-CN,zh-TW,ko` | 27 × 4 = 108 |
| 2.3 | `/translate.sanscrit ch09 --type=sloka --languages=th,zh-CN,zh-TW,ko` | 34 × 4 = 136 |
| 2.4 | `/translate.sanscrit ch10 --type=sloka --languages=th,zh-CN,zh-TW,ko` | 40 × 4 = 160 |
| 2.5 | `/translate.sanscrit ch11 --type=sloka --languages=th,zh-CN,zh-TW,ko` | 52 × 4 = 208 |
| 2.6 | `/translate.sanscrit ch12 --type=sloka --languages=th,zh-CN,zh-TW,ko` | 16 × 4 = 64 |
| 2.7 | `/translate.sanscrit ch13 --type=sloka --languages=th,zh-CN,zh-TW,ko` | 31 × 4 = 124 |
| 2.8 | `/translate.sanscrit ch14 --type=sloka --languages=th,zh-CN,zh-TW,ko` | 24 × 4 = 96 |
| 2.9 | `/translate.sanscrit ch15 --type=sloka --languages=th,zh-CN,zh-TW,ko` | 20 × 4 = 80 |
| 2.10 | `/translate.sanscrit ch16 --type=sloka --languages=th,zh-CN,zh-TW,ko` | 21 × 4 = 84 |
| 2.11 | `/translate.sanscrit ch17 --type=sloka --languages=th,zh-CN,zh-TW,ko` | 27 × 4 = 108 |
| 2.12 | `/translate.sanscrit ch18 --type=sloka --languages=th,zh-CN,zh-TW,ko` | 75 × 4 = 300 |

**Phase 2 Total:** 397 × 4 = **1,588 `_sloka.txt` files**

**Checkpoint:** th, zh-CN, zh-TW, ko now 100% complete (663 slokas each)

---

### Phase 3: Переводы ja, el, ka, hy, he, ar, tr, sw (18 calls)

Генерация `_sloka.txt` для 8 оставшихся языков, все 18 глав.

| Task | Command | Output Files |
|------|---------|--------------|
| 3.1 | `/translate.sanscrit ch01 --type=sloka --languages=ja,el,ka,hy,he,ar,tr,sw` | 37 × 8 = 296 |
| 3.2 | `/translate.sanscrit ch02 --type=sloka --languages=ja,el,ka,hy,he,ar,tr,sw` | 72 × 8 = 576 |
| 3.3 | `/translate.sanscrit ch03 --type=sloka --languages=ja,el,ka,hy,he,ar,tr,sw` | 43 × 8 = 344 |
| 3.4 | `/translate.sanscrit ch04 --type=sloka --languages=ja,el,ka,hy,he,ar,tr,sw` | 42 × 8 = 336 |
| 3.5 | `/translate.sanscrit ch05 --type=sloka --languages=ja,el,ka,hy,he,ar,tr,sw` | 27 × 8 = 216 |
| 3.6 | `/translate.sanscrit ch06 --type=sloka --languages=ja,el,ka,hy,he,ar,tr,sw` | 45 × 8 = 360 |
| 3.7 | `/translate.sanscrit ch07 --type=sloka --languages=ja,el,ka,hy,he,ar,tr,sw` | 30 × 8 = 240 |
| 3.8 | `/translate.sanscrit ch08 --type=sloka --languages=ja,el,ka,hy,he,ar,tr,sw` | 27 × 8 = 216 |
| 3.9 | `/translate.sanscrit ch09 --type=sloka --languages=ja,el,ka,hy,he,ar,tr,sw` | 34 × 8 = 272 |
| 3.10 | `/translate.sanscrit ch10 --type=sloka --languages=ja,el,ka,hy,he,ar,tr,sw` | 40 × 8 = 320 |
| 3.11 | `/translate.sanscrit ch11 --type=sloka --languages=ja,el,ka,hy,he,ar,tr,sw` | 52 × 8 = 416 |
| 3.12 | `/translate.sanscrit ch12 --type=sloka --languages=ja,el,ka,hy,he,ar,tr,sw` | 16 × 8 = 128 |
| 3.13 | `/translate.sanscrit ch13 --type=sloka --languages=ja,el,ka,hy,he,ar,tr,sw` | 31 × 8 = 248 |
| 3.14 | `/translate.sanscrit ch14 --type=sloka --languages=ja,el,ka,hy,he,ar,tr,sw` | 24 × 8 = 192 |
| 3.15 | `/translate.sanscrit ch15 --type=sloka --languages=ja,el,ka,hy,he,ar,tr,sw` | 20 × 8 = 160 |
| 3.16 | `/translate.sanscrit ch16 --type=sloka --languages=ja,el,ka,hy,he,ar,tr,sw` | 21 × 8 = 168 |
| 3.17 | `/translate.sanscrit ch17 --type=sloka --languages=ja,el,ka,hy,he,ar,tr,sw` | 27 × 8 = 216 |
| 3.18 | `/translate.sanscrit ch18 --type=sloka --languages=ja,el,ka,hy,he,ar,tr,sw` | 75 × 8 = 600 |

**Phase 3 Total:** 663 × 8 = **5,304 `_sloka.txt` files**

**Checkpoint:** All 12 languages now 100% complete

---

## File Change Summary

| Phase | Files Created | Type |
|-------|---------------|------|
| 1 | 7,956 | `_translit.txt` |
| 2 | 1,588 | `_sloka.txt` |
| 3 | 5,304 | `_sloka.txt` |
| **Total** | **14,848** | new files |

Note: Phase 1 also overwrites 1,064 existing wrong translits (th, zh-CN, zh-TW, ko ch 1-6).

## Execution Command

For each task, run:

```bash
/translate.sanscrit \
  data/original/ \
  data/translated/ \
  --chapter={NN} \
  --type={translit|sloka} \
  --languages={lang1,lang2,...}
```

Save results immediately after each call.

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| API timeout | Medium | Low | Retry 3 times |
| Wrong script in translit | Low | Medium | Spot-check after Phase 1 |
| Mixed script in translation | Low | Medium | Regenerate affected slokas |
| Inconsistent terminology | Low | High | Use same source reading for all langs |

## Rollback Strategy

If implementation fails:
1. Backup exists at `data.backup/` from previous migration
2. Can revert individual language folders
3. Meta files can be regenerated from file counts

## Checkpoints

### After Phase 1 (call 18):
- [ ] All 7,956 `_translit.txt` files exist
- [ ] th translits use Thai script (ไทย)
- [ ] ko translits use Hangul (한글)
- [ ] zh-CN translits use Simplified (简体)
- [ ] ja translits use Katakana (カタカナ)
- [ ] he/ar translits are RTL

### After Phase 2 (call 30):
- [ ] th has 663 `_sloka.txt` files
- [ ] zh-CN has 663 `_sloka.txt` files
- [ ] zh-TW has 663 `_sloka.txt` files
- [ ] ko has 663 `_sloka.txt` files

### After Phase 3 (call 48):
- [ ] All 12 languages have 663 slokas each
- [ ] Total: 7,956 `_sloka.txt` + 7,956 `_translit.txt` = 15,912 files
- [ ] Update meta files with final counts

---

## Approval

- [x] Approved on: 2026-03-31
