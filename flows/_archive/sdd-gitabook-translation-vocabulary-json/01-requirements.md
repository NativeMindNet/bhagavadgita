# Requirements: Gitabook Translation Vocabulary JSON

> Version: 0.1 (Draft)
> Status: IN PROGRESS
> Last Updated: 2026-03-26

## Problem Statement

Текущие данные словаря (vocabulary) для шлок Бхагавад-гиты хранятся в CSV файле (`Gita_Vocabularies.csv`) только на русском языке. Для международного приложения необходимы переводы словаря на азиатские языки:
- Тайский (th)
- Китайский (zh-CN, zh-TW)
- Корейский (ko)
- Японский (ja)

Нужно:
1. Конвертировать vocabulary из CSV в JSON формат
2. Добавить переводы meanings на целевые языки
3. Добавить транскрипцию на языках назначения

## User Stories

### Primary

**As a** разработчик мобильного приложения
**I want** vocabulary в JSON формате для каждого языка
**So that** загружать только нужный язык без лишних данных

**As a** пользователь из Азии
**I want** видеть пословный перевод на моем языке
**So that** понимать значение каждого санскритского слова

**As a** изучающий санскрит
**I want** транскрипцию санскритских слов на моем языке
**So that** правильно произносить термины

## Scope

### In Scope

- Конвертация `Gita_Vocabularies.csv` в JSON
- **Объединение vocabulary из двух источников**:
  - BookId 1 (RU/ШМ) — русские переводы + кириллическая транслитерация
  - BookId 2 (EN/SM) — английские переводы + IAST транслитерация
- Перевод `Translation` (meaning) на 5 языков:
  - Thai (th)
  - Chinese Simplified (zh-CN)
  - Chinese Traditional (zh-TW)
  - Korean (ko)
  - Japanese (ja)
- **Транслитерация санскритских слов на языках назначения**:
  - Тайская транскрипция
  - Китайская транскрипция (пиньинь + фонетика)
  - Корейская транскрипция
  - Японская транскрипция (ромадзи + кана)
- Создание отдельных файлов vocabulary для каждой главы

### Out of Scope

- Перевод самих санскритских слов (Text поле)
- Аудио произношение vocabulary
- Модификация оригинальных chapter-XX.json файлов

## Source Data Priority

### Для перевода meaning:

1. **Русский (ru)** — основной источник смысла (BookId 1)
2. **Английский (en)** — второй источник смысла (BookId 2)
3. **Тайский, Китайский, Корейский, Японский** — перевод с RU/EN
4. **Санскрит** — ТОЛЬКО для уточнения формы и терминов

### Для транслитерации:

1. **Кириллица** (из RU источника) — базовая транслитерация
2. **IAST** (из EN источника) — международная стандартная транслитерация
3. **Транскрипция на языках назначения**:
   - Тайская — фонетическая транскрипция
   - Китайская — пиньинь + фонетическая адаптация
   - Корейская — хангыль транскрипция
   - Японская — ромадзи + кана транскрипция

## Target Languages

| Code | Language | Native Name | Script |
|------|----------|-------------|--------|
| th | Thai | ภาษาไทย | Thai |
| zh-CN | Chinese (Simplified) | 简体中文 | Han |
| zh-TW | Chinese (Traditional) | 繁體中文 | Han |
| ko | Korean | 한국어 | Hangul |
| ja | Japanese | 日本語 | Kanji/Kana |

## Acceptance Criteria

### Must Have

1. **Given** vocabulary CSV файл
   **When** конвертируется в JSON
   **Then** создаются отдельные файлы `vocab_XX.json` для каждой главы (1-18)

2. **Given** vocabulary entry
   **When** переводится meaning
   **Then** используется приоритет RU → EN → DE/ES → Sanskrit

3. **Given** санскритское слово
   **When** сохраняется транскрипция
   **Then** используется тот же формат, что в legacy CSV (кириллица)

4. **Given** vocabulary JSON файл
   **When** загружается
   **Then** содержит все vocabulary entries для данной главы с translations на 5 языков

5. **Given** завершение перевода главы
   **When** сохраняются результаты
   **Then** азиатские переводы сохраняются ТОЛЬКО в:
   - `chapter-XX-asian-translations.json` (для шлок)
   - `vocab_XX.json` (для словаря, с пометкой `approved: false`)
   - Оригинал `chapter-XX.json` НЕ модифицируется

6. **Given** процесс перевода
   **When** формируется контекст
   **Then** глава и словарь переводятся ВМЕСТЕ (один контекст на главу)

## Open Questions

- [x] ~~Нужно ли отдельное JSON файл для vocabulary или интегрировать в главы?~~ → Интегрировать в главы (как в legacy)
- [ ] Какой формат транскрипции предпочтителен для каждого языка?
- [ ] Нужно ли добавлять примеры использования для каждого слова?
- [ ] Требуется ли валидация переводов носителями языка?
- [ ] Как обрабатывать многозначные слова?

## Constraints

- **Encoding**: UTF-8 для всех файлов
- **Compatibility**: JSON должен быть читаем в браузере и мобильных приложениях
- **Size**: Vocabulary не должен значительно увеличивать размер глав

## Dependencies

- Связан с `sdd-bhagavadgita-json-translations` (основная структура глав)
- Source: `/legacy/csv/books/Gita_Vocabularies.csv`
- Target: `data/chapters/chapter-XX.json` или `data/vocabulary/`

## Translation Workflow

### Automated Agent Translation

Перевод выполняется **автоматически** через запуск агента:

1. **Команда**: `/translate.sanscrit [путь к сохраняемому файлу]`
2. **Процесс**:
   - Агент извлекает данные главы (шлоки + vocabulary)
   - Агент переводит на ko, th, zh-CN, zh-TW, ja
   - Агент добавляет транслитерацию на языках назначения
   - Агент сохраняет результат в указанный файл
3. **Блокировка**: Следующая глава не переводится, пока не сохранён результат текущей

### Sequential Execution

```
Chapter 1 → Agent → Save → Validate → Chapter 2 → Agent → Save → ...
```

- **Sequential**: Агенты запускаются последовательно
- **Immediate Save**: Результат сохраняется сразу после обработки
- **No Manual Intervention**: Полностью автоматизированный процесс

## References

- Source vocabulary: `/legacy/csv/books/Gita_Vocabularies.csv`
- Related flow: `sdd-bhagavadgita-json-translations`
- Existing schema: `data/schema/chapter.schema.json`

---

## Approval

- [x] Reviewed by: User
- [x] Approved on: 2026-03-26
- [x] Notes: Vocabulary в отдельных файлах vocab_XX.json. Транскрипция как в legacy CSV. Азиатские переводы — в chapter-XX-asian-translations.json (оригинал не модифицируется). Глава + словарь переводятся вместе в одном контексте.
