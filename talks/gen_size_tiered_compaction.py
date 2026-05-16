#!/usr/bin/env python3
"""Size-Tiered Compaction Strategy diagram."""

from excalidraw_lib import Doc

d = Doc(seed_base=820000)
RED = "#E23956"; LRED = "#F8CDD6"; FLRED = "#FDECEF"
ORANGE = "#FF611D"; LORANGE = "#FFE0D0"
GREY = "#737A82"; INK = "#2B1321"; NAVY = "#16222E"

d.text("title", 20, 8, 700, 22, "Size-Tiered: group by size, merge when N accumulate",
       size=14, color=INK)

# Tier 1: 4 small files
TY = 70
def tier_label(eid, x, y, txt):
    d.text(eid, x, y, 140, 16, txt, size=11, color=GREY, align="right")

# Tier 1
for i in range(4):
    d.rect(f"t1_{i}", 180 + i*42, TY, 36, 36, stroke=RED, bg=LRED, sw=1, roundness=3)
    d.text(f"t1_{i}t", 180 + i*42, TY, 36, 36, "8MB", size=9, color=RED)
tier_label("t1lbl", 30, TY + 10, "tier 1 (small):")

# Arrow: merge
d.arrow("am1", 360, TY + 18, [[0, 0], [40, 60]], color=ORANGE, sw=1.5, roughness=0)
d.text("am1t", 405, TY + 30, 60, 14, "merge", size=10, color=ORANGE)

# Tier 2: 4 medium
T2Y = TY + 90
for i in range(4):
    d.rect(f"t2_{i}", 180 + i*62, T2Y, 56, 50, stroke=RED, bg=LRED, sw=1, roundness=3)
    d.text(f"t2_{i}t", 180 + i*62, T2Y, 56, 50, "32MB", size=10, color=RED)
tier_label("t2lbl", 30, T2Y + 18, "tier 2 (medium):")

d.arrow("am2", 430, T2Y + 25, [[0, 0], [60, 70]], color=ORANGE, sw=1.5, roughness=0)
d.text("am2t", 485, T2Y + 50, 60, 14, "merge", size=10, color=ORANGE)

# Tier 3: 1 large
T3Y = T2Y + 110
d.rect("t3", 180, T3Y, 270, 70, stroke=RED, bg="#F09CAB", sw=1, roundness=3)
d.text("t3t", 180, T3Y, 270, 70, "128MB merged", size=12, color=RED)
tier_label("t3lbl", 20, T3Y + 28, "tier 3 (large):")

# Right side: how it works summary
d.text("h0", 520, 70, 240, 18, "Rules", size=13, color=INK, align="left")
for i, line in enumerate([
    "• files grouped by size (×4 buckets)",
    "• when N=4 of same size: merge",
    "• result joins the next-larger tier",
    "• low write amp at steady state",
]):
    d.text(f"h{i+1}", 520, 92 + i*22, 240, 18, line, size=11, color=INK, align="left")

d.save("/home/kostja/work/kostja.github.io/assets/img/talks/size_tiered_compaction.excalidraw")
