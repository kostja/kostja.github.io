#!/usr/bin/env python3
"""What per-block metadata unlocks — TTL drop, MinHash skip, stitching."""

from excalidraw_lib import Doc

d = Doc(seed_base=900000)
RED = "#E23956"; LRED = "#F8CDD6"
BLUE = "#4B7BE5"; LBLUE = "#DBE6FA"
TEAL = "#2D9B8E"; LTEAL = "#CDF0EB"
ORANGE = "#FF611D"; LORANGE = "#FFE0D0"
GREY = "#737A82"; INK = "#2B1321"
DEAD = "#B91A36"; LDEAD = "#F09CAB"

d.text("title", 20, 8, 760, 22,
       "Per-block metadata unlocks new operations",
       size=14, color=INK)

# Two run files of blocks
ROW_W = 760; BLOCK_W = 90; BLOCK_H = 60
BLOCKS_PER_ROW = 7
ROW_X0 = (800 - BLOCKS_PER_ROW * BLOCK_W - (BLOCKS_PER_ROW - 1) * 6) / 2

ROW_A_Y = 60
d.text("a_lbl", 20, ROW_A_Y - 18, 200, 14, "run-file A", size=11, color=INK, align="left")

# A's blocks: with various tags
A_TAGS = [
    ("TTL ✗", LDEAD, DEAD, "drop"),    # expired
    ("ok", LBLUE, BLUE, ""),
    ("MinHash ≈ 0", LTEAL, TEAL, "skip"),
    ("ok", LBLUE, BLUE, ""),
    ("TTL ✗", LDEAD, DEAD, "drop"),
    ("ok", LBLUE, BLUE, ""),
    ("stitch", LORANGE, ORANGE, "reflink"),
]
for i, (tag, fill, stroke, action) in enumerate(A_TAGS):
    bx = ROW_X0 + i * (BLOCK_W + 6)
    d.rect(f"a_b_{i}", bx, ROW_A_Y, BLOCK_W, BLOCK_H, stroke=stroke, bg=fill, sw=1, roundness=3)
    d.text(f"a_b_t{i}", bx, ROW_A_Y + 4, BLOCK_W, 18, f"blk{i}", size=10, color=stroke)
    d.text(f"a_b_n{i}", bx, ROW_A_Y + 22, BLOCK_W, 16, tag, size=9, color=stroke)
    if action:
        d.text(f"a_b_a{i}", bx, ROW_A_Y + 40, BLOCK_W, 16,
               "→ " + action, size=9, color=stroke)

ROW_B_Y = ROW_A_Y + BLOCK_H + 70
d.text("b_lbl", 20, ROW_B_Y - 18, 200, 14, "run-file B", size=11, color=INK, align="left")
B_TAGS = [
    ("ok", LBLUE, BLUE, ""),
    ("ok", LBLUE, BLUE, ""),
    ("MinHash ≈ 0", LTEAL, TEAL, "skip"),
    ("merge", LORANGE, ORANGE, "rewrite"),
    ("ok", LBLUE, BLUE, ""),
    ("ok", LBLUE, BLUE, ""),
    ("stitch", LORANGE, ORANGE, "reflink"),
]
for i, (tag, fill, stroke, action) in enumerate(B_TAGS):
    bx = ROW_X0 + i * (BLOCK_W + 6)
    d.rect(f"b_b_{i}", bx, ROW_B_Y, BLOCK_W, BLOCK_H, stroke=stroke, bg=fill, sw=1, roundness=3)
    d.text(f"b_b_t{i}", bx, ROW_B_Y + 4, BLOCK_W, 18, f"blk{i}", size=10, color=stroke)
    d.text(f"b_b_n{i}", bx, ROW_B_Y + 22, BLOCK_W, 16, tag, size=9, color=stroke)
    if action:
        d.text(f"b_b_a{i}", bx, ROW_B_Y + 40, BLOCK_W, 16,
               "→ " + action, size=9, color=stroke)

# Legend
LEG_Y = ROW_B_Y + BLOCK_H + 30
LEG_X = 30
def chip(eid, x, y, w, h, txt, stroke, fill):
    d.rect(eid, x, y, w, h, stroke=stroke, bg=fill, sw=1, roundness=3)
    d.text(eid + "_t", x, y, w, h, txt, size=10, color=stroke)

chip("lg1", LEG_X, LEG_Y, 90, 24, "TTL drop", DEAD, LDEAD)
chip("lg2", LEG_X + 110, LEG_Y, 110, 24, "MinHash skip", TEAL, LTEAL)
chip("lg3", LEG_X + 240, LEG_Y, 110, 24, "stitch / merge", ORANGE, LORANGE)
chip("lg4", LEG_X + 370, LEG_Y, 70, 24, "keep", BLUE, LBLUE)

d.text("ann", 20, LEG_Y + 38, 760, 18,
       "Multi-tenant SaaS with per-tenant TTL — whole blocks expire without merging.",
       size=12, color=INK)

d.save("/home/kostja/work/kostja.github.io/assets/img/talks/block_workload.excalidraw")
