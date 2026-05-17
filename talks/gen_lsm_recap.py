#!/usr/bin/env python3
"""LSM recap — memtable → flush → merge (Russian).

Box sizes are proportional to data volume:
- memtable ≈ each L0 run (each is a single flush worth of data)
- L1 ≈ 2× one L0 run (it absorbs flushes as they accumulate)
- L2 ≈ slightly larger than 2× L1
"""

from excalidraw_lib import Doc

d = Doc(seed_base=810000)
RED = "#E23956"; LRED = "#F8CDD6"
NAVY = "#16222E"; GREY = "#737A82"
ORANGE = "#FF611D"
INK = "#2B1321"

d.text("t", 20, 10, 940, 28,
       "Путь записи: memtable → дамп → слияние", size=20, color=INK)

# Main horizontal arrows centered on AXIS_Y. Arrow labels sit a generous
# 38 px above each arrow so the arrowhead doesn't crowd the text.
AXIS_Y = 140

# Memtable (1 unit), centered on AXIS_Y
MT_X, MT_W, MT_H = 30, 80, 80
MT_Y = AXIS_Y - MT_H // 2
d.rect("mt", MT_X, MT_Y, MT_W, MT_H, stroke=RED, bg=LRED, sw=1, roundness=3)
d.text("mt_t", MT_X, MT_Y, MT_W, MT_H, "memtable\n(RAM)", size=13, color=RED)

# Arrow: write (above the memtable, pointing in)
WRITE_Y = 80
d.arrow("a_w", MT_X, WRITE_Y, [[0, 0], [70, 0]],
        color=NAVY, sw=2, roughness=0)
d.text("a_w_t", MT_X, WRITE_Y - 38, 70, 18,
       "запись", size=13, color=NAVY)

# Arrow: flush
A1_X = MT_X + MT_W + 10
d.arrow("a_f", A1_X, AXIS_Y, [[0, 0], [50, 0]],
        color=ORANGE, sw=2, roughness=0)
d.text("a_f_t", A1_X, AXIS_Y - 38, 50, 18,
       "дамп", size=13, color=ORANGE)

# L0 — three flushed files, each 1 unit
L0_X = A1_X + 60; L0_W = 80; L0_H = 80; L0_GAP = 8
L0_Y = AXIS_Y - L0_H // 2
for i in range(3):
    d.rect(f"l0_{i}", L0_X + i * (L0_W + L0_GAP), L0_Y, L0_W, L0_H,
           stroke=RED, bg=LRED, sw=1, roundness=3)
    d.text(f"l0_{i}t", L0_X + i * (L0_W + L0_GAP), L0_Y, L0_W, L0_H,
           f"run{i}\n8 МБ", size=12, color=RED)
L0_END = L0_X + 3 * L0_W + 2 * L0_GAP
d.text("l0_lbl", L0_X, L0_Y + L0_H + 10, L0_END - L0_X, 20,
       "L0 (свежие дампы)", size=13, color=GREY)

# Arrow: L0 → L1
A2_X = L0_END + 10
d.arrow("a_m", A2_X, AXIS_Y, [[0, 0], [50, 0]],
        color=ORANGE, sw=2, roughness=0)
d.text("a_m_t", A2_X - 15, AXIS_Y - 38, 80, 18,
       "слияние", size=13, color=ORANGE)

# L1 ≈ 2 units
L1_W, L1_H = 160, 100
L1_X = A2_X + 60; L1_Y = AXIS_Y - L1_H // 2
d.rect("l1", L1_X, L1_Y, L1_W, L1_H, stroke=RED, bg="#F09CAB", sw=1, roundness=3)
d.text("l1_t", L1_X, L1_Y, L1_W, L1_H, "merged\n24 МБ", size=14, color=RED)
d.text("l1_lbl", L1_X, L1_Y + L1_H + 10, L1_W, 20, "L1", size=13, color=GREY)

# Arrow: L1 → L2
A3_X = L1_X + L1_W + 10
d.arrow("a_m2", A3_X, AXIS_Y, [[0, 0], [50, 0]],
        color=ORANGE, sw=2, roughness=0)

# L2 ≈ 2.2× L1
L2_W, L2_H = 280, 130
L2_X = A3_X + 60; L2_Y = AXIS_Y - L2_H // 2
d.rect("l2", L2_X, L2_Y, L2_W, L2_H, stroke=RED, bg="#E96B80", sw=1, roundness=3)
d.text("l2_t", L2_X, L2_Y, L2_W, L2_H, "compacted\n240 МБ", size=14, color="#7C1324")
d.text("l2_lbl", L2_X, L2_Y + L2_H + 10, L2_W, 20, "L2 (старое)", size=13, color=GREY)

# Bottom annotation
ANN_Y = L2_Y + L2_H + 50
d.text("ann", 20, ANN_Y, L2_X + L2_W, 22,
       "Каждый compaction обменивает I/O на короткие пути чтения и удаление tombstone-ов.",
       size=14, color=INK)

d.save("/home/kostja/work/kostja.github.io/assets/img/talks/lsm_recap.excalidraw")
