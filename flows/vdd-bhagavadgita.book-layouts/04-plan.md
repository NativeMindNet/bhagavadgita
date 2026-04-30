# Implementation Plan: Bhagavad Gita Book Layouts

This plan details the steps to implement the UI layouts, design system, and responsive structure for the Bhagavad Gita Flutter app, as defined in `03-specifications.md` and `02-visual.md`.

## Phase 1: Design System & Theme Integration

Goal: Establish the core visual identity and fix the broken theme wiring.

- [ ] **Task 1.1: Fix Theme Wiring in `app/app.dart`**
  - Replace non-existent `import 'theme/gita_theme.dart'` with `import '../ui/theme/app_theme.dart'`.
  - Update `GitaBookApp` to use `buildAppTheme()` instead of `GitaTheme.light()`.
  - Verify that the app builds and applies the base red theme.
- [ ] **Task 1.2: Refine Design System Components**
  - Verify `app_colors.dart` covers all required colors (#FF5252, #FB9A6A, etc.).
  - Verify `app_text.dart` includes all required styles (PTSans, Devanagari fallback).
  - Add missing styles if needed (e.g., `SlokaSectionHeader`, `VariantPill` style).
- [ ] **Task 1.3: Font Loading Verification**
  - Ensure `PTSans` is correctly declared in `pubspec.yaml` and assets are present.
  - Verify `Noto Sans Devanagari` fallback works (bundled or via `google_fonts`).

## Phase 2: Splash & Onboarding

Goal: Implement the entry experience.

- [ ] **Task 2.1: Update Splash Screen**
  - Update `lib/features/splash/splash_screen.dart` layout to match `02-visual.md`.
  - Implement the red gradient background.
  - Add "OM" logo placeholder and branded title styling.
  - Add linear progress with percentage text.
- [ ] **Task 2.2: Implement Onboarding Guide**
  - Create `lib/features/onboarding/onboarding_screen.dart` (if not fully implemented).
  - Implement 3-page swiper using `PageView`.
  - Add page indicators (dots).
  - Wire "Skip" and "Done" buttons to update `appOnboardingController`.

## Phase 3: Contents & Navigation

Goal: Implement the primary navigation hub.

- [ ] **Task 3.1: Contents Screen UI Refresh**
  - Update `ContentsScreen` AppBar to use `AppColors.red1`.
  - Ensure Quote of the Day card matches styling (centered, italic, author badge).
- [ ] **Task 3.2: Verse Grid in Chapter Tiles**
  - Modify `lib/features/contents/widgets/chapter_expandable_tile.dart`.
  - Replace simple `Wrap` with a more structured grid if needed, ensuring `4-6` style ranges (from `Sloka.name`) are handled.
  - Implement selection highlighting (last read sloka).
- [ ] **Task 3.3: Search Reveal & Transition**
  - Verify `CircularRevealPageRoute` in `ContentsScreen`.
  - Ensure `SearchScreen` uses the white AppBar variant.

## Phase 4: Sloka Detail & Reader Experience

Goal: Implement the core reading experience with multiple layouts.

- [ ] **Task 4.1: Sloka Screen Layout Variants**
  - Implement conditional layout for `SlokaScreen`:
    - Red AppBar (Phone/Legacy).
    - White Topbar (“К оглавлению”) + Actions (Tablet/Compact).
- [ ] **Task 4.2: Round Navigation Buttons**
  - Implement `RoundNavButtons` widget.
  - On tablet/compact, overlay these buttons on the left/right sides of the content.
- [ ] **Task 4.3: Multi-Variant Sections**
  - Update `SlokaScreen` to support multiple translations/commentaries if present in the data.
  - Implement `VariantPill` widget to label these blocks (e.g., `Ru`, `En SP`).
- [ ] **Task 4.4: Audio Mini-Player**
  - Implement `MiniPlayerBar` (compact version of `AudioPlayerBar`).
  - Add to the bottom of `SlokaScreen` when audio is active.
- [ ] **Task 4.5: Note Editor Styling**
  - Update the Note section to match the compact design (Gray background, Save button styling).

## Phase 5: Settings & Preferences

Goal: Implement the compact settings UI.

- [ ] **Task 5.1: Settings Screen UI Refresh**
  - Update `SettingsScreen` to use section headers (uppercase, Gray 2).
  - Use compact toggle rows with red accent.
- [ ] **Task 5.2: Traktovki Selection**
  - Implement the "Трактовки" section with multi-select checkmarks.
  - Add "Скачать" (Download) action placeholder for missing content.

## Phase 6: Tablet & Responsive Scaffolding

Goal: Finalize the dual-pane experience.

- [ ] **Task 6.1: Master-Detail Scaffolds**
  - Verify and refine `lib/features/tablet/contents_chapter_scaffold.dart`.
  - Implement `TabletBookmarksSlokaScaffold` (split-view for bookmarks).
- [ ] **Task 6.2: Tablet Split-View Optimizations**
  - Ensure 40/60 split ratio.
  - Synchronize selection between master list and detail view.

## Phase 7: Verification & Polishing

- [ ] **Task 7.1: Golden Tests / Widget Tests**
  - Create tests for major layout states (Contents expanded, Sloka phone/tablet).
- [ ] **Task 7.2: Visual Regression Check**
  - Manually verify all screens against ASCII mockups in `02-visual.md`.
- [ ] **Task 7.3: Performance Audit**
  - Ensure smooth scrolling and transitions on target devices.

## Rollout Strategy

1.  Start with Theme fix and Font verification (Phase 1).
2.  Implement UI refreshes screen by screen (Contents -> Sloka -> Settings).
3.  Add Tablet-specific layouts.
4.  Final polish and testing.
