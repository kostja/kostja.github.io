#!/usr/bin/env python3
"""STCS workload shine — write-heavy append-only ingest (Russian)."""

from excalidraw_lib import Doc

d = Doc(seed_base=910000)
RED = "#E23956"; LRED = "#F8CDD6"
GREEN = "#2E7D32"; LGREEN = "#C8E6C9"
ORANGE = "#FF611D"
GREY = "#737A82"; INK = "#2B1321"

d.text("title", 20, 10, 1100, 28,
       "STCS сияет: запись доминирует, чтения редкие",
       size=20, color=INK)

# LEFT PANEL: burst of incoming writes hitting tiers
PX0 = 30
d.text("p1t", PX0, 70, 540, 24, "1. Поток записи, низкий write amp",
       size=16, color=INK, align="left")

# Multiple write arrows entering memtable
MT_X = 240; MT_Y = 130
d.rect("mt", MT_X, MT_Y, 130, 80, stroke=RED, bg=LRED, sw=1, roundness=3)
d.text("mt_t", MT_X, MT_Y, 130, 80, "memtable", size=14, color=RED)

for i in range(5):
    sy = 110 + i * 16
    d.arrow(f"w_{i}", PX0, sy, [[0, 0], [200, 30 + i * 2]],
            color=GREY, sw=1.5, roughness=0, ss="dashed")

d.text("w_lbl", PX0, 95, 200, 22, "поток записей", size=14, color=GREY, align="left")

# Tiers below memtable
TX = MT_X - 30; TY = MT_Y + 110
for i, (w, h, count) in enumerate([(60, 40, 4), (80, 50, 3), (120, 60, 1)]):
    for j in range(count):
        d.rect(f"t{i}_{j}", TX + j * (w + 6), TY + i * 80, w, h,
               stroke=RED, bg=LRED, sw=1, roundness=3)

d.text("wa_lbl", PX0, TY + 60, 200, 22,
       "write amp ≈ 1.5×", size=16, color=GREEN, align="left")
d.text("wa_lbl2", PX0, TY + 92, 200, 22,
       "износ SSD: низкий", size=14, color=GREEN, align="left")

# RIGHT PANEL: workloads list
PX1 = 660
d.text("p2t", PX1, 70, 460, 24, "2. Типичные нагрузки",
       size=16, color=INK, align="left")

CASES = [
    ("Audit-логи финансовых операций",
     "поток append, чтение только при инциденте"),
    ("Телеметрия и event-стримы",
     "millions of events/sec, выборки за прошлый день"),
    ("Журналы изменений (CDC)",
     "запись непрерывная, чтение — рефиды конкретных tx"),
    ("Архивное хранение (cold storage)",
     "запись регулярная, чтение редкое и батчевое"),
]
for i, (h, b) in enumerate(CASES):
    y = 110 + i * 80
    d.rect(f"c_{i}", PX1, y, 460, 64, stroke=GREEN, bg=LGREEN, sw=1, roundness=3)
    d.text(f"c_h{i}", PX1 + 14, y + 6, 440, 22, h, size=14, color=GREEN, align="left")
    d.text(f"c_b{i}", PX1 + 14, y + 32, 440, 22, b, size=12, color=INK, align="left")

# Bottom annotation
d.text("ann", 20, 460, 1100, 22,
       "Сценарии «write amp — главное, p99 чтения вторично».",
       size=14, color=INK)

d.save("/home/kostja/work/kostja.github.io/assets/img/talks/stcs_workload_shine.excalidraw")
