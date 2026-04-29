# Status: sdd-bhagavadgita-book-flutter-refactoring

## Current Phase

IMPLEMENTATION

## Phase Status

IN_PROGRESS

## Last Updated

2026-04-28 by GPT-5.4

## Blockers

- Не подтвержден объем встроенного офлайн-слепка и политика “full vs partial” языков
- Не подтвержден storage stack для локальной БД

## Progress

- [x] Requirements drafted
- [x] Requirements approved
- [x] Specifications drafted
- [x] Specifications approved
- [ ] Plan drafted
- [x] Plan approved
- [x] Implementation started
- [ ] Implementation complete

## Context Notes

- Источники миграции: `legacy/legacy_bhagavadgita_book_java`, `legacy/legacy_bhagavadgita_book_swift`, `legacy/legacy_bhagavadgitabook_db`
- Целевой runtime: Flutter app в `app/bhagavadgita_book`
- Ключевое требование: offline-first с локальным последним слепком данных и встроенным fallback-набором
- Используем существующие legacy endpoint'ы `Data/Languages`, `Data/Books`, `Data/Chapters`, `Data/Quotes`
- Контентные источники для seed/пополнения: `data/` (primary), `bak/` (secondary rich), `legacy_bhagavadgitabook_db` (tertiary verify/audio)
- Фоновая стратегия: lazy load и периодическое обновление данных без блокировки основного чтения
- Splash screen рассматривается как часть startup/bootstrap потока, а не просто декоративный экран
- Пользовательские данные должны быть отделены от контентного snapshot слоя
- Спецификация описывает `stale-while-revalidate`, atomic snapshot replace и раздельные content/user tables

## Next Actions

1. Подготовить `03-plan.md` с задачами по content audit matrix, seed сборке, bootstrap, local DB, API layer, reader modules и sync orchestration
2. Согласовать план
