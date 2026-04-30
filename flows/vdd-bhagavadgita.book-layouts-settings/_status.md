# Status: vdd-bhagavadgita.book-layouts-settings

## Current Phase

REQUIREMENTS

## Phase Status

DRAFTING

## Last Updated

2026-04-30 by GPT-5.2 (Cursor)

## Blockers

- None

## Progress

- [x] Requirements drafted  ← current
- [ ] Requirements approved
- [ ] Visual mockups drafted
- [ ] Visual approved
- [ ] Specifications drafted
- [ ] Specifications approved
- [ ] Plan drafted
- [ ] Plan approved
- [ ] Implementation started
- [ ] Implementation complete
- [ ] Documentation drafted
- [ ] Documentation approved

## Context Notes

Key decisions and context for resuming:

- Settings scope: **languages** (content translations + UI locale), **audio** (Sanskrit/Translation + download/delete + autoplay), and **books/interpretations** (download per selected languages).
- Legacy UX references:
  - Android: `legacy/legacy_bhagavadgita.book_java/app/src/main/java/com/ethnoapp/bgita/screens/SettingsActivity.java`
  - iOS: `legacy/legacy_bhagavadgita.book_swift/Gita/ViewControllers/SettingsViewController.swift`
- Current Flutter baseline:
  - Reader toggles exist: `app/bhagavadgita.book/lib/features/settings/settings_screen.dart`
  - Persistence exists: `app/bhagavadgita.book/lib/features/settings/reader_settings.dart`
- Languages source of truth (legacy DB export): `legacy/legacy_bhagavadgita.book_db/Books/db_languages.csv`, `db_books.csv`.

## Fork History

- None

## Next Actions

1. Draft `02-visual.md` ASCII mockups for Settings + sub-screens (languages + audio + books).
2. Draft `03-specifications.md` (data model + persistence + integration points in Flutter app).
3. Draft `04-plan.md` (task breakdown + files list).
