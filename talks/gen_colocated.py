#!/usr/bin/env python3
"""Generate co-located compute diagram: traditional vs co-located architecture."""

import json

elements = []
_seed = 1200000


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
         family=3, align="center", valign="middle"):
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


def line(eid, x, y, points, color="#1e1e1e", sw=2, ss="solid",
         end_arrow=None):
    elements.append({
        "type": "line", "id": eid,
        "x": x, "y": y,
        "width": max(abs(p[0]) for p in points),
        "height": max(abs(p[1]) for p in points) if any(p[1] for p in points) else 0,
        "angle": 0, "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": sw, "strokeStyle": ss,
        "roughness": 2, "opacity": 100,
        "seed": seed(), "version": 1, "versionNonce": seed(),
        "isDeleted": False, "groupIds": [], "frameId": None,
        "boundElements": None, "updated": 1710000000000,
        "link": None, "locked": False,
        "roundness": {"type": 2},
        "points": points,
        "lastCommittedPoint": None,
        "startBinding": None, "endBinding": None,
        "startArrowhead": None,
        "endArrowhead": end_arrow
    })


# ── Layout constants ────────────────────────────────────
X0, Y0 = 20, 20
BOX_W = 140
BOX_H = 80
ARROW_LEN = 80
GAP = 60  # gap between left and right diagrams

# Colors
GRAY_STROKE = "#737A82"
GRAY_FILL = "#E8EAED"
RED_STROKE = "#E23956"
RED_FILL = "#F8CDD6"
DEEP_RED_FILL = "#F09CAB"
TEXT_COLOR = "#2B1321"

# ── LEFT: Traditional architecture ──────────────────────
# Title
text("left_title", X0, Y0, BOX_W * 2 + ARROW_LEN, 20,
     "Traditional: client–server", size=15, color=GRAY_STROKE)

ly = Y0 + 30

# App Server box
rect("app_box", X0, ly, BOX_W, BOX_H,
     stroke=GRAY_STROKE, bg=GRAY_FILL, sw=2)
text("app_lbl", X0, ly, BOX_W, BOX_H,
     "Application\nServer", size=14, color=TEXT_COLOR)

# Arrow: app → db
arrow_x = X0 + BOX_W
arrow_y = ly + BOX_H / 2
line("net_arrow", arrow_x, arrow_y,
     [[0, 0], [ARROW_LEN, 0]],
     color=GRAY_STROKE, sw=2, end_arrow="arrow")
text("net_lbl", arrow_x, arrow_y - 22, ARROW_LEN, 16,
     "network", size=11, color=GRAY_STROKE)

# DB box
db_x = X0 + BOX_W + ARROW_LEN
rect("db_box", db_x, ly, BOX_W, BOX_H,
     stroke=GRAY_STROKE, bg=GRAY_FILL, sw=2)
text("db_lbl", db_x, ly, BOX_W, BOX_H,
     "Database", size=14, color=TEXT_COLOR)

# Latency label
text("lat_left", X0, ly + BOX_H + 10, BOX_W * 2 + ARROW_LEN, 18,
     "~1 ms per data access", size=14, color=GRAY_STROKE)

# ── RIGHT: Co-located compute ──────────────────────────
rx = db_x + BOX_W + GAP

# Title
text("right_title", rx, Y0, BOX_W + 50, 20,
     "Co-located: plugin in DB", size=15, color=RED_STROKE)

ry = Y0 + 30

# Outer DB box (bigger)
OUTER_W = BOX_W + 50
OUTER_H = BOX_H + 30
rect("coloc_outer", rx, ry, OUTER_W, OUTER_H,
     stroke=RED_STROKE, bg=RED_FILL, sw=2)
text("coloc_db_lbl", rx, ry, OUTER_W, 22,
     "Picodata instance", size=13, color=RED_STROKE)

# Inner plugin box
INNER_W = OUTER_W - 30
INNER_H = 40
inner_x = rx + 15
inner_y = ry + 28
rect("plugin_box", inner_x, inner_y, INNER_W, INNER_H,
     stroke=RED_STROKE, bg=DEEP_RED_FILL, sw=1, roughness=1)
text("plugin_lbl", inner_x, inner_y, INNER_W, INNER_H,
     "Plugin (Rust)", size=14, color=TEXT_COLOR)

# Data label below plugin
text("data_lbl", rx, inner_y + INNER_H + 4, OUTER_W, 16,
     "data in RAM", size=11, color="#737A82")

# Latency label
text("lat_right", rx, ry + OUTER_H + 10, OUTER_W, 18,
     "~1 μs per data access", size=14, color=RED_STROKE)

# ── VS divider ──────────────────────────────────────────
vs_x = db_x + BOX_W + GAP / 2 - 10
vs_y = ly + BOX_H / 2 - 10
text("vs", vs_x, vs_y, 20, 20, "→", size=20, color=GRAY_STROKE)

# ── Bottom: key point ──────────────────────────────────
bottom_y = ly + BOX_H + 40
text("bottom", X0, bottom_y, 600, 20,
     "1000x faster data access = plugins run where data lives",
     size=16, color=RED_STROKE, align="left")


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

outpath = "/home/kostja/work/kostja.github.io/assets/img/talks/colocated.excalidraw"
with open(outpath, "w") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)

print(f"Written {len(elements)} elements to {outpath}")
