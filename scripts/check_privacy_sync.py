#!/usr/bin/env python3
"""Fail if the two published privacy-policy pages disagree.

Extracts the visible text of the <main id="ar"> and <main id="en"> blocks
from the old page (eliaamir.github.io/sekka-privacy/, source at
../sekka-privacy/index.html) and the new page (privacy/index.html in this
repo), strips markup, normalizes whitespace, and diffs each language block.
Exits non-zero and prints a diff if anything differs.

The old page carries two small additions the new page must NOT carry: the
canonical link and the "also published at sekka-eg.com/privacy" banner line.
Those live outside the <main id="..."> blocks, so they never enter this
comparison.

Usage:
    python3 scripts/check_privacy_sync.py [old_path] [new_path]

Defaults assume the sibling-repo layout used on this machine:
    old_path = ../sekka-privacy/index.html
    new_path = privacy/index.html
"""
import re
import sys
from html import unescape
from pathlib import Path

MAIN_RE = re.compile(
    r'<main\s+id="(ar|en)"[^>]*>(.*?)</main>', re.DOTALL
)
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def extract_blocks(html: str) -> dict:
    blocks = {}
    for match in MAIN_RE.finditer(html):
        lang, inner = match.group(1), match.group(2)
        text = TAG_RE.sub(" ", inner)
        text = unescape(text)
        text = WS_RE.sub(" ", text).strip()
        blocks[lang] = text
    return blocks


def main():
    here = Path(__file__).resolve().parent.parent
    old_path = Path(sys.argv[1]) if len(sys.argv) > 1 else here.parent / "sekka-privacy" / "index.html"
    new_path = Path(sys.argv[2]) if len(sys.argv) > 2 else here / "privacy" / "index.html"

    if not old_path.exists():
        print(f"FAIL: old policy not found at {old_path}")
        return 2
    if not new_path.exists():
        print(f"FAIL: new policy not found at {new_path}")
        return 2

    old_blocks = extract_blocks(old_path.read_text(encoding="utf-8"))
    new_blocks = extract_blocks(new_path.read_text(encoding="utf-8"))

    ok = True
    for lang in ("ar", "en"):
        old_text = old_blocks.get(lang)
        new_text = new_blocks.get(lang)
        if old_text is None or new_text is None:
            print(f"FAIL: missing <main id=\"{lang}\"> block in one of the two files")
            ok = False
            continue
        if old_text != new_text:
            ok = False
            print(f"FAIL: '{lang}' policy text differs between\n  {old_path}\n  {new_path}\n")
            # show first point of divergence
            for i, (a, b) in enumerate(zip(old_text, new_text)):
                if a != b:
                    start = max(0, i - 60)
                    print(f"  first divergence at char {i}:")
                    print(f"    old: ...{old_text[start:i+60]}...")
                    print(f"    new: ...{new_text[start:i+60]}...")
                    break
            else:
                print(f"    length differs: old={len(old_text)} new={len(new_text)}")
        else:
            print(f"OK: '{lang}' policy text is identical ({len(old_text)} chars)")

    if ok:
        print("\nOK: both languages match word-for-word between old and new pages.")
        return 0
    else:
        print("\nFAIL: policy text has drifted — fix before publishing.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
