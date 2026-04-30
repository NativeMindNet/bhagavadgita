# Implementation Plan: bhagavadgita.book Audio Player

> Version: 1.0  
> Status: DRAFT  
> Last Updated: 2026-04-30  
> Specifications: `flows/sdd-bhagavadgita.book-audioplayer/02-specifications.md`

## Summary

Сначала фиксируем источник аудио и базовую UX-форму (минимальный мини-плеер), затем внедряем сервис/контроллер проигрывания, подключаем UI точки входа, и проверяем на iOS/Android.

## Task Breakdown

### Phase 1: Foundations

#### Task 1.1: Confirm scope + track mapping
- **Description**: определить, что именно проигрываем (глава/стих/раздел) и откуда берём аудио.
- **Files**:
  - `flows/sdd-bhagavadgita.book-audioplayer/01-requirements.md` - Modify
  - `flows/sdd-bhagavadgita.book-audioplayer/02-specifications.md` - Modify
- **Dependencies**: None
- **Verification**: updated requirements/spec with decisions
- **Complexity**: Low

#### Task 1.2: Add audio playback dependency
- **Description**: подключить выбранный пакет (например `just_audio`) и базовую конфигурацию.
- **Files**:
  - `app/bhagavadgita.book/pubspec.yaml` - Modify
- **Dependencies**: Task 1.1
- **Verification**: `flutter pub get`
- **Complexity**: Low

### Phase 2: Core playback

#### Task 2.1: Implement `AudioPlayerService` + controller/state
- **Description**: реализовать сервис и состояние плеера (load/play/pause/seek) и стримы для UI.
- **Files**:
  - `app/bhagavadgita.book/lib/` - Create/Modify
- **Dependencies**: Task 1.2
- **Verification**: minimal demo widget or unit tests
- **Complexity**: Medium

### Phase 3: UI integration

#### Task 3.1: Add entry points (Play buttons)
- **Description**: добавить кнопку Play/controls на релевантных экранах контента.
- **Files**:
  - `app/bhagavadgita.book/lib/...` - Modify
- **Dependencies**: Task 2.1
- **Verification**: manual play starts from content screen
- **Complexity**: Medium

#### Task 3.2: Add mini-player host
- **Description**: закрепить мини-плеер в общей структуре навигации/скелета приложения.
- **Files**:
  - `app/bhagavadgita.book/lib/...` - Modify/Create
- **Dependencies**: Task 2.1
- **Verification**: mini-player visible + controls work across navigation
- **Complexity**: Medium

### Phase 4: Testing & polish

#### Task 4.1: Manual verification iOS/Android
- **Description**: прогнать сценарии play/pause/seek, ошибки загрузки, навигацию.
- **Files**:
  - `flows/sdd-bhagavadgita.book-audioplayer/04-implementation-log.md` - Update
- **Dependencies**: Tasks 3.1–3.2
- **Verification**: checklist completed
- **Complexity**: Low

## File Change Summary

| File | Action | Reason |
|------|--------|--------|
| `app/bhagavadgita.book/pubspec.yaml` | Modify | Add playback package |
| `app/bhagavadgita.book/lib/**` | Create/Modify | Service/controller + widgets |
| `flows/sdd-bhagavadgita.book-audioplayer/*` | Create/Modify | Keep spec artifacts current |

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Package limitations | Medium | Medium | pick proven package (`just_audio`) |
| UX scope creep | Medium | Medium | explicit non-goals + phased rollout |
| Platform differences | Medium | Medium | test early on both platforms |

## Rollback Strategy

1. Remove new UI entry points / mini-player.
2. Remove playback dependency from `pubspec.yaml`.

---

## Approval

- [ ] Reviewed by: [name]
- [ ] Approved on: [date]
- [ ] Notes: [any conditions or clarifications]
