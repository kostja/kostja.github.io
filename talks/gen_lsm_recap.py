#!/usr/bin/env python3
"""LSM recap — memtable → flush → merge (Russian)."""

from excalidraw_lib import Doc

d = Doc(seed_base=810000)
RED = "#E23956"; LRED = "#F8CDD6"
NAVY = "#16222E"; GREY = "#737A82"
ORANGE = "#FF611D"
INK = "#2B1321"

d.text("t", 20, 10, 900, 28, "Путь записи: memtable → дамп → слияние", size=20, color=INK)

# Memtable
d.rect("mt", 30, 80, 170, 110, stroke=RED, bg=LRED, sw=1, roundness=3)
d.text("mt_t", 30, 80, 170, 110, "memtable\n(RAM)", size=18, color=RED)

# Arrow: write
d.arrow("a_w", 30, 60, [[0, 0], [80, 0]], color=NAVY, sw=2, roughness=0)
d.text("a_w_t", 30, 36, 80, 18, "запись", size=14, color=NAVY)

# Arrow: flush
d.arrow("a_f", 205, 135, [[0, 0], [70, 0]], color=ORANGE, sw=2, roughness=0)
d.text("a_f_t", 205, 110, 70, 18, "дамп", size=14, color=ORANGE)

# L0 — three flushed files
L0_X = 285; L0_Y = 80
for i in range(3):
    d.rect(f"l0_{i}", L0_X + i * 75, L0_Y, 65, 110, stroke=RED, bg=LRED, sw=1, roundness=3)
    d.text(f"l0_{i}t", L0_X + i * 75, L0_Y, 65, 110, f"run{i}\n8 МБ", size=14, color=RED)
d.text("l0_lbl", L0_X, L0_Y + 120, 215, 20, "L0 (свежие дампы)", size=14, color=GREY)

# Arrow: merge → L1
d.arrow("a_m", 515, 135, [[0, 0], [70, 0]], color=ORANGE, sw=2, roughness=0)
d.text("a_m_t", 515, 110, 70, 18, "слияние", size=14, color=ORANGE)

# L1 — merged
d.rect("l1", 595, 80, 120, 110, stroke=RED, bg="#F09CAB", sw=1, roundness=3)
d.text("l1_t", 595, 80, 120, 110, "merged\n24 МБ", size=16, color=RED)
d.text("l1_lbl", 595, 200, 120, 20, "L1", size=14, color=GREY)

# Arrow merge → L2
d.arrow("a_m2", 720, 135, [[0, 0], [70, 0]], color=ORANGE, sw=2, roughness=0)

# L2
d.rect("l2", 800, 60, 160, 150, stroke=RED, bg="#E96B80", sw=1, roundness=3)
d.text("l2_t", 800, 60, 160, 150, "compacted\n240 МБ", size=16, color="#7C1324")
d.text("l2_lbl", 800, 220, 160, 20, "L2 (старые данные)", size=14, color=GREY)

# Bottom annotation
d.text("ann", 20, 270, 940, 22,
       "Каждый compaction обменивает I/O на короткие пути чтения и удаление tombstone-ов.",
       size=16, color=INK)

d.save("/home/kostja/work/kostja.github.io/assets/img/talks/lsm_recap.excalidraw")
