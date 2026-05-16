#!/usr/bin/env python3
"""Size-Tiered Compaction Strategy diagram (Russian)."""

from excalidraw_lib import Doc

d = Doc(seed_base=820000)
RED = "#E23956"; LRED = "#F8CDD6"
ORANGE = "#FF611D"
GREY = "#737A82"; INK = "#2B1321"

d.text("title", 20, 10, 1000, 28,
       "Size-Tiered: группировка по размеру, слияние при накоплении N",
       size=20, color=INK)

def tier_label(eid, x, y, txt):
    d.text(eid, x, y, 220, 22, txt, size=14, color=GREY, align="right")

# Tier 1
TY = 80
for i in range(4):
    d.rect(f"t1_{i}", 280 + i * 60, TY, 52, 50, stroke=RED, bg=LRED, sw=1, roundness=3)
    d.text(f"t1_{i}t", 280 + i * 60, TY, 52, 50, "8 МБ", size=12, color=RED)
tier_label("t1lbl", 30, TY + 14, "уровень 1 (мелкие):")

# Arrow: merge
d.arrow("am1", 520, TY + 25, [[0, 0], [50, 70]], color=ORANGE, sw=1.5, roughness=0)
d.text("am1t", 570, TY + 40, 80, 18, "слияние", size=14, color=ORANGE)

# Tier 2
T2Y = TY + 110
for i in range(4):
    d.rect(f"t2_{i}", 280 + i * 80, T2Y, 72, 60, stroke=RED, bg=LRED, sw=1, roundness=3)
    d.text(f"t2_{i}t", 280 + i * 80, T2Y, 72, 60, "32 МБ", size=14, color=RED)
tier_label("t2lbl", 30, T2Y + 20, "уровень 2 (средние):")

d.arrow("am2", 600, T2Y + 30, [[0, 0], [70, 80]], color=ORANGE, sw=1.5, roughness=0)
d.text("am2t", 680, T2Y + 60, 80, 18, "слияние", size=14, color=ORANGE)

# Tier 3
T3Y = T2Y + 130
d.rect("t3", 280, T3Y, 350, 80, stroke=RED, bg="#F09CAB", sw=1, roundness=3)
d.text("t3t", 280, T3Y, 350, 80, "128 МБ — слито", size=16, color=RED)
tier_label("t3lbl", 30, T3Y + 28, "уровень 3 (большой):")

# Right side: rules
PX = 700; PY = TY
d.text("h0", PX, PY, 280, 22, "Правила", size=16, color=INK, align="left")
for i, line in enumerate([
    "• файлы группируются по размеру",
    "• при N=4 одного размера → слияние",
    "• результат идёт в следующий уровень",
    "• в стабильном режиме — низкий",
    "  write amplification",
]):
    d.text(f"h{i+1}", PX, PY + 30 + i * 24, 320, 22, line, size=14, color=INK, align="left")

d.save("/home/kostja/work/kostja.github.io/assets/img/talks/size_tiered_compaction.excalidraw")
