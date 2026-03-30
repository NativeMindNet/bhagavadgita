#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bhagavat-Gita Markdown Book Generator

Generates complete Bhagavat-gita books in Chinese, Thai, and Hebrew
from existing JSON source data in /data/chapters format.

Usage:
    python generate_gitabook_md.py [--languages zh-CN,th,he] [--output-dir OUTPUT]

Author: Generated for Gita Book Project
Date: 2026-03-27
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


# Configuration
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "chapters"
OUTPUT_DIR = BASE_DIR / "data" / "chapters" / "generated"

# Language configurations
LANG_CONFIG = {
    "zh-CN": {
        "name": "Chinese",
        "native_name": "中文",
        "dir": "ltr",
        "book_title": "博伽梵歌",
        "chapter_prefix": "第",
        "chapter_suffix": "章",
        "glossary_title": "词汇表",
        "comments_title": "注释",
        "sloka_title": "诗节",
        "sanskrit_title": "梵文原文",
        "translation_title": "译文",
        "vocabulary_title": "词汇",
        "await_translation": "⚠️ **Awaiting translation**",
        "translation_note": "_Note: Translation pending approval_",
        "toc_title": "目录",
        "meta_title": "元信息",
        "about_book": "About This Book",
        "language_label": "Language",
        "text_direction": "Text direction",
        "total_chapters": "Total chapters",
        "total_slokas": "Total slokas",
        "translation_status": "Translation Status",
        "translation_available": "✓ Translation available (pending approval)",
        "translation_awaiting": "⚠️ **Awaiting translation**",
        "translation_awaiting_desc": "This book has complete structure, but all translations are missing. Please use English versions as reference.",
        "generated": "Generated",
        "tool": "Tool",
    },
    "th": {
        "name": "Thai",
        "native_name": "ไทย",
        "dir": "ltr",
        "book_title": "ภควัทคีตา",
        "chapter_prefix": "บทที่",
        "chapter_suffix": "",
        "glossary_title": "ศัพท์บัญญัติ",
        "comments_title": "หมายเหตุ",
        "sloka_title": "โศลก",
        "sanskrit_title": "ภาษาสันสกฤต",
        "translation_title": "คำแปล",
        "vocabulary_title": "ศัพท์",
        "await_translation": "⚠️ **Awaiting translation**",
        "translation_note": "_หมายเหตุ: กำลังรอการอนุมัติ_",
        "toc_title": "สารบัญ",
        "meta_title": "ข้อมูลเมตา",
        "about_book": "เกี่ยวกับหนังสือเล่มนี้",
        "language_label": "ภาษา",
        "text_direction": "ทิศทางข้อความ",
        "total_chapters": "บททั้งหมด",
        "total_slokas": "โศลกทั้งหมด",
        "translation_status": "สถานะการแปล",
        "translation_available": "✓ มีคำแปลแล้ว (รอการอนุมัติ)",
        "translation_awaiting": "⚠️ **กำลังรอการแปล**",
        "translation_awaiting_desc": "หนังสือนี้มีโครงสร้างสมบูรณ์ แต่ยังขาดคำแปลภาษาไทย กรุณาใช้เวอร์ชันภาษาอังกฤษเป็นข้อมูลอ้างอิง",
        "generated": "สร้างเมื่อ",
        "tool": "เครื่องมือ",
    },
    "he": {
        "name": "Hebrew",
        "native_name": "עברית",
        "dir": "rtl",
        "book_title": "בהגווד גיטה",
        "chapter_prefix": "פרק",
        "chapter_suffix": "",
        "glossary_title": "אוצר מילים",
        "comments_title": "הערות",
        "sloka_title": "פסוק",
        "sanskrit_title": "סקריט",
        "translation_title": "תרגום",
        "vocabulary_title": "אוצר מילים",
        "await_translation": "⚠️ **Awaiting translation**",
        "translation_note": "_הערה: תרגום ממתין לאישור_",
        "toc_title": "תוכן עניינים",
        "meta_title": "מטא נתונים",
        "about_book": "אודות ספר זה",
        "language_label": "שפה",
        "text_direction": "כיוון טקסט",
        "total_chapters": "סך הכל פרקים",
        "total_slokas": "סך הכל פסוקים",
        "translation_status": "מצב תרגום",
        "translation_available": "✓ תרגום זמין (ממתין לאישור)",
        "translation_awaiting": "⚠️ **ממתין לתרגום**",
        "translation_awaiting_desc": "ספר זה נוצר עם מבנה מלא, אך כל התרגומים לעברית חסרים. נא להשתמש בגרסאות האנגלית כהפניה.",
        "generated": "נוצר",
        "tool": "כלי",
    },
}


class GitaBookGenerator:
    """Main generator class for Bhagavat-gita Markdown books."""

    def __init__(self, languages: List[str] = None, output_dir: Path = None):
        self.languages = languages or ["zh-CN", "th", "he"]
        self.output_dir = output_dir or OUTPUT_DIR
        self.chapters_data = {}
        self.vocabulary_data = {}
        self.asian_translations = {}
        
        # Statistics
        self.stats = {
            "chapters_processed": 0,
            "slokas_processed": 0,
            "translations_missing": 0,
        }

    def load_data(self):
        """Load all source JSON data."""
        print("Loading source data...")
        
        # Load original chapters (1-18)
        for i in range(1, 19):
            chapter_file = DATA_DIR / "original" / f"chapter-{i:02d}.json"
            if chapter_file.exists():
                with open(chapter_file, "r", encoding="utf-8") as f:
                    self.chapters_data[i] = json.load(f)
                print(f"  ✓ Loaded chapter {i}")
            else:
                print(f"  ✗ Missing: {chapter_file}")

        # Load Asian translations (chapters 1-6)
        for i in range(1, 7):
            asian_file = DATA_DIR / "asian" / f"chapter-{i:02d}-asian-translations.json"
            if asian_file.exists():
                with open(asian_file, "r", encoding="utf-8") as f:
                    self.asian_translations[i] = json.load(f)
                print(f"  ✓ Loaded Asian translations for chapter {i}")

        # Load vocabulary from ch-XX directories
        for i in range(1, 19):
            vocab_file = DATA_DIR / f"ch-{i:02d}" / "vocabulary-source.json"
            if vocab_file.exists():
                with open(vocab_file, "r", encoding="utf-8") as f:
                    self.vocabulary_data[i] = json.load(f)
                print(f"  ✓ Loaded vocabulary for chapter {i}")

        print(f"\nLoaded {len(self.chapters_data)} chapters, "
              f"{len(self.asian_translations)} Asian translations, "
              f"{len(self.vocabulary_data)} vocabulary files\n")

    def get_translation(self, sloka: Dict, lang: str, field: str = "text") -> Optional[str]:
        """Get translation for a sloka, handling missing data gracefully."""
        translations = sloka.get("translations", {})
        if lang in translations:
            return translations[lang].get(field)
        return None

    def is_translation_approved(self, sloka: Dict, lang: str) -> bool:
        """Check if translation is approved."""
        translations = sloka.get("translations", {})
        if lang in translations:
            return translations[lang].get("approved", False)
        return False

    def get_chapter_title(self, chapter_num: int, lang: str) -> str:
        """Get chapter title in target language."""
        chapter_data = self.chapters_data.get(chapter_num, {})
        title_data = chapter_data.get("title", {})
        
        if lang in title_data:
            return title_data[lang].get("text", "")
        
        # Fall back to English if available
        if "en" in title_data:
            return title_data["en"].get("text", f"Chapter {chapter_num}")
        
        return f"Chapter {chapter_num}"

    def generate_sloka_md(self, sloka: Dict, lang: str, config: Dict) -> str:
        """Generate Markdown for a single sloka."""
        lines = []
        sloka_num = sloka.get("number", "?.?")

        # Sloka header
        lines.append(f"## {config['sloka_title']} {sloka_num}\n")

        # Sanskrit
        lines.append(f"### {config['sanskrit_title']}\n")
        lines.append("```sanskrit")
        lines.append(sloka.get("sanskrit", ""))
        lines.append("```\n")

        # Transliteration (if available)
        if sloka.get("transliteration"):
            lines.append("**Transliteration:**\n")
            lines.append(f"_{sloka.get('transliteration', '')}_\n")

        # Translation
        lines.append(f"### {config['translation_title']}\n")
        translation = self.get_translation(sloka, lang)

        if translation:
            approved = self.is_translation_approved(sloka, lang)
            lines.append(f"> {translation}\n")
            if not approved:
                lines.append("> \n")
                lines.append(f"> {config['translation_note']}\n")
        else:
            lines.append(f"> {config['await_translation']}\n")
            lines.append("> \n")
            # Include English as reference
            en_translation = self.get_translation(sloka, "en")
            if en_translation:
                lines.append(f"> **English reference:** {en_translation}\n")
            self.stats["translations_missing"] += 1

        # Vocabulary
        vocab = sloka.get("vocabulary", [])
        if vocab:
            lines.append(f"### {config['vocabulary_title']}\n")
            lines.append("| Word | Meaning (EN) |")
            lines.append("|------|--------------|")

            for word in sorted(vocab, key=lambda x: x.get("order", 0)):
                word_text = word.get("word", "")
                meaning_en = word.get("meaning", {}).get("en", {}).get("text", "")

                # Add target language if available
                meaning_target = word.get("meaning", {}).get(lang, {}).get("text", "")
                if meaning_target:
                    lines.append(f"| {word_text} | {meaning_en} | {meaning_target} |")
                else:
                    lines.append(f"| {word_text} | {meaning_en} | {config['await_translation']} |")

            lines.append("")

        lines.append("---\n")

        return "\n".join(lines)

    def generate_chapter_md(self, chapter_num: int, lang: str, config: Dict) -> str:
        """Generate complete Markdown for a chapter."""
        chapter_data = self.chapters_data.get(chapter_num, {})

        if not chapter_data:
            return f"# Error: Chapter {chapter_num} not found\n"

        lines = []

        # Chapter title
        title = self.get_chapter_title(chapter_num, lang)
        chapter_prefix = config['chapter_prefix']
        chapter_suffix = config['chapter_suffix']

        if lang == "zh-CN":
            lines.append(f"# {chapter_prefix}{chapter_num}{chapter_suffix}: {title}\n")
        else:
            lines.append(f"# {chapter_prefix} {chapter_num}{chapter_suffix}: {title}\n")

        # Meta information
        meta = chapter_data.get("meta", {})
        lines.append(f"**{config['meta_title']}:**\n")
        lines.append(f"- {config['total_slokas']}: {meta.get('totalSlokas', 'N/A')}")
        lines.append(f"- Version: {meta.get('version', 'N/A')}")
        lines.append(f"- Updated: {meta.get('lastUpdated', 'N/A')}\n")

        lines.append("---\n")

        # Slokas
        slokas = chapter_data.get("slokas", [])
        for sloka in slokas:
            lines.append(self.generate_sloka_md(sloka, lang, config))
            self.stats["slokas_processed"] += 1

        return "\n".join(lines)

    def generate_glossary_md(self, lang: str, config: Dict) -> str:
        """Generate glossary from all vocabulary data."""
        lines = []
        lines.append(f"# {config['glossary_title']}\n")
        lines.append(f"_Glossary / {config['glossary_title']}_\n")
        lines.append("---\n")

        # Collect all unique vocabulary
        all_words = {}
        for chapter_num, vocab_data in self.vocabulary_data.items():
            vocabulary = vocab_data.get("vocabulary", [])
            for word in vocabulary:
                word_text = word.get("word", "")
                if word_text and word_text not in all_words:
                    all_words[word_text] = {
                        "en": word.get("meaning", {}).get("en", {}).get("text", ""),
                        "zh-CN": word.get("meaning", {}).get("zh-CN", {}).get("text", ""),
                        "th": word.get("meaning", {}).get("th", {}).get("text", ""),
                        "he": word.get("meaning", {}).get("he", {}).get("text", ""),
                    }

        # Group by first letter
        lines.append("## A–Z\n")
        lines.append("| Word | English | " +
                    f"{config['native_name']} | Status |")
        lines.append("|------|---------|" +
                    f"{'-' * len(config['native_name'])}|--------|")

        for word_text in sorted(all_words.keys()):
            meanings = all_words[word_text]
            target_meaning = meanings.get(lang, "")

            if target_meaning:
                status = "✓"
            else:
                status = "⚠️ Awaiting translation"

            lines.append(f"| {word_text} | {meanings['en']} | " +
                        f"{target_meaning or config['await_translation']} | {status} |")

        lines.append("\n---\n")
        lines.append(f"**Total words:** {len(all_words)}\n")

        return "\n".join(lines)

    def generate_comments_md(self, lang: str, config: Dict) -> str:
        """Generate comments file noting missing translations."""
        lines = []
        lines.append(f"# {config['comments_title']}\n")
        lines.append(f"_Translation Notes_\n")
        lines.append("---\n")

        lines.append("## Translation Status Overview\n")

        if lang == "he":
            lines.append(f"### ⚠️ {config['translation_awaiting']}\n")
            lines.append(f"{config['translation_awaiting_desc']}\n")
        else:
            lines.append(f"### Status for {config['native_name']}\n")

            # List chapters with unapproved translations
            unapproved = []
            for chapter_num, chapter_data in self.chapters_data.items():
                slokas = chapter_data.get("slokas", [])
                for sloka in slokas:
                    if not self.is_translation_approved(sloka, lang):
                        unapproved.append(f"{chapter_num}:{sloka.get('number', '?')}")

            if unapproved:
                lines.append(f"**Slokas awaiting approval** ({len(unapproved)}):\n")
                # Group by chapter
                by_chapter = {}
                for item in unapproved:
                    ch = item.split(":")[0]
                    if ch not in by_chapter:
                        by_chapter[ch] = []
                    by_chapter[ch].append(item.split(":")[1])

                for ch in sorted(by_chapter.keys()):
                    lines.append(f"- Chapter {ch}: {', '.join(by_chapter[ch])}")
            else:
                lines.append("✓ All translations approved\n")

        lines.append("\n---\n")

        # Missing vocabulary
        lines.append("## Vocabulary\n")

        missing_vocab = []
        for chapter_num, vocab_data in self.vocabulary_data.items():
            vocabulary = vocab_data.get("vocabulary", [])
            for word in vocabulary:
                target = word.get("meaning", {}).get(lang, {}).get("text", "")
                if not target:
                    missing_vocab.append({
                        "chapter": chapter_num,
                        "word": word.get("word", ""),
                        "en": word.get("meaning", {}).get("en", {}).get("text", ""),
                    })

        if missing_vocab:
            lines.append(f"**Words awaiting translation** ({len(missing_vocab)}):\n\n")
            lines.append("| Word | English Meaning | Chapter |")
            lines.append("|------|-----------------|---------|")
            for item in missing_vocab[:50]:  # Limit to first 50
                lines.append(f"| {item['word']} | {item['en']} | {item['chapter']} |")

            if len(missing_vocab) > 50:
                lines.append(f"\n_... and {len(missing_vocab) - 50} more words_")
        else:
            lines.append("✓ All vocabulary translated\n")

        lines.append("\n---\n")
        lines.append(f"_{config['generated']}: {datetime.now().isoformat()}_\n")

        return "\n".join(lines)

    def generate_readme_md(self, lang: str, config: Dict) -> str:
        """Generate README with table of contents."""
        lines = []

        # Title with RTL support if needed
        if config['dir'] == 'rtl':
            lines.append(f'<div dir="{config["dir"]}">')

        lines.append(f"# {config['book_title']}\n")
        lines.append(f"_Bhagavad Gita / {config['native_name']}_\n")

        if config['dir'] == 'rtl':
            lines.append('</div>\n')

        lines.append(f"**{config['toc_title']}**\n")

        # Table of contents
        for i in range(1, 19):
            title = self.get_chapter_title(i, lang)
            chapter_prefix = config['chapter_prefix']
            chapter_suffix = config['chapter_suffix']

            if lang == "zh-CN":
                lines.append(f"- [{chapter_prefix}{i}{chapter_suffix}: {title}](chapter-{i:02d}.md)")
            else:
                lines.append(f"- [{chapter_prefix} {i}{chapter_suffix}: {title}](chapter-{i:02d}.md)")

        lines.append(f"\n- [{config['glossary_title']}](glossary.md)")
        lines.append(f"- [{config['comments_title']}](comments.md)\n")

        lines.append("---\n")

        # Meta information
        lines.append(f"## {config['about_book']}\n")
        lines.append(f"**{config['language_label']}:** {config['native_name']} ({lang})\n")
        lines.append(f"**{config['text_direction']}:** {config['dir'].upper()}\n")
        lines.append(f"**{config['total_chapters']}:** 18\n")

        # Count total slokas
        total_slokas = sum(
            ch.get("meta", {}).get("totalSlokas", 0)
            for ch in self.chapters_data.values()
        )
        lines.append(f"**{config['total_slokas']}:** ~{total_slokas}\n")

        # Translation status
        lines.append(f"\n## {config['translation_status']}\n")

        if lang == "he":
            lines.append(f"{config['translation_awaiting']}\n")
            lines.append(f"{config['translation_awaiting_desc']}\n")
        else:
            lines.append(f"{config['translation_available']}\n")

        lines.append("\n---\n")
        lines.append(f"_{config['generated']}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n")
        lines.append(f"_{config['tool']}: generate_gitabook_md.py_\n")

        return "\n".join(lines)

    def generate_language_book(self, lang: str):
        """Generate complete book for a single language."""
        print(f"\n{'='*50}")
        print(f"Generating {LANG_CONFIG[lang]['name']} book...")
        print(f"{'='*50}")
        
        config = LANG_CONFIG[lang]
        lang_dir = self.output_dir / lang.lower().replace("-", "")
        lang_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate README
        print(f"  📖 Creating README.md...")
        readme = self.generate_readme_md(lang, config)
        with open(lang_dir / "README.md", "w", encoding="utf-8") as f:
            f.write(readme)
        
        # Generate chapters
        for i in range(1, 19):
            print(f"  📜 Generating chapter {i}...")
            chapter_md = self.generate_chapter_md(i, lang, config)
            with open(lang_dir / f"chapter-{i:02d}.md", "w", encoding="utf-8") as f:
                f.write(chapter_md)
            self.stats["chapters_processed"] += 1
        
        # Generate glossary
        print(f"  📚 Creating glossary...")
        glossary = self.generate_glossary_md(lang, config)
        with open(lang_dir / "glossary.md", "w", encoding="utf-8") as f:
            f.write(glossary)
        
        # Generate comments
        print(f"  📝 Creating comments file...")
        comments = self.generate_comments_md(lang, config)
        with open(lang_dir / "comments.md", "w", encoding="utf-8") as f:
            f.write(comments)
        
        print(f"  ✓ {lang} book complete!")

    def generate_all(self):
        """Generate books for all configured languages."""
        self.load_data()
        
        for lang in self.languages:
            if lang in LANG_CONFIG:
                self.generate_language_book(lang)
            else:
                print(f"⚠️ Unknown language: {lang}")
        
        # Print summary
        print(f"\n{'='*50}")
        print("GENERATION COMPLETE")
        print(f"{'='*50}")
        print(f"Chapters processed: {self.stats['chapters_processed']}")
        print(f"Slokas processed: {self.stats['slokas_processed']}")
        print(f"Missing translations noted: {self.stats['translations_missing']}")
        print(f"\nOutput directory: {self.output_dir}")
        print(f"Languages: {', '.join(self.languages)}")

    def run(self):
        """Main entry point."""
        print("Bhagavat-Gita Markdown Book Generator")
        print("=" * 50)
        print(f"Output: {self.output_dir}")
        print(f"Languages: {', '.join(self.languages)}\n")
        
        self.generate_all()


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate Bhagavat-gita Markdown books"
    )
    parser.add_argument(
        "--languages", "-l",
        default="zh-CN,th,he",
        help="Comma-separated language codes (default: zh-CN,th,he)"
    )
    parser.add_argument(
        "--output-dir", "-o",
        type=Path,
        default=None,
        help="Output directory (default: data/chapters/generated)"
    )
    
    args = parser.parse_args()
    languages = [l.strip() for l in args.languages.split(",")]
    
    generator = GitaBookGenerator(
        languages=languages,
        output_dir=args.output_dir
    )
    generator.run()


if __name__ == "__main__":
    main()
