#!/usr/bin/env python3
"""2D time × key continuum: compaction as cluster covering.

Updates plotted as dots in (time, key) space. Three cluster shapes —
diagonal stripe, dense blob, scattered noise — and how files (axis-aligned
rectangles) try to cover them. After-compaction inset shown BELOW the
plot to avoid label crowding inside the scatter area.
"""

import math
import hashlib
from excalidraw_lib import Doc

d = Doc(seed_base=940000)
RED = "#E23956"
BLUE = "#4B7BE5"
ORANGE = "#FF611D"
GREEN = "#2E7D32"
GREY = "#737A82"; INK = "#2B1321"
DOT = "#2B1321"

d.text("title", 20, 10, 1200, 30,
       "Compaction как кластеризация в (время, ключ)",
       size=22, color=INK)

# ── Coordinate plane ──────────────────────────────────────
PX0 = 130; PY0 = 80
PW = 780; PH = 320

# Axes
d.line("ax_x", PX0, PY0 + PH, [[0, 0], [PW + 12, 0]],
       color=GREY, sw=2, roughness=0)
d.line("ax_y", PX0, PY0, [[0, 0], [0, PH + 12]],
       color=GREY, sw=2, roughness=0)

d.text("lbl_x", PX0, PY0 + PH + 16, PW, 24,
       "время →", size=16, color=GREY, align="right")
d.text("lbl_y", 20, PY0 + PH/2 - 14, 100, 24,
       "ключ ↑", size=16, color=GREY, align="right")

d.rect("frame", PX0, PY0, PW, PH, stroke=GREY, bg="transparent", sw=0.5,
       roundness=0)


def dot(eid, x, y, r=4, color=DOT):
    d.rect(eid, x - r, y - r, 2 * r, 2 * r,
           stroke=color, bg=color, sw=1, fill="solid", roundness=0)


def prng(i):
    h = hashlib.md5(str(i).encode()).digest()
    return (h[0] - 128) / 128.0


# ── Cluster 1: DIAGONAL STRIPE (time-series / key-order sweep) ──
x1a, y1a = PX0 + 40,  PY0 + PH - 40
x1b, y1b = PX0 + 340, PY0 + 40
N1 = 26
for i in range(N1):
    t = i / (N1 - 1)
    cx = x1a + (x1b - x1a) * t
    cy = y1a + (y1b - y1a) * t
    j = prng(i) * 14
    dx = -(y1b - y1a)
    dy = (x1b - x1a)
    m = math.hypot(dx, dy)
    px = cx + dx / m * j
    py = cy + dy / m * j
    dot(f"d1_{i}", px, py, r=4, color=RED)

# Loose rectangle covering the diagonal
RECT1_X = PX0 + 20; RECT1_Y = PY0 + 20
RECT1_W = 350; RECT1_H = PH - 40
d.rect("r1", RECT1_X, RECT1_Y, RECT1_W, RECT1_H,
       stroke=RED, bg="transparent", sw=2.5, ss="dashed", roundness=3)
# Loose-fit caption — top inside the rectangle
d.text("r1_lbl", RECT1_X + 10, RECT1_Y + 8, 380, 22,
       "файл накрывает диагональ", size=14, color=RED, align="left")
d.text("r1_lbl2", RECT1_X + 10, RECT1_Y + RECT1_H - 28, 380, 22,
       "(половина площади пуста)", size=12, color=RED, align="left")

# ── Cluster 2: DENSE BLOB (hot-key OLTP churn) ──
CX2, CY2 = PX0 + 580, PY0 + 170
N2 = 32
for i in range(N2):
    rx = prng(i + 200) * 60
    ry = prng(i + 300) * 36
    dot(f"d2_{i}", CX2 + rx, CY2 + ry, r=4, color=BLUE)

# Tight rectangle around the blob
RECT2_X = CX2 - 70; RECT2_Y = CY2 - 46
RECT2_W = 140; RECT2_H = 92
d.rect("r2", RECT2_X, RECT2_Y, RECT2_W, RECT2_H,
       stroke=BLUE, bg="transparent", sw=2.5, ss="dashed", roundness=3)
# Tight-fit caption — above the rectangle, with breathing room
d.text("r2_lbl", RECT2_X - 80, RECT2_Y - 32, 380, 22,
       "файл накрывает кластер плотно", size=13, color=BLUE, align="left")

# ── Cluster 3: SCATTERED (random noise) ──
for i in range(14):
    rx = (prng(i + 500) + 1) / 2 * (PW - 80) + PX0 + 40
    ry = (prng(i + 600) + 1) / 2 * (PH - 80) + PY0 + 40
    dot(f"d3_{i}", rx, ry, r=3, color=GREY)

# ── After-compaction inset BELOW the plot ──
INS_Y = PY0 + PH + 60
# Caption on the left
d.text("comp_lbl", PX0 + 20, INS_Y - 24, 520, 24,
       "после слияния — по одной строке на ключ:",
       size=14, color=GREEN, align="left")
# Single thin line of dots
COMP_X0 = PX0 + 60
for i in range(20):
    dot(f"comp_{i}", COMP_X0 + i * 16, INS_Y, r=4, color=GREEN)

# Arrow from blob down to the compacted line
d.arrow("arr", CX2 - 80, CY2 + 50, [[0, 0], [-160, INS_Y - CY2 - 60]],
        color=ORANGE, sw=2, roughness=0)
d.text("arr_t", CX2 - 270, CY2 + 130, 160, 22,
       "compaction",
       size=14, color=ORANGE, align="right")

# ── Annotations below everything ──────────────────────────
BOT_Y = INS_Y + 50
d.text("ann1", 20, BOT_Y, 1280, 26,
       "Файл, SSTable, run — осе-выровненный прямоугольник, накрывающий кластер обновлений.",
       size=14, color=INK)
d.text("ann2", 20, BOT_Y + 30, 1280, 26,
       "Чем плотнее прямоугольник к форме кластера, тем меньше bloat и read amp.",
       size=14, color=GREY)

d.save("/home/kostja/work/kostja.github.io/assets/img/talks/compaction_continuum.excalidraw")
