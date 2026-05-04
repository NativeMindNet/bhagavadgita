# Visual and messaging: Bhagavad Gita Book

> Version: 1.0 (restored from legacy)  
> Status: DRAFT  
> Last updated: 2026-05-04

## 1. Visual principles (legacy Android + iOS)

- **Palette (Android reader emphasis)**: Strong **red** toolbar brand (`R.color.red_1`, `red_3`) with **white** text on primary chrome; **black_20** status bar overlay on shloka screen (phone).
- **iOS**: Asset-driven chrome (`Assets.xcassets`: bookmarks, audio controls, dividers, guide illustrations `icn_guide*`).
- **Typography**: System defaults on iOS; Android `support` design era — prefer **readable serif/sans** for verse body in future Flutter; legacy mixes custom list cells (`item_sloka.xml`, `ShlokaChapterContentsTableViewCell`).
- **Iconography**: Distinct icons for bookmarked vs not, comment vs commented, audio transport (legacy asset sets).

## 2. Motion and density

- Legacy: standard push transitions (UIKit `pushViewController`); fragment transactions on Android.
- **Flutter target**: keep motion subtle; respect Material + Cupertino platform norms.

## 3. Messaging themes (product copy)

- **Tone**: Respectful, neutral instructional (guide screens), error strings via Android `R.string.error_*`.
- **Onboarding**: Guide flow explains gestures / reading model before dropping into contents (exact strings in legacy storyboards / `strings.xml` — extract when localizing Flutter).

## 4. Generative prompts (optional, for redesign)

Use when regenerating UI for Flutter without copying legacy pixels:

```
Mobile reading app for Bhagavad Gita, clean spiritual aesthetic, warm off-white reading surface,
deep red accents for toolbar and primary actions, high contrast verse typography,
chapter list with circular book initials, minimal chrome, support light/dark in modern version.
Russian and English UI labels acceptable. No decorative deities in generic chrome.
```

## 5. Traceability to UX

| UX rule | Visual expression |
|---------|-------------------|
| Reader focus | Full-screen verse area; toolbar recedes or adapts (legacy Android color flip) |
| Bookmark state | Distinct filled/outline bookmark icons (both platforms) |

## Approvals

**Approval phrase to advance**: “visual and messaging approved”
