#!/usr/bin/env python3
"""File stitching — FICLONERANGE / copy_file_range / reflinks."""

from excalidraw_lib import Doc

d = Doc(seed_base=870000)
RED = "#E23956"; LRED = "#F8CDD6"
BLUE = "#4B7BE5"; LBLUE = "#DBE6FA"
TEAL = "#2D9B8E"; LTEAL = "#CDF0EB"
ORANGE = "#FF611D"; LORANGE = "#FFE0D0"
GREY = "#737A82"; INK = "#2B1321"

d.text("title", 20, 8, 760, 22,
       "File stitching — splice fragments by reference, no byte copy",
       size=14, color=INK)

# Two source run-files (top row)
SY = 60; FW = 280; FH = 60
def page(eid, x, y, w, h, fill, stroke):
    d.rect(eid, x, y, w, h, stroke=stroke, bg=fill, sw=1, roundness=2)

# Source file A
d.text("a_lbl", 20, SY - 20, FW, 16, "run-file A", size=11, color=INK, align="left")
for i in range(8):
    page(f"a_{i}", 20 + i * 35, SY, 32, FH, LBLUE, BLUE)
    d.text(f"a_{i}t", 20 + i * 35, SY, 32, FH, f"p{i}", size=9, color=BLUE)

# Source file B
BX = 480
d.text("b_lbl", BX, SY - 20, FW, 16, "run-file B", size=11, color=INK, align="left")
for i in range(8):
    page(f"b_{i}", BX + i * 35, SY, 32, FH, LRED, RED)
    d.text(f"b_{i}t", BX + i * 35, SY, 32, FH, f"q{i}", size=9, color=RED)

# Arrows down to destination
d.arrow("af", 80, SY + FH + 10, [[0, 0], [60, 80]], color=ORANGE, sw=1.5, roughness=0,
        ss="dashed")
d.text("af_t", 100, SY + FH + 40, 90, 14, "reflink", size=10, color=ORANGE)
d.arrow("bf", 540, SY + FH + 10, [[0, 0], [-60, 80]], color=ORANGE, sw=1.5, roughness=0,
        ss="dashed")
d.text("bf_t", 460, SY + FH + 40, 90, 14, "reflink", size=10, color=ORANGE)

# Destination file: pages from A and B spliced
DY = SY + FH + 90
d.text("d_lbl", 20, DY - 20, 760, 16,
       "merged run-file C  (shares physical extents with A & B)", size=11, color=INK, align="left")
for i in range(4):
    page(f"d_a_{i}", 140 + i * 35, DY, 32, FH, LBLUE, BLUE)
    d.text(f"d_a_t{i}", 140 + i * 35, DY, 32, FH, f"p{i}", size=9, color=BLUE)
for i in range(4):
    page(f"d_b_{i}", 140 + (i + 4) * 35, DY, 32, FH, LRED, RED)
    d.text(f"d_b_t{i}", 140 + (i + 4) * 35, DY, 32, FH, f"q{i}", size=9, color=RED)

# Right-side: syscall list
PX = 540; PY = DY - 10
d.rect("k_box", PX, PY, 240, 100, stroke=GREY, bg="#F4F5F6", sw=1, roundness=3)
d.text("k_t", PX, PY + 4, 240, 16, "Kernel & filesystem", size=12, color=INK)
for i, s in enumerate([
    "• ioctl FICLONERANGE (Linux)",
    "• copy_file_range() (Linux)",
    "• btrfs, XFS reflinks",
    "• ZFS clone, APFS clonefile",
]):
    d.text(f"k_l{i}", PX + 8, PY + 24 + i * 18, 240, 16, s, size=10, color=INK, align="left")

# Annotation
d.text("ann", 20, DY + FH + 30, 760, 18,
       "CoW: shared blocks become independent only when one side is overwritten.",
       size=12, color=GREY)

d.save("/home/kostja/work/kostja.github.io/assets/img/talks/file_stitching.excalidraw")
