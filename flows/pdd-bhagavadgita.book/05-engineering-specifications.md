# Engineering specifications: Bhagavad Gita Book

> Version: 1.0 (restored from legacy)  
> Status: DRAFT  
> Last updated: 2026-05-04

## 1. System context

```
┌─────────────┐     HTTPS/HTTP      ┌──────────────────────────────┐
│ iOS Gita    │ ──────────────────► │ app.bhagavadgitaapp.online   │
│ Swift       │   POST /api/Data/*  │ (JSON envelope)              │
└─────────────┘                     └──────────────────────────────┘
┌─────────────┐                     ▲
│ Android     │ ────────────────────┘
│ Java        │
└─────────────┘
       │
       ▼
┌─────────────┐
│ SQLite      │  bhagavad-gita.sqlite (Documents / app storage)
│ + assets    │  bundled seed DB + downloaded audio/files
└─────────────┘
```

**Forward implementation**: `app/bhagavadgita.book` (Flutter) should treat this document + linked SDDs as parity reference.

---

## 2. Backend (remote API) — contract only

| Concern | Detail |
|---------|--------|
| Base path | `{HOST}/api/` |
| Methods | POST (Swift `GitaRequestManager.performRequest` method `"POST"` for all listed actions) |
| Success | `code == 0`, use `data` |
| Errors | Non-zero `code`, human `message` |

**Android request builder**: `com.ethnoapp.bgita.server.GitaRequest` extends `HttpRequest`, URL = `BuildConfig.HOST + "/api/" + action`.

**Swift request builder**: `GitaRequestManager.kServerUrl` + action string; unwraps envelope in `processReceivedData`.

---

## 3. iOS client (Swift)

| Area | Location / notes |
|------|------------------|
| App entry | `Gita/AppDelegate.swift` — DB init, `DownloadInfo.clearAll()`, GA init, request timeout 120s |
| Networking | `Gita/Model/DataAccess/GitaRequestManager.swift`, `Gita/Libraries/RequestManager/*` |
| Persistence | `Gita/Libraries/DbLibrary/DbHelper.swift`, `DbConnection`, generated / hand models under `Model/` |
| UI | `Gita/ViewControllers/*.swift`, `Gita/Views/*.swift` |
| Analytics | `GAHelper` — property id `UA-91314625-2` |

**Host constants** (`GitaRequestManager.swift`):

- Production: `http://app.bhagavadgitaapp.online`
- Commented dev: `http://gita.dev.ironwaterstudio.com`

---

## 4. Android client (Java)

| Area | Location / notes |
|------|------------------|
| Application class | `com.ethnoapp.bgita.ApplicationEx` |
| HTTP stack | `com.ironwaterstudio.server.http.HttpHelper`, `HttpRequest`, `ServiceCallTask` |
| API wrapper | `com.ethnoapp.bgita.server.DataService` |
| Models | `com.ethnoapp.bgita.model.*` (`Settings`, `Books`, `Chapters`, `Languages`, `Quote`, …) |
| UI | `com.ethnoapp.bgita.screens.*`, `fragments.*`, `adapters.*` |
| Build flavors | `dev` / `live` — `HOST` string in `app/build.gradle` |

**Dependencies** (Gradle): AppCompat/Design/RecyclerView/CardView, Gson, ViewPagerIndicator, Play Services Analytics, Firebase Messaging, Facebook SDK.

---

## 5. Data serialization

- **Android**: Gson + `ApiResult` / `Serializer` abstraction (`com.ironwaterstudio.server.serializers`).
- **Swift**: `NSDictionary` / `[String:Any]` parsing in model `getFromDictionary` extensions.

---

## 6. Local database

- File: `bhagavad-gita.sqlite`
- Swift upgrade: delete + recopy from bundle when `user_version` in bundle > user copy (see `DbHelper.updateIfNeeded()`).
- **Flutter implication**: implement explicit migration policy; do not silently rely on iOS legacy wipe semantics without product sign-off.

---

## 7. Non-functional (observed defaults)

| Topic | Value / behavior |
|-------|------------------|
| Swift request timeout | Config default 240s in `RequestManagerConfiguration`; app sets 120s in `AppDelegate` |
| Android connection timeout | `HttpHelper.CONNECTION_TIMEOUT` = 30000 ms |
| Retries | Swift `RequestManagerConfiguration.retriesCount` default 3 |

---

## 8. SDD / VDD delegation

| Topic | Flow |
|-------|------|
| Flutter API client parity | `flows/sdd-bhagavadgita.book-api-client/` |
| Content matrix / quotes | `flows/sdd-bhagavadgita.book-content/` |
| Local DB schema | `flows/sdd-bhagavadgita.book-database/`, `sdd-bhagavadgita.book-database-schema/` |
| Audio | `flows/sdd-bhagavadgita.book-audioplayer/` |

---

## Approvals

**Approval phrase to advance**: “engineering specifications approved”
