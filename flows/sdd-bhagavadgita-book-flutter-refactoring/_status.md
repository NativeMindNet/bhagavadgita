# Status: sdd-bhagavadgita-book-flutter-refactoring

## Current Phase

REQUIREMENTS

## Phase Status

DRAFTING

## Last Updated

2026-04-28 by GPT-5.4

## Blockers

- Требуется review и approval требований перед переходом к `02-specifications.md`
- Не подтвержден backend-контракт и объем встроенного офлайн-слепка

## Progress

- [x] Requirements drafted
- [ ] Requirements approved
- [ ] Specifications drafted
- [ ] Specifications approved
- [ ] Plan drafted
- [ ] Plan approved
- [ ] Implementation started
- [ ] Implementation complete

## Context Notes

- Источники миграции: `legacy/legacy_bhagavadgita_book_java`, `legacy/legacy_bhagavadgita_book_swift`, `legacy/legacy_bhagavadgitabook_db`
- Целевой runtime: Flutter app в `app/bhagavadgita_book`
- Ключевое требование: offline-first с локальным последним слепком данных и встроенным fallback-набором
- Фоновая стратегия: lazy load и периодическое обновление данных без блокировки основного чтения
- Пользовательские данные должны быть отделены от контентного snapshot слоя

## Next Actions

1. Согласовать `01-requirements.md`
2. Подготовить `02-specifications.md` с архитектурой snapshot store, sync pipeline и Flutter-модульной структурой
