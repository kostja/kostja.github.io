#!/usr/bin/env python3
"""Generate Picodata data distribution diagram — star schema per RS.

Each RS has two nested rectangles:
- Outer rectangle (gray) = global tables (WAREHOUSE, ITEM)
- Inner rectangle (colored per RS) = co-distributed star schema:
    CUSTOMER → ORDERS → STOCK (all keyed by W_ID)
RS labels sit above each box.
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


def line(eid, x, y, points, color="#1e1e1e", sw=2, ss="solid"):
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
        "startArrowhead": None, "endArrowhead": None
    })


# ── Layout constants ──────────────────────────────────
OUTER_W = 220
RS_GAP = 30
RS_LBL_H = 28
OUTER_PAD = 14        # padding from outer to inner rect

TBL_W = 66
TBL_H = 22

# Inner rect: star schema layout (relative to inner top)
IPAD = 10
CUST_RY = IPAD                        # CUSTOMER
ORD_RY = CUST_RY + TBL_H + 14        # ORDERS (fact)
STOCK_RY = ORD_RY + TBL_H + 14       # STOCK
BKT_RY = STOCK_RY + TBL_H + 8        # bucket range label
INNER_H = BKT_RY + 16 + IPAD

# Outer rect: WAREHOUSE on top, inner rect in middle, ITEM below
OUTER_TOP_ZONE = TBL_H + 14   # WAREHOUSE box + gap
OUTER_BOT_ZONE = TBL_H + 14   # ITEM box + gap
OUTER_H = OUTER_TOP_ZONE + INNER_H + OUTER_BOT_ZONE + OUTER_PAD

X0, Y0 = 20, 20

# ── Colors ────────────────────────────────────────────
OUTER_STROKE = "#737A82"
OUTER_FILL = "#E8EAED"
RS_LABEL_COLOR = "#E23956"

INNER_COLORS = [
    {"stroke": "#E23956", "fill": "#F09CAB"},   # RS 1 — red
    {"stroke": "#FF611D", "fill": "#FFCDB8"},   # RS 2 — orange
    {"stroke": "#1A6B3C", "fill": "#C8E6D4"},   # RS 3 — green
]

TEXT_COLOR = "#2B1321"
HINT_COLOR = "#737A82"

# ── RS data ───────────────────────────────────────────
rs_data = [
    {"label": "RS 1", "buckets": "bkt 1\u20131000"},
    {"label": "RS 2", "buckets": "bkt 1001\u20132000"},
    {"label": "RS 3", "buckets": "bkt 2001\u20133000"},
]

for i, rs in enumerate(rs_data):
    ox = X0 + i * (OUTER_W + RS_GAP)
    oy = Y0 + RS_LBL_H  # outer box top (label is above)

    colors = INNER_COLORS[i]

    # ── RS label above box ─────────────────────────────
    text(f"rs{i}_lbl", ox, Y0, OUTER_W, RS_LBL_H,
         rs["label"], size=18, color=RS_LABEL_COLOR)

    # ── Outer rectangle — WAREHOUSE (global) ───────────
    rect(f"outer{i}", ox, oy, OUTER_W, OUTER_H,
         stroke=OUTER_STROKE, bg=OUTER_FILL, sw=2)

    # ── WAREHOUSE (global) — top of outer rect ──────────
    wh_w = OUTER_W - 2 * OUTER_PAD
    wh_x = ox + OUTER_PAD
    wh_y = oy + 6
    rect(f"wh{i}", wh_x, wh_y, wh_w, TBL_H,
         stroke=OUTER_STROKE, bg=OUTER_FILL, sw=1)
    text(f"wh{i}_lbl", wh_x, wh_y, wh_w, TBL_H,
         "WAREHOUSE (global)", size=10, color=HINT_COLOR)

    # ── Inner rectangle — co-distributed star schema ───
    ix = ox + OUTER_PAD
    iy = oy + OUTER_TOP_ZONE
    iw = OUTER_W - 2 * OUTER_PAD

    rect(f"inner{i}", ix, iy, iw, INNER_H,
         stroke=colors["stroke"], bg=colors["fill"], sw=2)

    # ── Star schema tables inside inner rect ───────────
    cx_mid = ix + iw / 2  # horizontal center of inner rect

    # CUSTOMER — top center (dimension)
    cust_x = cx_mid - TBL_W / 2
    cust_y = iy + CUST_RY
    rect(f"cust{i}", cust_x, cust_y, TBL_W, TBL_H,
         stroke=colors["stroke"], bg=colors["fill"], sw=1)
    text(f"cust{i}_t", cust_x, cust_y, TBL_W, TBL_H,
         "CUSTOMER", size=10, color=TEXT_COLOR)

    # ORDERS — center (fact table, bolder)
    ord_x = cx_mid - TBL_W / 2
    ord_y = iy + ORD_RY
    rect(f"ord{i}", ord_x, ord_y, TBL_W, TBL_H,
         stroke=colors["stroke"], bg=colors["fill"], sw=2)
    text(f"ord{i}_t", ord_x, ord_y, TBL_W, TBL_H,
         "ORDERS", size=10, color=TEXT_COLOR)

    # STOCK — bottom center (dimension)
    stock_x = cx_mid - TBL_W / 2
    stock_y = iy + STOCK_RY
    rect(f"stock{i}", stock_x, stock_y, TBL_W, TBL_H,
         stroke=colors["stroke"], bg=colors["fill"], sw=1)
    text(f"stock{i}_t", stock_x, stock_y, TBL_W, TBL_H,
         "STOCK", size=10, color=TEXT_COLOR)

    # ── Lines: CUSTOMER→ORDERS, ORDERS→STOCK ──────────
    # CUSTOMER bottom → ORDERS top
    line(f"l_co{i}", cx_mid, cust_y + TBL_H,
         [[0, 0], [0, ord_y - (cust_y + TBL_H)]],
         color=colors["stroke"], sw=1)

    # ORDERS bottom → STOCK top
    line(f"l_os{i}", cx_mid, ord_y + TBL_H,
         [[0, 0], [0, stock_y - (ord_y + TBL_H)]],
         color=colors["stroke"], sw=1)

    # ── Bucket range label ─────────────────────────────
    text(f"bkt{i}", ix, iy + BKT_RY, iw, 14,
         rs["buckets"], size=11, color=colors["stroke"])

    # ── ITEM (global) — bottom of outer rect ─────────────
    item_w = OUTER_W - 2 * OUTER_PAD
    item_x = ox + OUTER_PAD
    item_y = iy + INNER_H + 6
    rect(f"item{i}", item_x, item_y, item_w, TBL_H,
         stroke=OUTER_STROKE, bg=OUTER_FILL, sw=1)
    text(f"item{i}_t", item_x, item_y, item_w, TBL_H,
         "ITEM (global)", size=10, color=HINT_COLOR)

# ── Annotation bullets ────────────────────────────────
anno_y = Y0 + RS_LBL_H + OUTER_H + 16
anno_x = X0
anno_w = 3 * OUTER_W + 2 * RS_GAP

annotations = [
    "co-distributed tables \u2192 JOIN locally, zero network hops",
    "global tables \u2192 dimension data available on every node",
]

for k, atxt in enumerate(annotations):
    ty = anno_y + k * 22
    text(f"anno{k}", anno_x, ty, anno_w, 20,
         f"\u2022 {atxt}", size=14, color=TEXT_COLOR, align="left", valign="top")

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
