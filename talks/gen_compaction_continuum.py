#!/usr/bin/env python3
"""2D time × key continuum: compaction as cluster covering.

Plots updates as dots in (time, key) space. Shows three natural cluster
shapes — diagonal stripe, dense blob, scattered noise — and how files
(axis-aligned rectangles) try to cover them. Punchline: tight cover on
the blob, wasteful cover on the diagonal; compaction collapses a cluster
to a deduplicated line.
"""

import math
from excalidraw_lib import Doc

d = Doc(seed_base=940000)
RED = "#E23956"; LRED = "#F8CDD6"
BLUE = "#4B7BE5"; LBLUE = "#DBE6FA"
TEAL = "#2D9B8E"; LTEAL = "#CDF0EB"
ORANGE = "#FF611D"; LORANGE = "#FFE0D0"
GREEN = "#2E7D32"; LGREEN = "#C8E6C9"
GREY = "#737A82"; INK = "#2B1321"
DOT = "#2B1321"

d.text("title", 20, 10, 1200, 28,
       "Compaction как кластеризация в (время, ключ)",
       size=20, color=INK)

# ── Coordinate plane ──────────────────────────────────────
PX0 = 120; PY0 = 70
PW = 780; PH = 360

# Axes
d.line("ax_x", PX0, PY0 + PH, [[0, 0], [PW + 10, 0]],
       color=GREY, sw=2, roughness=0)
d.line("ax_y", PX0, PY0, [[0, 0], [0, PH + 10]],
       color=GREY, sw=2, roughness=0)

# Axis labels
d.text("lbl_x", PX0, PY0 + PH + 12, PW, 22,
       "время →", size=14, color=GREY, align="right")
d.text("lbl_y", 20, PY0 + PH/2 - 12, 90, 22,
       "ключ ↑", size=14, color=GREY, align="right")

# Plot frame (faint)
d.rect("frame", PX0, PY0, PW, PH, stroke=GREY, bg="transparent", sw=0.5,
       roundness=0)


def dot(eid, x, y, r=3, color=DOT):
    """Tiny filled square as a scatter point."""
    d.rect(eid, x - r, y - r, 2 * r, 2 * r,
           stroke=color, bg=color, sw=1, fill="solid", roundness=0)


# ── Cluster 1: DIAGONAL STRIPE (time-series / key-order sweep) ──
# Line from (PX0+40, PY0+PH-40) → (PX0+340, PY0+40), with perpendicular jitter
import hashlib
def prng(i):
    h = hashlib.md5(str(i).encode()).digest()
    return (h[0] - 128) / 128.0

x1a, y1a = PX0 + 40,  PY0 + PH - 40
x1b, y1b = PX0 + 340, PY0 + 40
N1 = 28
for i in range(N1):
    t = i / (N1 - 1)
    cx = x1a + (x1b - x1a) * t
    cy = y1a + (y1b - y1a) * t
    # perpendicular jitter
    j = prng(i) * 14
    dx = -(y1b - y1a)
    dy = (x1b - x1a)
    m = math.hypot(dx, dy)
    px = cx + dx / m * j
    py = cy + dy / m * j
    dot(f"d1_{i}", px, py, r=3, color=RED)

# Label for diagonal
d.text("c1_lbl", PX0 + 220, PY0 + PH - 18, 200, 22,
       "key-order sweep", size=12, color=RED, align="left")

# Loose rectangle covering the diagonal (axis-aligned, lots of empty area)
RECT1_X = PX0 + 20; RECT1_Y = PY0 + 20
RECT1_W = 350; RECT1_H = PH - 40
d.rect("r1", RECT1_X, RECT1_Y, RECT1_W, RECT1_H,
       stroke=RED, bg="transparent", sw=2, ss="dashed", roundness=3)
d.text("r1_lbl", RECT1_X + 6, RECT1_Y + 4, 200, 18,
       "файл (range × time)", size=11, color=RED, align="left")
d.text("r1_lbl2", RECT1_X + 6, RECT1_Y + RECT1_H - 22, 220, 18,
       "большая часть площади — пустая", size=10, color=RED, align="left")

# ── Cluster 2: DENSE BLOB (hot-key OLTP churn) ──
CX2, CY2 = PX0 + 540, PY0 + 200
N2 = 32
for i in range(N2):
    rx = prng(i + 200) * 50
    ry = prng(i + 300) * 32
    dot(f"d2_{i}", CX2 + rx, CY2 + ry, r=3, color=BLUE)

# Tight rectangle around the blob (good fit)
RECT2_X = CX2 - 58; RECT2_Y = CY2 - 40
RECT2_W = 120; RECT2_H = 82
d.rect("r2", RECT2_X, RECT2_Y, RECT2_W, RECT2_H,
       stroke=BLUE, bg="transparent", sw=2, ss="dashed", roundness=3)
d.text("r2_lbl", RECT2_X, RECT2_Y - 22, RECT2_W + 80, 18,
       "файл накрывает кластер плотно", size=11, color=BLUE, align="left")

# ── Cluster 3: SCATTERED (random noise) ──
for i in range(15):
    rx = (prng(i + 500) + 1) / 2 * (PW - 60) + PX0 + 30
    ry = (prng(i + 600) + 1) / 2 * (PH - 60) + PY0 + 30
    dot(f"d3_{i}", rx, ry, r=2, color=GREY)

# ── After-compaction inset: collapse blob → line ──
# Arrow from blob to inset
INS_X = PX0 + 540; INS_Y = PY0 + PH - 50
d.arrow("arr", CX2 + 70, CY2 + 30, [[0, 0], [-10, INS_Y - CY2 - 30]],
        color=ORANGE, sw=1.5, roughness=0)
# Single-row "after compaction" — thin band of dots
COMP_Y = INS_Y
COMP_X0 = CX2 - 50
for i in range(12):
    dot(f"comp_{i}", COMP_X0 + i * 10, COMP_Y, r=3, color=GREEN)
d.text("comp_lbl", COMP_X0 - 200, COMP_Y - 10, 200, 18,
       "после слияния:", size=11, color=GREEN, align="right")
d.text("comp_lbl2", COMP_X0 - 200, COMP_Y + 6, 200, 18,
       "по одному ключу",  size=11, color=GREEN, align="right")

# ── Annotations below the plot ────────────────────────────
BOT_Y = PY0 + PH + 40
d.text("ann1", 20, BOT_Y, 1180, 22,
       "Файл, SSTable, run — это всегда осе-выровненный прямоугольник, накрывающий естественный кластер обновлений.",
       size=14, color=INK)
d.text("ann2", 20, BOT_Y + 26, 1180, 22,
       "Чем точнее прямоугольник подогнан под форму кластера — тем меньше bloat и тем меньше read amp.",
       size=14, color=GREY)

d.save("/home/kostja/work/kostja.github.io/assets/img/talks/compaction_continuum.excalidraw")
