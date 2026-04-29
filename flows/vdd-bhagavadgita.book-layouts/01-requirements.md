# Requirements: Bhagavad Gita Book Layouts (Flutter)

> Version: 1.1
> Status: APPROVED
> Last Updated: 2026-04-30

## Problem Statement

The existing Flutter app (`app/bhagavadgita.book`) has basic screen scaffolding but lacks proper visual design and layout implementation. The app needs to combine the best UX/UI features from both legacy apps (Swift iOS and Java Android) while being implemented in Flutter for cross-platform compatibility.

Currently:
- Basic `ContentsScreen` with simple ListView
- Basic `SlokaScreen` with minimal styling
- No branded color scheme applied
- No custom typography
- Missing several screens, animations, and advanced features

## User Stories

### Primary

**As a** reader of Bhagavad Gita
**I want** a beautiful, readable app with Sanskrit text and translations
**So that** I can study the verses with clear typography and easy navigation

**As a** returning user
**I want** to bookmark verses and add personal notes
**So that** I can track my study progress and reflections

**As a** multilingual user
**I want** to choose my preferred translation language
**So that** I can understand the verses in my native language

### Secondary

**As a** user
**I want** audio playback of Sanskrit verses AND translations
**So that** I can learn proper pronunciation and listen while reading

**As a** new user
**I want** an onboarding guide
**So that** I understand how to use the app features

**As a** tablet user
**I want** an optimized dual-pane layout
**So that** I can see chapters and content simultaneously

## Acceptance Criteria

### Must Have

1. **Given** the app launches
   **When** data is ready
   **Then** show Contents screen with 18 chapters in styled list

2. **Given** I am on Contents screen
   **When** I tap a chapter
   **Then** navigate to Chapter screen showing all slokas in that chapter

3. **Given** I am viewing a sloka
   **When** the sloka loads
   **Then** display Sanskrit text, transliteration, translation, vocabulary, and commentary with proper typography

4. **Given** I am viewing a sloka
   **When** I tap bookmark icon
   **Then** toggle bookmark state with visual feedback

5. **Given** I am on Settings screen
   **When** I toggle display options
   **Then** reader view updates to show/hide sections accordingly

6. **Given** I tap the search icon
   **When** search panel opens
   **Then** show circular reveal animation (Material Design)

7. **Given** I am on audio player
   **When** I select audio type
   **Then** can play either Sanskrit pronunciation OR translation audio

### Should Have

1. Bottom audio player bar with dual-track support (Sanskrit/Translation)
2. Search functionality with results highlighting
3. Search within bookmarks (including notes content)
4. Bookmarks list with swipe-to-delete gesture
5. Quote of the day feature
6. Multiple commentary interpretations per sloka (with author badges)
7. Auto-play next sloka option
8. 3-page onboarding guide with page indicators
9. Download progress tracking for audio files

### Won't Have (This Iteration)

- Full offline mode (streaming first, downloads optional)
- Facebook SDK integration
- Multiple book editions simultaneously
- Social sharing

## Design System Requirements

### Color Palette (from legacy apps)

| Name | Hex | Usage |
|------|-----|-------|
| Red Primary (red1) | #FF5252 | AppBar, accent, switches, buttons |
| Red Secondary (red2) | #FB9A6A | Gradients, splash |
| Red Dark (red3) | #C94545 | StatusBar (Android) |
| Gray 1 | #4A4A4A | Primary text |
| Gray 2 | #9B9B9B | Secondary text, captions |
| Gray 3 | #C7C7CC | Borders, dividers |
| Gray 4 | #E8E8E8 | Light backgrounds |
| Gray 5 | #F9F9F9 | Very light backgrounds |
| White | #FFFFFF | Background, nav bar text |
| White 30% | #4DFFFFFF | Overlay effects |
| Black 20% | #33000000 | Shadows, scrim |

### Typography

| Style | Font | Size | Weight | Usage |
|-------|------|------|--------|-------|
| Nav Title | PT Sans | 18 | Regular | AppBar titles |
| Heading | PT Sans | 20 | Bold | Sloka names, section titles |
| Body | PT Sans | 16 | Regular | Translations, comments |
| Body Italic | PT Sans | 16 | Italic | Transcription |
| Sanskrit | Kohinoor Devanagari | 18 | Regular | Sanskrit verses (centered) |
| Caption | PT Sans | 14 | Regular | Secondary info, subtitles |
| Label | PT Sans | 12 | Bold | Badges, initials |
| Splash Title | PT Sans | 30 | Regular | Splash screen |
| Guide Title | PT Sans | 20 | Regular | Onboarding titles |
| Guide Text | PT Sans | 15 | Regular | Onboarding content |

### Iconography

From legacy Assets:
- **Audio**: play, pause, forward, back, audio progress bar
- **Navigation**: back arrow, disclosure chevron, arrow
- **Actions**: bookmark (filled/unfilled), comment, search, settings, share, save
- **Status**: checkmark, delete, dot indicators (active/inactive)
- **Visual**: circle_initials (author badge), dividers, gradient backgrounds

### Animations

| Animation | Type | Duration | Usage |
|-----------|------|----------|-------|
| Circular Reveal | Search panel | 300ms | Search open/close |
| Scrim Overlay | Fade | 200ms | Search backdrop |
| Snap to Edge | Swipe | 600ms | Swipe actions |
| Page Transition | Slide | 300ms | ViewPager navigation |
| Smooth Scroll | Spring | variable | Scroll to item |

## Screens Required

### 1. Splash Screen
- Red gradient background (#FB9A6A to #FF5252)
- App logo centered
- Loading indicator for initial data fetch
- Progress percentage text (0-100%)
- Optional: Download audio dialog (Yes/No)

### 2. Onboarding Guide (3 pages)
```
+---------------+    +---------------+    +---------------+
|  Page 1       |    |  Page 2       |    |  Page 3       |
|  Welcome &    | -> |  Navigation   | -> |  Features     |
|  Purpose      |    |  Tutorial     |    |  Overview     |
|               |    |               |    |               |
| [Skip] [Next] |    | [Back] [Next] |    | [Back] [Done] |
|     o . .     |    |     . o .     |    |     . . o     |
+---------------+    +---------------+    +---------------+
```
- ViewPager with IconPageIndicator
- Conditional button visibility (Back hidden on first, Next→Done on last)
- Show only on first launch (track via settings)

### 3. Contents Screen (Main)
- Red AppBar with title "Contents"
- Search icon (circular reveal animation), Settings icon
- Optional: Quote of the day card at top
- 18 chapters in scrollable list
- Each chapter: position number, name, disclosure chevron
- Expandable chapters to show slokas inline (optional)

### 4. Chapter Screen
- AppBar with chapter title
- List of slokas in chapter
- Each sloka: position, name, bookmark indicator
- Tap navigates to Sloka screen

### 5. Sloka Detail Screen
- AppBar with "Sloka" title, bookmark button
- Previous/Next navigation buttons (horizontal row)
- Sloka name heading (bold, 20pt)
- **Sections (each toggleable via settings):**
  - Sanskrit text (Kohinoor, 18pt, centered)
  - Separator line
  - Transcription (PT Sans Italic, 16pt)
  - Vocabulary list (word → translation)
  - Translation (PT Sans, 16pt)
  - Commentary with author badges (circle with initials)
- Personal notes section with TextField + Save button
- **Bottom Audio Player Bar:**
  - Play/Pause button
  - Progress bar (horizontal)
  - Track selector: Sanskrit / Translation
  - Auto-play toggle

### 6. Settings Screen
- Sections with headers (uppercase, gray2):

**Display Options:**
| Option | Type | Default |
|--------|------|---------|
| Show Sanskrit | Toggle | ON |
| Show Transcription | Toggle | ON |
| Show Translation | Toggle | ON |
| Show Vocabulary | Toggle | ON |
| Show Commentary | Toggle | ON |

**Audio Options:**
| Option | Type | Default |
|--------|------|---------|
| Download Sanskrit Audio | Toggle + Progress | OFF |
| Download Translation Audio | Toggle + Progress | OFF |
| Auto-play Next | Toggle | OFF |

**Languages:**
- Language selector (navigates to Language screen)

**Books/Commentaries:**
- List of available commentaries with download status

### 7. Search Screen
- **Circular reveal animation** on open
- Search input field with clear button
- Scrim overlay behind search
- Results list with query highlighting
- Tap result navigates to Sloka screen
- Search scope: All / Bookmarks only

### 8. Bookmarks Screen
- List of bookmarked slokas
- **SwipeLayout** for swipe-to-delete
- Each item shows: chapter, sloka name, note preview (if exists)
- Search within bookmarks (including notes)
- Empty state with icon and message
- Tap navigates to Sloka screen

### 9. Language Selection Screen
- List of available languages
- Checkmark on selected language
- Tap to select and return

## Component Library

### Reusable Components

1. **SearchPanelView**
   - Circular reveal animation
   - Scrim overlay
   - Query text callbacks

2. **SwipeLayout**
   - Horizontal swipe gesture
   - Snap-to-edge animation
   - Delete action reveal

3. **AudioPlayerBar**
   - Play/Pause button
   - Progress indicator
   - Track selector (Sanskrit/Translation)

4. **PageIndicator**
   - Dot indicators
   - Active/inactive states

5. **AuthorBadge**
   - Circle with initials
   - Red border, red text

6. **SettingsToggle**
   - Label + Switch
   - Red accent color

7. **DownloadProgress**
   - Circular progress indicator
   - Percentage text

## Tablet/Responsive Layout

### Phone Layout
- Single column, full-screen navigation
- Bottom sheet for audio player

### Tablet Layout (sw720dp)
- **Dual-pane**: Chapters list (left) + Content (right)
- Master-detail pattern
- Dynamic StatusBar color based on active fragment
- Landscape optimizations

## Audio System Requirements

### Dual-Track Audio
```
Sloka Audio:
├── Sanskrit pronunciation (audio_sanskrit field)
└── Translation reading (audio field)
```

### Audio States
| State | Icon | Behavior |
|-------|------|----------|
| Not Downloaded | Download icon | Tap to download |
| Downloading | Progress % | Show progress |
| Downloaded | Play icon | Ready to play |
| Playing | Pause icon | Tap to pause |
| Paused | Play icon | Tap to resume |

### Auto-play Feature
- When enabled: automatically play next sloka after current finishes
- Respects selected track type (Sanskrit or Translation)

## Constraints

- **Technical**: Must work with existing Drift database schema
- **Platform**: iOS and Android via Flutter
- **Performance**: Smooth scrolling on 700+ slokas
- **Accessibility**: Support dynamic text sizing
- **Assets**: Port icons from legacy apps, use Google Fonts for PT Sans
- **Audio**: Use `just_audio` + `audio_service` packages

## Flutter Package Recommendations

| Feature | Package |
|---------|---------|
| Audio playback | `just_audio`, `audio_service` |
| Downloads | `flutter_downloader` or `dio` |
| Swipe actions | `flutter_slidable` |
| Animations | `flutter_animate` or built-in |
| Onboarding | `introduction_screen` or custom PageView |
| Icons | Custom assets from legacy |
| Fonts | `google_fonts` (PT Sans) + bundled Kohinoor |

## Open Questions

- [x] Color scheme - confirmed from Style.swift
- [x] Typography - confirmed PT Sans + Kohinoor Devanagari
- [x] Audio system - dual track from Java app
- [x] Animations - circular reveal from Java app
- [x] Tablet layout priority: implement in v1
- [x] Push notifications: implement in v1
- [ ] Font licensing: PT Sans via Google Fonts OK, Kohinoor needs check

## References

- Legacy Swift app: `legacy/legacy_bhagavadgita.book_swift/`
- Legacy Java app: `legacy/legacy_bhagavadgita.book_java/`
- Style definitions: `legacy/legacy_bhagavadgita.book_swift/Gita/Resources/Style.swift`
- Android colors: `legacy/legacy_bhagavadgita.book_java/app/src/main/res/values/colors.xml`
- Existing Flutter screens: `app/bhagavadgita.book/lib/features/`
- Database schema: `app/bhagavadgita.book/lib/data/local/tables.dart`

---

## Approval

- [x] Reviewed by: Anton
- [x] Approved on: 2026-04-30
- [x] Notes: Tablet layout and push notifications included in v1
