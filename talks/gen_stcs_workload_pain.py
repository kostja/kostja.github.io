#!/usr/bin/env python3
"""STCS workload pain — major compaction doubles disk, scattered key versions."""

from excalidraw_lib import Doc

d = Doc(seed_base=830000)
RED = "#E23956"; LRED = "#F8CDD6"
ORANGE = "#FF611D"; LORANGE = "#FFE0D0"
GREY = "#737A82"; INK = "#2B1321"; NAVY = "#16222E"
GREEN = "#2E7D32"; LGREEN = "#C8E6C9"
DANGER = "#B91A36"; LDANGER = "#F09CAB"

d.text("title", 20, 8, 720, 22,
       "STCS pain: disk-doubling during major compaction + scattered versions",
       size=14, color=INK)

# LEFT PANEL: disk usage timeline
PX0 = 30; PY0 = 70
d.text("p1t", PX0, PY0, 360, 18, "1. Disk usage during major compaction", size=13, color=INK, align="left")

# baseline disk usage bar (dataset = 1 TB)
BAR_Y = PY0 + 40; BAR_H = 30
d.rect("b_steady", PX0, BAR_Y, 200, BAR_H, stroke=GREY, bg="#E8E9EB", sw=1, roundness=3)
d.text("b_steady_t", PX0, BAR_Y, 200, BAR_H, "live data  1 TB", size=11, color=INK)

# during major compaction: 2× spike
d.rect("b_spike", PX0, BAR_Y + 50, 200, BAR_H, stroke=DANGER, bg=LDANGER, sw=1, roundness=3)
d.text("b_spike_t1", PX0, BAR_Y + 50, 200, BAR_H, "live data  1 TB", size=11, color=DANGER)
d.rect("b_spike2", PX0 + 200, BAR_Y + 50, 200, BAR_H, stroke=DANGER, bg=LDANGER, sw=1,
       fill="cross-hatch", roundness=3)
d.text("b_spike2_t", PX0 + 200, BAR_Y + 50, 200, BAR_H, "merge output  1 TB", size=11, color=DANGER)

d.text("b_lbl1", PX0, BAR_Y - 20, 200, 14, "steady state", size=10, color=GREY, align="left")
d.text("b_lbl2", PX0, BAR_Y + 30, 200, 14, "during major compaction → 2× peak", size=10, color=DANGER, align="left")
d.text("b_oom", PX0, BAR_Y + 90, 400, 16, "→ OOM disk: provision 2× or it fails", size=11, color=DANGER, align="left")

# RIGHT PANEL: scattered key versions
PX1 = 460; PY1 = 70
d.text("p2t", PX1, PY1, 320, 18, "2. One key, N tiers, N reads", size=13, color=INK, align="left")

# 5 tiers stacked vertically, key 'k42' appearing in each
for i in range(5):
    ty = PY1 + 36 + i * 32
    d.rect(f"tier{i}", PX1, ty, 200, 26, stroke=GREY, bg="#F4F5F6", sw=1, roundness=3)
    d.text(f"tier_lbl{i}", PX1 + 4, ty, 80, 26,
           f"tier {i+1}", size=10, color=GREY, align="left")
    # mark with key version
    d.rect(f"k_{i}", PX1 + 90, ty + 3, 100, 20, stroke=DANGER, bg=LDANGER, sw=1, roundness=3)
    d.text(f"k_t{i}", PX1 + 90, ty + 3, 100, 20,
           f"k42 v{5-i}", size=10, color=DANGER)

d.text("read_lbl", PX1, PY1 + 36 + 5*32 + 8, 200, 16,
       "read(k42) → merge 5 versions", size=11, color=DANGER, align="left")

# Bottom annotation
d.text("ann", 20, 280, 760, 18,
       "Time-series ingest: each update lands in a new tier; read amp grows with tier count.",
       size=12, color=INK)

d.save("/home/kostja/work/kostja.github.io/assets/img/talks/stcs_workload_pain.excalidraw")
