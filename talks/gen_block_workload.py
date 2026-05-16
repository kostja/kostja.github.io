#!/usr/bin/env python3
"""What per-block metadata unlocks (Russian)."""

from excalidraw_lib import Doc

d = Doc(seed_base=900000)
RED = "#E23956"
BLUE = "#4B7BE5"; LBLUE = "#DBE6FA"
TEAL = "#2D9B8E"; LTEAL = "#CDF0EB"
ORANGE = "#FF611D"; LORANGE = "#FFE0D0"
GREY = "#737A82"; INK = "#2B1321"
DEAD = "#B91A36"; LDEAD = "#F09CAB"

d.text("title", 20, 10, 1100, 28,
       "Метаданные блока открывают новые операции",
       size=20, color=INK)

BW = 140; BH = 86
N = 7
ROW_W = 1080
ROW_X = (1120 - N * BW - (N - 1) * 8) / 2

# Run A
A_Y = 90
d.text("a_lbl", 30, A_Y - 26, 240, 22, "run-файл A",
       size=16, color=INK, align="left")

A_TAGS = [
    ("TTL ✗",       LDEAD,   DEAD,   "удалить"),
    ("ok",          LBLUE,   BLUE,   ""),
    ("MinHash ≈ 0", LTEAL,   TEAL,   "пропустить"),
    ("ok",          LBLUE,   BLUE,   ""),
    ("TTL ✗",       LDEAD,   DEAD,   "удалить"),
    ("ok",          LBLUE,   BLUE,   ""),
    ("сшить",       LORANGE, ORANGE, "reflink"),
]
for i, (tag, fill, stroke, action) in enumerate(A_TAGS):
    bx = ROW_X + i * (BW + 8)
    d.rect(f"a_b_{i}", bx, A_Y, BW, BH, stroke=stroke, bg=fill, sw=1, roundness=3)
    d.text(f"a_b_t{i}", bx, A_Y + 6, BW, 22, f"блок {i}", size=14, color=stroke)
    d.text(f"a_b_n{i}", bx, A_Y + 32, BW, 22, tag, size=12, color=stroke)
    if action:
        d.text(f"a_b_a{i}", bx, A_Y + 58, BW, 22,
               "→ " + action, size=12, color=stroke)

# Run B
B_Y = A_Y + BH + 60
d.text("b_lbl", 30, B_Y - 26, 240, 22, "run-файл B",
       size=16, color=INK, align="left")

B_TAGS = [
    ("ok",          LBLUE,   BLUE,   ""),
    ("ok",          LBLUE,   BLUE,   ""),
    ("MinHash ≈ 0", LTEAL,   TEAL,   "пропустить"),
    ("слить",       LORANGE, ORANGE, "переписать"),
    ("ok",          LBLUE,   BLUE,   ""),
    ("ok",          LBLUE,   BLUE,   ""),
    ("сшить",       LORANGE, ORANGE, "reflink"),
]
for i, (tag, fill, stroke, action) in enumerate(B_TAGS):
    bx = ROW_X + i * (BW + 8)
    d.rect(f"b_b_{i}", bx, B_Y, BW, BH, stroke=stroke, bg=fill, sw=1, roundness=3)
    d.text(f"b_b_t{i}", bx, B_Y + 6, BW, 22, f"блок {i}", size=14, color=stroke)
    d.text(f"b_b_n{i}", bx, B_Y + 32, BW, 22, tag, size=12, color=stroke)
    if action:
        d.text(f"b_b_a{i}", bx, B_Y + 58, BW, 22,
               "→ " + action, size=12, color=stroke)

# Legend
LEG_Y = B_Y + BH + 40; LEG_X = 30
def chip(eid, x, y, w, h, txt, stroke, fill):
    d.rect(eid, x, y, w, h, stroke=stroke, bg=fill, sw=1, roundness=3)
    d.text(eid + "_t", x, y, w, h, txt, size=14, color=stroke)

chip("lg1", LEG_X,         LEG_Y, 170, 32, "удаление по TTL",  DEAD,   LDEAD)
chip("lg2", LEG_X + 190,   LEG_Y, 170, 32, "MinHash skip",     TEAL,   LTEAL)
chip("lg3", LEG_X + 380,   LEG_Y, 200, 32, "сшить / слить",    ORANGE, LORANGE)
chip("lg4", LEG_X + 600,   LEG_Y, 130, 32, "оставить",         BLUE,   LBLUE)

d.text("ann", 20, LEG_Y + 50, 1100, 22,
       "Multi-tenant SaaS с per-tenant TTL: целые блоки expire без слияния.",
       size=14, color=INK)

d.save("/home/kostja/work/kostja.github.io/assets/img/talks/block_workload.excalidraw")
