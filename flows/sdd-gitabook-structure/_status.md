# Status: sdd-gitabook-structure

## Current Phase

REQUIREMENTS

## Phase Status

DRAFTING

## Last Updated

2026-03-29 by Claude

## Blockers

- None

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

Key decisions and context for resuming:

**Согласованные решения:**
- Структура: Language-First (по языкам → по главам → по шлокам)
- Формат: plain text (.txt)
- Именование файлов: chapter-{N}-{sloka}-{lang}_{type}.txt
- Именование папок: chapter-{N}-{lang}/
- Транслитерация: отдельный файл в нативной письменности каждого языка
- Комментарии: отдельный файл рядом (если есть)
- Корневые папки: `sanskrit/`, `original/`, `translated/`
- Санскрит: на верхнем уровне `sanskrit/` (первоисточник)
- Vocabulary: только в `original/` языках (_vocabulary.json в папке главы)
- Vocabulary: перевод слов с санскрита (sanskrit + word + meaning)
- Vocabulary для translated: генерируется конкатенацией смыслов из original

**Языки:**
- Оригиналы: ru, en, de, es (+ sanskrit)
- Переводы: ko, th, zh-CN, zh-TW, el, ka, hy, he, ar, tr, sw

**Транслитерация по письменностям:**
- Кириллица: ru
- IAST (латиница): en, de, es, tr, sw
- Хангыль: ko
- Тайское: th
- Иероглифы: zh-CN (упр.), zh-TW (трад.)
- Греческое: el
- Грузинское: ka
- Армянское: hy
- Ивритское: he
- Арабское: ar

## Next Actions

1. Изучить текущую структуру данных и понять требования
2. Задокументировать requirements
3. Дождаться одобрения от пользователя
