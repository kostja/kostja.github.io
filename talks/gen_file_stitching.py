#!/usr/bin/env python3
"""File stitching (Russian)."""

from excalidraw_lib import Doc

d = Doc(seed_base=870000)
RED = "#E23956"; LRED = "#F8CDD6"
BLUE = "#4B7BE5"; LBLUE = "#DBE6FA"
ORANGE = "#FF611D"
GREY = "#737A82"; INK = "#2B1321"

d.text("title", 20, 10, 1100, 28,
       "File stitching: сращивание фрагментов по ссылке, без копирования байт",
       size=20, color=INK)

# Sources
SY = 80; FH = 80; PW = 42

d.text("a_lbl", 30, SY - 24, 360, 22, "run-файл A", size=16, color=INK, align="left")
for i in range(8):
    d.rect(f"a_{i}", 30 + i * 45, SY, PW, FH, stroke=BLUE, bg=LBLUE, sw=1, roundness=2)
    d.text(f"a_{i}t", 30 + i * 45, SY, PW, FH, f"p{i}", size=12, color=BLUE)

BX = 620
d.text("b_lbl", BX, SY - 24, 360, 22, "run-файл B", size=16, color=INK, align="left")
for i in range(8):
    d.rect(f"b_{i}", BX + i * 45, SY, PW, FH, stroke=RED, bg=LRED, sw=1, roundness=2)
    d.text(f"b_{i}t", BX + i * 45, SY, PW, FH, f"q{i}", size=12, color=RED)

# Reflink arrows
d.arrow("af", 100, SY + FH + 10, [[0, 0], [80, 90]], color=ORANGE, sw=1.5, roughness=0,
        ss="dashed")
d.text("af_t", 120, SY + FH + 45, 100, 22, "reflink", size=14, color=ORANGE)

d.arrow("bf", 700, SY + FH + 10, [[0, 0], [-80, 90]], color=ORANGE, sw=1.5, roughness=0,
        ss="dashed")
d.text("bf_t", 580, SY + FH + 45, 100, 22, "reflink", size=14, color=ORANGE)

# Destination file
DY = SY + FH + 115
d.text("d_lbl", 30, DY - 26, 1100, 22,
       "результат C  (разделяет физические экстенты с A и B)",
       size=16, color=INK, align="left")
DX0 = 280
for i in range(4):
    d.rect(f"d_a_{i}", DX0 + i * 45, DY, PW, FH, stroke=BLUE, bg=LBLUE, sw=1, roundness=2)
    d.text(f"d_a_t{i}", DX0 + i * 45, DY, PW, FH, f"p{i}", size=12, color=BLUE)
for i in range(4):
    d.rect(f"d_b_{i}", DX0 + (i + 4) * 45, DY, PW, FH, stroke=RED, bg=LRED, sw=1, roundness=2)
    d.text(f"d_b_t{i}", DX0 + (i + 4) * 45, DY, PW, FH, f"q{i}", size=12, color=RED)

# Kernel & FS box
KX = 700; KY = DY - 20
d.rect("k_box", KX, KY, 380, 150, stroke=GREY, bg="#F4F5F6", sw=1, roundness=3)
d.text("k_t", KX, KY + 8, 380, 24, "Ядро и ФС", size=16, color=INK)
for i, s in enumerate([
    "• ioctl FICLONERANGE (Linux)",
    "• copy_file_range() (Linux)",
    "• btrfs, XFS reflinks",
    "• ZFS clone, APFS clonefile",
]):
    d.text(f"k_l{i}", KX + 14, KY + 36 + i * 24, 360, 22, s, size=14, color=INK, align="left")

# Annotation — placed below both the destination row of pages AND
# the Kernel & FS box, whichever is lower.
ANN_Y = max(DY + FH, KY + 150) + 20
d.text("ann", 20, ANN_Y, 1100, 22,
       "CoW: общие блоки становятся независимыми только при перезаписи одной из сторон.",
       size=14, color=GREY)

d.save("/home/kostja/work/kostja.github.io/assets/img/talks/file_stitching.excalidraw")
