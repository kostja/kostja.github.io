#!/usr/bin/env python3
"""Leveled Compaction Strategy diagram."""

from excalidraw_lib import Doc

d = Doc(seed_base=840000)
RED = "#E23956"; LRED = "#F8CDD6"
BLUE = "#4B7BE5"; LBLUE = "#DBE6FA"
GREY = "#737A82"; INK = "#2B1321"
ORANGE = "#FF611D"

d.text("title", 20, 8, 700, 22,
       "Leveled: non-overlapping levels, each ×10 the size",
       size=14, color=INK)

# L0: 4 small files (can overlap)
LX0 = 140
def small_file(eid, x, y, w, h, label, stroke, fill, fs="solid"):
    d.rect(eid, x, y, w, h, stroke=stroke, bg=fill, sw=1, fill=fs, roundness=3)
    d.text(eid + "_t", x, y, w, h, label, size=9, color=stroke)

L0Y = 50
d.text("l0lbl", 20, L0Y + 8, 110, 16, "L0 (overlap)", size=11, color=GREY, align="right")
for i in range(4):
    small_file(f"l0_{i}", LX0 + i*60, L0Y, 50, 28, "a–z", RED, LRED)

# L1: tiles of non-overlapping ranges
L1Y = L0Y + 60
d.text("l1lbl", 20, L1Y + 8, 110, 16, "L1  (10×, no overlap)", size=11, color=GREY, align="right")
RANGES_L1 = ["a–e", "f–j", "k–o", "p–t", "u–z"]
for i, r in enumerate(RANGES_L1):
    small_file(f"l1_{i}", LX0 + i*60, L1Y, 56, 28, r, BLUE, LBLUE)

# L2: more, smaller tiles
L2Y = L1Y + 60
d.text("l2lbl", 20, L2Y + 8, 110, 16, "L2  (100×)", size=11, color=GREY, align="right")
RANGES_L2 = ["a-c", "d-e", "f-h", "i-j", "k-m", "n-o", "p-r", "s-t", "u-w", "x-z"]
for i, r in enumerate(RANGES_L2):
    small_file(f"l2_{i}", LX0 + i*30, L2Y, 26, 28, r, BLUE, LBLUE)

# L3: even more
L3Y = L2Y + 60
d.text("l3lbl", 20, L3Y + 8, 110, 16, "L3  (1000×)", size=11, color=GREY, align="right")
for i in range(20):
    d.rect(f"l3_{i}", LX0 + i*15, L3Y, 13, 28, stroke=BLUE, bg=LBLUE, sw=1, roundness=3)

# Right side: properties
PX = 480
d.text("h0", PX, L0Y, 240, 18, "Properties", size=13, color=INK, align="left")
for i, line in enumerate([
    "• point read: ≤ 1 file per level",
    "• read amp = O(log₁₀ N)",
    "• levels disjoint by key range",
    "• promotion = re-merge whole range",
]):
    d.text(f"h{i+1}", PX, L0Y + 24 + i*22, 270, 18, line, size=11, color=INK, align="left")

# Arrow: promotion
d.arrow("prom", 100, L0Y + 28, [[0, 0], [0, 160]], color=ORANGE, sw=1.5, roughness=0)
d.text("prom_t", 30, L0Y + 90, 80, 16, "promotion", size=10, color=ORANGE)

d.save("/home/kostja/work/kostja.github.io/assets/img/talks/leveled_compaction.excalidraw")
