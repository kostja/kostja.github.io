#!/usr/bin/env python3
"""Three-level layout — run › block › page (Russian)."""

from excalidraw_lib import Doc

d = Doc(seed_base=890000)
RED = "#E23956"; LRED = "#F8CDD6"
BLUE = "#4B7BE5"; LBLUE = "#DBE6FA"
GREY = "#737A82"; INK = "#2B1321"

d.text("title", 20, 10, 1100, 28,
       "Трёхуровневая структура: run › block › page",
       size=20, color=INK)

# Top: the run-file
RX = 40; RY = 80; RW = 1020; RH = 44
d.rect("run", RX, RY, RW, RH, stroke=RED, bg=LRED, sw=2, roundness=3)
d.text("run_t", RX + 14, RY, 360, RH, "run-файл  (≈ SSTable)",
       size=16, color=RED, align="left")
d.text("run_n", RX + RW - 360, RY, 350, RH,
       "принадлежит уровню LSM", size=14, color=GREY, align="right")

# Middle: blocks
BY = RY + RH + 22; BW = 168; BH = 76; NB = 6
BX0 = RX + (RW - NB * BW - (NB - 1) * 8) / 2
for i in range(NB):
    bx = BX0 + i * (BW + 8)
    d.rect(f"blk_{i}", bx, BY, BW, BH, stroke=BLUE, bg=LBLUE, sw=1.5, roundness=3)
    d.text(f"blk_{i}t", bx, BY + 6, BW, 22, f"блок {i}", size=14, color=BLUE)
    d.text(f"blk_{i}m", bx, BY + 32, BW, 40,
           "50–100 страниц\nфильтр • min/max • TTL", size=12, color=GREY)

# Pages — zoom
PY_LBL = BY + BH + 28
d.text("p_lbl", 30, PY_LBL, 1080, 22,
       "(увеличение: страницы внутри одного блока)",
       size=14, color=GREY, align="center")

PY = PY_LBL + 26; PW = 42; PH = 44; NP = 16
PX0 = (1100 - NP * PW - (NP - 1) * 4) / 2
for i in range(NP):
    px = PX0 + i * (PW + 4)
    d.rect(f"p_{i}", px, PY, PW, PH, stroke=GREY, bg="#F4F5F6", sw=1, roundness=2)
    d.text(f"p_{i}t", px, PY, PW, PH, str(i), size=12, color=GREY)
d.text("p_n", 30, PY + PH + 10, 1080, 22,
       "page = единица I/O (4–8 КБ)", size=14, color=GREY)

# Annotations
ay = PY + PH + 50
d.text("ann1", 20, ay, 1100, 22,
       "Метаданные блока = минимальная единица для планировщика.",
       size=14, color=INK)
d.text("ann2", 20, ay + 26, 1100, 22,
       "Каталог блоков в RAM; тела блоков подгружаются по требованию.",
       size=14, color=GREY)

d.save("/home/kostja/work/kostja.github.io/assets/img/talks/three_level_format.excalidraw")
