#!/usr/bin/env python3
"""Generate Picodata failure-domains + tiers diagram — 3 DC columns."""

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
DC1_W = 180;  DC2_W = 180;  DC3_W = 100
DC_GAP = 24
DC_LBL_H = 28;  DC_PAD = 12
X0, Y0 = 20, 50          # Y0 leaves room for DC labels above

TIER_LBL_H = 16;  TIER_GAP = 10;  SECT_PAD = 6
INST_H = 28;  INST_GAP = 4
INST_INSET = 4            # inset of instance boxes from section edges

RAFT_H = 36;  RAFT_GAP = 20

# ── Tier definitions ──────────────────────────────────
TIERS = {
    "hot": {
        "name": "hot storage",
        "stroke": "#E23956", "fill": "#F8CDD6", "inst_fill": "#FDECEF",
    },
    "cold": {
        "name": "cold storage",
        "stroke": "#FF611D", "fill": "#FFE0D0", "inst_fill": "#FFF3EC",
    },
    "compute": {
        "name": "compute",
        "stroke": "#16222E", "fill": "#CFD3D6", "inst_fill": "#E8EAED",
    },
    "arbiter": {
        "name": "arbiter",
        "stroke": "#737A82", "fill": "#E8EAED", "inst_fill": "#F4F5F6",
    },
}

# Instances per tier per DC
DC_TIERS = {
    "DC 1": [
        ("hot",     ["RS 1 leader", "RS 2 follower"]),
        ("cold",    ["RS 1 leader"]),
        ("compute", ["node 1"]),
        ("arbiter", ["node 1"]),
    ],
    "DC 2": [
        ("hot",     ["RS 1 follower", "RS 2 leader"]),
        ("cold",    ["RS 1 follower"]),
        ("compute", ["node 2"]),
        ("arbiter", ["node 2"]),
    ],
    "DC 3": [
        ("arbiter", ["node 3"]),
    ],
}

DC_WIDTHS = {"DC 1": DC1_W, "DC 2": DC2_W, "DC 3": DC3_W}

# ── Compute tier section heights ──────────────────────
TIER_ORDER = ["hot", "cold", "compute", "arbiter"]
TIER_INST_COUNT = {"hot": 2, "cold": 1, "compute": 1, "arbiter": 1}


def section_height(n_inst):
    return (TIER_LBL_H + SECT_PAD
            + n_inst * INST_H + max(0, n_inst - 1) * INST_GAP
            + SECT_PAD)


SECTION_HEIGHTS = {t: section_height(TIER_INST_COUNT[t]) for t in TIER_ORDER}

# Total inner height (same for all DCs — DC 3 just has empty space)
total_sections_h = (sum(SECTION_HEIGHTS[t] for t in TIER_ORDER)
                    + (len(TIER_ORDER) - 1) * TIER_GAP)
DC_H = DC_PAD + total_sections_h + DC_PAD

# Y offset of each tier section relative to DC box top
tier_y_offsets = {}
y_off = DC_PAD
for t in TIER_ORDER:
    tier_y_offsets[t] = y_off
    y_off += SECTION_HEIGHTS[t] + TIER_GAP

# ── Colors ────────────────────────────────────────────
RAFT_STROKE = "#2B1321"
RAFT_FILL = "#F0E8ED"
TEXT_COLOR = "#2B1321"

# ── Draw DCs ──────────────────────────────────────────
dc_x_positions = {}
cx = X0

for dc_name in ["DC 1", "DC 2", "DC 3"]:
    w = DC_WIDTHS[dc_name]
    dc_x_positions[dc_name] = cx
    dc_id = dc_name.replace(" ", "")

    # DC outline
    rect(f"dc_{dc_id}", cx, Y0, w, DC_H,
         stroke="#1e1e1e", bg="transparent", sw=2)

    # DC label (above the box)
    text(f"dc_{dc_id}_lbl", cx, Y0 - DC_LBL_H - 4, w, DC_LBL_H,
         dc_name, size=16, color=TEXT_COLOR)

    # Tier sections
    inst_w = w - 2 * DC_PAD

    for tier_key, instances in DC_TIERS[dc_name]:
        tier = TIERS[tier_key]
        sh = SECTION_HEIGHTS[tier_key]
        sy = Y0 + tier_y_offsets[tier_key]

        # Section background band
        rect(f"sect_{dc_id}_{tier_key}", cx + DC_PAD, sy, inst_w, sh,
             stroke=tier["stroke"], bg=tier["fill"], sw=1, roundness=3)

        # Tier label at top of band
        text(f"slbl_{dc_id}_{tier_key}",
             cx + DC_PAD, sy + 2, inst_w, TIER_LBL_H,
             tier["name"], size=11, color=tier["stroke"])

        # Instance boxes
        iy = sy + TIER_LBL_H + SECT_PAD
        box_w = inst_w - 2 * INST_INSET
        for j, inst_label in enumerate(instances):
            rect(f"i_{dc_id}_{tier_key}_{j}",
                 cx + DC_PAD + INST_INSET, iy, box_w, INST_H,
                 stroke=tier["stroke"], bg=tier["inst_fill"],
                 sw=1, roundness=3)
            text(f"it_{dc_id}_{tier_key}_{j}",
                 cx + DC_PAD + INST_INSET, iy, box_w, INST_H,
                 inst_label, size=11, color=tier["stroke"])
            iy += INST_H + INST_GAP

    cx += w + DC_GAP

# ── Raft bar at bottom ────────────────────────────────
raft_y = Y0 + DC_H + RAFT_GAP
total_w = cx - DC_GAP - X0

rect("raft_bar", X0, raft_y, total_w, RAFT_H,
     stroke=RAFT_STROKE, bg=RAFT_FILL, sw=2)

text("raft_lbl", X0, raft_y, total_w, RAFT_H,
     "Raft ring \u2014 schema \u00b7 topology \u00b7 bucket map",
     size=13, color=RAFT_STROKE)

# ── Dashed vertical lines from DCs to Raft bar ───────
for dc_name in ["DC 1", "DC 2", "DC 3"]:
    w = DC_WIDTHS[dc_name]
    lx = dc_x_positions[dc_name] + w / 2
    line(f"conn_{dc_name.replace(' ', '')}",
         lx, Y0 + DC_H,
         [[0, 0], [0, RAFT_GAP]],
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
