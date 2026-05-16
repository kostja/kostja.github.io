#!/usr/bin/env python3
"""When stitching helps despite plan trimming (Russian)."""

from excalidraw_lib import Doc

d = Doc(seed_base=880000)
RED = "#E23956"; LRED = "#F8CDD6"
BLUE = "#4B7BE5"; LBLUE = "#DBE6FA"
DANGER = "#B91A36"; LDANGER = "#F09CAB"
GREY = "#737A82"; INK = "#2B1321"
ORANGE = "#FF611D"; LORANGE = "#FFE0D0"

d.text("title", 20, 10, 1200, 28,
       "Два файла одного кластера: пересечение 10%, остальное независимо",
       size=20, color=INK)

PW = 42; FH = 64
TOTAL = 20
ROW_X = 30

# Run A
SY = 80
d.text("a_lbl", ROW_X, SY - 26, 600, 22, "run A  (старые: a–z)",
       size=16, color=INK, align="left")
for i in range(TOTAL):
    is_overlap = i in (9, 10)
    fill = LDANGER if is_overlap else LBLUE
    stroke = DANGER if is_overlap else BLUE
    d.rect(f"a_{i}", ROW_X + i * PW, SY, PW - 2, FH, stroke=stroke, bg=fill, sw=1, roundness=2)

# Run B
BY = SY + 120
d.text("b_lbl", ROW_X, BY - 26, 800, 22,
       "run B  (out-of-order backfill: разбросан, пересечение только на k–l)",
       size=16, color=INK, align="left")
for i in range(TOTAL):
    is_overlap = i in (9, 10)
    fill = LDANGER if is_overlap else LRED
    stroke = DANGER if is_overlap else RED
    d.rect(f"b_{i}", ROW_X + i * PW, BY, PW - 2, FH, stroke=stroke, bg=fill, sw=1, roundness=2)

# Bracket marking overlap
OVL_X0 = ROW_X + 9 * PW; OVL_W = 2 * PW - 2
d.rect("ovl", OVL_X0 - 4, SY - 10, OVL_W + 8, FH + (BY - SY) + 18,
       stroke=DANGER, bg="transparent", sw=2, ss="dashed", roundness=3)
d.text("ovl_t", OVL_X0 - 60, SY - 50, OVL_W + 120, 22,
       "10% пересечения → слить", size=14, color=DANGER)

# Destination
DY = BY + 120
d.text("d_lbl", ROW_X, DY - 26, 1100, 22,
       "результат: reflink 90%, слить только пересечение",
       size=16, color=INK, align="left")
for i in range(TOTAL):
    if i in (9, 10):
        fill = LORANGE; stroke = ORANGE
    elif i < 9:
        fill = LBLUE; stroke = BLUE
    else:
        fill = LRED; stroke = RED
    d.rect(f"d_{i}", ROW_X + i * PW, DY, PW - 2, FH, stroke=stroke, bg=fill, sw=1, roundness=2)

# Bottom labels
d.text("from_a", ROW_X + 4 * PW - 60, DY + FH + 8, 200, 18,
       "из A (reflink)", size=12, color=BLUE)
d.text("from_b", ROW_X + 15 * PW - 60, DY + FH + 8, 200, 18,
       "из B (reflink)", size=12, color=RED)
d.text("merged", OVL_X0 - 30, DY + FH + 8, OVL_W + 60, 18,
       "слито", size=12, color=ORANGE)

# Right side: real workloads
PX = 920; PY = SY
d.text("ex_t", PX, PY - 26, 260, 22, "Реальные нагрузки",
       size=16, color=INK, align="left")
for i, line in enumerate([
    "• out-of-order backfill",
    "• миграция схемы",
    "• пакетные корректировки",
    "• запоздавшие CDC-события",
]):
    d.text(f"ex_{i}", PX, PY + i * 28, 280, 22, line, size=14, color=INK, align="left")

# Annotation
d.text("ann", 20, DY + FH + 38, 1200, 22,
       "Усечение плана оставило эти файлы вместе — но новых байт нужно только 10%.",
       size=14, color=GREY)

d.save("/home/kostja/work/kostja.github.io/assets/img/talks/stitching_workload.excalidraw")
