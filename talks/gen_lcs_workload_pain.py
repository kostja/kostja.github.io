#!/usr/bin/env python3
"""LCS workload pain — write-amp cascade, SSD wear, throughput collapse."""

from excalidraw_lib import Doc

d = Doc(seed_base=850000)
RED = "#E23956"; LRED = "#F8CDD6"
DANGER = "#B91A36"; LDANGER = "#F09CAB"
ORANGE = "#FF611D"; LORANGE = "#FFE0D0"
BLUE = "#4B7BE5"; LBLUE = "#DBE6FA"
GREY = "#737A82"; INK = "#2B1321"

d.text("title", 20, 8, 720, 22,
       "LCS pain: 1 byte at L0 → 30 bytes through the cascade",
       size=14, color=INK)

# LEFT PANEL: write amplification cascade
PX0 = 30
d.text("p1t", PX0, 50, 360, 18, "1. Write-amp cascade", size=13, color=INK, align="left")

# 5 levels with bytes-rewritten counter
LEVELS = [(0, "L0 → flush", "1×", LRED, RED),
          (1, "L1 → merge", "10×", LBLUE, BLUE),
          (2, "L2 → merge", "10×", LBLUE, BLUE),
          (3, "L3 → merge", "10×", LBLUE, BLUE),
          (4, "Σ total", "31×", LDANGER, DANGER)]

LY0 = 80
for lvl, name, mult, fill, stroke in LEVELS:
    y = LY0 + lvl * 38
    d.rect(f"l_{lvl}", PX0, y, 200, 30, stroke=stroke, bg=fill, sw=1, roundness=3)
    d.text(f"l_{lvl}_n", PX0 + 8, y, 150, 30, name, size=11, color=stroke, align="left")
    d.text(f"l_{lvl}_m", PX0 + 150, y, 50, 30, mult, size=12, color=stroke)
    if lvl > 0 and lvl < 4:
        d.arrow(f"l_{lvl}_a", PX0 + 100, y - 8, [[0, 0], [0, -8]], color=ORANGE, sw=1.5, roughness=0)

# RIGHT PANEL: throughput collapse
PX1 = 440
d.text("p2t", PX1, 50, 320, 18, "2. Sustained throughput collapses", size=13, color=INK, align="left")

# Simple line graph: throughput vs time
GX0 = PX1; GY0 = 90; GW = 280; GH = 130
d.rect("g_box", GX0, GY0, GW, GH, stroke=GREY, bg="transparent", sw=1, roundness=0)
# X axis label
d.text("g_x", GX0, GY0 + GH + 4, GW, 14, "time →", size=10, color=GREY, align="right")
d.text("g_y", GX0 - 60, GY0 + GH/2 - 10, 58, 16, "MB/s", size=10, color=GREY, align="right")

# Curve: high, then collapse
d.line("g_l1", GX0 + 10, GY0 + 30, [[0, 0], [60, 5]], color=BLUE, sw=2, roughness=0)
d.line("g_l2", GX0 + 70, GY0 + 35, [[0, 0], [40, 25]], color=DANGER, sw=2, roughness=0)
d.line("g_l3", GX0 + 110, GY0 + 60, [[0, 0], [80, 35]], color=DANGER, sw=2, roughness=0)
d.line("g_l4", GX0 + 190, GY0 + 95, [[0, 0], [80, 15]], color=DANGER, sw=2, roughness=0)

d.text("ann_high", GX0 + 20, GY0 + 10, 90, 14, "ingest peak", size=10, color=BLUE, align="left")
d.text("ann_collapse", GX0 + 140, GY0 + 110, 130, 14, "compaction debt", size=10, color=DANGER, align="left")

# SSD wear icon (just text in box)
WX = PX1; WY = GY0 + GH + 30
d.rect("wbox", WX, WY, 280, 36, stroke=DANGER, bg=LDANGER, sw=1, roundness=3)
d.text("wt", WX, WY, 280, 36, "SSD wear (DWPD) — the hard ceiling", size=11, color=DANGER)

# Bottom annotation
d.text("ann", 20, 290, 760, 18,
       "Bulk ingest (CDC, backfill, IoT): write amp turns SSD wear into the bottleneck.",
       size=12, color=INK)

d.save("/home/kostja/work/kostja.github.io/assets/img/talks/lcs_workload_pain.excalidraw")
