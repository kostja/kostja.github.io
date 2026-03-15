#!/usr/bin/env python3
"""Generate Picodata cluster assembly diagram.

Shows 2 servers (failure domains) with 4 instances forming 2 replica sets.
Leaders are distributed across servers. Replication arrows connect RS pairs.
"""

import json

elements = []
_seed = 800000


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
X0, Y0 = 20, 50
SVR_W = 160;  SVR_GAP = 80
SVR_PAD = 12; SVR_LBL_H = 24
INST_W = SVR_W - 2 * SVR_PAD
INST_H = 48;  INST_GAP = 20
ROLE_H = 16   # height of role label below instance box

# ── Colors ────────────────────────────────────────────
SVR_STROKE = "#737A82"
TEXT_COLOR = "#2B1321"

RS_COLORS = {
    1: {"stroke": "#E23956", "leader": "#F09CAB", "follower": "#FDECEF"},
    2: {"stroke": "#FF611D", "leader": "#FFB08E", "follower": "#FFF3EC"},
}

# ── Instance placement ───────────────────────────────
# (server, row, instance_num, rs, role)
# Leaders distributed across servers for failure domain safety.
INSTANCES = [
    (1, 0, 1, 1, "leader"),
    (1, 1, 4, 2, "follower"),
    (2, 0, 2, 1, "follower"),
    (2, 1, 3, 2, "leader"),
]

# ── Compute server box height ─────────────────────────
N_ROWS = 2
inner_h = N_ROWS * (INST_H + ROLE_H) + (N_ROWS - 1) * INST_GAP
SVR_H = SVR_LBL_H + SVR_PAD + inner_h + SVR_PAD

# ── Draw server boxes ────────────────────────────────
for s in (1, 2):
    sx = X0 + (s - 1) * (SVR_W + SVR_GAP)
    # Label above
    text(f"svr{s}_lbl", sx, Y0 - 28, SVR_W, 24,
         f"server {s}", size=16, color=SVR_STROKE)
    # Box
    rect(f"svr{s}", sx, Y0, SVR_W, SVR_H,
         stroke=SVR_STROKE, bg="transparent", sw=2)

# ── Draw instances ────────────────────────────────────
inst_pos = {}  # (rs, role) -> (center_x, center_y, server)

for s, row, inum, rs, role in INSTANCES:
    sx = X0 + (s - 1) * (SVR_W + SVR_GAP)
    ix = sx + SVR_PAD
    iy = Y0 + SVR_LBL_H + SVR_PAD + row * (INST_H + ROLE_H + INST_GAP)

    c = RS_COLORS[rs]
    bg = c["leader"] if role == "leader" else c["follower"]
    sw = 2 if role == "leader" else 1

    # Instance box
    rect(f"inst{inum}", ix, iy, INST_W, INST_H,
         stroke=c["stroke"], bg=bg, sw=sw, roundness=3)
    text(f"inst{inum}_lbl", ix, iy, INST_W, INST_H,
         f"instance {inum}", size=13, color=c["stroke"])

    # Role label below box
    text(f"inst{inum}_role", ix, iy + INST_H + 1, INST_W, ROLE_H,
         f"RS {rs} {role}", size=11, color=TEXT_COLOR)

    inst_pos[(rs, role)] = (ix, iy, s)

# ── Replication arrows between RS pairs ───────────────
for rs in (1, 2):
    lx, ly, ls = inst_pos[(rs, "leader")]
    fx, fy, fs = inst_pos[(rs, "follower")]
    c = RS_COLORS[rs]
    arrow_y = ly + INST_H / 2

    if ls < fs:
        # Leader on left server → follower on right server
        ax_start = lx + INST_W + 2
        ax_end = fx - 2
    else:
        # Leader on right server → follower on left server
        ax_start = lx - 2
        ax_end = fx + INST_W + 2

    line(f"repl_rs{rs}", ax_start, arrow_y,
         [[0, 0], [ax_end - ax_start, 0]],
         color=c["stroke"], sw=2, ss="dashed", end_arrow="arrow")


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

outpath = "/home/kostja/work/kostja.github.io/assets/img/talks/cluster_assembly.excalidraw"
with open(outpath, "w") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)

print(f"Written {len(elements)} elements to {outpath}")
