#!/usr/bin/env python3
"""Generate a terminal-style demo slide showing a real Picodata SQL session."""

import json

elements = []
_seed = 1700000


def seed():
    global _seed
    _seed += 1
    return _seed


def rect(eid, x, y, w, h, stroke="#1e1e1e", bg="transparent",
         fill="solid", sw=2, ss="solid", opacity=100, roundness=3,
         roughness=2):
    elements.append({
        "type": "rectangle", "id": eid,
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": bg,
        "fillStyle": fill, "strokeWidth": sw, "strokeStyle": ss,
        "roughness": roughness, "opacity": opacity,
        "seed": seed(), "version": 1, "versionNonce": seed(),
        "isDeleted": False, "groupIds": [], "frameId": None,
        "boundElements": None, "updated": 1710000000000,
        "link": None, "locked": False,
        "roundness": {"type": roundness} if roundness else None
    })


def text(eid, x, y, w, h, txt, size=14, color="#1e1e1e",
         family=3, align="left", valign="middle"):
    elements.append({
        "type": "text", "id": eid,
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 2, "opacity": 100,
        "seed": seed(), "version": 1, "versionNonce": seed(),
        "isDeleted": False, "groupIds": [], "frameId": None,
        "boundElements": None, "updated": 1710000000000,
        "link": None, "locked": False, "roundness": None,
        "text": txt, "fontSize": size, "fontFamily": family,
        "textAlign": align, "verticalAlign": valign,
        "containerId": None, "originalText": txt, "lineHeight": 1.2
    })


def ellipse(eid, x, y, w, h, stroke="#1e1e1e", bg="transparent",
            fill="solid", sw=2, roughness=0):
    elements.append({
        "type": "ellipse", "id": eid,
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": bg,
        "fillStyle": fill, "strokeWidth": sw, "strokeStyle": "solid",
        "roughness": roughness, "opacity": 100,
        "seed": seed(), "version": 1, "versionNonce": seed(),
        "isDeleted": False, "groupIds": [], "frameId": None,
        "boundElements": None, "updated": 1710000000000,
        "link": None, "locked": False,
        "roundness": {"type": 2}
    })


# ── Colors ──────────────────────────────────────────────
TERM_BG = "#1e1e2e"        # dark terminal background
TERM_BORDER = "#45475a"    # subtle border
TITLE_BAR = "#313244"      # macOS-style title bar
GREEN = "#a6e3a1"          # prompt / SQL keywords
WHITE = "#cdd6f4"          # normal text
GRAY = "#6c7086"           # comments / dim text
YELLOW = "#f9e2af"         # strings
RED_DOT = "#f38ba8"        # window dot
YELLOW_DOT = "#f9e2af"
GREEN_DOT = "#a6e3a1"
RED_STROKE = "#E23956"     # Picodata brand

# ── Layout ──────────────────────────────────────────────
X0, Y0 = 10, 10
TERM_W = 620
TITLE_H = 28
PAD = 14
LINE_H = 15
FONT_SIZE = 12

# Terminal content lines (prompt + SQL + output)
lines = [
    ("green",  "picodata> \\set language sql"),
    ("white",  ""),
    ("green",  "picodata> CREATE TABLE weather ("),
    ("white",  "              city TEXT NOT NULL,"),
    ("white",  "              temp DOUBLE NOT NULL,"),
    ("white",  "              PRIMARY KEY (city)"),
    ("white",  "          ) USING MEMTX DISTRIBUTED BY (city);"),
    ("gray",   "1"),
    ("white",  ""),
    ("green",  "picodata> INSERT INTO weather"),
    ("white",  "          VALUES ('Moscow', 15.2),"),
    ("white",  "                 ('Berlin', 18.7),"),
    ("white",  "                 ('Tokyo', 22.1);"),
    ("gray",   "3"),
    ("white",  ""),
    ("green",  "picodata> SELECT * FROM weather ORDER BY city;"),
    ("white",  "+--------+------+"),
    ("white",  "| city   | temp |"),
    ("white",  "+========+======+"),
    ("white",  "| Berlin | 18.7 |"),
    ("white",  "| Moscow | 15.2 |"),
    ("white",  "| Tokyo  | 22.1 |"),
    ("white",  "+--------+------+"),
    ("gray",   "(3 rows)"),
]

BODY_H = PAD + len(lines) * LINE_H + PAD
TERM_H = TITLE_H + BODY_H

# ── Title bar ───────────────────────────────────────────
rect("title_bar", X0, Y0, TERM_W, TITLE_H,
     stroke=TERM_BORDER, bg=TITLE_BAR, sw=1, roughness=0)

# Traffic light dots
dot_y = Y0 + TITLE_H // 2 - 5
for i, color in enumerate([RED_DOT, YELLOW_DOT, GREEN_DOT]):
    ellipse(f"dot_{i}", X0 + 12 + i * 18, dot_y, 10, 10,
            stroke=color, bg=color, sw=0, roughness=0)

# Title text
text("title_text", X0, Y0 + 2, TERM_W, TITLE_H - 2,
     "picodata connect demo@127.0.0.1:3301",
     size=11, color=GRAY, align="center")

# ── Terminal body ───────────────────────────────────────
rect("term_body", X0, Y0 + TITLE_H, TERM_W, BODY_H,
     stroke=TERM_BORDER, bg=TERM_BG, sw=1, roughness=0)

# ── Terminal text lines ─────────────────────────────────
color_map = {
    "green": GREEN,
    "white": WHITE,
    "gray": GRAY,
    "yellow": YELLOW,
}

for i, (ctype, content) in enumerate(lines):
    if not content:
        continue
    ly = Y0 + TITLE_H + PAD + i * LINE_H
    text(f"line_{i}", X0 + PAD, ly, TERM_W - 2 * PAD, LINE_H,
         content, size=FONT_SIZE, color=color_map[ctype])


# ── Write output ────────────────────────────────────────
doc = {
    "type": "excalidraw",
    "version": 2,
    "source": "https://excalidraw.com",
    "elements": elements,
    "appState": {
        "gridSize": None,
        "viewBackgroundColor": "transparent"
    },
    "files": {}
}

outpath = "/home/kostja/work/kostja.github.io/assets/img/talks/demo.excalidraw"
with open(outpath, "w") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)

print(f"Written {len(elements)} elements to {outpath}")
