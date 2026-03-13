#!/usr/bin/env python3
"""Generate 'Three database architectures' triptych Excalidraw diagram."""

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
         family=3, align="center", valign="top"):
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


# ── Layout ──────────────────────────────────────────────
COL_W = 280
COL_GAP = 40
X0 = 20
Y0 = 20

COL_X = [X0 + i * (COL_W + COL_GAP) for i in range(3)]

COLS = [
    {"name": "Shared-Storage", "stroke": "#16222E", "fill": "#2B1321",
     "light": "#CFD3D6", "example": "Neon, Aurora"},
    {"name": "Shared-Memory", "stroke": "#FF611D", "fill": "#FFB08E",
     "light": "#FFE0D0", "example": "PostgreSQL"},
    {"name": "Shared-Nothing", "stroke": "#E23956", "fill": "#F09CAB",
     "light": "#F8CDD6", "example": "Picodata"},
]

ANNOTATIONS = [
    "compute ↔ storage\nover network",
    "backends contend on\nshared memory",
    "shard-per-core:\nno locks, no contention",
]

# ── Column titles (standalone text, no container) ──────
for i, col in enumerate(COLS):
    cx = COL_X[i]
    text(f"title_{i}", cx, Y0, COL_W, 24,
         col["name"], size=20, color=col["stroke"])
    text(f"example_{i}", cx, Y0 + 26, COL_W, 16.8,
         col["example"], size=14, color="#2B1321")

# ── Compute boxes ──────────────────────────────────────
BOX_W = 70
BOX_H = 40
BOX_Y = Y0 + 60
BOX_GAP = 10


def box_x(col_i, box_j):
    total = 3 * BOX_W + 2 * BOX_GAP
    start = COL_X[col_i] + (COL_W - total) / 2
    return start + box_j * (BOX_W + BOX_GAP)


# Columns 0 and 1: Compute/Backend boxes + arrows to shared resource
for i in range(2):
    col = COLS[i]
    for j in range(3):
        bx = box_x(i, j)
        rect(f"compute_{i}_{j}", bx, BOX_Y, BOX_W, BOX_H,
             stroke=col["stroke"], bg=col["light"], fill="solid", sw=2)
        if i == 0:
            labels = ["Compute 1", "Compute 2", "Compute 3"]
        else:
            labels = ["Backend 1", "Backend 2", "Backend 3"]
        # Center text inside box (standalone, no containerId)
        text(f"compute_{i}_{j}_t", bx, BOX_Y + (BOX_H - 14.4) / 2,
             BOX_W, 14.4, labels[j], size=12, color=col["stroke"])

    # Arrows converging to shared block
    SHARED_Y = BOX_Y + BOX_H + 100
    SHARED_W = 200
    SHARED_H = 50
    shared_cx = COL_X[i] + COL_W / 2

    for j in range(3):
        bx = box_x(i, j) + BOX_W / 2
        by = BOX_Y + BOX_H
        line(f"arrow_{i}_{j}", bx, by,
             [[0, 0], [shared_cx - bx, SHARED_Y - by]],
             color=col["stroke"], sw=2, end_arrow="arrow")

    # Shared resource block
    sx = COL_X[i] + (COL_W - SHARED_W) / 2
    label = "Shared Storage" if i == 0 else "Shared Memory"
    rect(f"shared_{i}", sx, SHARED_Y, SHARED_W, SHARED_H,
         stroke=col["stroke"], bg=col["fill"], fill="solid", sw=3)
    text(f"shared_{i}_t", sx, SHARED_Y + (SHARED_H - 16.8) / 2,
         SHARED_W, 16.8, label, size=14, color=col["stroke"])


# Column 2: Shared-Nothing — taller CPU+Shard stacked boxes
col = COLS[2]
TALL_H = 120
TALL_W = 70
SHARD_SPLIT = 55

for j in range(3):
    bx = box_x(2, j)
    rect(f"unit_{j}", bx, BOX_Y, TALL_W, TALL_H,
         stroke=col["stroke"], bg=col["light"], fill="solid", sw=2)

    # CPU label (top half)
    text(f"cpu_{j}", bx, BOX_Y + 14, TALL_W, 14.4,
         f"CPU {j+1}", size=12, color=col["stroke"])

    # Divider
    div_y = BOX_Y + SHARD_SPLIT
    line(f"div_{j}", bx, div_y, [[0, 0], [TALL_W, 0]],
         color=col["stroke"], sw=1, ss="dashed")

    # Shard label (bottom half)
    text(f"shard_{j}", bx, div_y + 14, TALL_W, 14.4,
         f"Shard {j+1}", size=12, color=col["stroke"])

# Dashed empty box (no shared state)
SHARED_Y = BOX_Y + BOX_H + 100
SHARED_W = 200
SHARED_H = 50
sx = COL_X[2] + (COL_W - SHARED_W) / 2
rect("no_shared", sx, SHARED_Y, SHARED_W, SHARED_H,
     stroke="#2B1321", bg="transparent", fill="solid",
     sw=1, ss="dashed")
text("no_shared_t", sx, SHARED_Y + (SHARED_H - 16.8) / 2,
     SHARED_W, 16.8, "no shared state", size=14, color="#2B1321")


# ── Bottom annotations ──────────────────────────────────
ANNOT_Y = SHARED_Y + SHARED_H + 25
for i in range(3):
    text(f"annot_{i}", COL_X[i], ANNOT_Y, COL_W, 33.6,
         ANNOTATIONS[i], size=14, color=COLS[i]["stroke"])


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

outpath = "/home/kostja/work/kostja.github.io/assets/img/talks/db_architectures.excalidraw"
with open(outpath, "w") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)

print(f"Written {len(elements)} elements to {outpath}")
