#!/usr/bin/env python3
"""Generate Ouroboros & blue/green deploy diagram.

Shows two clusters (production + staging) connected by async logical
replication, with numbered upgrade steps.
"""

import json

elements = []
_seed = 1400000


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


def ellipse(eid, x, y, w, h, stroke="#1e1e1e", bg="transparent",
            fill="solid", sw=2, roughness=2):
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
BLUE_STROKE = "#4B7BE5"
BLUE_FILL = "#DBE6FA"
GREEN_STROKE = "#1A6B3C"
GREEN_FILL = "#C8E6D4"
RED_STROKE = "#E23956"
RED_FILL = "#F8CDD6"
GRAY_STROKE = "#737A82"
GRAY_FILL = "#E8EAED"
TEXT_COLOR = "#2B1321"

# ── Layout ──────────────────────────────────────────────
X0, Y0 = 20, 20
CLUSTER_W = 240
CLUSTER_H = 130
CLUSTER_GAP = 140  # horizontal gap for the replication arrow
RS_W = 60
RS_H = 40

# ── Production cluster (left, blue) ────────────────────
prod_x = X0
prod_y = Y0 + 24

# Cluster box
rect("prod_box", prod_x, prod_y, CLUSTER_W, CLUSTER_H,
     stroke=BLUE_STROKE, bg=BLUE_FILL, sw=2)

# Title
text("prod_title", prod_x, prod_y + 4, CLUSTER_W, 20,
     "Production cluster", size=15, color=BLUE_STROKE)

# RS boxes inside
rs_y = prod_y + 32
rs_gap = 12
for i in range(3):
    rx = prod_x + 20 + i * (RS_W + rs_gap)
    rect(f"prod_rs{i}", rx, rs_y, RS_W, RS_H,
         stroke=BLUE_STROKE, bg="#A8C4F0", sw=1, roughness=1)
    text(f"prod_rs{i}_lbl", rx, rs_y, RS_W, RS_H,
         f"RS {i+1}", size=11, color=BLUE_STROKE)

# Plugin version label
text("prod_plugin", prod_x, rs_y + RS_H + 8, CLUSTER_W, 16,
     "plugin v1.0 + data", size=12, color=BLUE_STROKE)

# "PRODUCTION" label above
text("prod_label", prod_x, Y0, CLUSTER_W, 20,
     "Blue (production)", size=13, color=BLUE_STROKE, align="left")

# ── Staging cluster (right, green) ──────────────────────
stag_x = prod_x + CLUSTER_W + CLUSTER_GAP
stag_y = prod_y

rect("stag_box", stag_x, stag_y, CLUSTER_W, CLUSTER_H,
     stroke=GREEN_STROKE, bg=GREEN_FILL, sw=2)

text("stag_title", stag_x, stag_y + 4, CLUSTER_W, 20,
     "Staging cluster", size=15, color=GREEN_STROKE)

rs_y2 = stag_y + 32
for i in range(3):
    rx = stag_x + 20 + i * (RS_W + rs_gap)
    rect(f"stag_rs{i}", rx, rs_y2, RS_W, RS_H,
         stroke=GREEN_STROKE, bg="#7ED4C8", sw=1, roughness=1)
    text(f"stag_rs{i}_lbl", rx, rs_y2, RS_W, RS_H,
         f"RS {i+1}", size=11, color=GREEN_STROKE)

text("stag_plugin", stag_x, rs_y2 + RS_H + 8, CLUSTER_W, 16,
     "plugin v2.0 + data copy", size=12, color=GREEN_STROKE)

text("stag_label", stag_x, Y0, CLUSTER_W, 20,
     "Green (staging)", size=13, color=GREEN_STROKE, align="left")

# ── Replication arrow (production → staging) ────────────
arrow_x = prod_x + CLUSTER_W
arrow_y = prod_y + CLUSTER_H / 2
line("repl_arrow", arrow_x, arrow_y,
     [[0, 0], [CLUSTER_GAP, 0]],
     color=RED_STROKE, sw=3, end_arrow="arrow")

# Ouroboros label on arrow
text("repl_label", arrow_x, arrow_y - 24, CLUSTER_GAP, 16,
     "Ouroboros", size=14, color=RED_STROKE)
text("repl_desc", arrow_x, arrow_y - 10, CLUSTER_GAP, 14,
     "async logical", size=11, color=GRAY_STROKE)
text("repl_desc2", arrow_x, arrow_y + 8, CLUSTER_GAP, 14,
     "replication", size=11, color=GRAY_STROKE)

# ── Upgrade steps below ─────────────────────────────────
steps_y = prod_y + CLUSTER_H + 32
step_h = 18
total_w = CLUSTER_W * 2 + CLUSTER_GAP

STEPS = [
    ("①", "Create staging cluster with Ouroboros — production data, zero impact"),
    ("②", "Deploy & test plugin v2.0 on staging with real production data"),
    ("③", "Upgrade plugin on production, migrate schema (backward-compatible)"),
    ("④", "Drop backward compatibility shims, complete migration"),
]

for k, (num, desc) in enumerate(STEPS):
    sy = steps_y + k * step_h
    text(f"step_num_{k}", X0, sy, 20, step_h,
         num, size=13, color=RED_STROKE, align="left")
    text(f"step_desc_{k}", X0 + 24, sy, total_w - 24, step_h,
         desc, size=12, color=TEXT_COLOR, align="left")


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

outpath = "/home/kostja/work/kostja.github.io/assets/img/talks/ouroboros.excalidraw"
with open(outpath, "w") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)

print(f"Written {len(elements)} elements to {outpath}")
