#!/usr/bin/env python3
"""Shrink an .excalidraw file to fit a target canvas width.

For each element: scale x, y, width, height (and line points) by a uniform
factor chosen so the rightmost edge fits within TARGET_W. Font sizes are
scaled the same way but clamped to a minimum of MIN_FONT, so text stays
readable on the smaller canvas.

The net effect: a diagram that was designed for a 1100px viewBox becomes
a ~720px viewBox with the same content arrangement; text uses fonts
12-16 instead of 14-22; rendered at 720px on the page, fonts display at
true pixel size matching Vinyl-article diagrams.
"""

import json
import sys

TARGET_W = 720
MIN_FONT = 12
PAD = 8  # right-edge breathing room


def scale_excalidraw(path, target_w=TARGET_W, min_font=MIN_FONT):
    with open(path) as f:
        doc = json.load(f)

    els = doc.get("elements", [])
    if not els:
        return

    # Find current rightmost edge
    max_x = 0
    for el in els:
        ex = el.get("x", 0) + el.get("width", 0)
        if ex > max_x:
            max_x = ex
    if max_x <= target_w + PAD:
        print(f"  {path}: already fits ({max_x:.0f}px); skipping")
        return

    scale = target_w / (max_x + PAD)
    print(f"  {path}: max_x={max_x:.0f} -> scale={scale:.3f}")

    for el in els:
        for k in ("x", "y", "width", "height"):
            if k in el and isinstance(el[k], (int, float)):
                el[k] = el[k] * scale
        if "fontSize" in el and isinstance(el["fontSize"], (int, float)):
            el["fontSize"] = max(min_font, el["fontSize"] * scale)
        if "points" in el and isinstance(el["points"], list):
            el["points"] = [[p[0] * scale, p[1] * scale] for p in el["points"]]
        # strokeWidth: leave alone (rough sketch lines look bad if too thin)

    with open(path, "w") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
    print(f"  {path}: scaled")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        scale_excalidraw(p)
