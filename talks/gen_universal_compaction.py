#!/usr/bin/env python3
"""Universal Compaction Strategy — Cassandra UCS / RocksDB Universal."""

from excalidraw_lib import Doc

d = Doc(seed_base=860000)
RED = "#E23956"; LRED = "#F8CDD6"
BLUE = "#4B7BE5"; LBLUE = "#DBE6FA"
TEAL = "#2D9B8E"; LTEAL = "#CDF0EB"
ORANGE = "#FF611D"
GREY = "#737A82"; INK = "#2B1321"

d.text("title", 20, 8, 760, 22,
       "Universal: one knob (W) per level — tiered ↔ leveled",
       size=14, color=INK)

# Show 4 levels, each with different W
LEVELS = [
    ("L0", -2, "tiered (W=−2)", 8, LRED, RED, "4 files/level"),
    ("L1", -1, "tiered (W=−1)", 6, LRED, RED, "tiered"),
    ("L2",  0, "balanced (W=0)", 4, LBLUE, BLUE, "hybrid"),
    ("L3",  2, "leveled (W=+2)", 3, LTEAL, TEAL, "no overlap"),
]

LY0 = 60; ROW_H = 60
LX0 = 100

for i, (name, w, label, count, fill, stroke, note) in enumerate(LEVELS):
    y = LY0 + i * ROW_H
    # label
    d.text(f"n_{i}", 20, y + 18, 80, 18, name, size=13, color=GREY, align="right")
    # boxes
    if i < 2:  # tiered: equal size, multiple
        for j in range(count):
            d.rect(f"b_{i}_{j}", LX0 + j * 50, y + 10, 44, 30, stroke=stroke,
                   bg=fill, sw=1, roundness=3)
    elif i == 2:  # balanced
        for j in range(count):
            d.rect(f"b_{i}_{j}", LX0 + j * 80, y + 5, 72, 40, stroke=stroke,
                   bg=fill, sw=1, roundness=3)
    else:  # leveled — non-overlapping ranges
        labels = ["a-h", "i-p", "q-z"]
        for j in range(count):
            d.rect(f"b_{i}_{j}", LX0 + j * 110, y, 100, 50, stroke=stroke,
                   bg=fill, sw=1, roundness=3)
            d.text(f"b_{i}_{j}t", LX0 + j * 110, y, 100, 50,
                   labels[j], size=11, color=stroke)
    # note
    d.text(f"nt_{i}", 480, y + 18, 280, 18, label, size=11, color=stroke, align="left")

# Annotations
d.text("ann1", 20, LY0 + 4 * ROW_H + 30, 760, 18,
       "Cassandra UCS / RocksDB Universal: scaling_parameter (W) tunes each level.",
       size=12, color=INK)
d.text("ann2", 20, LY0 + 4 * ROW_H + 52, 760, 18,
       "Compromise — assumes you know the workload, and that one knob is enough.",
       size=12, color=GREY)

d.save("/home/kostja/work/kostja.github.io/assets/img/talks/universal_compaction.excalidraw")
