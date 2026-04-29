# Status: sdd-bhagavadgita-book-flutter-refactoring

## Current Phase

IMPLEMENTATION

## Phase Status

IN_PROGRESS

## Last Updated

2026-04-28 by GPT-5.4

## Blockers

- TBD: объем встроенного офлайн-слепка (full vs minimal) для v1 seed

## Progress

- [x] Requirements drafted
- [x] Requirements approved
- [x] Specifications drafted
- [x] Specifications approved
- [x] Plan drafted
- [x] Plan approved
- [x] Implementation started
- [ ] Implementation complete

## Context Notes

- Источники миграции: `legacy/legacy_bhagavadgita_book_java`, `legacy/legacy_bhagavadgita_book_swift`, `legacy/legacy_bhagavadgitabook_db`
- Целевой runtime: Flutter app в `app/bhagavadgita.book`
- Ключевое требование: offline-first с локальным последним слепком данных и встроенным fallback-набором
- Используем существующие legacy endpoint'ы `Data/Languages`, `Data/Books`, `Data/Chapters`, `Data/Quotes`
- Контентные источники для seed/пополнения: `data/` (primary), `bak/` (secondary rich), `legacy_bhagavadgitabook_db` (tertiary verify/audio)
- Фоновая стратегия: lazy load и периодическое обновление данных без блокировки основного чтения
- Splash screen рассматривается как часть startup/bootstrap потока, а не просто декоративный экран
- Пользовательские данные должны быть отделены от контентного snapshot слоя
- Спецификация описывает `stale-while-revalidate`, atomic snapshot replace и раздельные content/user tables

## Next Actions

1. Завершить Phase 1: seed installer + snapshot meta/atomic replace (без затирания user data)
2. Подключить legacy API client (4 endpoint'а) и sync-orchestrator (startup + stale-while-revalidate)
3. Довести reader MVP (contents → chapter → shloka) до отображения данных из локальной БД
