#!/usr/bin/env python3
"""LCS workload pain — Russian."""

from excalidraw_lib import Doc

d = Doc(seed_base=850000)
RED = "#E23956"; LRED = "#F8CDD6"
DANGER = "#B91A36"; LDANGER = "#F09CAB"
ORANGE = "#FF611D"
BLUE = "#4B7BE5"; LBLUE = "#DBE6FA"
GREY = "#737A82"; INK = "#2B1321"

d.text("title", 20, 10, 1100, 28,
       "LCS болит: 1 байт на L0 → 30 байт через каскад",
       size=20, color=INK)

# LEFT PANEL: write amplification cascade
PX0 = 30
d.text("p1t", PX0, 65, 480, 24, "1. Каскад write-amp", size=16, color=INK, align="left")

LEVELS = [
    (0, "L0 → дамп",   "1×",  LRED,    RED),
    (1, "L1 → слияние","10×", LBLUE,   BLUE),
    (2, "L2 → слияние","10×", LBLUE,   BLUE),
    (3, "L3 → слияние","10×", LBLUE,   BLUE),
    (4, "Σ всего",     "31×", LDANGER, DANGER),
]
LY0 = 100; ROW_H = 50
for lvl, name, mult, fill, stroke in LEVELS:
    y = LY0 + lvl * ROW_H
    d.rect(f"l_{lvl}", PX0, y, 320, 40, stroke=stroke, bg=fill, sw=1, roundness=3)
    d.text(f"l_{lvl}_n", PX0 + 10, y, 240, 40, name, size=14, color=stroke, align="left")
    d.text(f"l_{lvl}_m", PX0 + 240, y, 70, 40, mult, size=18, color=stroke)
    if 0 < lvl < 4:
        d.arrow(f"l_{lvl}_a", PX0 + 160, y - 10, [[0, 0], [0, -10]], color=ORANGE, sw=1.5, roughness=0)

# RIGHT PANEL: throughput collapse
PX1 = 530
d.text("p2t", PX1, 65, 580, 24, "2. Пропускная способность падает",
       size=16, color=INK, align="left")

GX0 = PX1 + 60; GY0 = 110; GW = 480; GH = 160
d.rect("g_box", GX0, GY0, GW, GH, stroke=GREY, bg="transparent", sw=1, roundness=0)
d.text("g_x", GX0, GY0 + GH + 6, GW, 18, "время →", size=12, color=GREY, align="right")
d.text("g_y", PX1, GY0 + GH/2 - 12, 56, 22, "МБ/с", size=14, color=GREY, align="right")

d.line("g_l1", GX0 + 10, GY0 + 30, [[0, 0], [110, 8]], color=BLUE, sw=2, roughness=0)
d.line("g_l2", GX0 + 120, GY0 + 38, [[0, 0], [70, 35]], color=DANGER, sw=2, roughness=0)
d.line("g_l3", GX0 + 190, GY0 + 73, [[0, 0], [120, 45]], color=DANGER, sw=2, roughness=0)
d.line("g_l4", GX0 + 310, GY0 + 118, [[0, 0], [150, 20]], color=DANGER, sw=2, roughness=0)

d.text("ann_high", GX0 + 30, GY0 + 6, 110, 18, "пик записи", size=12, color=BLUE, align="left")
d.text("ann_collapse", GX0 + 220, GY0 + 130, 200, 18, "compaction-долг",
       size=12, color=DANGER, align="left")

# SSD wear box
WY = GY0 + GH + 40
d.rect("wbox", GX0, WY, GW, 50, stroke=DANGER, bg=LDANGER, sw=1, roundness=3)
d.text("wt", GX0, WY, GW, 50,
       "Износ SSD (DWPD) — жёсткий потолок", size=14, color=DANGER)

# Bottom annotation
d.text("ann", 20, 410, 1100, 22,
       "Bulk ingest (CDC, backfill, IoT): write amp превращает износ SSD в бутылочное горлышко.",
       size=14, color=INK)

d.save("/home/kostja/work/kostja.github.io/assets/img/talks/lcs_workload_pain.excalidraw")
