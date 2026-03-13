#!/usr/bin/env python3
"""Generate Picodata buckets diagram — unit of data distribution."""

import json

elements = []
_seed = 600000

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
RS_W = 220
RS_H = 130
RS_GAP = 50
X0, Y0 = 20, 20

BUCKET_SZ = 34
BUCKET_GAP = 8
BUCKETS_PER_ROW = 3

# Colors
RS_STROKE = "#E23956"
RS_FILL = "#F8CDD6"
BUCKET_STROKE = "#E23956"
BUCKET_FILL = "#F09CAB"
LABEL_COLOR = "#E23956"
ANNO_COLOR = "#2B1321"
HINT_COLOR = "#737A82"

# ── RS boxes ──────────────────────────────────────────
rs_data = [
    {"label": "RS 1", "buckets": [1, 2, 3, 4, 5, 6]},
    {"label": "RS 2", "buckets": [7, 8, 9, 10, 11]},
    {"label": "RS 3", "buckets": [], "hint": "(empty —\njust joined)"},
]

for i, rs in enumerate(rs_data):
    rx = X0 + i * (RS_W + RS_GAP)
    ry = Y0

    # RS box
    rect(f"rs{i}", rx, ry, RS_W, RS_H,
         stroke=RS_STROKE, bg=RS_FILL, sw=2)

    # RS label
    text(f"rs{i}_lbl", rx, ry + 6, RS_W, 22,
         rs["label"], size=18, color=LABEL_COLOR)

    # Bucket squares
    bx0 = rx + (RS_W - BUCKETS_PER_ROW * BUCKET_SZ
                - (BUCKETS_PER_ROW - 1) * BUCKET_GAP) / 2
    by0 = ry + 34

    for j, bnum in enumerate(rs["buckets"]):
        col = j % BUCKETS_PER_ROW
        row = j // BUCKETS_PER_ROW
        bx = bx0 + col * (BUCKET_SZ + BUCKET_GAP)
        by = by0 + row * (BUCKET_SZ + BUCKET_GAP)

        rect(f"b{bnum}", bx, by, BUCKET_SZ, BUCKET_SZ,
             stroke=BUCKET_STROKE, bg=BUCKET_FILL, sw=1, roundness=3)
        text(f"b{bnum}_t", bx, by, BUCKET_SZ, BUCKET_SZ,
             str(bnum), size=14, color=LABEL_COLOR)

    # Hint text for empty RS
    if "hint" in rs:
        text(f"rs{i}_hint", rx, ry + 40, RS_W, 60,
             rs["hint"], size=16, color=HINT_COLOR)

# ── In-flight bucket (B12) from RS 2 → RS 3 ──────────
# Position the bucket between RS 2 and RS 3
flight_x = X0 + 2 * (RS_W + RS_GAP) - RS_GAP / 2 - BUCKET_SZ / 2
flight_y = Y0 + RS_H + 20

rect("b12", flight_x, flight_y, BUCKET_SZ, BUCKET_SZ,
     stroke=BUCKET_STROKE, bg=BUCKET_FILL, sw=1, roundness=3)
text("b12_t", flight_x, flight_y, BUCKET_SZ, BUCKET_SZ,
     "12", size=14, color=LABEL_COLOR)

# Dashed arrow from RS 2 right edge → bucket
arrow_y = flight_y + BUCKET_SZ / 2
rs2_right = X0 + 1 * (RS_W + RS_GAP) + RS_W
line("arrow_from", rs2_right, arrow_y,
     [[0, 0], [flight_x - rs2_right - 4, 0]],
     color=RS_STROKE, sw=2, ss="dashed", end_arrow="arrow")

# Dashed arrow from bucket → RS 3 left edge
rs3_left = X0 + 2 * (RS_W + RS_GAP)
line("arrow_to", flight_x + BUCKET_SZ + 4, arrow_y,
     [[0, 0], [rs3_left - flight_x - BUCKET_SZ - 4, 0]],
     color=RS_STROKE, sw=2, ss="dashed", end_arrow="arrow")

# "rebalancing" label
text("rebal_lbl", rs2_right, flight_y + BUCKET_SZ + 6,
     rs3_left - rs2_right, 20,
     "rebalancing", size=16, color=ANNO_COLOR)

# ── Annotation bullets ────────────────────────────────
anno_y = flight_y + BUCKET_SZ + 40
anno_x = X0
anno_w = 3 * RS_W + 2 * RS_GAP

annotations = [
    "co-distributed tables → join locality",
    "drivers cache bucket→shard map",
    "new node joins with 0 buckets, receives them gradually",
]

for k, atxt in enumerate(annotations):
    ty = anno_y + k * 24
    text(f"anno{k}", anno_x, ty, anno_w, 20,
         f"• {atxt}", size=16, color=ANNO_COLOR, align="left", valign="top")

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

outpath = "/home/kostja/work/kostja.github.io/assets/img/talks/buckets.excalidraw"
with open(outpath, "w") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)

print(f"Written {len(elements)} elements to {outpath}")
