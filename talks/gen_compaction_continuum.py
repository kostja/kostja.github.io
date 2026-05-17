#!/usr/bin/env python3
"""2D (key × time) continuum: compaction as cluster covering.

Axes:
- X = key  (grows right)
- Y = time (grows UP — newer events at the top, like a Tetris board)

Three natural cluster shapes:
- Diagonal stripe = key-order sweep / time-series append
- Tall narrow blob = hot OLTP keys updated continuously
- Scattered = random workload noise

Files (axis-aligned rectangles) try to cover those clusters; after a
compaction, a cluster collapses to one entry per key (a horizontal row
shown in the right-hand inset).
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

d.text("title", 20, 10, 1240, 30,
       "Compaction как кластеризация в пространстве (время, ключ)",
       size=22, color=INK)

# ── Labels above the plot, color-coded to their rectangles ────
# These sit BETWEEN the title and the plot so they cannot overlap
# the scatter points.
d.text("r1_lbl", 100, 50, 380, 22,
       "файл ограничивает диагональ", size=14, color=RED, align="left")
d.text("r2_lbl", 360, 50, 420, 22,
       "файл плотно ограничивает кластер", size=14, color=BLUE, align="right")

# ── Coordinate plane ──────────────────────────────────────
PX0 = 100; PY0 = 90
PW = 660; PH = 420
PX1 = PX0 + PW   # 760
PY1 = PY0 + PH   # 510

# Axes with arrowheads. Y axis is drawn from bottom-up so its arrow
# points up (= "time grows up"). X axis points right naturally.
d.arrow("ax_x", PX0, PY1, [[0, 0], [PW + 12, 0]],
        color=GREY, sw=2, roughness=0)
d.arrow("ax_y", PX0, PY1 + 12, [[0, 0], [0, -(PH + 22)]],
        color=GREY, sw=2, roughness=0)

# Axis labels — direction is conveyed by the axis arrowheads, so the
# labels carry just the name. Boxes sized to stay clear of the heads.
d.text("lbl_x", PX0, PY1 + 22, PW + 12, 22,
       "ключ", size=16, color=GREY, align="right")
d.text("lbl_y", 0, PY0 - 6, 80, 22,
       "время", size=16, color=GREY, align="right")

# (No plot frame — the axes define the plot boundary. A frame
# rectangle drawn at (PX0, PY0)+(PW, PH) would overlap the axes
# along its left and bottom edges.)


def dot(eid, x, y, r=4, color=DOT):
    d.rect(eid, x - r, y - r, 2 * r, 2 * r,
           stroke=color, bg=color, sw=1, fill="solid", roundness=0)


def prng(i):
    h = hashlib.md5(str(i).encode()).digest()
    return (h[0] - 128) / 128.0


# ── Cluster 1: DIAGONAL stripe (key-order sweep) ──
# Bottom-left of plot (early time, low keys) to upper-mid (recent, mid keys).
x1a, y1a = PX0 + 50,  PY1 - 50
x1b, y1b = PX0 + 380, PY0 + 60
N1 = 26
for i in range(N1):
    t = i / (N1 - 1)
    cx = x1a + (x1b - x1a) * t
    cy = y1a + (y1b - y1a) * t
    j = prng(i) * 14
    dx = -(y1b - y1a); dy = (x1b - x1a)
    m = math.hypot(dx, dy)
    px = cx + dx / m * j
    py = cy + dy / m * j
    dot(f"d1_{i}", px, py, r=4, color=RED)

# Loose axis-aligned rectangle around diagonal.
# (The diagonal lives in the bottom-left half; this rectangle wraps it
# generously so the two empty corners — upper-left and lower-right of
# the rectangle — are visible.)
RECT1_X = PX0 + 30; RECT1_Y = PY0 + 30
RECT1_W = 380; RECT1_H = PH - 60
d.rect("r1", RECT1_X, RECT1_Y, RECT1_W, RECT1_H,
       stroke=RED, bg="transparent", sw=2.5, ss="dashed", roundness=3)

# ── Cluster 2: TALL BLOB (hot OLTP keys) ──
# Narrow X (a few hot keys), wide Y (continuous over time).
# Placed in the upper-right of the plot so it doesn't overlap the
# diagonal cluster or its rectangle.
CX2, CY2 = PX0 + 555, PY0 + 195
N2 = 30
for i in range(N2):
    rx = prng(i + 200) * 28
    ry = prng(i + 300) * 110
    dot(f"d2_{i}", CX2 + rx, CY2 + ry, r=4, color=BLUE)

# Tight rectangle hugging the blob
RECT2_X = CX2 - 38; RECT2_Y = CY2 - 130
RECT2_W = 76; RECT2_H = 260
d.rect("r2", RECT2_X, RECT2_Y, RECT2_W, RECT2_H,
       stroke=BLUE, bg="transparent", sw=2.5, ss="dashed", roundness=3)

# Blue OUTLIERS — points that belong to the same hot-key cluster
# semantically (occasional updates to neighboring keys, occasional
# off-window timestamps) but fall outside the axis-aligned rectangle.
# Their presence is the visual argument that the rectangle is only
# an approximation of the cluster's real shape.
OUTLIERS = [
    (RECT2_X + RECT2_W / 2 - 5, RECT2_Y - 14),         # just above
    (RECT2_X + RECT2_W / 2 + 8, RECT2_Y + RECT2_H + 16),  # just below
    (RECT2_X - 16, RECT2_Y + RECT2_H * 0.42),          # just left
    (RECT2_X + RECT2_W + 18, RECT2_Y + RECT2_H * 0.62),  # just right
]
for i, (ox, oy) in enumerate(OUTLIERS):
    dot(f"d2o_{i}", ox, oy, r=4, color=BLUE)

# ── Cluster 3: SCATTERED noise ──
# Grey dots placed in the lower-mid empty zone of the plot —
# outside both R1 (which covers the diagonal in the left half) and
# R2 (which covers the blob in the right half).
for i in range(8):
    rx = prng(i + 500) * 40 + PX0 + 460  # x: 520-600
    ry = (prng(i + 600) + 1) / 2 * 100 + PY0 + 290  # y: 380-480
    dot(f"d3_{i}", rx, ry, r=3, color=GREY)

# ── After-compaction inset, right of the plot ──
# A separate small panel showing the collapsed result: one dot per key.
INS_X = 800; INS_Y = PY0 + 80
INS_W = 460; INS_H = 240
d.rect("inset", INS_X, INS_Y, INS_W, INS_H,
       stroke=GREEN, bg="transparent", sw=1, roundness=3)
d.text("comp_lbl", INS_X + 12, INS_Y + 14, INS_W - 24, 24,
       "после слияния: 1 точка = 1 ключ",
       size=14, color=GREEN, align="left")

# Compacted row of dots near the bottom of the inset
COMP_Y = INS_Y + INS_H - 40
COMP_X0 = INS_X + 30
for i in range(20):
    dot(f"comp_{i}", COMP_X0 + i * 20, COMP_Y, r=4, color=GREEN)

# Arrow from blob → inset entry. Goes outside the plot (around the
# right edge) so it doesn't cross any scatter points.
d.arrow("arr",
        RECT2_X + RECT2_W + 4, CY2,
        [[0, 0], [INS_X - (RECT2_X + RECT2_W) - 8, 0]],
        color=ORANGE, sw=2, roughness=0)
d.text("arr_t",
       RECT2_X + RECT2_W + 6, CY2 - 50, 200, 22,
       "compaction", size=14, color=ORANGE, align="left")

# ── Annotations at the bottom ──
ANN_Y = PY1 + 60
d.text("ann1", 20, ANN_Y, 1240, 26,
       "Файл, SSTable, run — выровненный по осям прямоугольник, ограничивающий кластер обновлений.",
       size=14, color=INK)
d.text("ann2", 20, ANN_Y + 30, 1240, 26,
       "Чем плотнее прямоугольник к форме кластера, тем меньше bloat и read amp.",
       size=14, color=GREY)

d.save("/home/kostja/work/kostja.github.io/assets/img/talks/compaction_continuum.excalidraw")
