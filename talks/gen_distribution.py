#!/usr/bin/env python3
"""Generate Picodata data distribution diagram — co-distributed & global tables.

Each RS is drawn as two nested rectangles:
- Outer rectangle (same gray in all RS) = global table data (WAREHOUSE)
- Inner rectangle (different color per RS) = co-distributed data (ORDERS, CUSTOMER)

This visually shows that global data is identical everywhere, while
co-distributed data is unique per replica set.
"""

import json

elements = []
_seed = 900000

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

# ── Layout constants ──────────────────────────────────
OUTER_W = 200
OUTER_H = 180
RS_GAP = 30
X0, Y0 = 20, 20

INNER_PAD = 14        # padding from outer to inner rect
INNER_TOP = 56        # top offset for inner rect (below outer label area)

# Colors — outer (global) is same everywhere, inner (local) varies per RS
OUTER_STROKE = "#737A82"
OUTER_FILL = "#E8EAED"

INNER_COLORS = [
    {"stroke": "#E23956", "fill": "#F09CAB"},   # RS 1 — red
    {"stroke": "#FF611D", "fill": "#FFCDB8"},   # RS 2 — orange
    {"stroke": "#1A6B3C", "fill": "#C8E6D4"},   # RS 3 — green
]

TEXT_COLOR = "#2B1321"
HINT_COLOR = "#737A82"
LABEL_COLOR = "#2B1321"

# ── RS data ───────────────────────────────────────────
rs_data = [
    {"label": "RS 1", "buckets": "buckets 1–3"},
    {"label": "RS 2", "buckets": "buckets 4–6"},
    {"label": "RS 3", "buckets": "buckets 7–9"},
]

for i, rs in enumerate(rs_data):
    ox = X0 + i * (OUTER_W + RS_GAP)
    oy = Y0

    # Outer rectangle — global data (same color in all RS)
    rect(f"outer{i}", ox, oy, OUTER_W, OUTER_H,
         stroke=OUTER_STROKE, bg=OUTER_FILL, sw=2)

    # RS label at top
    text(f"rs{i}_lbl", ox, oy + 4, OUTER_W, 20,
         rs["label"], size=16, color=LABEL_COLOR)

    # "WAREHOUSE (global)" label in outer area
    text(f"outer{i}_t", ox, oy + 24, OUTER_W, 16,
         "WAREHOUSE (global)", size=11, color=HINT_COLOR)

    # Inner rectangle — co-distributed data (unique color per RS)
    ix = ox + INNER_PAD
    iy = oy + INNER_TOP
    iw = OUTER_W - 2 * INNER_PAD
    ih = OUTER_H - INNER_TOP - INNER_PAD

    colors = INNER_COLORS[i]
    rect(f"inner{i}", ix, iy, iw, ih,
         stroke=colors["stroke"], bg=colors["fill"], sw=2, roundness=3)

    # Table names inside inner rect
    text(f"inner{i}_t1", ix, iy + 6, iw, 18,
         "ORDERS", size=13, color=TEXT_COLOR)
    text(f"inner{i}_t2", ix, iy + 26, iw, 18,
         "CUSTOMER", size=13, color=TEXT_COLOR)

    # "(co-distributed)" hint
    text(f"inner{i}_hint", ix, iy + 48, iw, 14,
         "(co-distributed)", size=10, color=HINT_COLOR)

    # Bucket range
    text(f"inner{i}_bkt", ix, iy + ih - 18, iw, 16,
         rs["buckets"], size=11, color=colors["stroke"])

# ── Annotation bullets ────────────────────────────────
anno_y = Y0 + OUTER_H + 16
anno_x = X0
anno_w = 3 * OUTER_W + 2 * RS_GAP

annotations = [
    "co-distributed tables → JOIN locally, zero network hops",
    "global tables → dimension data available on every node",
]

for k, atxt in enumerate(annotations):
    ty = anno_y + k * 22
    text(f"anno{k}", anno_x, ty, anno_w, 20,
         f"• {atxt}", size=14, color=TEXT_COLOR, align="left", valign="top")

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

outpath = "/home/kostja/work/kostja.github.io/assets/img/talks/distribution.excalidraw"
with open(outpath, "w") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)

print(f"Written {len(elements)} elements to {outpath}")
