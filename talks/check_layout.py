#!/usr/bin/env python3
"""Sanity check: for each text element, does the text plausibly fit its box?

Cascadia Code is monospace. We estimate width per char ≈ fontSize * 0.6
(slightly over-estimates for digits / narrow chars, which is the safe side).
Reports text elements whose estimated rendered width exceeds their container
width by more than 5%.
"""

import json
import os
import sys

# Cascadia mono approximate width per character per pixel of font size.
CHAR_WIDTH_RATIO = 0.60
# Allow 5% slack — Cascadia handles Cyrillic slightly narrower in practice.
TOLERANCE = 1.05


def check_file(path):
    d = json.load(open(path))
    issues = []
    for el in d.get("elements", []):
        if el.get("type") != "text":
            continue
        text = el.get("text", "")
        size = el.get("fontSize", 14)
        # Longest line in multiline text
        max_line = max(text.split("\n"), key=len) if text else ""
        # Cyrillic chars take slightly more visual width
        n_chars = len(max_line)
        est_w = n_chars * size * CHAR_WIDTH_RATIO
        box_w = el.get("width", 0)
        if box_w > 0 and est_w > box_w * TOLERANCE:
            issues.append((text[:40], size, n_chars, int(est_w), int(box_w)))
    return issues


def main():
    talks_dir = "/home/kostja/work/kostja.github.io/assets/img/talks"
    files = sorted(f for f in os.listdir(talks_dir) if f.endswith(".excalidraw"))
    any_issue = False
    for f in files:
        path = os.path.join(talks_dir, f)
        issues = check_file(path)
        if issues:
            any_issue = True
            print(f"\n=== {f} ===")
            for text, size, n, est, box in issues:
                print(f"  '{text}'  (size={size}, chars={n}, est={est}px, box={box}px)")
    if not any_issue:
        print("All text fits within boxes.")
    return 1 if any_issue else 0


if __name__ == "__main__":
    sys.exit(main())
