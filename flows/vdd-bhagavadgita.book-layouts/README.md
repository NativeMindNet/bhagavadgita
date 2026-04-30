# VDD: Bhagavad Gita Book Layouts (Flutter)

> Status: DRAFT  
> Last Updated: 2026-04-30  
> Requirements: `01-requirements.md`  
> Visual: `02-visual.md`  
> Specs: `03-specifications.md`  
> Plan: `04-plan.md`  
> Implementation log: `05-implementation-log.md`

## What this delivers

This VDD flow implements the **approved UI layouts** for the Bhagavad Gita Flutter app:

- A consistent **design system** (colors + typography)
- Updated layouts for key reading screens (Contents → Chapter → Sloka)
- Settings screen with reader toggles
- Search screen with **circular reveal** transition
- Tablet **dual‑pane** layouts (master-detail)

## Where it lives in the app

Primary Flutter app: `app/bhagavadgita.book/`

Key code areas:
- Theme:
  - `app/bhagavadgita.book/lib/app/theme/gita_colors.dart`
  - `app/bhagavadgita.book/lib/app/theme/gita_theme.dart`
- Screens:
  - `app/bhagavadgita.book/lib/features/contents/contents_screen.dart`
  - `app/bhagavadgita.book/lib/features/reader/chapter_screen.dart`
  - `app/bhagavadgita.book/lib/features/reader/sloka_screen.dart`
  - `app/bhagavadgita.book/lib/features/search/search_screen.dart`
  - `app/bhagavadgita.book/lib/features/settings/settings_screen.dart`
- Tablet:
  - `app/bhagavadgita.book/lib/features/tablet/contents_chapter_scaffold.dart`
  - `app/bhagavadgita.book/lib/features/tablet/chapter_sloka_scaffold.dart`

## How it works (plain language)

- When the app starts, you see a **red gradient splash** while local data initializes.
- The main screen is **Contents**: a styled list of the 18 chapters.
- Tapping a chapter opens a list of its slokas; tapping a sloka opens the **Sloka detail** screen.
- The Sloka screen shows sections (Sanskrit, transcription, translation, commentary, vocabulary) controlled by **Settings toggles**.
- Search opens with a **circular reveal** animation and shows matching slokas.
- On tablets, the app switches to a **split layout** where lists are on the left and details on the right.

## Test / verification

From `app/bhagavadgita.book/`:

- `flutter analyze`
- `flutter test`

## Known placeholders

- **Quote-of-the-day**: UI slot exists (`QuoteCard`), wiring to real data can be added next.
- **Audio player**: `AudioPlayerBar` is currently a layout shell (controls shown; real playback later).

## Approval

- [ ] Reviewed by: Anton
- [ ] Approved on: [date]
- [ ] Notes:

