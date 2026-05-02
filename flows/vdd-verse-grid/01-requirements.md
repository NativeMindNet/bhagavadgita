# Requirements: Verse Grid (universal shloka navigation chips)

> Version: 1.0  
> Status: DRAFT  
> Last Updated: 2026-05-02  
> Related: `../vdd-bhagavadgita.book-layouts/` (full app layouts)

## Problem Statement

Readers need a **compact map of all shlokas in a chapter** without scrolling a long list. The same visual pattern appears on **phone** (inline under an expanded chapter on Contents) and **tablet** (master pane: chapters + verse grid beside sloka detail). Today that pattern is easy to describe in mockups but easy to implement inconsistently unless **one universal format** defines what a “chip” is, how ranges are labeled, and how selection and taps behave.

This flow isolates those rules so other surfaces (e.g. bookmarks labels `1.32–34`, search hits) can stay aligned with the grid.

## User Stories

### Primary

**As a** reader  
**I want** to see all verse positions in a chapter as tappable chips, including grouped ranges where appropriate  
**So that** I can jump to any shloka quickly

**As a** reader on a tablet  
**I want** the verse grid in the master pane to stay in sync with the sloka open in the detail pane  
**So that** I always see which chip is “current”

### Secondary

**As a** reader  
**I want** range chips (e.g. `4–6`) to behave predictably when tapped  
**So that** I am not surprised by which shloka opens first

## Acceptance Criteria

### Must Have

1. **Given** a chapter with an ordered list of shlokas  
   **When** the verse grid is shown  
   **Then** the UI renders a **sequence of segments** per the universal model in `03-specifications.md` (no overlapping segments; every listed shloka belongs to exactly one segment).

2. **Given** a segment that spans more than one shloka  
   **When** it is displayed  
   **Then** its **display token** follows the labeling rules in `03-specifications.md` (e.g. `4-6` or localized hyphen convention).

3. **Given** a currently open shloka (by id)  
   **When** its segment is visible  
   **Then** that segment appears in the **selected** visual state (same semantics on phone and tablet).

4. **Given** the user taps a segment  
   **When** navigation completes  
   **Then** the app opens **one** target shloka defined by the **tap resolution** policy in `03-specifications.md` (default: first shloka in segment).

### Should Have

1. Segment grouping policy is **configurable** or **data-driven** in the future (e.g. editorial “verse runs” not only consecutive integers) without changing the segment **type** (single vs range).

2. Accessibility: chips have a meaningful combined label (chapter + range) for screen readers.

### Won’t Have (this flow)

- Styling of AppBar, typography of sloka body, audio player (owned by layouts / other flows).
- Full bookmark or search implementation (only **label alignment** with grid tokens is in scope for references).

## Constraints

- **Data**: Must work with existing `Chapter` + ordered `List<Sloka>` from local DB; no schema change required for the baseline format.
- **Platforms**: Same rules on iOS, Android, tablet breakpoints used by `vdd-bhagavadgita.book-layouts`.
- **i18n**: Display tokens use **ASCII digits** and hyphen/minus for range in stored spec examples; UI may localize separator in implementation.

## Open Questions

- [ ] **Range tap**: always first shloka vs bottom sheet to pick shloka inside range (see `03-specifications.md`).
- [ ] **Grouping source**: keep “consecutive positions only” vs introduce explicit grouping from snapshot/editorial metadata.

## References

- Visual source of truth (excerpted): `02-visual.md`
- Canonical format: `03-specifications.md`
- Implementation sketch: `04-plan.md`
- Parent flow: `../vdd-bhagavadgita.book-layouts/01-requirements.md`

---

## Approval

- [ ] Reviewed by: Anton  
- [ ] Approved on:  
- [ ] Notes:
