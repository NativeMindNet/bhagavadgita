#!/usr/bin/env python3
"""
Batch process transliterations for all 18 chapters.
"""

import subprocess
import sys

PYTHON = "/opt/homebrew/bin/python3.13"
SCRIPT = "/Users/anton/proj/gita/scripts/generate_transliterations.py"
LANGUAGES = ["th", "zh-CN", "zh-TW", "ko", "ja", "el", "ka", "hy", "he", "ar", "tr", "sw"]

def main():
    lang_args = " ".join(LANGUAGES)
    
    for chapter in range(1, 19):
        print(f"\n{'='*60}")
        print(f"Processing Chapter {chapter}...")
        print('='*60)
        
        cmd = [PYTHON, SCRIPT, "--chapter", str(chapter), "--languages"] + LANGUAGES
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Print summary
        for line in result.stdout.split('\n'):
            if 'TOTAL' in line or 'Processing' in line:
                print(line)
        
        if result.returncode != 0:
            print(f"Error processing chapter {chapter}:")
            print(result.stderr)
    
    print("\n" + "="*60)
    print("Phase 1 Complete!")
    print("="*60)

if __name__ == '__main__':
    main()
