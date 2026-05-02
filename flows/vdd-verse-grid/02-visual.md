# Visual Mockups: Verse Grid

> Version: 1.0  
> Status: DRAFT (content matches parent approval)  
> Last Updated: 2026-05-02  
> Requirements: `01-requirements.md`  
> Parent: `../vdd-bhagavadgita.book-layouts/02-visual.md` (full app, approved 2026-04-30)

## Overview

ASCII mockups **only** for the verse grid: expanded chapter on phone, and tablet master pane with grid + detail. Symbol legend for the full app lives in the parent `02-visual.md`.

---

## Phone: Expanded Chapter (Verse Grid)

Chapters expand in-place to show verse numbers. Some numbers may be grouped as ranges.

```
+------------------------------------------+
|########## RED APPBAR #FF5252 ############|
|=  #sett   Бхагавад Гита      #srch  #bk =|
+------------------------------------------+
|  Глава 1                                 |
|  Осмотр Армий                     ^      |
|  46 шлок                                  |
|                                          |
|   ( 1 )  2   3  4-6  7  8-9  10          |
|    11   12  13   14  15  16  17-18       |
|    19   20 21-23 24  25  26   27         |
|    28   29  30   31 32-34 35  36         |
|   37-38 39  40   41  42  43  44          |
|    45   46                               |
|                                          |
|  ----------------------------------------|
|  Глава 2                           v     |
|  Душа в мире материи                    |
|  ----------------------------------------|
+------------------------------------------+
```

Legend:

- `^` / `v` = expanded / collapsed chevron  
- `( 1 )` = selected verse chip  
- `4-6` = verse range chip  

---

## Tablet (Landscape): Chapters + Verse Grid + Sloka Detail

Matches store screenshots: chapter list expands to verse chips on the left; right pane shows selected sloka.

```
+--------------------------------------------------------------------------------+
|########################## RED APPBAR #FF5252 ##################################|
|=  #sett   Бхагавад Гита                           #srch  #cmt  #bk  #more      =|
+--------------------------------------------------------------------------------+
|  CHAPTERS + VERSE GRID (Master)        |  SLOKA DETAIL (Detail)                |
|                                       |                                       |
|  Глава 4                               |  (◀)                           (▶)   |
|  Йога обретения духовного знания   ^   |                                       |
|  42 шлок                                |                4.19                   |
|                                        |     Йога обретения духовного знания   |
|   1  2  3  4  5  6  7                   |                ---                    |
|   8  9 10 11 12 13 14                   |  Sanskrit / transcription...          |
|  15 16 17 18 (19) 20 21                 |                ---                    |
|  22 23 24 25 26 27 28                   |  Word-by-word...                      |
|  29 30 31 32-34 35 36                   |                ---                    |
|  37-38 39 40 41 42                      |  [ Ru ] / [ En SM ] / [ En SP ]...    |
|                                        |  Translation + commentary blocks...   |
|  ------------------------------------- |                                       |
|  Глава 5  Деятельность в отречении  v  |                                       |
|  ------------------------------------- |                                       |
+--------------------------------------------------------------------------------+
|############################### MINI PLAYER ####################################|
|  4.19 Йога обретения духовн...   [▶]    [=====>                         ]     |
+--------------------------------------------------------------------------------+
```

Legend:

- `(19)` = selected verse chip in grid  
- `#more` = overflow menu  

---

## Approval

- [ ] Reviewed by:  
- [ ] Approved on:  
- [ ] Notes: Parent layouts visual was approved 2026-04-30; re-approve if this standalone doc becomes binding.
