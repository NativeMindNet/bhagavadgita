# Requirements: Bhagavad Gita JSON Translations

> Version: 1.4
> Status: APPROVED
> Last Updated: 2026-03-26

## Problem Statement

Текущие данные Бхагавад-гиты хранятся в монолитных CSV файлах:
- Все шлоки в одном файле (Gita_Slokas.csv, 3.7MB)
- Сложно работать с отдельными главами
- Нет единого формата для мультиязычного контента
- Отсутствуют переводы на азиатские языки (корейский, тайский, китайский)

Нужно:
1. Разбить контент на отдельные JSON файлы по главам (18 файлов)
2. Добавить недостающие переводы существующих языков
3. Добавить переводы на новые языки

## User Stories

### Primary

**As a** разработчик
**I want** JSON файлы разбитые по главам
**So that** можно загружать только нужную главу, а не весь контент

**As a** пользователь из Азии
**I want** читать Гиту на своем родном языке (корейский, тайский, китайский)
**So that** понимать священный текст без языкового барьера

**As a** контент-менеджер
**I want** единый JSON формат для всех переводов
**So that** легко добавлять новые языки

## Scope: Author SM/ШМ Only

**В скоупе только книги Шридхара Махараджа (SM/ШМ):**

| BookId | Язык | Название | Initials |
|--------|------|----------|----------|
| 1 | ru | Бхагавад Гита Жемчужина мудрости Востока | ШМ |
| 2 | en | Bhagavad-gītā. The Hidden Treasure of the Sweet Absolute | SM |
| 11 | de | Die BHAGAVAD-GITA in Deutsch | SM |
| 14 | es | Śrīmad Bhagavad-Gītā | SM |

**SM = SCSM = ШМ = ШЧСМ** — Sri Chaitanya Saraswat Math / Шри Чайтанья Сарасват Матх

**НЕ в скоупе:** VC (Visvanath Cakravarti), SP (Swami Prabhupada)

## Scope: Two Phases

### Phase 1: CSV → JSON Conversion
Конвертировать существующие CSV в структурированные JSON по главам.

**Входные данные:**
- `Gita_Slokas.csv` (санскрит + переводы)
- `Gita_Vocabularies.csv` (пословный перевод)
- `db_chapters.csv` (названия глав)

**Выходные данные:**
```
data/chapters/
├── chapter-01.json
├── chapter-02.json
├── ...
└── chapter-18.json
```

### Phase 2: Add Translations
После завершения Phase 1 - добавить переводы.

**Целевые языки:**
- Основные (дополнить недостающие): en, ru, de, es
- Новые азиатские:
  - Корейский (ko)
  - Тайский (th)
  - Китайский традиционный (zh-TW)
  - Китайский упрощенный (zh-CN)
  - Китайский кантонский (zh-HK) - опционально

**Источники для перевода (порядок подачи):**
1. **Русский (ru)** — основной источник смысла
2. **Английский (en)** — второй источник смысла
3. **Немецкий (de), Испанский (es)** — дополнительный контекст
4. **Санскрит + транслитерация** — ПОСЛЕДНИЙ, только для уточнения терминов

**Важно:** Понимание смысла текста берётся из русского и английского переводов. Санскрит используется только для более точной формулировки терминов и имён, но НЕ как основа для понимания.

## Acceptance Criteria

### Must Have (Phase 1)

1. **Given** CSV файлы
   **When** запускается конвертация
   **Then** создается 18 JSON файлов (по одному на главу)

2. **Given** JSON файл главы
   **When** открывается файл
   **Then** содержит: оригинал санскрит, транслитерацию, все существующие переводы

3. **Given** шлока в JSON
   **When** у неё есть комментарий
   **Then** комментарий включен в структуру шлоки

4. **Given** шлока в JSON
   **When** у неё есть словарь (vocabulary)
   **Then** пословный перевод включен в массив `vocabulary`

### Must Have (Phase 2)

5. **Given** JSON файл главы
   **When** добавляются переводы
   **Then** структура файла остается совместимой

6. **Given** новый язык (ko, th, zh-*)
   **When** добавляется перевод
   **Then** переводятся: название главы, текст шлоки, комментарий

7. **Given** процесс перевода шлоки
   **When** Claude получает задачу на перевод
   **Then** на вход подаются: ru → en → de/es → санскрит (последний, только для терминов)

### Should Have

- Валидация JSON Schema
- Транслитерация для азиатских языков (романизация)
- Метаданные о источнике перевода

### Won't Have (This Iteration)

- Аудио файлы (остаются отдельно)
- Переводы vocabulary на новые языки
- Интерактивный редактор переводов

## Translation Input Format

При переводе шлоки Claude получает переводы в порядке приоритета:

```
Шлока 1.1

═══ ОСНОВНЫЕ ИСТОЧНИКИ СМЫСЛА ═══

[RU] Дхритараштра сказал: Санджая! Что произошло, когда мои сыновья
     и сыновья Панду сошлись для битвы на священной земле Курукшетры?

[EN] Dhritarashtra said: O Sanjaya, what happened when my sons and
     the sons of Pandu assembled on the sacred field of Kurukshetra?

═══ ДОПОЛНИТЕЛЬНЫЙ КОНТЕКСТ ═══

[DE] Dhritarashtra sprach: O Sanjaya, was geschah, als meine Söhne...

[ES] Dhritarashtra dijo: Oh Sanjaya, ¿qué sucedió cuando mis hijos...

═══ САНСКРИТ (только для уточнения терминов) ═══

Деванагари: धृतराष्ट्र उवाच...
Транслитерация: dhṛtarāṣṭra uvāca...

---
Переведи на: ko, th, zh-CN, zh-TW
Смысл бери из RU/EN. Санскрит — только для точности терминов.
```

## JSON Structure (Draft)

```json
{
  "chapter": 1,
  "title": {
    "sanskrit": "अर्जुनविषादयोग",
    "transliteration": "arjuna-viṣāda-yoga",
    "en": "Arjuna's Grief",
    "ru": "Скорбь Арджуны",
    "de": "Arjunas Kummer",
    "es": "La aflicción de Arjuna",
    "ko": "아르주나의 슬픔",
    "th": "ความทุกข์ของอรชุน",
    "zh-CN": "阿周那的悲伤",
    "zh-TW": "阿周那的悲傷"
  },
  "slokas": [
    {
      "number": "1.1",
      "order": 1,
      "sanskrit": "धृतराष्ट्र उवाच...",
      "transliteration": "dhṛtarāṣṭra uvāca...",
      "translations": {
        "en": { "text": "Dhritarashtra said...", "approved": true },
        "ru": { "text": "Дхритараштра сказал...", "approved": true },
        "ko": { "text": "드리타라슈트라가 말했다...", "approved": false },
        "th": { "text": "ธฤตราษฏร์กล่าวว่า...", "approved": false },
        "zh-CN": { "text": "持国王说...", "approved": false }
      },
      "comment": {
        "en": { "text": "Commentary text...", "approved": true },
        "ru": { "text": "Текст комментария...", "approved": true }
      },
      "vocabulary": [
        {
          "word": "धृतराष्ट्र",
          "transliteration": "dhṛtarāṣṭra",
          "meaning": {
            "ru": "Дхритараштра (имя царя)",
            "en": "Dhritarashtra (name of the king)"
          }
        }
      ],
      "audio": {
        "recitation": "/Files/audio1.mp3",
        "sanskrit": "/Files/sanskrit1.mp3"
      }
    }
  ]
}
```

## Constraints

- **Encoding**: UTF-8 для всех файлов
- **Validation**: JSON Schema для валидации структуры
- **Size**: Один файл главы < 500KB
- **Compatibility**: JSON должен быть читаем в браузере и мобильных приложениях

## Open Questions

- [x] ~~Какой API использовать для переводов?~~ → Claude (прямо в диалоге)
- [x] ~~Нужна ли ручная проверка?~~ → Да, флаг `approved: true/false`
- [x] ~~Куда сохранять?~~ → `data/chapters/`
- [ ] Включать ли романизацию (pinyin для китайского)?
- [x] ~~Разбивка на части для перевода~~ → По главам (18 итераций, ~30KB на главу)

## Dependencies

- Phase 1 должна быть завершена перед Phase 2
- Связан с `sdd-gitabook-database` (схема БД)

## References

- Legacy CSV analysis: `flows/legacy/understanding/_root.md`
- Source data: `/legacy/csv/Books/`
- Database schema: `flows/sdd-gitabook-database/`

---

## Approval

- [x] Reviewed by: User
- [x] Approved on: 2026-03-26
- [x] Notes: Санскрит последний, только для терминов. Смысл из RU/EN.
