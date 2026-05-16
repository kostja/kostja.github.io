#!/usr/bin/env python3
"""When stitching pays despite plan trimming — narrow overlap workload."""

from excalidraw_lib import Doc

d = Doc(seed_base=880000)
RED = "#E23956"; LRED = "#F8CDD6"
BLUE = "#4B7BE5"; LBLUE = "#DBE6FA"
DANGER = "#B91A36"; LDANGER = "#F09CAB"
GREY = "#737A82"; INK = "#2B1321"
ORANGE = "#FF611D"

d.text("title", 20, 8, 760, 22,
       "Two runs in one overlapping cluster — 10% overlap, 90% independent",
       size=14, color=INK)

# Run A: spans a-z, mostly cold
SY = 60; FH = 50; PW = 32
TOTAL = 20
d.text("a_lbl", 20, SY - 20, 800, 16, "run A  (old: a–z)", size=11, color=INK, align="left")
for i in range(TOTAL):
    is_overlap = i in (9, 10)
    fill = LDANGER if is_overlap else LBLUE
    stroke = DANGER if is_overlap else BLUE
    d.rect(f"a_{i}", 20 + i * PW, SY, PW - 2, FH, stroke=stroke, bg=fill, sw=1, roundness=2)

# Run B: spans a-z too (out-of-order backfill), most pages non-overlapping
BY = SY + 90
d.text("b_lbl", 20, BY - 20, 800, 16,
       "run B  (out-of-order backfill: scattered, but overlap on k–l only)",
       size=11, color=INK, align="left")
for i in range(TOTAL):
    is_overlap = i in (9, 10)
    fill = LDANGER if is_overlap else LRED
    stroke = DANGER if is_overlap else RED
    d.rect(f"b_{i}", 20 + i * PW, BY, PW - 2, FH, stroke=stroke, bg=fill, sw=1, roundness=2)

# Bracket marking the narrow overlap region
OVL_X0 = 20 + 9 * PW; OVL_W = 2 * PW - 2
d.rect("ovl", OVL_X0 - 2, SY - 8, OVL_W + 4, FH + BY - SY + 16,
       stroke=DANGER, bg="transparent", sw=2, ss="dashed", roundness=3)
d.text("ovl_t", OVL_X0 - 20, SY - 30, OVL_W + 40, 14,
       "10% overlap → merge", size=10, color=DANGER)

# Destination row: stitched output
DY = BY + 90
d.text("d_lbl", 20, DY - 20, 800, 16,
       "result: reflink the non-overlapping 90%, merge only the overlap",
       size=11, color=INK, align="left")
for i in range(TOTAL):
    if i in (9, 10):
        fill = "#FFE0D0"; stroke = ORANGE
    elif i < 9:
        fill = LBLUE; stroke = BLUE  # from A
    else:
        fill = LRED; stroke = RED  # from B
    d.rect(f"d_{i}", 20 + i * PW, DY, PW - 2, FH, stroke=stroke, bg=fill, sw=1, roundness=2)

# Labels for source
d.text("from_a", 20 + 4 * PW - 30, DY + FH + 4, 80, 14, "from A (reflink)", size=9, color=BLUE)
d.text("from_b", 20 + 15 * PW - 40, DY + FH + 4, 100, 14, "from B (reflink)", size=9, color=RED)
d.text("merged", OVL_X0 - 20, DY + FH + 4, OVL_W + 40, 14, "merged", size=9, color=ORANGE)

# Right side workload examples
PX = 700; PY = SY
d.text("ex_t", PX - 40, PY - 20, 200, 16, "Real workloads", size=12, color=INK, align="left")
for i, line in enumerate([
    "• out-of-order backfill",
    "• schema migration",
    "• batch corrections",
    "• late-arriving CDC events",
]):
    d.text(f"ex_{i}", PX - 40, PY + 8 + i * 20, 200, 16, line, size=11, color=INK, align="left")

# Annotation
d.text("ann", 20, DY + FH + 30, 760, 18,
       "Plan trimming kept these two files together — but only 10% needs new bytes.",
       size=12, color=GREY)

d.save("/home/kostja/work/kostja.github.io/assets/img/talks/stitching_workload.excalidraw")
