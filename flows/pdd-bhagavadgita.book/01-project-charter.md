# Project charter: Bhagavad Gita Book

> Version: 1.0 (restored from legacy native apps)  
> Status: DRAFT  
> Last updated: 2026-05-04  
> Sources: `legacy/legacy_bhagavadgita.book_swift/`, `legacy/legacy_bhagavadgita.book_java/`

## Executive summary

**Bhagavad Gita Book** is a reader application for the Bhagavad Gita: multiple languages and translations, chapter/shloka (verse) navigation, local persistence, optional audio, bookmarks, notes, daily quote, search, and first-launch guide. Legacy implementations are **native iOS (Swift)** and **native Android (Java)** sharing the same **HTTP JSON API** and the same conceptual content model.

## Vision and positioning

- **Vision**: Give users a reliable, offline-capable way to read and listen to the Gita with consistent structure across books and languages.
- **Positioning**: Content-centric spiritual reader (not social, not a game); Iron Water Studio / Ethnoapp lineage.
- **North-star metric**: Successful content sync + stable read path (open app → open shloka) with minimal support burden.

## Goals and non-goals

### Goals

1. Present **books → chapters → shlokas** with correct text and commentary where stored locally.
2. **Bootstrap catalog** from API (`Languages`, `Books`, `Chapters`) and **quote of the day** (`Quotes`).
3. **On-device SQLite** as primary store for reader data; resilient DB upgrade path when bundled DB version increases.
4. **Download** per-book assets (including audio paths per legacy Swift migration notes).
5. **Reader affordances**: bookmarks, per-shloka notes, global search, settings (language, book, interpretation options where applicable).

### Non-goals (as evidenced by legacy scope)

- No in-app social feed or user-generated public content.
- No account-based reading list sync across devices (device token used for API auth, not full account UX in reviewed paths).
- Legacy stacks are **not** maintained as product targets; **Flutter** (`app/bhagavadgita.book`) is the forward implementation surface.

## Target users and jobs-to-be-done

| Segment | Primary job-to-be-done |
|---------|-------------------------|
| Daily reader | Open last position, continue chapter, bookmark verses |
| Student / researcher | Search text, compare interpretation settings, read commentary |
| Listener | Play verse audio where downloaded |

## Scope boundaries

- **In scope**: API contract summarized in engineering spec; local schema; navigation and reader features listed in UX spec.
- **Out scope**: Backend implementation details of `app.bhagavadgitaapp.online` (not in repo).
- **Dependencies**: Remote API availability; Firebase on Android for messaging/analytics (see Android `google-services.json`); Google Analytics on iOS (`UA-91314625-2` in `AppDelegate.swift`).

## Success metrics and guardrails

| Metric | Target | Notes |
|--------|--------|--------|
| API compatibility | Preserve `code`/`data`/`message` semantics | Critical for Flutter `LegacyApiClient` parity |
| Offline read | Works without network after download | Core value |
| Store compliance | Follow platform rules for spiritual content apps | Charter-level guardrail |

## High-level user journeys

1. **First launch**: Splash → load languages/books (if not initialized) → guide (iOS `GuideViewController` / Android `GuideActivity`) → main reader.
2. **Returning user**: Splash → main **chapters list** → **shloka** screen; optional **Quote** flow from contents.
3. **Settings**: Change language/book, interpretation-related toggles (Swift `SettingsViewController` / Android `SettingsActivity`).

Diagrams: add under `artifacts/` and link from `03-product-ux-specification.md`.

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| HTTP (non-TLS) hosts in legacy | Security / store policy | Modern app must use HTTPS endpoints |
| DB wipe on version jump (Swift `updateIfNeeded`) | User data loss perception | Document migration strategy in Flutter |
| Old Android SDK 26 | Play policy | Target SDK lift in new app |

## Legacy provenance

| App | Bundle / application id | Primary host (release flavor) |
|-----|-------------------------|----------------------------------|
| iOS Gita | (see `Gita/Info.plist` in legacy tree) | `http://app.bhagavadgitaapp.online` |
| Android | `com.ethnoapp.bgita` | `live` flavor `BuildConfig.HOST` |

## Approvals

**Approval phrase to advance**: “project charter approved”
