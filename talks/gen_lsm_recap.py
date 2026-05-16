#!/usr/bin/env python3
"""LSM recap — memtable → flush → merge cascade."""

from excalidraw_lib import Doc

d = Doc(seed_base=810000)

RED = "#E23956"; LRED = "#F8CDD6"; FLRED = "#FDECEF"
NAVY = "#16222E"; GREY = "#737A82"; LGREY = "#E8E9EB"
ORANGE = "#FF611D"; LORANGE = "#FFE0D0"
INK = "#2B1321"

# Title
d.text("t", 20, 10, 700, 22, "Write path: memtable → flush → merge", size=15, color=INK)

# Memtable (left)
d.labeled_rect("mt", 30, 70, 130, 90, "memtable\n(RAM)",
               stroke=RED, fill=LRED)

# Arrow: write
d.arrow("a_w", 30, 50, [[0, 0], [60, 0]], color=NAVY, sw=2)
d.text("a_w_t", 30, 30, 60, 16, "write", size=11, color=NAVY)

# Arrow: flush
d.arrow("a_f", 165, 115, [[0, 0], [60, 0]], color=ORANGE, sw=2)
d.text("a_f_t", 165, 95, 60, 16, "flush", size=11, color=ORANGE)

# L0 — three flushed files
def run(eid, x, y, w, h, label, stroke, fill, fill_style="solid"):
    d.rect(eid, x, y, w, h, stroke=stroke, bg=fill, sw=1, fill=fill_style, roundness=3)
    d.text(eid + "_t", x, y, w, h, label, size=10, color=stroke)

L0_X = 230; L0_Y = 70
for i in range(3):
    run(f"l0_{i}", L0_X + i * 60, L0_Y, 50, 90, f"run{i}\n8MB", RED, LRED)
d.text("l0_lbl", L0_X, L0_Y + 100, 170, 16, "L0 (recent flushes)", size=11, color=GREY)

# Arrow: merge
d.arrow("a_m", 415, 115, [[0, 0], [60, 0]], color=ORANGE, sw=2)
d.text("a_m_t", 415, 95, 60, 16, "merge", size=11, color=ORANGE)

# L1 — one merged file
run("l1", 480, 70, 90, 90, "merged\n24MB", RED, "#F09CAB")
d.text("l1_lbl", 480, 170, 90, 16, "L1", size=11, color=GREY)

# Arrow: merge
d.arrow("a_m2", 575, 115, [[0, 0], [60, 0]], color=ORANGE, sw=2)

# L2 — one large file
run("l2", 640, 50, 120, 130, "compacted\n240MB", RED, "#E96B80")
d.text("l2_lbl", 640, 190, 120, 16, "L2 (older data)", size=11, color=GREY)

# Bottom annotation
d.text("ann", 20, 230, 740, 18,
       "Each compaction trades I/O cost for shorter read paths and dropped tombstones.",
       size=12, color=INK)

d.save("/home/kostja/work/kostja.github.io/assets/img/talks/lsm_recap.excalidraw")
