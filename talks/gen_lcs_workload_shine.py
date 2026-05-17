#!/usr/bin/env python3
"""LCS workload shine — read-heavy OLTP with hot keys (Russian)."""

from excalidraw_lib import Doc

d = Doc(seed_base=920000)
BLUE = "#4B7BE5"; LBLUE = "#DBE6FA"
GREEN = "#2E7D32"; LGREEN = "#C8E6C9"
ORANGE = "#FF611D"
GREY = "#737A82"; INK = "#2B1321"

d.text("title", 20, 10, 1100, 28,
       "LCS оптимальна для OLTP с горячими ключами и предсказуемой p99",
       size=20, color=INK)

# LEFT PANEL: point-read traverses one file per level
PX0 = 30
d.text("p1t", PX0, 70, 540, 24, "1. Точечное чтение: ≤ 1 файл/уровень",
       size=16, color=INK, align="left")

# Levels with point-read arrow
LEVELS_X = 100
LEVELS = [
    ("L0", 4, 60),
    ("L1", 5, 64),
    ("L2", 5, 64),
    ("L3", 5, 64),
]
LY0 = 110
for i, (name, n, fw) in enumerate(LEVELS):
    y = LY0 + i * 60
    d.text(f"l_n_{i}", 30, y + 16, 60, 22, name, size=14, color=GREY, align="right")
    for j in range(n):
        is_hit = (j == 2)
        stroke = ORANGE if is_hit else BLUE
        fill = "#FFE0D0" if is_hit else LBLUE
        d.rect(f"l_{i}_{j}", LEVELS_X + j * 80, y, fw, 50,
               stroke=stroke, bg=fill, sw=2 if is_hit else 1, roundness=3)

# Arrow showing point-read path
d.arrow("pr", LEVELS_X + 250, LY0 - 18, [[0, 0], [0, 4 * 60 - 10]],
        color=ORANGE, sw=2, roughness=0)
d.text("pr_t", LEVELS_X + 220, LY0 - 40, 130, 22,
       "read(k)", size=14, color=ORANGE)

# Read amp summary
d.text("ra", PX0, LY0 + 4 * 60 + 10, 540, 22,
       "read amp ≈ 4   |   space amp ≈ 1.1×", size=16, color=GREEN, align="left")

# RIGHT PANEL: workloads list
PX1 = 660
d.text("p2t", PX1, 70, 460, 24, "2. Типичные нагрузки",
       size=16, color=INK, align="left")

CASES = [
    ("OLTP-ядро (профили, сессии)",
     "точечные чтения, мало горячих ключей"),
    ("Поиск по PK в API",
     "p99 — SLA, жёсткий latency-бюджет"),
    ("Каталоги и справочники",
     "плотный набор ключей, редкие обновления"),
    ("Read-replica для аналитики",
     "сканы по диапазонам, мало пересечений"),
]
for i, (h, b) in enumerate(CASES):
    y = 110 + i * 80
    d.rect(f"c_{i}", PX1, y, 460, 64, stroke=GREEN, bg=LGREEN, sw=1, roundness=3)
    d.text(f"c_h{i}", PX1 + 14, y + 6, 440, 22, h, size=14, color=GREEN, align="left")
    d.text(f"c_b{i}", PX1 + 14, y + 32, 440, 22, b, size=12, color=INK, align="left")

d.text("ann", 20, 460, 1100, 22,
       "Нагрузки, где p99 чтения важнее, чем стоимость записи.",
       size=14, color=INK)

d.save("/home/kostja/work/kostja.github.io/assets/img/talks/lcs_workload_shine.excalidraw")
