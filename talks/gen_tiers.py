#!/usr/bin/env python3
"""Generate Picodata cluster tiers diagram — tier mechanism with Raft ring."""

import json

elements = []
_seed = 700000

def seed():
    global _seed
    _seed += 1
    return _seed

def rect(eid, x, y, w, h, stroke="#1e1e1e", bg="transparent",
         fill="solid", sw=2, ss="solid", opacity=100, roundness=3):
    elements.append({
        "type": "rectangle", "id": eid,
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": bg,
        "fillStyle": fill, "strokeWidth": sw, "strokeStyle": ss,
        "roughness": 2, "opacity": opacity,
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
        "startArrowhead": None, "endArrowhead": end_arrow
    })

# ── Layout constants ──────────────────────────────────
TIER_W = 170
TIER_H = 180
TIER_GAP = 30
X0, Y0 = 20, 20

RS_W = 60
RS_H = 30
RS_GAP_X = 10
RS_GAP_Y = 8

RAFT_H = 36
RAFT_GAP = 25

# ── Color palette ─────────────────────────────────────
TIERS = [
    {
        "name": "Storage\n(hot, RAM)",
        "stroke": "#E23956", "fill": "#F8CDD6",
        "rs_fill": "#FDECEF",
        "rs": ["RS 1", "RS 2"],
        "props": "buckets: 3000\nRF: 3",
    },
    {
        "name": "Storage\n(cold, LSM)",
        "stroke": "#FF611D", "fill": "#FFE0D0",
        "rs_fill": "#FFF3EC",
        "rs": ["RS 3", "RS 4"],
        "props": "buckets: 1000\nRF: 2",
    },
    {
        "name": "Compute\n(SQL)",
        "stroke": "#16222E", "fill": "#CFD3D6",
        "rs_fill": "#E8EAED",
        "rs": ["RS 5", "RS 6"],
        "props": "buckets: 0\nRF: 2",
    },
    {
        "name": "Arbiter",
        "stroke": "#737A82", "fill": "#E8EAED",
        "rs_fill": "#F4F5F6",
        "rs": ["RS 7", "RS 8", "RS 9"],
        "props": "buckets: 0\nRF: 3\ncan_vote: true",
    },
]

RAFT_STROKE = "#2B1321"
RAFT_FILL = "#F0E8ED"
TEXT_COLOR = "#2B1321"

# ── Draw tier boxes ───────────────────────────────────
for i, tier in enumerate(TIERS):
    tx = X0 + i * (TIER_W + TIER_GAP)
    ty = Y0

    # Tier box
    rect(f"tier{i}", tx, ty, TIER_W, TIER_H,
         stroke=tier["stroke"], bg=tier["fill"], sw=2)

    # Tier label (top)
    text(f"tier{i}_lbl", tx, ty + 6, TIER_W, 36,
         tier["name"], size=14, color=tier["stroke"])

    # RS boxes inside tier
    rs_list = tier["rs"]
    # Layout RS boxes in rows of 2
    cols = 2
    rs_block_w = cols * RS_W + (cols - 1) * RS_GAP_X
    rs_x0 = tx + (TIER_W - rs_block_w) / 2
    rs_y0 = ty + 52

    for j, rs_name in enumerate(rs_list):
        col = j % cols
        row = j // cols
        rx = rs_x0 + col * (RS_W + RS_GAP_X)
        ry = rs_y0 + row * (RS_H + RS_GAP_Y)

        rect(f"rs{i}_{j}", rx, ry, RS_W, RS_H,
             stroke=tier["stroke"], bg=tier["rs_fill"], sw=1, roundness=3)
        text(f"rs{i}_{j}_t", rx, ry, RS_W, RS_H,
             rs_name, size=12, color=tier["stroke"])

    # Properties text (bottom of tier box)
    props_y = ty + TIER_H - 46
    text(f"tier{i}_props", tx + 4, props_y, TIER_W - 8, 40,
         tier["props"], size=11, color=TEXT_COLOR, align="left", valign="top")

# ── Raft bar at bottom ────────────────────────────────
raft_x = X0
raft_y = Y0 + TIER_H + RAFT_GAP
total_w = 4 * TIER_W + 3 * TIER_GAP

rect("raft_bar", raft_x, raft_y, total_w, RAFT_H,
     stroke=RAFT_STROKE, bg=RAFT_FILL, sw=2)

text("raft_lbl", raft_x, raft_y, total_w, RAFT_H,
     "Raft ring — schema · topology · bucket map · users · ACL",
     size=13, color=RAFT_STROKE)

# ── Dashed vertical lines from tiers to Raft bar ─────
for i in range(4):
    cx = X0 + i * (TIER_W + TIER_GAP) + TIER_W / 2
    line_y_start = Y0 + TIER_H
    line_y_end = raft_y

    line(f"conn{i}", cx, line_y_start,
         [[0, 0], [0, line_y_end - line_y_start]],
         color=RAFT_STROKE, sw=1, ss="dashed")

# ── Write output ──────────────────────────────────────
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

outpath = "/home/kostja/work/kostja.github.io/assets/img/talks/tiers.excalidraw"
with open(outpath, "w") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)

print(f"Written {len(elements)} elements to {outpath}")
