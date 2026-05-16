#!/usr/bin/env python3
"""Three-level layout — run › block › page."""

from excalidraw_lib import Doc

d = Doc(seed_base=890000)
RED = "#E23956"; LRED = "#F8CDD6"
BLUE = "#4B7BE5"; LBLUE = "#DBE6FA"
TEAL = "#2D9B8E"; LTEAL = "#CDF0EB"
ORANGE = "#FF611D"; LORANGE = "#FFE0D0"
GREY = "#737A82"; INK = "#2B1321"

d.text("title", 20, 8, 760, 22,
       "Three-level layout: run › block › page",
       size=15, color=INK)

# Top: the run-file
RX = 30; RY = 60; RW = 740; RH = 30
d.rect("run", RX, RY, RW, RH, stroke=RED, bg=LRED, sw=2, roundness=3)
d.text("run_t", RX + 8, RY, RW, RH, "run-file  (≈ SSTable)", size=12, color=RED, align="left")
d.text("run_n", RX + RW - 200, RY, 200, RH,
       "logically owned by an LSM level", size=10, color=GREY, align="right")

# Middle: blocks
BY = RY + RH + 14
BW = 100; BH = 50; NB = 7
BX0 = RX + (RW - NB * BW - (NB - 1) * 6) / 2
for i in range(NB):
    bx = BX0 + i * (BW + 6)
    d.rect(f"blk_{i}", bx, BY, BW, BH, stroke=BLUE, bg=LBLUE, sw=1.5, roundness=3)
    d.text(f"blk_{i}t", bx, BY + 4, BW, 18, f"block {i}", size=10, color=BLUE)
    d.text(f"blk_{i}m", bx, BY + 22, BW, 28,
           "50–100 pages\nfilter • min/max • TTL", size=8, color=GREY)

# Bottom: pages within one block (expanded view)
PY_LBL = BY + BH + 18
d.text("p_lbl", 30, PY_LBL, 740, 14, "(zoom: pages within one block)",
       size=11, color=GREY, align="center")

PY = PY_LBL + 18
PW = 28; PH = 36; NP = 16
PX0 = (800 - NP * PW - (NP - 1) * 2) / 2
for i in range(NP):
    px = PX0 + i * (PW + 2)
    d.rect(f"p_{i}", px, PY, PW, PH, stroke=GREY, bg="#F4F5F6", sw=1, roundness=2)
    d.text(f"p_{i}t", px, PY, PW, PH, str(i), size=9, color=GREY)
d.text("p_n", 30, PY + PH + 6, 740, 14,
       "page = physical I/O unit (4–8 KB)", size=11, color=GREY)

# Right margin: per-block metadata box
MX = 600; MY = BY + BH + 12
# (handled inline via block sub-labels above)

# Bottom annotation
d.text("ann1", 20, PY + PH + 30, 760, 18,
       "Block-level metadata = the smallest unit the scheduler reasons about.",
       size=12, color=INK)
d.text("ann2", 20, PY + PH + 52, 760, 18,
       "Block directory stays in RAM; block bodies paged in on demand.",
       size=12, color=GREY)

d.save("/home/kostja/work/kostja.github.io/assets/img/talks/three_level_format.excalidraw")
