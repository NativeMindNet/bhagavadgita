# Specifications: bhagavadgita.book Audio Player

> Version: 1.0  
> Status: DRAFT  
> Last Updated: 2026-04-30  
> Requirements: `flows/sdd-bhagavadgita.book-audioplayer/01-requirements.md`

## Overview

Добавляем аудио-плеер в Flutter приложение: воспроизведение выбранного аудиотрека, базовые элементы управления (play/pause/seek), отображение прогресса, и доступ к управлению при навигации внутри приложения (например, мини-плеер).

## Affected Systems

| System | Impact | Notes |
|--------|--------|------|
| `app/bhagavadgita.book/pubspec.yaml` | Modify | Add audio playback dependency |
| `app/bhagavadgita.book/lib/` | Modify/Create | Player state/service + UI widgets |
| Existing reading/content screens | Modify | Add entry point (Play) + mini-player host |

## Architecture

### Proposed components

- `AudioPlayerService`: тонкая обёртка над выбранным пакетом воспроизведения (init/load/play/pause/seek/dispose).
- `AudioPlayerController` (state): хранит текущий трек, позицию/длительность, состояние (playing/paused/buffering/error).
- UI:
  - Entry point (Play) на релевантных экранах
  - Mini-player (bottom bar) с основными контролами
  - (опционально) Full-player screen

### Data Flow

1. UI выбирает `AudioTrack` (id, title, source)
2. Controller вызывает Service `load(track)` и `play()`
3. Service стримит обновления позиции/статуса → Controller → UI

## Interfaces

### Data model (draft)

```dart
class AudioTrack {
  final String id;
  final String title;
  final Uri source;
}
```

## Behavior Specifications

### Happy Path

1. Пользователь нажимает Play на главе/контенте
2. Трек загружается и начинается воспроизведение
3. UI показывает прогресс и состояние
4. Пользователь ставит паузу/перематывает/продолжает

### Edge Cases

| Case | Trigger | Expected Behavior |
|------|---------|-------------------|
| Load error | invalid URL / missing asset | Show non-blocking error UI, stay paused |
| Buffering | slow network | Show buffering indicator, keep controls responsive |
| Navigation | user changes screen | Playback continues (unless explicitly stopped), mini-player remains accessible |

### Error Handling

| Error | Cause | Response |
|-------|-------|----------|
| Playback init failure | unsupported format / platform issue | Show error message + disable play |

## Dependencies

### Requires

- Finalize audio source decision (assets vs remote vs hybrid)
- Choose playback package (likely `just_audio`; background playback may add `audio_service`)

## Testing Strategy

### Unit Tests

- [ ] Controller state transitions (play/pause/seek/error)

### Manual Verification

- [ ] Play/pause/seek works on Android
- [ ] Play/pause/seek works on iOS
- [ ] Mini-player persists across in-app navigation

---

## Approval

- [ ] Reviewed by: [name]
- [ ] Approved on: [date]
- [ ] Notes: [any conditions or clarifications]
