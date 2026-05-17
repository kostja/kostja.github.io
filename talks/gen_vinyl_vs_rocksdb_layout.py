#!/usr/bin/env python3
"""Side-by-side: same dataset in Vinyl ranges×levels vs RocksDB SSTables.

Goal: terminology bridge — show how identical data maps to two different
file layouts. Areas are proportionate, so the audience sees that both
engines manage similar volumes despite different file structures.
"""

from excalidraw_lib import Doc

d = Doc(seed_base=930000)
RED = "#E23956"; LRED = "#F8CDD6"
BLUE = "#4B7BE5"; LBLUE = "#DBE6FA"
TEAL = "#2D9B8E"; LTEAL = "#CDF0EB"
ORANGE = "#FF611D"; LORANGE = "#FFE0D0"
GREY = "#737A82"; INK = "#2B1321"

d.text("title", 20, 10, 1200, 28,
       "Один и тот же датасет: Vinyl vs RocksDB",
       size=20, color=INK)

# ── LEFT PANEL: Vinyl ─────────────────────────────────────
LX = 30; LW = 580
d.text("l_t", LX, 60, LW, 22, "Vinyl: ranges × levels",
       size=16, color=RED, align="left")

# 3 range columns: a-h, i-p, q-z
COL_W = 150; COL_GAP = 20
COLS_X0 = LX + 30
COL_HDR_Y = 100

for i, name in enumerate(["a–h", "i–p", "q–z"]):
    x = COLS_X0 + i * (COL_W + COL_GAP)
    d.text(f"col_{i}", x, COL_HDR_Y, COL_W, 22, name,
           size=14, color=GREY)

# L0: ONE run spanning all 3 ranges
L0_Y = 130; L0_H = 32
L0_W = 3 * COL_W + 2 * COL_GAP
d.rect("l0", COLS_X0, L0_Y, L0_W, L0_H,
       stroke=RED, bg="#FAEAED", sw=1.5, roundness=3)
d.text("l0_t", COLS_X0, L0_Y, L0_W, L0_H,
       "L0 run-file  (один файл, 3 slice-а)",
       size=12, color=RED)

# Slice boundary marks (dashed verticals across L0)
for i in range(1, 3):
    sx = COLS_X0 + i * COL_W + (i - 1) * COL_GAP + COL_GAP / 2
    d.line(f"slc_{i}", sx, L0_Y, [[0, 0], [0, L0_H]],
           color=ORANGE, sw=1, ss="dashed", roughness=0)

# L1: per-range, medium
L1_Y = L0_Y + L0_H + 14; L1_H = 70
for i in range(3):
    x = COLS_X0 + i * (COL_W + COL_GAP)
    d.rect(f"l1_{i}", x, L1_Y, COL_W, L1_H,
           stroke=RED, bg=LRED, sw=1, roundness=3)
    d.text(f"l1_t{i}", x, L1_Y, COL_W, L1_H, "L1 run",
           size=14, color=RED)

# L2: per-range, large
L2_Y = L1_Y + L1_H + 14; L2_H = 140
for i in range(3):
    x = COLS_X0 + i * (COL_W + COL_GAP)
    d.rect(f"l2_{i}", x, L2_Y, COL_W, L2_H,
           stroke=RED, bg="#F09CAB", sw=1, roundness=3)
    d.text(f"l2_t{i}", x, L2_Y, COL_W, L2_H, "L2 run",
           size=14, color="#7C1324")

# Bottom label position is computed after both panels are laid out
# (see end of file). The left-panel bottom annotation is rendered there.

# ── RIGHT PANEL: RocksDB ──────────────────────────────────
RX = LX + LW + 40; RW = 540
d.text("r_t", RX, 60, RW, 22, "RocksDB: levels × SSTables",
       size=16, color=BLUE, align="left")

# Keyspace label on top
KSP_Y = 100
d.text("k_t", RX, KSP_Y, RW, 22, "key range  (a–z)",
       size=14, color=GREY)

# L0: 2 small SSTs (may overlap)
R_L0_Y = 130; R_L0_H = 32
SST0_W = 110
d.rect("r_l0_0", RX, R_L0_Y, SST0_W, R_L0_H,
       stroke=BLUE, bg=LBLUE, sw=1, roundness=3)
d.text("r_l0_0t", RX, R_L0_Y, SST0_W, R_L0_H, "SST", size=12, color=BLUE)
d.rect("r_l0_1", RX + SST0_W + 8, R_L0_Y, SST0_W, R_L0_H,
       stroke=BLUE, bg=LBLUE, sw=1, roundness=3)
d.text("r_l0_1t", RX + SST0_W + 8, R_L0_Y, SST0_W, R_L0_H, "SST", size=12, color=BLUE)
d.text("r_l0_lbl", RX + 240, R_L0_Y + 6, 160, 22,
       "L0  (overlap)", size=12, color=GREY, align="left")

# L1: 4 non-overlapping SSTs spanning keyspace
R_L1_Y = R_L0_Y + R_L0_H + 14; R_L1_H = 70
SST1_W = (RW - 3 * 6) / 4
for i in range(4):
    x = RX + i * (SST1_W + 6)
    d.rect(f"r_l1_{i}", x, R_L1_Y, SST1_W, R_L1_H,
           stroke=BLUE, bg=LBLUE, sw=1, roundness=3)
    d.text(f"r_l1_t{i}", x, R_L1_Y, SST1_W, R_L1_H, "SST",
           size=12, color=BLUE)
d.text("r_l1_lbl", RX, R_L1_Y + R_L1_H + 14, RW, 16,
       "L1  (4 SST, без пересечений)", size=11, color=GREY, align="left")

# L2: 10 smaller SSTs spanning keyspace, larger total area
R_L2_Y = R_L1_Y + R_L1_H + 44; R_L2_H = 140
N_L2 = 10
SST2_W = (RW - (N_L2 - 1) * 4) / N_L2
for i in range(N_L2):
    x = RX + i * (SST2_W + 4)
    d.rect(f"r_l2_{i}", x, R_L2_Y, SST2_W, R_L2_H,
           stroke=BLUE, bg="#A8C4F0", sw=1, roundness=3)
    d.text(f"r_l2_t{i}", x, R_L2_Y, SST2_W, R_L2_H, "SST",
           size=10, color="#1E4A8C")
d.text("r_l2_lbl", RX, R_L2_Y + R_L2_H + 14, RW, 16,
       "L2  (10 SST × 64 МБ, без пересечений)", size=11, color=GREY, align="left")

# ── Bottom labels for both panels and the global annotation ──
# Place below the rightmost-bottom element across both panels so
# nothing collides with the L2 rects or the right-side level labels.
LEFT_PANEL_BOT = L2_Y + L2_H
RIGHT_PANEL_BOT = R_L2_Y + R_L2_H + 30   # +30 covers r_l2_lbl gap (14) + height (16)
BOTTOM = max(LEFT_PANEL_BOT, RIGHT_PANEL_BOT) + 16

d.text("v_b", LX, BOTTOM, LW + 40, 20,
       "файл = run, разбиение = range, ссылка = slice",
       size=12, color=GREY)
d.text("r_b", RX, BOTTOM, RW + 40, 20,
       "файл = SSTable, разбиение = level, размер ~ const",
       size=12, color=GREY)

# Full-width annotation
ANN_Y = BOTTOM + 36
d.text("ann", 20, ANN_Y, 1200, 22,
       "Один объём данных, разные единицы учёта. Стоимости I/O в установившемся режиме сопоставимы.",
       size=14, color=INK)

d.save("/home/kostja/work/kostja.github.io/assets/img/talks/vinyl_vs_rocksdb_layout.excalidraw")
