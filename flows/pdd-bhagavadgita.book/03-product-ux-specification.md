# Product UX specification: Bhagavad Gita Book

> Version: 1.0 (restored from legacy)  
> Status: DRAFT  
> Last updated: 2026-05-04

## 1. Platforms and constraints

| Surface | Notes |
|---------|--------|
| **iOS** | UIKit, storyboards/nibs mix; `CustomNavigationController`; iPhone + iPad behaviors differ for split/detail |
| **Android** | API 18–26 era; `MainActivity` + fragments; `values-sw720dp` / `is_tablet` for two-pane |

## 2. Navigation model

### 2.1 iOS (Swift) — primary screens

| Screen (ViewController) | Role |
|-------------------------|------|
| `SplashViewController` | First run / data init gate |
| `GuideViewController` / `GuideNotesViewController` / `GuideItemViewController` | Onboarding / help |
| `ContentsViewController` | Hub: chapters, navigation to shloka, quote, bookmarks, search results |
| `ShlokaViewController` | Primary reader |
| `BookmarksViewController` | Saved verses |
| `CommentViewController` | Commentary UI for shloka context |
| `QuoteViewController` | Daily quote presentation |
| `SettingsViewController` / `SettingsLanguageViewController` | Language, book, interpretation-related options |
| `ContentsSearchResultViewController` | Global search hits |

### 2.2 Android (Java) — primary screens

| Screen | Role |
|--------|------|
| `SplashActivity` | Launch / init |
| `GuideActivity` | Onboarding |
| `MainActivity` | Host: `ChaptersFragment` default; `SlokasFragment`; `BookmarksFragment`; `NoteFragment` |
| `LanguagesActivity` | Language selection flow |
| `SettingsActivity` | Settings entry from toolbar home on root back stack |
| `QuoteActivity` | Quote display |

### 2.3 Android fragment graph (simplified)

- `MainActivity` container → starts with **ChaptersFragment**.
- **SlokasFragment** opened via `SlokasFragment.show(...)` (also from bookmark intent extra).
- Toolbar: **bookmarks** action changes title and nav icon; **search** opens `SearchPanelView`.
- Tablet: optional simultaneous **NoteFragment** / detail rules in `fragmentLifecycleCallbacks`.

## 3. Screen inventory (consolidated)

| # | User goal | Primary CTA | iOS | Android |
|---|-----------|-------------|-----|---------|
| 1 | Pick language | Continue | Settings language VC | `LanguagesActivity` |
| 2 | Browse chapters | Open shloka | `ContentsViewController` | `ChaptersFragment` |
| 3 | Read verse | Bookmark / note / audio | `ShlokaViewController` | `SlokasFragment` |
| 4 | See daily quote | Dismiss / share (if any) | `QuoteViewController` | `QuoteActivity` |
| 5 | Manage bookmarks | Open verse | `BookmarksViewController` | `BookmarksFragment` |
| 6 | Configure app | Save | `SettingsViewController` | `SettingsActivity` |
| 7 | Find text | Select result | Search results VC | Search panel + results |

## 4. Global UX rules

- **Toolbar / navigation**: Android uses red/white status bar theming when `SlokasFragment` visible on phone (see `MainActivity` lifecycle).
- **Search**: Global search panel can restore open state across rotation (`UiConstants.KEY_SEARCH_*`).
- **Tablet**: Master/detail conventions — toolbar icon flips between settings and back when note fragment destroys on tablet (`NoteFragment` branch).

## 5. Access and gating

| Capability | Required state |
|------------|----------------|
| Read downloaded book | Book marked downloaded + DB populated |
| API catalog fetch | Network; first-run may block on splash until `dataInitialized` (Swift `Settings`) |

## 6. User journey attachments

Add flowchart under `flows/pdd-bhagavadgita.book/artifacts/` and reference here, e.g. `artifacts/user-flow.png`.

## Approvals

**Approval phrase to advance**: “product ux approved”
