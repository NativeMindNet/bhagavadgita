# Implementation Log: bhagavadgita-book-flutter-refactoring

> Started: 2026-04-28  
> Plan: `flows/sdd-bhagavadgita-book-flutter-refactoring/03-plan.md`

## Progress Tracker

| Task | Status | Notes |
|------|--------|-------|
| Phase 0.1 Content audit matrix | Done | Скрипт + артефакты `content-matrix.json/.md` |
| Phase 0.2 v1 language policy doc | Done | `artifacts/v1-language-policy.md` |
| Phase 1 Storage stack | In progress | `drift` schema + codegen, app стартует через Splash |
| Phase 1 Seed installer | Pending | Bundled seed snapshot и установка |
| Phase 2 Legacy API client | Pending | `Data/Languages|Books|Chapters|Quotes` |
| Phase 3 Splash/bootstrap | Pending | Startup states + быстрый вход |
| Phase 4 Reader MVP | Pending | Contents/Reader |
| Phase 5 User data | Pending | Bookmarks/notes/search |
| Phase 6 Sync orchestration | Pending | stale-while-revalidate |

## Session Log

### Session 2026-04-28

#### Completed

- Реализован скрипт аудита покрытия данных: `scripts/content_audit_matrix.py`
- Сгенерированы артефакты:
  - `flows/sdd-bhagavadgita-book-flutter-refactoring/artifacts/content-matrix.json`
  - `flows/sdd-bhagavadgita-book-flutter-refactoring/artifacts/content-matrix.md`

#### Findings (high-signal)

- В `data/meta/languages.json` перечислены `tr` и `sw`, но в `data/translated/` они не обнаружены (как минимум, отсутствует директория/контент).
- Набор translated-языков в `data/` неравномерен по типам контента (например, `el/ka/hy` без `sloka`, `zh-CN` частично без `sloka`, `ja` “рваный”).

#### Next

- Зафиксировать v1 policy “full vs partial/hidden” на основе артефактов матрицы (Task 0.2).
