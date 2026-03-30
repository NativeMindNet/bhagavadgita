#!/usr/bin/env python3
"""
Generate Bhagavad Gita books in Markdown format for Thai and Traditional Chinese.
"""

import json
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).parent.parent
CHAPTERS_DIR = BASE_DIR / "data" / "chapters"
OUTPUT_DIR = BASE_DIR / "generated"

# Language configurations
LANGUAGES = {
    "th": {
        "name": "Thai",
        "book_title": "ภควัทคีตา",
        "chapter_format": "บทที่ {n}: {title}",
        "verse_label": "โศลก",
        "sanskrit_label": "สันสกฤต",
        "transliteration_label": "การถอดเสียง",
        "translation_label": "คำแปล",
        "vocabulary_label": "คำศัพท์",
        "glossary_title": "ศัพท์บัญญัติ",
        "notes_title": "หมายเหตุ",
        "toc_title": "สารบัญ",
        "verses_label": "โศลก",
        "word_col": "คำ",
        "transliteration_col": "การถอดเสียง",
        "meaning_col": "ความหมาย",
    },
    "zh-TW": {
        "name": "Traditional Chinese",
        "book_title": "《博伽梵歌》",
        "chapter_format": "第{n}章：{title}",
        "verse_label": "詩節",
        "sanskrit_label": "梵文",
        "transliteration_label": "音譯",
        "translation_label": "譯文",
        "vocabulary_label": "詞彙",
        "glossary_title": "詞彙表",
        "notes_title": "註釋",
        "toc_title": "目錄",
        "verses_label": "詩節",
        "word_col": "詞彙",
        "transliteration_col": "音譯",
        "meaning_col": "釋義",
    }
}

# Chinese number mapping
CHINESE_NUMS = {
    1: "一", 2: "二", 3: "三", 4: "四", 5: "五",
    6: "六", 7: "七", 8: "八", 9: "九", 10: "十",
    11: "十一", 12: "十二", 13: "十三", 14: "十四", 15: "十五",
    16: "十六", 17: "十七", 18: "十八"
}


def get_translation(obj: dict, lang: str, fallback_lang: str = "en", mark_fallback: bool = True) -> str:
    """Extract translation text from object, with fallback."""
    if lang in obj:
        val = obj[lang]
        if isinstance(val, dict):
            text = val.get("text", "")
            if text:
                return text
        elif val:
            return val
    if fallback_lang in obj:
        val = obj[fallback_lang]
        prefix = "[EN] " if mark_fallback else ""
        if isinstance(val, dict):
            return f"{prefix}{val.get('text', '')}"
        return f"{prefix}{val}"
    return ""


def get_chapter_title(chapter_data: dict, asian_data: Optional[dict], lang: str) -> str:
    """Get chapter title, preferring asian data for Asian languages."""
    # First try asian data (more complete for Asian languages)
    if asian_data:
        title = asian_data.get("title", {}).get(lang, "")
        if title:
            return title

    # Then try source data
    title = get_translation(chapter_data.get("title", {}), lang, mark_fallback=False)
    if title and not title.startswith("[EN]"):
        return title

    # Fallback to English
    return get_translation(chapter_data.get("title", {}), "en", mark_fallback=False)


def load_chapter(chapter_num: int) -> dict:
    """Load chapter source JSON."""
    path = CHAPTERS_DIR / f"ch-{chapter_num:02d}" / "chapter-source.json"
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_asian_translations(chapter_num: int) -> Optional[dict]:
    """Load Asian translations JSON if exists."""
    path = CHAPTERS_DIR / f"ch-{chapter_num:02d}" / "chapter-asian.json"
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def generate_chapter_md(chapter_data: dict, asian_data: Optional[dict], lang: str, cfg: dict) -> str:
    """Generate markdown for a single chapter."""
    chapter_num = chapter_data["chapter"]

    # Get chapter title
    title = get_chapter_title(chapter_data, asian_data, lang)

    # Format chapter title
    if lang == "zh-TW":
        chapter_title = f"第{CHINESE_NUMS.get(chapter_num, chapter_num)}章：{title}"
    else:
        chapter_title = cfg["chapter_format"].format(n=chapter_num, title=title)

    total_slokas = chapter_data.get("meta", {}).get("totalSlokas", len(chapter_data.get("slokas", [])))

    lines = [
        f"# {chapter_title}",
        "",
        f"> {total_slokas} {cfg['verses_label']}",
        "",
        "---",
        ""
    ]

    # Process slokas
    for sloka in chapter_data.get("slokas", []):
        sloka_num = sloka.get("number", "")
        sanskrit = sloka.get("sanskrit", "")
        transliteration = sloka.get("transliteration", "")

        # Get translation from source or asian
        translation = get_translation(sloka.get("translations", {}), lang)
        if not translation and asian_data:
            sloka_asian = asian_data.get("slokas", {}).get(sloka_num, {})
            if lang in sloka_asian:
                val = sloka_asian[lang]
                if isinstance(val, dict):
                    translation = val.get("text", "")
                else:
                    translation = val
        if not translation:
            translation = get_translation(sloka.get("translations", {}), "en")

        lines.extend([
            f"## {cfg['verse_label']} {sloka_num}",
            "",
            f"### {cfg['sanskrit_label']}",
            "",
            "```",
            sanskrit,
            "```",
            "",
            f"### {cfg['transliteration_label']}",
            "",
            transliteration,
            "",
            f"### {cfg['translation_label']}",
            "",
            f"> {translation}",
            ""
        ])

        # Vocabulary
        vocab = sloka.get("vocabulary", [])
        if vocab:
            lines.extend([
                f"### {cfg['vocabulary_label']}",
                "",
                f"| {cfg['word_col']} | {cfg['transliteration_col']} | {cfg['meaning_col']} |",
                "|------|-----------------|---------|"
            ])
            for v in vocab:
                word = v.get("word", "")
                trans = v.get("transliteration", "")
                meaning = get_translation(v.get("meaning", {}), lang)
                if not meaning:
                    meaning = get_translation(v.get("meaning", {}), "ru")
                if not meaning:
                    meaning = get_translation(v.get("meaning", {}), "en")
                lines.append(f"| {word} | {trans} | {meaning} |")
            lines.append("")

        lines.extend(["---", ""])

    return "\n".join(lines)


def generate_readme(lang: str, cfg: dict, chapter_titles: list) -> str:
    """Generate README.md with table of contents."""
    lines = [
        f"# {cfg['book_title']}",
        "",
        f"## {cfg['toc_title']}",
        ""
    ]

    for i, title in enumerate(chapter_titles, 1):
        if lang == "zh-TW":
            ch_label = f"第{CHINESE_NUMS.get(i, i)}章"
        else:
            ch_label = f"บทที่ {i}"
        lines.append(f"{i}. [{ch_label}: {title}](chapter-{i:02d}.md)")

    lines.extend([
        "",
        f"- [{cfg['glossary_title']}](glossary.md)",
        f"- [{cfg['notes_title']}](comments.md)",
        ""
    ])

    return "\n".join(lines)


def generate_glossary(lang: str, cfg: dict) -> str:
    """Generate glossary placeholder."""
    return f"# {cfg['glossary_title']}\n\n*Coming soon*\n"


def generate_comments(lang: str, cfg: dict) -> str:
    """Generate comments/notes placeholder."""
    return f"# {cfg['notes_title']}\n\n*Coming soon*\n"


def generate_book(lang: str):
    """Generate complete book for a language."""
    cfg = LANGUAGES[lang]
    out_dir = OUTPUT_DIR / lang
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nGenerating {cfg['name']} book...")

    chapter_titles = []

    for chapter_num in range(1, 19):
        print(f"  Chapter {chapter_num}...", end=" ")

        chapter_data = load_chapter(chapter_num)
        asian_data = load_asian_translations(chapter_num)

        # Get chapter title for TOC
        title = get_chapter_title(chapter_data, asian_data, lang)
        chapter_titles.append(title)

        # Generate chapter markdown
        md = generate_chapter_md(chapter_data, asian_data, lang, cfg)

        out_file = out_dir / f"chapter-{chapter_num:02d}.md"
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(md)

        sloka_count = len(chapter_data.get("slokas", []))
        print(f"{sloka_count} slokas")

    # Generate README
    readme = generate_readme(lang, cfg, chapter_titles)
    with open(out_dir / "README.md", 'w', encoding='utf-8') as f:
        f.write(readme)
    print("  README.md")

    # Generate glossary
    glossary = generate_glossary(lang, cfg)
    with open(out_dir / "glossary.md", 'w', encoding='utf-8') as f:
        f.write(glossary)
    print("  glossary.md")

    # Generate comments
    comments = generate_comments(lang, cfg)
    with open(out_dir / "comments.md", 'w', encoding='utf-8') as f:
        f.write(comments)
    print("  comments.md")

    print(f"  -> {out_dir}/")


def main():
    """Generate books for Thai and Traditional Chinese."""
    print("=" * 50)
    print("Bhagavad Gita Book Generator")
    print("=" * 50)

    for lang in ["th", "zh-TW"]:
        generate_book(lang)

    print("\n" + "=" * 50)
    print("Done!")
    print("=" * 50)


if __name__ == "__main__":
    main()
