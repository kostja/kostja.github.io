#!/usr/bin/env python3
"""Generate plugin lifecycle triptych: manifest, migration, config."""

import json

elements = []
_seed = 1300000


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
PANEL_W = 240
PANEL_H = 180
PANEL_GAP = 20
TITLE_H = 24
CODE_PAD = 12

# Colors
RED_STROKE = "#E23956"
RED_FILL = "#F8CDD6"
DEEP_RED_FILL = "#F09CAB"
GRAY_STROKE = "#737A82"
GRAY_FILL = "#E8EAED"
NAVY_STROKE = "#16222E"
NAVY_FILL = "#CFD3D6"
TEXT_COLOR = "#2B1321"
CODE_COLOR = "#2B1321"

# ── Panel definitions ───────────────────────────────────
PANELS = [
    {
        "title": "1. Manifest",
        "stroke": RED_STROKE,
        "fill": RED_FILL,
        "code": [
            "name: weather_plugin",
            "version: 0.2.0",
            "",
            "services:",
            "  - name: weather_svc",
            "    default_config:",
            "      api_key: \"...\"",
            "",
            "migration:",
            "  - 0001_weather.db",
        ],
    },
    {
        "title": "2. Configure & enable",
        "stroke": GRAY_STROKE,
        "fill": GRAY_FILL,
        "code": [
            "ALTER PLUGIN weather_plugin",
            "  0.2.0 SET ENABLED;",
            "",
            "ALTER SERVICE weather_svc",
            "  SET TIER = 'compute';",
            "",
            "-- max 2 versions live",
            "-- consistent across nodes",
        ],
    },
    {
        "title": "3. Migration & upgrade",
        "stroke": NAVY_STROKE,
        "fill": NAVY_FILL,
        "code": [
            "-- pico.UP",
            "CREATE TABLE weather (",
            "  city TEXT,",
            "  temp DOUBLE",
            ") DISTRIBUTED BY (city);",
            "",
            "-- pico.DOWN",
            "DROP TABLE weather;",
        ],
    },
]

# ── Draw panels ─────────────────────────────────────────
for i, panel in enumerate(PANELS):
    px = X0 + i * (PANEL_W + PANEL_GAP)

    # Panel background
    rect(f"panel_{i}", px, Y0, PANEL_W, PANEL_H,
         stroke=panel["stroke"], bg=panel["fill"], sw=2,
         roughness=1)

    # Title
    text(f"title_{i}", px, Y0 + 4, PANEL_W, TITLE_H,
         panel["title"], size=15, color=panel["stroke"])

    # Code lines
    code_y = Y0 + TITLE_H + 10
    line_h = 14
    for j, code_line in enumerate(panel["code"]):
        if code_line:
            text(f"code_{i}_{j}", px + CODE_PAD, code_y + j * line_h,
                 PANEL_W - 2 * CODE_PAD, line_h,
                 code_line, size=11, color=CODE_COLOR, align="left")

# ── Arrows between panels ──────────────────────────────
for i in range(2):
    ax = X0 + (i + 1) * PANEL_W + i * PANEL_GAP + PANEL_GAP / 2
    ay = Y0 + PANEL_H / 2
    line(f"arrow_{i}", ax, ay,
         [[0, 0], [PANEL_GAP - 4, 0]],
         color=GRAY_STROKE, sw=2, ss="solid",
         end_arrow="arrow")

# ── Bottom annotations ──────────────────────────────────
total_w = 3 * PANEL_W + 2 * PANEL_GAP
bottom_y = Y0 + PANEL_H + 14

annotations = [
    "Versioned — at most 2 plugin versions live in a cluster (blue/green upgrades)",
    "Migrations run as distributed transactions — auto-rollback on failure",
    "All management via SQL — auditable and scriptable",
]

for k, ann in enumerate(annotations):
    text(f"ann_{k}", X0, bottom_y + k * 18, total_w, 16,
         "• " + ann, size=12, color=GRAY_STROKE, align="left")


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

outpath = "/home/kostja/work/kostja.github.io/assets/img/talks/plugin_lifecycle.excalidraw"
with open(outpath, "w") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)

print(f"Written {len(elements)} elements to {outpath}")
