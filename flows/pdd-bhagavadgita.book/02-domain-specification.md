# Domain specification: Bhagavad Gita Book

> Version: 1.0 (restored from legacy)  
> Status: DRAFT  
> Last updated: 2026-05-04

## 1. Glossary

| Term | Definition |
|------|------------|
| **Book** | A translation/edition within a **Language**; has `id`, `languageId`, `name`, `initials`, `chaptersCount`. |
| **Chapter** | Ordered section of a book; linked by `bookId`. |
| **Shloka / Sloka** | Verse unit; Android uses `SlokasFragment`, Swift `ShlokaViewController`. |
| **Quote** | Daily (or promotional) quote object from `Data/Quotes`. |
| **Device token** | Opaque string sent as `Authorization: Gita <token>` on Android when present (`Settings.deviceToken`). |
| **Api envelope** | Server returns JSON wrapper: success when `code == 0` and `data` populated; otherwise `message` describes failure. |

## 2. Core entities and relationships

```
Language 1──* Book 1──* Chapter 1──* Shloka (stored in SQLite; text/commentary/blob fields per schema)
                    └── download state + audio files (per-book, per-translation in legacy Swift)
Settings: languageId, bookId, selected shloka id, app state (e.g. download vs ready), serialized AppSettings
Bookmarks / Notes: attached to shloka identity (implementation in local DB + UI)
```

## 3. Remote API (domain contract)

**Base URL** (production in both codebases):

- `http://app.bhagavadgitaapp.online/api/`  
- Android **dev** flavor: `http://gita.dev.ironwaterstudio.com` (see `app/build.gradle`).

**Transport**: POST to `{base}{Action}` with JSON body. Swift `GitaRequestManager` wraps params as `["params": …]` for actions that need a body; `Data/Languages` and `Data/Quotes` use empty params object.

**Envelope** (Swift `processReceivedData`, Android `ApiResult`):

| Field | Meaning |
|-------|---------|
| `code` | `0` = success (Swift unwraps `data`); Android `ApiResult.SUCCESS = 0` |
| `data` | Payload (object or array) |
| `message` | Human-readable error |

**Documented actions** (both platforms aligned):

| Action | Params | Result shape |
|--------|--------|----------------|
| `Data/Languages` | (empty) | Array of **Language** |
| `Data/Books` | `ids`: int[] | Array of **Book** |
| `Data/Chapters` | `bookId`: int | Array of **Chapter** (Swift sets `bookId` on each item) |
| `Data/Quotes` | (empty) | Single **Quote** object |

**Headers**:

- Android `GitaRequest`: `accept-language` = device default language code; optional `Authorization: Gita <deviceToken>`.

**iOS reference**: `Gita/Model/DataAccess/GitaRequestManager.swift` (inline API help URL historically pointed at `http://gita.dev.ironwaterstudio.com/help/api/`).

## 4. Local persistence domain

- **SQLite** database file name: `bhagavad-gita.sqlite` (Swift `DbHelper`).
- **Initialization**: copy bundled DB to Documents if missing; exclude from backup where implemented.
- **Upgrade**: compare `PRAGMA user_version` between user DB and bundled resource DB; if bundle newer, **replace** user DB file (Swift behavior — strong operational semantics for migrations).

## 5. Client-only domain rules

| Rule | Source |
|------|--------|
| Incomplete downloads cleared on launch | Swift `DownloadInfo.clearAll()` in `AppDelegate` |
| Selected shloka reset on launch (legacy Swift) | `Settings.shared.selectedShloka` reset in `AppDelegate` — product choice to revisit in Flutter |
| Search panel closes on fragment lifecycle | Android `MainActivity` + `SearchPanelView` |

## 6. Third-party domain touchpoints

- **Google Analytics**: iOS tracking id in `AppDelegate`; Android `play-services-analytics` + `GaUtils`.
- **Firebase**: Android project `bhagavad-gita-a3e05` (FCM-capable dependencies in Gradle).
- **Facebook SDK**: present on Android (`facebook-android-sdk`); treat as integration surface, not core reader domain.

## 7. Traceability to charter

| Charter goal | Supported by |
|--------------|----------------|
| Offline read | §4 Local persistence |
| Catalog correctness | §3 API entities |
| Multi-language | `Data/Languages` + `languageId` on books |

## Approvals

**Approval phrase to advance**: “domain specification approved”
