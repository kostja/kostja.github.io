#!/usr/bin/env python3
"""Generate Picodata shared-nothing architecture Excalidraw diagram."""

import json, os

elements = []
_seed = 500000

def seed():
    global _seed
    _seed += 1
    return _seed

def rect(eid, x, y, w, h, stroke="#1e1e1e", bg="transparent",
         fill="solid", sw=2, ss="solid", opacity=100,
         bound_text=None, roundness=3):
    be = [{"id": bound_text, "type": "text"}] if bound_text else None
    elements.append({
        "type": "rectangle", "id": eid,
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": bg,
        "fillStyle": fill, "strokeWidth": sw, "strokeStyle": ss,
        "roughness": 2, "opacity": opacity,
        "seed": seed(), "version": 1, "versionNonce": seed(),
        "isDeleted": False, "groupIds": [], "frameId": None,
        "boundElements": be, "updated": 1710000000000,
        "link": None, "locked": False,
        "roundness": {"type": roundness} if roundness else None
    })

def text(eid, x, y, w, h, txt, size=14, color="#1e1e1e",
         family=3, align="center", valign="middle", container=None):
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
        "containerId": container, "originalText": txt, "lineHeight": 1.2
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

# ── Layout ──────────────────────────────────────────────
DC_W = 286
DC_H = 400
DC_GAP = 130
DC_Y = 60
DC_XS = [50, 50 + DC_W + DC_GAP, 50 + 2 * (DC_W + DC_GAP)]

# Server box inside each DC
SRV_MARGIN = 20
SRV_Y_OFF = 55  # from DC top

INST_W = 195
INST_H = 65
INST_GAP = 23  # vertical gap between instances
INST_X_OFF = (DC_W - INST_W) / 2
INST_Y0 = SRV_Y_OFF + 40  # first instance, relative to DC top

# RS colors
RS = [
    {"stroke": "#16222E", "active": "#737A82", "standby": "#CFD3D6"},  # navy
    {"stroke": "#FF611D", "active": "#FFB08E", "standby": "#FFE0D0"},  # Pico Orange
    {"stroke": "#E23956", "active": "#F09CAB", "standby": "#F8CDD6"},  # Pico Red
]

# ── DC boxes ────────────────────────────────────────────
for dc in range(3):
    dx = DC_XS[dc]
    # DC box
    rect(f"dc{dc}", dx, DC_Y, DC_W, DC_H,
         stroke="#2B1321", bg="transparent", sw=2, ss="solid")
    # DC label
    text(f"dc{dc}_lbl", dx, DC_Y + 10, DC_W, 28,
         f"DC {dc+1}", size=24, color="#2B1321")
    # Server box
    sx = dx + SRV_MARGIN
    sy = DC_Y + SRV_Y_OFF
    sw = DC_W - 2 * SRV_MARGIN
    sh = DC_H - SRV_Y_OFF - SRV_MARGIN
    rect(f"srv{dc}", sx, sy, sw, sh,
         stroke="#737A82", bg="transparent", sw=1, ss="dashed")
    # Server label
    text(f"srv{dc}_lbl", sx, sy + 6, sw, 19,
         f"server {dc+1}", size=16, color="#737A82")

# ── Instances ───────────────────────────────────────────
inst_centers = {}  # (dc, rs) -> (cx, cy) for drawing connections

for dc in range(3):
    dx = DC_XS[dc]
    for rs in range(3):
        is_leader = (dc == rs)
        ix = dx + INST_X_OFF
        iy = DC_Y + INST_Y0 + rs * (INST_H + INST_GAP)

        color = RS[rs]["stroke"]
        bg = RS[rs]["active"] if is_leader else RS[rs]["standby"]
        stroke_w = 3 if is_leader else 2

        rid = f"i_d{dc}r{rs}"
        tid = f"i_d{dc}r{rs}_t"

        rect(rid, ix, iy, INST_W, INST_H,
             stroke=color, bg=bg, fill="solid", sw=stroke_w,
             roundness=3)

        # Label (standalone text, centered in box)
        role = "leader" if is_leader else "follower"
        label = f"RS {rs+1} {role}"
        text(tid, ix, iy + (INST_H - 19) / 2, INST_W, 19,
             label, size=16, color=color)

        # Store center coords for connections
        inst_centers[(dc, rs)] = (ix + INST_W / 2, iy + INST_H / 2)

# ── Replication lines ───────────────────────────────────
# Horizontal connections between same-RS instances across DCs
for rs in range(3):
    color = RS[rs]["stroke"]
    for dc_from, dc_to in [(0, 1), (1, 2)]:
        x1 = DC_XS[dc_from] + INST_X_OFF + INST_W  # right edge
        x2 = DC_XS[dc_to] + INST_X_OFF              # left edge
        y = DC_Y + INST_Y0 + rs * (INST_H + INST_GAP) + INST_H / 2
        line(f"conn_rs{rs}_{dc_from}{dc_to}", x1, y,
             [[0, 0], [x2 - x1, 0]], color=color, sw=2, ss="dashed")

# ── Bottom connection arcs (DC3 back to DC1 to complete the ring) ──
for rs in range(3):
    color = RS[rs]["stroke"]
    # From bottom of DC3 instance, curve down, then to DC1 instance bottom
    x_right = DC_XS[2] + INST_X_OFF + INST_W / 2   # center of DC3 instance
    x_left = DC_XS[0] + INST_X_OFF + INST_W / 2     # center of DC1 instance
    y_inst = DC_Y + INST_Y0 + rs * (INST_H + INST_GAP) + INST_H  # bottom of instance

    # Arc goes: down from DC3, left below DCs, up to DC1
    arc_depth = 30 + rs * 15  # stagger arcs so they don't overlap
    y_bottom = DC_Y + DC_H + arc_depth

    line(f"arc_rs{rs}", x_right, y_inst, [
        [0, 0],
        [0, y_bottom - y_inst],
        [x_left - x_right, y_bottom - y_inst],
        [x_left - x_right, 0],
    ], color=color, sw=2, ss="dashed")

# ── Note ────────────────────────────────────────────────
note_y = DC_Y + DC_H + 30 + 3 * 15 + 15
total_w = DC_XS[2] + DC_W - DC_XS[0]
text("note", DC_XS[0], note_y, total_w, 24,
     "shared-nothing: each instance = dedicated CPU core(s)",
     size=20, color="#2B1321", align="center", valign="top")

# ── Legend ──────────────────────────────────────────────
leg_y = note_y + 30
leg_x = 250

# Leader
rect("leg_leader", leg_x, leg_y, 22, 22,
     stroke="#16222E", bg="#737A82", sw=3)
text("leg_leader_t", leg_x + 28, leg_y, 65, 22,
     "leader", size=16, color="#16222E", align="left")

# Follower
rect("leg_follower", leg_x + 120, leg_y, 22, 22,
     stroke="#16222E", bg="#CFD3D6", sw=2)
text("leg_follower_t", leg_x + 148, leg_y, 80, 22,
     "follower", size=16, color="#2B1321", align="left")

# Replication line
line("leg_line", leg_x + 260, leg_y + 11, [[0, 0], [50, 0]],
     color="#2B1321", sw=2, ss="dashed")
text("leg_line_t", leg_x + 316, leg_y, 120, 22,
     "replication", size=16, color="#2B1321", align="left")

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

outpath = "/home/kostja/work/kostja.github.io/assets/img/talks/architecture.excalidraw"
with open(outpath, "w") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)

print(f"Written {len(elements)} elements to {outpath}")
