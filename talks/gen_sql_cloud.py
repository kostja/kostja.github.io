#!/usr/bin/env python3
"""Generate SQL tag cloud diagram for Picodata SQL support slide.

Keywords are color-coded by category and sized by importance.
Layout is a manually arranged grid to look like a natural tag cloud.
"""

import json

elements = []
_seed = 950000

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

# ── Category colors ───────────────────────────────────
# DQL (queries) — Pico Red
DQL_STROKE = "#E23956"
DQL_FILL = "#F8CDD6"
# DML (data changes) — Orange
DML_STROKE = "#FF611D"
DML_FILL = "#FFE0D0"
# DDL (schema) — Navy
DDL_STROKE = "#16222E"
DDL_FILL = "#CFD3D6"
# DCL (access control) — Purple-ish
DCL_STROKE = "#6B3FA0"
DCL_FILL = "#E8DBF5"
# Types — Gray
TYPE_STROKE = "#737A82"
TYPE_FILL = "#E8EAED"
# Picodata extensions — Pico Red bold
EXT_STROKE = "#E23956"
EXT_FILL = "#F09CAB"

TEXT_COLOR = "#2B1321"

# ── Tag definitions: (label, category, size_class) ────
# size_class: 3=large, 2=medium, 1=small
# Each tag gets: font_size, tag_h, approximate tag_w per char
SIZE_MAP = {
    3: {"fs": 20, "h": 40, "cw": 13},
    2: {"fs": 15, "h": 32, "cw": 10},
    1: {"fs": 12, "h": 26, "cw": 8},
}

TAGS = [
    # Row 0
    ("SELECT",          "dql", 3),
    ("JOIN",            "dql", 3),
    ("INSERT",          "dml", 3),
    ("CREATE TABLE",    "ddl", 3),
    ("WHERE",           "dql", 2),
    # Row 1
    ("GROUP BY",        "dql", 2),
    ("ORDER BY",        "dql", 2),
    ("CTE",             "dql", 2),
    ("WINDOW",          "dql", 2),
    ("UPDATE",          "dml", 2),
    ("DELETE",          "dml", 2),
    ("UNION",           "dql", 2),
    # Row 2
    ("SUBQUERY",        "dql", 2),
    ("GRANT",           "dcl", 2),
    ("REVOKE",          "dcl", 2),
    ("HAVING",          "dql", 1),
    ("LIMIT",           "dql", 1),
    ("DISTINCT",        "dql", 1),
    ("CASE",            "dql", 1),
    # Row 3
    ("ON CONFLICT",     "dml", 1),
    ("ALTER TABLE",     "ddl", 1),
    ("DROP",            "ddl", 1),
    ("INDEX",           "ddl", 1),
    ("VALUES",          "dql", 1),
    ("CALL",            "dml", 1),
    ("BACKUP",          "ddl", 1),
    ("ALTER SYSTEM",    "ddl", 1),
    # Row 4 — types
    ("INTEGER",         "type", 1),
    ("TEXT",            "type", 1),
    ("BOOLEAN",         "type", 1),
    ("DOUBLE",          "type", 1),
    ("DECIMAL",         "type", 1),
    ("UUID",            "type", 1),
    ("DATETIME",        "type", 1),
    # Row 5 — Picodata extensions + transactions
    ("DISTRIBUTED BY",  "ext", 2),
    ("DISTRIBUTED GLOBALLY", "ext", 2),
    ("BEGIN...COMMIT",  "dml", 2),
]

CAT_COLORS = {
    "dql": (DQL_STROKE, DQL_FILL),
    "dml": (DML_STROKE, DML_FILL),
    "ddl": (DDL_STROKE, DDL_FILL),
    "dcl": (DCL_STROKE, DCL_FILL),
    "type": (TYPE_STROKE, TYPE_FILL),
    "ext": (EXT_STROKE, EXT_FILL),
}

# ── Layout: arrange tags in rows ──────────────────────
X0, Y0 = 20, 20
TAG_PAD_X = 20       # horizontal padding inside tag
TAG_GAP_X = 8        # gap between tags
TAG_GAP_Y = 8        # gap between rows

# Define rows manually for a nice cloud look
ROWS = [
    # Row 0: big keywords
    [0, 1, 2, 3, 4],
    # Row 1: medium
    [5, 6, 7, 8, 9, 10, 11],
    # Row 2: medium + small
    [12, 13, 14, 15, 16, 17, 18],
    # Row 3: small DDL/DML
    [19, 20, 21, 22, 23, 24, 25, 26],
    # Row 4: types
    [27, 28, 29, 30, 31, 32, 33],
    # Row 5: picodata extensions + transactions
    [34, 35, 36],
]

y = Y0
for row_indices in ROWS:
    x = X0
    row_h = 0
    for idx in row_indices:
        label, cat, sz = TAGS[idx]
        s = SIZE_MAP[sz]
        stroke, bg = CAT_COLORS[cat]
        tw = len(label) * s["cw"] + 2 * TAG_PAD_X
        th = s["h"]
        row_h = max(row_h, th)

        rect(f"tag{idx}", x, y, tw, th,
             stroke=stroke, bg=bg, sw=1, roundness=3, roughness=1)
        text(f"tag{idx}_t", x, y, tw, th,
             label, size=s["fs"], color=stroke)

        x += tw + TAG_GAP_X

    y += row_h + TAG_GAP_Y

# ── Legend at bottom ──────────────────────────────────
legend_y = y + 4
legend_x = X0
LEGEND = [
    ("DQL", DQL_STROKE, DQL_FILL),
    ("DML", DML_STROKE, DML_FILL),
    ("DDL", DDL_STROKE, DDL_FILL),
    ("DCL", DCL_STROKE, DCL_FILL),
    ("types", TYPE_STROKE, TYPE_FILL),
    ("Picodata", EXT_STROKE, EXT_FILL),
]

for k, (lbl, stroke, bg) in enumerate(LEGEND):
    lx = legend_x + k * 90
    rect(f"leg{k}", lx, legend_y, 14, 14,
         stroke=stroke, bg=bg, sw=1, roundness=2)
    text(f"leg{k}_t", lx + 18, legend_y, 64, 14,
         lbl, size=11, color=stroke, align="left")

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

outpath = "/home/kostja/work/kostja.github.io/assets/img/talks/sql_cloud.excalidraw"
with open(outpath, "w") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)

print(f"Written {len(elements)} elements to {outpath}")
