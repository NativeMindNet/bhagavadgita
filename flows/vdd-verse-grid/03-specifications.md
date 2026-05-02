# Specifications: Universal Verse Grid Format (UVGF)

> Version: 1.0  
> Status: DRAFT  
> Last Updated: 2026-05-02  
> Requirements: `01-requirements.md`  
> Visual: `02-visual.md`

## Purpose

Define a **single canonical representation** of “what the verse grid shows” so that:

- Contents (phone) and tablet master pane render the **same** chip sequence for the same chapter.
- **Selection** and **tap** behavior are specified once.
- Other UI (bookmarks row `1.32-34`, search result lines) can reuse the same **display token** rules where applicable.

This document is **presentation-layer**: it does not change Drift schema; it describes inputs/outputs of the grid builder and chip widget.

---

## 1. Core types (logical model)

### 1.1 `VerseGridSegment`

A segment is one tappable chip in the grid.

| Field | Type | Meaning |
|--------|------|---------|
| `slokaIds` | ordered list of ids | All `Sloka` rows belonging to this chip, in **reading order** (same order as input list). |
| `kind` | `single` \| `range` | `single` if `slokaIds.length == 1`, else `range`. |

**Invariants**

- Segments form a **partition** of the chapter’s shlokas for the current view: every input sloka appears in exactly one segment, order preserved.
- Within a segment, `slokaIds` follow ascending list index (not necessarily global id order).

### 1.2 Display token (`displayToken`)

String shown on the chip (e.g. `19`, `4-6`, `32-34`).

**Rules** (baseline, ASCII-friendly):

1. Let `label(s)` for one sloka be: if `s.name` contains `.`, use the substring **after the last `.`**; else use decimal string of `s.position`.
2. **Single** segment: `displayToken = label(first sloka)`.
3. **Range** segment: `displayToken = label(first) + "-" + label(last)` (hyphen U+002D).

**Examples**

| Sloka names (suffix) | Segment kind | displayToken |
|----------------------|--------------|--------------|
| `1.19` only | single | `19` |
| `1.4`…`1.6` | range | `4-6` |
| positions only, no dot in name | single | `7` |

**Note:** If `name` suffixes are not monotonic even when positions are, the spec still allows `4-6` as **positional** labels from first/last in the segment; product may later clamp to `position`-only labels — document deviation in implementation log.

---

## 2. Segment builder (grouping policy)

**Input:** `List<Sloka> slokas` sorted the same way as the chapter list API returns (canonical chapter order).

**Baseline policy — “consecutive run merge”** (current Flutter implementation):

1. Walk `slokas` in order.
2. Start a new segment whenever `current.position != previous.position + 1` (using integer `Sloka.position` within chapter).
3. Each segment’s `slokaIds` = ordered ids in that run.

**Future policies** (same `VerseGridSegment` shape):

- **Explicit groups**: snapshot provides `groupId` per sloka; merge same `groupId` into one segment.
- **Never merge**: always `kind: single` (debug or A/B).

The UI widget should accept **already-built** `List<VerseGridSegment>` so grouping is testable separately from `Wrap` layout.

---

## 3. Selection

**Input:** `selectedSlokaId` (nullable).

**Rule:** Segment `S` is **selected** iff `selectedSlokaId` is non-null and `S.slokaIds` contains that id.

**UI:** Selected chip uses the same visual treatment on phone and tablet (e.g. filled accent — see layouts theme).

---

## 4. Tap resolution

**Default (approved for MVP):** On tap, navigate to the **first** sloka in `slokaIds` (smallest index in the ordered segment list).

**Alternative (open):** Show a small chooser for ranges with length > 1; then navigate to chosen sloka.

Implementations must document which policy they ship in `05-implementation-log.md`.

---

## 5. Layout widget contract

### Inputs

- `segments: List<VerseGridSegment>` (or internal type with `slokas: List<Sloka>` equivalent).
- `selectedSlokaId: int?`
- `onSlokaSelected(Sloka target)` callback after tap resolution.

### Layout

- Use a **flow** layout (`Wrap`-style) with consistent horizontal and run spacing (values from design system in layouts flow).
- Chips: material **ChoiceChip** or equivalent; `showCheckmark: false`; label = `displayToken`.

### Performance

- Typical chapter size ≤ 100 segments after merge; building segments is O(n). No async required for grid build.

---

## 6. Integration map

| Surface | Role |
|---------|------|
| `ChapterExpandableTile` | Builds segments from `slokas`, renders grid when expanded |
| Tablet `contents_chapter_scaffold` | Reuses same tile / same builder for master pane |
| Bookmarks / search (optional) | Use section 1.2 label rules for **text** consistency with chips |

---

## 7. Testing

- Unit: given fixed `List<Sloka>` with positions `[1,2,3,5,6]`, expect segments `[1-3], [5-6]` with correct `displayToken`s.
- Widget: goldens for selected single vs selected inside range.
- Tap: first sloka id is passed to navigation.

---

## Approval

- [ ] Reviewed by:  
- [ ] Approved on:  
- [ ] Notes:
