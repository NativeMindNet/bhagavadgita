# Status: vdd-verse-grid

## Current Phase

REQUIREMENTS (DRAFTING)

## Phase Status

DRAFTING

## Last Updated

2026-05-02 by Cursor Agent

## Blockers

- None

## Progress

- [x] Requirements drafted (extracted from layouts + universal format)
- [ ] Requirements approved
- [x] Visual mockups drafted (aligned with parent `vdd-bhagavadgita.book-layouts` approval 2026-04-30)
- [ ] Visual approved (for this flow as standalone)
- [x] Specifications drafted
- [ ] Specifications approved
- [x] Plan drafted
- [ ] Plan approved
- [ ] Implementation started
- [ ] Implementation complete
- [ ] Documentation drafted
- [ ] Documentation approved

## Context Notes

- **Fork / extract**: Verse grid visuals and behavior were originally defined in `flows/vdd-bhagavadgita.book-layouts/`. This flow owns the **canonical universal format** for verse chips and ranges; layouts flow links here.
- **Current app behavior** (`chapter_expandable_tile.dart`): segments are **maximal consecutive runs** by `Sloka.position` in list order; label uses `name` suffix after `.` when present, else `position`; tap always opens **first** `Sloka` in the segment.

## Fork History

- Extracted from: `vdd-bhagavadgita.book-layouts` on 2026-05-02
- Reason: Isolate reusable “verse grid” semantics (phone + tablet) from full layouts VDD.

## Next Actions

1. User review: universal segment format in `03-specifications.md`
2. Approve requirements → visual (already copied) → specs → plan
3. Optional: promote `_SlokaRange` to shared `VerseGridSegment` type in app code per plan

## References

- Parent layouts: `../vdd-bhagavadgita.book-layouts/02-visual.md` (full app context)
- Requirements: `01-requirements.md`
- Specifications (format): `03-specifications.md`
