# Implementation Plan: Settings (Languages + Audio) — Bhagavad Gita Flutter

> Version: 1.0  
> Status: DRAFT  
> Last Updated: 2026-04-30  
> Specifications: `03-specifications.md`

## Summary

Сделать Settings как в legacy (Android/iOS): секции, подэкраны выбора языков (контент vs UI), базовые аудио-переключатели с UX “confirm download/delete” и прогрессом, и блок “Interpretations/Books” (список книг по выбранным языкам) — с постепенной интеграцией с данными (seed → repository/cache).

## Task Breakdown

### Phase 1: Foundation (state + persistence)

#### Task 1.1: App language controller + app locale wiring
- **Description**: Добавить `AppLanguageController` и пробросить `locale` в `MaterialApp` (system vs explicit).
- **Files**:
  - `app/bhagavadgita.book/lib/app/app.dart` (или место инициализации `MaterialApp`) — Modify
  - `app/bhagavadgita.book/lib/features/settings/app_language_controller.dart` — Create
- **Dependencies**: None
- **Verification**: смена языка в Settings меняет тексты UI без перезапуска.
- **Complexity**: Medium

#### Task 1.2: Flutter localization bootstrap (en/ru)
- **Description**: Подключить `flutter_localizations` и генерацию l10n; создать `app_en.arb` / `app_ru.arb` минимум для Settings.
- **Files**:
  - `app/bhagavadgita.book/pubspec.yaml` — Modify
  - `app/bhagavadgita.book/l10n.yaml` (если используем gen-l10n) — Create
  - `app/bhagavadgita.book/lib/l10n/*.arb` — Create
- **Dependencies**: Task 1.1 (желательно, но можно параллельно)
- **Verification**: `flutter gen-l10n` / build проходит; строки Settings берутся из локализации.
- **Complexity**: Medium

#### Task 1.3: Content languages controller (multi-select + guard)
- **Description**: Добавить `ContentLanguagesController` (selected language codes) с правилом “min 1 selected”.
- **Files**:
  - `app/bhagavadgita.book/lib/features/settings/content_languages_controller.dart` — Create
  - `app/bhagavadgita.book/lib/features/settings/models/language_option.dart` — Create (если нужно)
- **Dependencies**: None
- **Verification**: unit-test на guard + сохранение/восстановление prefs.
- **Complexity**: Low/Medium

#### Task 1.4: Audio settings controller (flags only)
- **Description**: Добавить `AudioSettingsController` (useTranslation/useSanskrit/autoPlayNext) без реальных скачиваний; подготовить UI states (stub).
- **Files**:
  - `app/bhagavadgita.book/lib/features/settings/audio_settings_controller.dart` — Create
- **Dependencies**: None
- **Verification**: toggles persist; `SlokaScreen` читает флаги (без playback).
- **Complexity**: Low

### Phase 2: Settings UI (screens + widgets)

#### Task 2.1: Refactor Settings screen into sections + reusable rows
- **Description**: Переделать `SettingsScreen` под макет `02-visual.md`.
- **Files**:
  - `app/bhagavadgita.book/lib/features/settings/settings_screen.dart` — Modify
  - `app/bhagavadgita.book/lib/features/settings/widgets/settings_section_header.dart` — Create
  - `app/bhagavadgita.book/lib/features/settings/widgets/setting_row.dart` — Create
  - `app/bhagavadgita.book/lib/features/settings/widgets/toggle_row.dart` — Create
- **Dependencies**: Phase 1 controllers
- **Verification**: визуально совпадает с ASCII; навигация на sub-screens работает.
- **Complexity**: Medium

#### Task 2.2: Content languages screen (multi-select)
- **Description**: Реализовать экран выбора языков контента + guard “last language”.
- **Files**:
  - `app/bhagavadgita.book/lib/features/settings/content_languages_screen.dart` — Create
- **Dependencies**: Task 1.3
- **Verification**: нельзя снять последний язык; summary обновляется.
- **Complexity**: Medium

#### Task 2.3: App language screen (radio list)
- **Description**: Экран выбора языка интерфейса (System default / explicit).
- **Files**:
  - `app/bhagavadgita.book/lib/features/settings/app_language_screen.dart` — Create
- **Dependencies**: Task 1.1, 1.2
- **Verification**: UI меняется сразу при выборе.
- **Complexity**: Medium

#### Task 2.4: Audio toggle UX (confirm dialogs + progress placeholders)
- **Description**: Диалоги подтверждения включения/удаления и отображение прогресса (можно stub state).
- **Files**:
  - `app/bhagavadgita.book/lib/features/settings/settings_screen.dart` — Modify
  - `app/bhagavadgita.book/lib/features/settings/widgets/toggle_row.dart` — Modify
- **Dependencies**: Task 1.4
- **Verification**: confirm dialogs появляются; toggle блокируется в “downloading” state.
- **Complexity**: Medium

### Phase 3: Books/Interpretations section (data plumbing)

#### Task 3.1: Define books settings contract (UI model + controller)
- **Description**: Создать `BooksSettingsController` и `BookSummary` модель; пока можно feed из seed/fixtures.
- **Files**:
  - `app/bhagavadgita.book/lib/features/settings/books_settings/books_settings_controller.dart` — Create
  - `app/bhagavadgita.book/lib/features/settings/books_settings/book_summary.dart` — Create
- **Dependencies**: Task 1.3
- **Verification**: Settings показывает список книг и состояния (↓/✓/progress).
- **Complexity**: Medium

#### Task 3.2: Integrate with real data source (incremental)
- **Description**: Подключить реальный репозиторий (seed JSON → позже backend/cache).
- **Files**:
  - `app/bhagavadgita.book/lib/data/*` — Modify/Create (по факту архитектуры)
- **Dependencies**: Task 3.1
- **Verification**: список совпадает с доступными книгами по языкам.
- **Complexity**: High (если сразу backend)

### Phase 4: Testing & Polish

#### Task 4.1: Unit + widget tests for controllers and key UX rules
- **Description**: Покрыть guard и locale override.
- **Files**:
  - `app/bhagavadgita.book/test/features/settings/*` — Create
- **Dependencies**: Phases 1-2
- **Verification**: `flutter test` green.
- **Complexity**: Medium

#### Task 4.2: Copy + adapt legacy strings into l10n keys
- **Description**: Добавить строки Settings из legacy (`Settings.*`) в ARB.
- **Files**:
  - `app/bhagavadgita.book/lib/l10n/app_en.arb` — Modify
  - `app/bhagavadgita.book/lib/l10n/app_ru.arb` — Modify
- **Dependencies**: Task 1.2
- **Verification**: нет “hardcoded” строк в Settings.
- **Complexity**: Low/Medium

## Dependency Graph

```
Task 1.1 ─┬─→ Task 2.3
          ├─→ Task 2.1 ─→ Task 2.2
Task 1.2 ─┘      │
Task 1.3 ────────┼─→ Task 3.1 ─→ Task 3.2
Task 1.4 ────────└─→ Task 2.4
                   ↓
                Task 4.1, 4.2
```

## File Change Summary

| File | Action | Reason |
|------|--------|--------|
| `app/bhagavadgita.book/lib/features/settings/settings_screen.dart` | Modify | New Settings layout + sections + navigation |
| `app/bhagavadgita.book/lib/features/settings/app_language_*` | Create | UI locale override |
| `app/bhagavadgita.book/lib/features/settings/content_languages_*` | Create | Multi-select content language |
| `app/bhagavadgita.book/lib/features/settings/audio_settings_controller.dart` | Create | Audio prefs flags |
| `app/bhagavadgita.book/lib/l10n/*` | Create/Modify | UI localization (en/ru) |

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Locale override complexity | Med | Med | keep `system` fallback; validate supportedLocales |
| Data source mismatch (seed vs legacy backend) | Med | High | start with fixtures/seed; design repo abstraction |
| Audio downloads not ready | High | Med | stub progress state; integrate real download manager later |

## Rollback Strategy

1. Keep old `ReaderSettingsController` keys unchanged.
2. If new localization wiring breaks build, fallback to hardcoded strings temporarily (only during dev), then re-enable gen-l10n.
3. Feature-flag new Settings sections if needed (optional).

## Checkpoints

- [ ] Phase 1: prefs controllers stable; no crashes on startup
- [ ] Phase 2: Settings UI matches `02-visual.md`
- [ ] Phase 3: books list shows correct filtering
- [ ] Phase 4: tests green; strings localized

## Open Implementation Questions

- [ ] Where is the best place to host global controllers (DI vs globals), given current code uses a global `readerSettingsController`?
- [ ] Do we want M3 widgets or legacy-like styling (may affect switch visuals)?

---

## Approval

- [ ] Reviewed by: Anton
- [ ] Approved on: [date]
- [ ] Notes: [any conditions or clarifications]
