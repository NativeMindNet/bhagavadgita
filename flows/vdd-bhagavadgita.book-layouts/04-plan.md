# Implementation Plan: Bhagavad Gita Book Layouts (Flutter)

> Version: 1.0  
> Status: APPROVED  
> Last Updated: 2026-04-30  
> Specifications: `03-specifications.md`

## Summary

Implement the approved layouts by introducing a small **design system layer** (theme, colors, typography), then refactoring each existing screen to match `02-visual.md`. Keep changes UI-focused and incremental, verifying after each phase with a quick run and a short manual checklist.

Guiding constraints:
- Preserve existing Drift + repositories behavior.
- Prefer **new reusable widgets** over copy/paste styles.
- Keep Material 3 unless it blocks parity (decision recorded as open question).

## Task Breakdown

### Phase 1: Foundation (Design System + primitives)

#### Task 1.1: Add design tokens and theme wiring
- **Description**: Replace seed theme with explicit color palette and basic typography mapping.
- **Files**:
  - `app/bhagavadgita.book/lib/app/app.dart` - Modify
  - `app/bhagavadgita.book/lib/app/theme/gita_theme.dart` - Create
  - `app/bhagavadgita.book/lib/app/theme/gita_colors.dart` - Create
- **Dependencies**: None
- **Verification**:
  - App boots; AppBar color/foreground look consistent in Contents/Settings
- **Complexity**: Medium

#### Task 1.2: Add core reusable UI widgets (v1)
- **Description**: Introduce reusable widgets used across multiple screens.
- **Files**:
  - `app/bhagavadgita.book/lib/features/shared/widgets/section_header.dart` - Create
  - `app/bhagavadgita.book/lib/features/shared/widgets/author_badge.dart` - Create
  - `app/bhagavadgita.book/lib/features/shared/widgets/quote_card.dart` - Create (optional stub)
  - `app/bhagavadgita.book/lib/features/shared/widgets/audio_player_bar.dart` - Create (layout shell)
- **Dependencies**: Task 1.1
- **Verification**:
  - Widgets render in isolation when placed in a screen
- **Complexity**: Low

### Phase 2: Screen layout parity (phone)

#### Task 2.1: Splash screen visual parity
- **Description**: Match gradient background and progress layout from mockups; keep retry behavior.
- **Files**:
  - `app/bhagavadgita.book/lib/features/splash/splash_screen.dart` - Modify
- **Dependencies**: Task 1.1
- **Verification**:
  - Launch shows gradient + centered title + progress
  - Error state still retries on tap
- **Complexity**: Low

#### Task 2.2: Contents screen parity (AppBar, list rows, quote slot, empty state)
- **Description**: Red AppBar with actions; list styling and empty state aligned to visual.
- **Files**:
  - `app/bhagavadgita.book/lib/features/contents/contents_screen.dart` - Modify
- **Dependencies**: Task 1.1, Task 1.2
- **Verification**:
  - Chapters list looks correct
  - Empty state is readable and aligned (when DB empty)
- **Complexity**: Medium

#### Task 2.3: Chapter screen parity (bookmark indicator)
- **Description**: Align row layout and bookmark indicator visuals with mockups.
- **Files**:
  - `app/bhagavadgita.book/lib/features/reader/chapter_screen.dart` - Modify
- **Dependencies**: Task 1.1
- **Verification**:
  - Bookmarked slokas show filled bookmark icon (and themed color)
- **Complexity**: Low

#### Task 2.4: Sloka detail parity (sections + note + audio bar shell)
- **Description**: Add section headers, separators, Sanskrit centering/font hook, commentary author badge, and persistent audio bar layout shell.
- **Files**:
  - `app/bhagavadgita.book/lib/features/reader/sloka_screen.dart` - Modify
  - `app/bhagavadgita.book/lib/features/shared/widgets/section_header.dart` - Use
  - `app/bhagavadgita.book/lib/features/shared/widgets/author_badge.dart` - Use
  - `app/bhagavadgita.book/lib/features/shared/widgets/audio_player_bar.dart` - Use
- **Dependencies**: Task 1.2
- **Verification**:
  - Toggling reader settings hides/shows sections correctly
  - Note editor still saves/loads
  - Bottom audio bar layout is present (even if non-functional)
- **Complexity**: High

#### Task 2.5: Settings screen parity (sections, headers, toggle styling)
- **Description**: Add section headers and align toggles’ visuals to design tokens while preserving behavior.
- **Files**:
  - `app/bhagavadgita.book/lib/features/settings/settings_screen.dart` - Modify
- **Dependencies**: Task 1.1
- **Verification**:
  - Toggle changes reflect on Sloka screen
  - Persist across restart
- **Complexity**: Medium

### Phase 3: Search circular reveal + scrim

#### Task 3.1: Search screen structure updates (white appbar, scrim-ready layout)
- **Description**: Update Search screen UI to match white AppBar style and layout expectations.
- **Files**:
  - `app/bhagavadgita.book/lib/features/search/search_screen.dart` - Modify
- **Dependencies**: Task 1.1
- **Verification**:
  - Search UI looks consistent and remains functional
- **Complexity**: Medium

#### Task 3.2: Circular reveal transition for opening/closing search
- **Description**: Implement a circular reveal route/transition when navigating to Search from Contents.
- **Files**:
  - `app/bhagavadgita.book/lib/features/contents/contents_screen.dart` - Modify (use custom route)
  - `app/bhagavadgita.book/lib/features/search/search_route.dart` - Create
  - `app/bhagavadgita.book/lib/features/search/widgets/circular_reveal.dart` - Create
- **Dependencies**: Task 3.1
- **Verification**:
  - Transition duration ~300ms
  - Looks like circular reveal from search icon position (best-effort)
- **Complexity**: High

### Phase 4: Tablet master-detail scaffolds

#### Task 4.1: Add breakpoint + tablet navigation scaffolds
- **Description**: Implement dual-pane layouts for Contents→Chapter and Chapter→Sloka on wide screens.
- **Files**:
  - `app/bhagavadgita.book/lib/features/tablet/breakpoints.dart` - Create
  - `app/bhagavadgita.book/lib/features/tablet/contents_chapter_scaffold.dart` - Create
  - `app/bhagavadgita.book/lib/features/tablet/chapter_sloka_scaffold.dart` - Create
  - `app/bhagavadgita.book/lib/features/contents/contents_screen.dart` - Modify (route to tablet scaffold when wide)
  - `app/bhagavadgita.book/lib/features/reader/chapter_screen.dart` - Modify (support embedding)
  - `app/bhagavadgita.book/lib/features/reader/sloka_screen.dart` - Modify (support embedding)
- **Dependencies**: Phase 2 complete
- **Verification**:
  - Resizing / running on tablet width shows dual-pane
  - Selection on left updates right pane without full navigation push (where appropriate)
- **Complexity**: High

### Phase 5: Polish + checks

#### Task 5.1: Fonts integration decision and implementation
- **Description**: Implement PT Sans via `google_fonts` and decide Devanagari font approach (licensing).
- **Files**:
  - `app/bhagavadgita.book/pubspec.yaml` - Modify (dependency + font assets if needed)
  - `app/bhagavadgita.book/lib/app/theme/gita_theme.dart` - Modify
- **Dependencies**: Task 1.1
- **Verification**:
  - Typography matches requirements table as closely as possible
- **Complexity**: Medium

#### Task 5.2: Manual QA pass against mockups
- **Description**: Quick pass across all 9 screens; ensure no regressions in DB-driven flows.
- **Files**: None (or small fixes in touched screens)
- **Dependencies**: All phases
- **Verification**:
  - Checklist in “Manual Verification” passes
- **Complexity**: Medium

## Dependency Graph

```
Task 1.1 ─→ Task 1.2 ─→ Task 2.2 ─┬─→ Task 2.4 ─→ Task 4.1
                │                ├─→ Task 2.3
                │                └─→ Task 2.5
Task 2.1 ───────┘

Task 3.1 ─→ Task 3.2

Task 5.1 (can happen anytime after 1.1)
Task 5.2 (final)
```

## File Change Summary

| File | Action | Reason |
|------|--------|--------|
| `app/bhagavadgita.book/lib/app/theme/gita_colors.dart` | Create | Centralize approved palette |
| `app/bhagavadgita.book/lib/app/theme/gita_theme.dart` | Create | Centralize ThemeData/typography |
| `app/bhagavadgita.book/lib/app/app.dart` | Modify | Use explicit theme |
| `app/bhagavadgita.book/lib/features/shared/widgets/*` | Create | Reuse across screens |
| `app/bhagavadgita.book/lib/features/search/search_route.dart` | Create | Circular reveal route |
| `app/bhagavadgita.book/lib/features/tablet/*` | Create | Dual-pane scaffolds |
| `app/bhagavadgita.book/lib/features/*/*_screen.dart` | Modify | Apply layout parity |

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Circular reveal feels off | Med | Med | Implement best-effort custom clip; tune duration/curve; fall back to fade if needed |
| Tablet scaffolds complicate navigation | Med | High | Keep tablet-only code isolated; embed screens with minimal assumptions |
| Font licensing (Kohinoor) | High | Med | Provide fallback Devanagari font (e.g. Noto Sans Devanagari) if licensing blocks |
| Styling regressions | Med | Med | Small PR-sized commits; verify after each phase |

## Rollback Strategy

If parity refactor causes issues:
1. Revert the last phase commit(s) (theme/screens are staged by phases).
2. Keep design system files; re-apply incrementally.

## Checkpoints

After each phase, verify:
- [ ] App builds and runs
- [ ] No crashes during navigation
- [ ] Contents → Chapter → Sloka path still works
- [ ] Settings toggles still persist and affect Sloka

## Open Implementation Questions

- [ ] Decide Material 3 vs Material 2 (keep M3 unless blocked)
- [ ] Confirm tablet breakpoint and exact pane ratio
- [ ] Decide Devanagari font strategy (Kohinoor vs fallback)

---

## Approval

- [x] Reviewed by: Anton
- [x] Approved on: 2026-04-30
- [x] Notes: Plan approved

