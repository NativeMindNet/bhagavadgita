# Status: sdd-vdd-bhagavadgita.book-audioplayer

## Current Phase

REQUIREMENTS

## Phase Status

DRAFTING

## Last Updated

2026-04-30 by GPT-5.2 (Cursor)

## Blockers

- Нужно найти/подключить источники `avadhuta`, `legacy-cookbook-swift`, `legacy-gitanjali-swift`, `legacy-sgg-ru-v1-swift` (в текущем репозитории не обнаружены).

## Progress

- [x] Requirements drafted  ← current
- [ ] Requirements approved
- [ ] Specifications drafted
- [ ] Specifications approved
- [ ] Plan drafted
- [ ] Plan approved
- [ ] Implementation started
- [ ] Implementation complete
- [ ] Documentation drafted
- [ ] Documentation approved

## Context Notes

Key decisions and context for resuming:

- В репозитории найдены два legacy‑референса аудио:
  - iOS Swift: `legacy/legacy_bhagavadgita.book_swift/` (`AVPlayer` + таймер прогресса/окончания, UI `ShlokaPlayerView`, настройки скачивания аудио санскрит/перевод + autoplay)
  - Android Java: `legacy/legacy_bhagavadgita.book_java/` (`MediaPlayer` + audio focus, скачивание аудио через `DownloadManager` и `AudioState`)
- Остальные указанные референсы пока отсутствуют в этом репозитории.
- Требования включают UX для phone/tablet/desktop и вариант desktop tray.

## References

- Legacy iOS audio: `legacy/legacy_bhagavadgita.book_swift/Gita/Libraries/SoundManager/SoundManager.swift`, `.../Model/AudioManager.swift`, `.../Views/ShlokaPlayerView.swift`
- Legacy Android audio: `legacy/legacy_bhagavadgita.book_java/app/src/main/java/com/ironwaterstudio/utils/SoundManager.java`, `.../model/audio/*`, `.../res/layout/activity_settings.xml`

## Next Actions

1. Получить доступ/пути к референсам: `avadhuta`, `legacy-cookbook-swift`, `legacy-gitanjali-swift`, `legacy-sgg-ru-v1-swift`
2. После обновления требований — перейти к `02-specifications.md` (только после явного approval requirements)

