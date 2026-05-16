#!/usr/bin/env python3
"""STCS workload pain — Russian."""

from excalidraw_lib import Doc

d = Doc(seed_base=830000)
RED = "#E23956"; LRED = "#F8CDD6"
ORANGE = "#FF611D"
GREY = "#737A82"; INK = "#2B1321"
DANGER = "#B91A36"; LDANGER = "#F09CAB"

d.text("title", 20, 10, 1100, 28,
       "STCS болит: удвоение диска при major compaction и разбросанные версии",
       size=20, color=INK)

# LEFT PANEL: disk usage during major compaction
PX0 = 30; PY0 = 75
d.text("p1t", PX0, PY0, 520, 24,
       "1. Использование диска при major compaction",
       size=16, color=INK, align="left")

# Steady state bar
BAR_Y = PY0 + 50; BAR_H = 40
d.rect("b_steady", PX0, BAR_Y, 280, BAR_H, stroke=GREY, bg="#E8E9EB", sw=1, roundness=3)
d.text("b_steady_t", PX0, BAR_Y, 280, BAR_H, "живые данные  1 ТБ", size=14, color=INK)
d.text("b_lbl1", PX0, BAR_Y - 24, 280, 20, "обычный режим",
       size=12, color=GREY, align="left")

# During major compaction: 2x spike
SPIKE_Y = BAR_Y + 75
d.rect("b_spike", PX0, SPIKE_Y, 280, BAR_H, stroke=DANGER, bg=LDANGER, sw=1, roundness=3)
d.text("b_spike_t1", PX0, SPIKE_Y, 280, BAR_H, "живые данные  1 ТБ", size=14, color=DANGER)
d.rect("b_spike2", PX0 + 280, SPIKE_Y, 280, BAR_H, stroke=DANGER, bg=LDANGER, sw=1,
       fill="cross-hatch", roundness=3)
d.text("b_spike2_t", PX0 + 280, SPIKE_Y, 280, BAR_H, "временный merge  1 ТБ", size=14, color=DANGER)
d.text("b_lbl2", PX0, SPIKE_Y - 24, 560, 20,
       "при major compaction → пик 2×", size=12, color=DANGER, align="left")
d.text("b_oom", PX0, SPIKE_Y + 60, 560, 22,
       "→ переполнение диска: либо запас 2×, либо отказ", size=14, color=DANGER, align="left")

# RIGHT PANEL: scattered key versions
PX1 = 660; PY1 = 75
d.text("p2t", PX1, PY1, 440, 24, "2. Один ключ, N уровней, N чтений",
       size=16, color=INK, align="left")

for i in range(5):
    ty = PY1 + 50 + i * 40
    d.rect(f"tier{i}", PX1, ty, 280, 32, stroke=GREY, bg="#F4F5F6", sw=1, roundness=3)
    d.text(f"tier_lbl{i}", PX1 + 6, ty, 110, 32,
           f"уровень {i+1}", size=12, color=GREY, align="left")
    d.rect(f"k_{i}", PX1 + 130, ty + 4, 140, 24, stroke=DANGER, bg=LDANGER, sw=1, roundness=3)
    d.text(f"k_t{i}", PX1 + 130, ty + 4, 140, 24,
           f"k42 v{5-i}", size=12, color=DANGER)

d.text("read_lbl", PX1, PY1 + 50 + 5 * 40 + 12, 280, 22,
       "read(k42) → слить 5 версий", size=14, color=DANGER, align="left")

# Bottom annotation
d.text("ann", 20, 380, 1100, 22,
       "Time-series: каждый update — в новый уровень; read amp растёт с числом уровней.",
       size=14, color=INK)

d.save("/home/kostja/work/kostja.github.io/assets/img/talks/stcs_workload_pain.excalidraw")
