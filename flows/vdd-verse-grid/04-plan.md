# Implementation Plan: Verse Grid (UVGF in code)

> Version: 1.0  
> Status: DRAFT  
> Last Updated: 2026-05-02  
> Specifications: `03-specifications.md`

## Goal

Align runtime code with **Universal Verse Grid Format** (`03-specifications.md`): explicit segment model, shared builder, consistent labels and selection.

## Current state

- `features/contents/widgets/chapter_expandable_tile.dart` implements grouping via private `_SlokaRange` and `_groupSlokaRanges` — behavior matches UVGF **consecutive run** policy but types are not shared or named per spec.

## Tasks

### T1 — Extract segment model (optional refactor)

1. Add `lib/features/contents/verse_grid_segment.dart` (or `lib/ui/verse_grid/` if reused broadly) with:
   - `VerseGridSegment` holding `List<Sloka> members` (or ids + resolve).
   - `String displayToken` getter implementing section 1.2 of `03-specifications.md`.
2. Add `List<VerseGridSegment> buildVerseGridSegments(List<Sloka> slokas)` implementing section 2 baseline policy.
3. Replace private `_SlokaRange` / `_groupSlokaRanges` in `chapter_expandable_tile.dart` with the shared builder.

**Files:** new dart file, `chapter_expandable_tile.dart`

**Risk:** Low; behavior should be unchanged if tests cover grouping.

### T2 — Tests

1. Unit tests for `buildVerseGridSegments` on edge cases: empty list, single sloka, all consecutive, gaps `[1,2,4,5]`.
2. Optional: widget test that selected sloka id in middle of range highlights the range chip.

**Files:** `test/.../verse_grid_segment_test.dart`

### T3 — Tablet parity

1. Confirm `contents_chapter_scaffold.dart` uses `ChapterExpandableTile` without duplicating grid logic (already imports tile — verify no second grouping path).

**Files:** `features/tablet/contents_chapter_scaffold.dart` (read-only check or small cleanup)

### T4 — Documentation

1. In app code, one-line doc reference to `flows/vdd-verse-grid/03-specifications.md` on the public builder if exported.

## Dependency order

```
T1 → T2 → T3
     ↘ T4 (can parallel with T2)
```

## Out of scope

- Changing tap policy to chooser (requires product decision in `01-requirements.md`).
- Bookmarks list label refactor (separate cosmetic task).

## Checkpoints

- [ ] `flutter test` passes for new unit tests
- [ ] Manual: expand chapter 1 on phone + tablet, selection matches open sloka

---

## Approval

- [ ] Reviewed by:  
- [ ] Approved on:  
- [ ] Notes:
