# Status: vdd-bhagavadgita.book-layouts-settings

## Current Phase

IMPLEMENTATION

## Phase Status

**BLOCKED** (critical compilation errors)

## Last Updated

2026-04-30 by Claude Opus 4.5

## Blockers

- **C1**: `settings_screen.dart` — дублирующийся код после строки 370, не компилируется
- **C2**: `settings_screen.dart` — отсутствует import `AppText`
- **C3**: `app_language_screen.dart` — использует несуществующий `RadioGroup`

## Progress

- [x] Requirements drafted
- [ ] Requirements approved
- [x] Visual mockups drafted
- [ ] Visual approved
- [x] Specifications drafted (v1.1 — добавлен gap analysis)
- [ ] Specifications approved
- [x] Plan drafted
- [ ] Plan approved
- [x] Implementation started
- [ ] Implementation complete ← **blocked by C1-C3**
- [ ] Documentation drafted
- [ ] Documentation approved

## Context Notes

Key decisions and context for resuming:

- Settings scope: **languages** (content translations + UI locale), **audio** (Sanskrit/Translation + download/delete + autoplay), and **books/interpretations** (download per selected languages).
- Legacy UX references:
  - Android: `legacy/legacy_bhagavadgita.book_java/.../SettingsActivity.java`
  - iOS: `legacy/legacy_bhagavadgita.book_swift/.../SettingsViewController.swift`
- Current Flutter files:
  - `settings_screen.dart` — BROKEN
  - `app_language_screen.dart` — BROKEN (RadioGroup)
  - `content_languages_*.dart` — OK
  - `audio_settings_controller.dart` — OK
  - `app.dart` — OK (locale wired)
  - `l10n/*.arb` — OK
- Specs v1.1 содержит полный план исправлений (Phase 1-4)

## Fork History

- None

## Next Actions

1. **Fix C1-C3** (Phase 1 в specs) — код должен компилироваться
2. **Fix W1** (Phase 2) — deprecated `activeColor`
3. **Fix G1-G3** (Phase 3) — logic gaps (audio disabled while downloading, "Not available", l10n)
4. Run `flutter analyze` + `flutter test`
5. Mark Implementation complete
6. Draft documentation
