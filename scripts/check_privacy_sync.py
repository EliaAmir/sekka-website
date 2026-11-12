#!/usr/bin/env python3
"""Fail if the two published privacy-policy pages disagree.

Extracts the visible text of the <main id="ar"> and <main id="en"> blocks
from the old page (eliaamir.github.io/sekka-privacy/, source at
../sekka-privacy/index.html) and the new page (privacy/index.html in this
repo), strips markup, normalizes whitespace, and diffs each language block.
Exits non-zero and prints a diff if anything differs.

Since the old address was retired (sekka-privacy d7cc7a3), its index.html holds
no policy text and only forwards to https://sekka-eg.com/privacy/. In that case
the check passes when the old page still forwards there (canonical link, meta
refresh and script) and the new page has both language blocks.

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
CANONICAL = "https://sekka-eg.com/privacy/"
# what the retired old page must contain to count as forwarding to the canonical page
FORWARD_MARKS = (
    f'<link rel="canonical" href="{CANONICAL}">',
    f'url={CANONICAL}"',
    f"location.replace('{CANONICAL}'",
)
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

    old_html = old_path.read_text(encoding="utf-8")
    old_blocks = extract_blocks(old_html)
    new_blocks = extract_blocks(new_path.read_text(encoding="utf-8"))

    # The old address is retired: sekka-privacy/index.html no longer carries the text, it forwards to the canonical page.
    # Then there is nothing to diff; check instead that it still forwards there and that the new page has both languages.
    if not old_blocks:
        missing = [m for m in FORWARD_MARKS if m not in old_html]
        if missing:
            print(f"FAIL: {old_path} carries no policy text and does not forward to {CANONICAL}:")
            for m in missing:
                print(f"  missing: {m}")
            return 1
        empty = [lang for lang in ("ar", "en") if not new_blocks.get(lang)]
        if empty:
            print(f"FAIL: {new_path} has no text in <main id=\"{'/'.join(empty)}\">")
            return 1
        print(f"OK: {old_path} forwards to {CANONICAL} (canonical, meta refresh and script), so there is no second copy to drift.")
        for lang in ("ar", "en"):
            print(f"OK: '{lang}' policy text present in {new_path} ({len(new_blocks[lang])} chars)")
        return 0

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
