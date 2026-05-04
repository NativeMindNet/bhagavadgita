# Master plan: Bhagavad Gita Book

> Version: 1.0  
> Status: DRAFT  
> Last updated: 2026-05-04

## 1. Milestones

| Milestone | Outcome |
|-----------|---------|
| **M0 — Program baseline** | This PDD directory + `_status.md` (this delivery) |
| **M1 — Contract lock** | Flutter `LegacyApiClient` + models match §API in `02`/`05` |
| **M2 — Reader parity** | Chapters → shloka, bookmarks, notes, search |
| **M3 — Media** | Audio download/play aligned with `sdd-bhagavadgita.book-audioplayer` |
| **M4 — Hardening** | HTTPS-only endpoints, telemetry refresh, target SDK / iOS min bump |

## 2. Workstreams

| Stream | Deliverable | Depends on |
|--------|-------------|------------|
| **Documentation** | PDD + SDDs updated when parity gaps found | M0 |
| **Flutter app** | `app/bhagavadgita.book` features | M1 |
| **Content / DB** | SQLite migrations, asset packs | `sdd-bhagavadgita.book-database*` |
| **Release** | CI/CD per `sdd-bhagavadgita.book-cicd*` | Stores policy |

## 3. Legacy code position

| Path | Role going forward |
|------|---------------------|
| `legacy/legacy_bhagavadgita.book_swift/` | Reference for iOS behavior and API usage |
| `legacy/legacy_bhagavadgita.book_java/` | Reference for Android behavior and API usage |

No requirement to modify legacy repos for new features; changes target Flutter unless doing hotfix archaeology.

## 4. Risks

| Risk | Mitigation |
|------|------------|
| Undocumented API actions beyond `Data/*` | Grep both legacies + capture in `02-domain-specification.md` |
| SQLite schema drift vs Flutter | Single schema source in `sdd-bhagavadgita.book-database-schema` |

## 5. Open decisions

| ID | Decision |
|----|----------|
| D1 | Whether Flutter preserves “reset selected shloka on every cold start” from Swift `AppDelegate` |
| D2 | HTTPS base URL mapping for production |

## Approvals

**Approval phrase to start program execution**: “master plan approved”
