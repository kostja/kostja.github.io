#!/usr/bin/env python3
"""Universal Compaction (Russian)."""

from excalidraw_lib import Doc

d = Doc(seed_base=860000)
RED = "#E23956"; LRED = "#F8CDD6"
BLUE = "#4B7BE5"; LBLUE = "#DBE6FA"
TEAL = "#2D9B8E"; LTEAL = "#CDF0EB"
GREY = "#737A82"; INK = "#2B1321"

d.text("title", 20, 10, 1100, 28,
       "Universal: одна ручка (W) на уровень — tiered ↔ leveled",
       size=20, color=INK)

LEVELS = [
    ("L0", "tiered (W=−2)",   8, LRED,  RED,  "tiered"),
    ("L1", "tiered (W=−1)",   6, LRED,  RED,  "tiered"),
    ("L2", "сбалансировано (W=0)", 4, LBLUE, BLUE, "hybrid"),
    ("L3", "leveled (W=+2)",  3, LTEAL, TEAL, "no overlap"),
]

LY0 = 75; ROW_H = 78; LX0 = 150
for i, (name, label, count, fill, stroke, note) in enumerate(LEVELS):
    y = LY0 + i * ROW_H
    d.text(f"n_{i}", 30, y + 24, 110, 26, name, size=18, color=GREY, align="right")
    if i < 2:
        for j in range(count):
            d.rect(f"b_{i}_{j}", LX0 + j * 60, y + 14, 54, 42, stroke=stroke,
                   bg=fill, sw=1, roundness=3)
    elif i == 2:
        for j in range(count):
            d.rect(f"b_{i}_{j}", LX0 + j * 100, y + 8, 90, 54, stroke=stroke,
                   bg=fill, sw=1, roundness=3)
    else:
        labels = ["a-h", "i-p", "q-z"]
        for j in range(count):
            d.rect(f"b_{i}_{j}", LX0 + j * 130, y + 2, 120, 64, stroke=stroke,
                   bg=fill, sw=1, roundness=3)
            d.text(f"b_{i}_{j}t", LX0 + j * 130, y + 2, 120, 64,
                   labels[j], size=14, color=stroke)
    d.text(f"nt_{i}", 660, y + 24, 360, 24, label, size=14, color=stroke, align="left")

# Annotations
ay = LY0 + 4 * ROW_H + 20
d.text("ann1", 20, ay, 1100, 22,
       "Cassandra UCS / RocksDB Universal: scaling_parameter (W) настраивает каждый уровень.",
       size=14, color=INK)
d.text("ann2", 20, ay + 28, 1100, 22,
       "Компромисс — предполагает, что вы знаете нагрузку и одной ручки достаточно.",
       size=14, color=GREY)

d.save("/home/kostja/work/kostja.github.io/assets/img/talks/universal_compaction.excalidraw")
