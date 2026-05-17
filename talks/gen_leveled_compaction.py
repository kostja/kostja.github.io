#!/usr/bin/env python3
"""Leveled Compaction Strategy diagram (Russian)."""

from excalidraw_lib import Doc

d = Doc(seed_base=840000)
RED = "#E23956"; LRED = "#F8CDD6"
BLUE = "#4B7BE5"; LBLUE = "#DBE6FA"
GREY = "#737A82"; INK = "#2B1321"
ORANGE = "#FF611D"

d.text("title", 20, 10, 1000, 28,
       "Непересекающиеся уровни, каждый ×10 по размеру",
       size=20, color=INK)

# L0: 4 small files (can overlap)
LX0 = 200
def file_box(eid, x, y, w, h, label, stroke, fill):
    d.rect(eid, x, y, w, h, stroke=stroke, bg=fill, sw=1, roundness=3)
    d.text(eid + "_t", x, y, w, h, label, size=12, color=stroke)

L0Y = 70
d.text("l0lbl", 0, L0Y + 12, 190, 22, "L0 (с пересечением)",
       size=14, color=GREY, align="right")
for i in range(4):
    file_box(f"l0_{i}", LX0 + i * 75, L0Y, 65, 36, "a–z", RED, LRED)

# L1
L1Y = L0Y + 70
d.text("l1lbl", 0, L1Y + 12, 190, 22, "L1  ×10",
       size=14, color=GREY, align="right")
for i, r in enumerate(["a–e", "f–j", "k–o", "p–t", "u–z"]):
    file_box(f"l1_{i}", LX0 + i * 75, L1Y, 70, 36, r, BLUE, LBLUE)

# L2
L2Y = L1Y + 70
d.text("l2lbl", 30, L2Y + 12, 160, 22, "L2  ×100",
       size=14, color=GREY, align="right")
RANGES_L2 = ["a-c","d-e","f-h","i-j","k-m","n-o","p-r","s-t","u-w","x-z"]
for i, r in enumerate(RANGES_L2):
    file_box(f"l2_{i}", LX0 + i * 38, L2Y, 35, 36, r, BLUE, LBLUE)

# L3
L3Y = L2Y + 70
d.text("l3lbl", 30, L3Y + 12, 160, 22, "L3  ×1000",
       size=14, color=GREY, align="right")
for i in range(20):
    d.rect(f"l3_{i}", LX0 + i * 19, L3Y, 17, 36, stroke=BLUE, bg=LBLUE, sw=1, roundness=3)

# Right side: properties
PX = 640
d.text("h0", PX, L0Y, 360, 24, "Свойства", size=16, color=INK, align="left")
for i, line in enumerate([
    "• точечное чтение: ≤ 1 файл/уровень",
    "• read amp = O(log₁₀ N)",
    "• уровни не пересекаются по ключу",
    "• продвижение = перезапись",
    "  всего диапазона",
]):
    d.text(f"h{i+1}", PX, L0Y + 30 + i * 26, 360, 22, line, size=14, color=INK, align="left")

# Arrow: promotion
d.arrow("prom", 175, L0Y + 36, [[0, 0], [0, 180]], color=ORANGE, sw=1.5, roughness=0)
d.text("prom_t", 70, L0Y + 100, 110, 22, "продвижение", size=12, color=ORANGE)

d.save("/home/kostja/work/kostja.github.io/assets/img/talks/leveled_compaction.excalidraw")
