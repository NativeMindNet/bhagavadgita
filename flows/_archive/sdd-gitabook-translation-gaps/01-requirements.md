# Requirements: Gitabook Translation V2

> Version: 1.0
> Status: DRAFT
> Last Updated: 2026-03-28

## Problem Statement

Не все переводы глав Бхагавад-гиты завершены. Анализ данных выявил пробелы:

### Asian языки (th, zh-CN, zh-TW, ja, ko)

| Главы | Проблема |
|-------|----------|
| Ch 01-06 | Отсутствует **ja** (японский) |
| Ch 07-18 | Отсутствует **zh-CN** (упрощённый китайский) |

### Other языки (he, ar, tr, sw)

| Главы | Проблема |
|-------|----------|
| Ch 01-06 | Содержат **английский текст** вместо переводов |
| Ch 07-18 | OK |

### Vocabulary

Все 18 глав имеют vocabulary-asian.json и vocabulary-other.json файлы.

### Comments (Комментарии)

Комментарии находятся в `legacy/csv/Books/Gita_Slokas.csv`:

| Источник | ChapterIds | Кол-во | Язык оригинала |
|----------|------------|--------|----------------|
| ШМ (Шрила Шридхар Махарадж) | 1-18 | 12 | RU |
| SM (Hidden Treasure) | 19-36 | 21 | EN |
| **Итого** | | **33** | |

Нужен перевод на все asian и other языки.

## User Stories

### Primary

**As a** читатель Бхагавад-гиты
**I want** полные переводы всех глав на всех целевых языках
**So that** я могу читать книгу на своём языке

## Acceptance Criteria

### Must Have

1. **Given** chapter-asian.json для глав 1-6
   **When** добавлен японский перевод
   **Then** файл содержит: ko, th, zh-CN, zh-TW, ja

2. **Given** chapter-asian.json для глав 7-18
   **When** добавлен zh-CN перевод
   **Then** файл содержит: ko, th, zh-CN, zh-TW, ja

3. **Given** chapter-other.json для глав 1-6
   **When** выполнен перевод на he, ar, tr, sw
   **Then** файл содержит настоящие переводы (не английский)

4. **Given** комментарии ШМ+SM (33 шт)
   **When** выполнен перевод на asian и other языки
   **Then** комментарии доступны на th, zh-CN, zh-TW, ja, ko, he, ar, tr, sw

### Should Have

- Единый формат для всех chapter-asian.json и chapter-other.json

### Won't Have (This Iteration)

- Комментарии (отсутствуют в исходных данных)
- Новые переводы vocabulary (уже существуют)
- Написание кода/скриптов

## Constraints

- **Инструмент**: Только `/translate.sanskrit` для переводов
- **Формат**: Сохранять существующий JSON формат
- **Процесс**: Контентная работа, без программирования

## Target Languages

| Группа | Языки | Коды |
|--------|-------|------|
| Asian | Тайский, Китайский (упр.), Китайский (трад.), Японский, Корейский | th, zh-CN, zh-TW, ja, ko |
| Other | Иврит, Арабский, Турецкий, Суахили | he, ar, tr, sw |

## Work Summary

| Задача | Объём | Языки | Операций |
|--------|-------|-------|----------|
| Добавить ja в chapter-asian | Ch 1-6 | ja | 6 |
| Добавить zh-CN в chapter-asian | Ch 7-18 | zh-CN | 12 |
| Перевести chapter-other | Ch 1-6 | he, ar, tr, sw | 6 |
| Перевести комментарии ШМ+SM | 33 шт | asian (5 langs) | 1 |
| Перевести комментарии ШМ+SM | 33 шт | other (4 langs) | 1 |
| **Итого** | - | - | **26** |

## Open Questions

- [x] Есть ли комментарии в исходных данных? → **Да, в legacy/csv/Books/Gita_Slokas.csv**
- [x] Какие комментарии переводить? → **ШМ (12) + SM (21) = 33 комментария**
- [x] Нужно ли переводить vocabulary? → **Нет, уже существуют**

## References

- Предыдущий flow: `sdd-gitabook-translations-combined`
- Данные: `data/chapters/ch-XX/`

---

## Approval

- [x] Reviewed by: User
- [x] Approved on: 2026-03-28
- [x] Notes: Scope confirmed - chapters + comments (ШМ+SM)
