#!/usr/bin/env python3
"""Generate use cases diagram: industry sectors with example workloads."""

import json

elements = []
_seed = 1600000


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


# ── Colors ──────────────────────────────────────────────
RED_STROKE = "#E23956"
RED_FILL = "#F8CDD6"
DEEP_RED_FILL = "#F09CAB"
GRAY_STROKE = "#737A82"
GRAY_FILL = "#E8EAED"
TEXT_COLOR = "#2B1321"

# ── Layout ──────────────────────────────────────────────
X0, Y0 = 20, 20
CARD_W = 180
CARD_H = 80
CARD_GAP_X = 20
CARD_GAP_Y = 16
COLS = 3
ROWS = 2

# Use case data: (title, description)
USE_CASES = [
    ("Banking & Finance",     "Real-time tarification\nFraud detection"),
    ("Telecom",               "Unified customer profile\nSession management"),
    ("Government",            "Network analysis\nDocument processing"),
    ("Manufacturing & IoT",   "Sensor data pipelines\nCost calculation"),
    ("E-commerce",            "Inventory & pricing\nRecommendations"),
    ("Gaming & AdTech",       "Leaderboards\nReal-time bidding"),
]

# ── Draw cards ──────────────────────────────────────────
for idx, (title, desc) in enumerate(USE_CASES):
    row = idx // COLS
    col = idx % COLS
    cx = X0 + col * (CARD_W + CARD_GAP_X)
    cy = Y0 + row * (CARD_H + CARD_GAP_Y)

    # Card background
    rect(f"card_{idx}", cx, cy, CARD_W, CARD_H,
         stroke=RED_STROKE, bg=RED_FILL, sw=2, roughness=1)

    # Title (top part of card)
    text(f"card_title_{idx}", cx, cy + 4, CARD_W, 22,
         title, size=14, color=RED_STROKE)

    # Description (lower part)
    text(f"card_desc_{idx}", cx, cy + 28, CARD_W, CARD_H - 32,
         desc, size=11, color=TEXT_COLOR)

# ── Tagline below ──────────────────────────────────────
total_w = COLS * CARD_W + (COLS - 1) * CARD_GAP_X
tag_y = Y0 + ROWS * (CARD_H + CARD_GAP_Y) + 8
text("tagline", X0, tag_y, total_w, 20,
     "10K+ TPS  •  microsecond latency  •  ACID across data centers",
     size=14, color=GRAY_STROKE)


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

outpath = "/home/kostja/work/kostja.github.io/assets/img/talks/use_cases.excalidraw"
with open(outpath, "w") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)

print(f"Written {len(elements)} elements to {outpath}")
