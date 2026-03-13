#!/usr/bin/env python3
"""Generate Picodata cluster assembly diagram in excalidraw style.

Shows 2 servers, a cluster with 2 replica sets, 4 instances with
replication arrows between active/standby pairs.
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
X0, Y0 = 20, 20
SVR_W = 200
SVR_H = 36
SVR_GAP = 20
CLUSTER_PAD = 16
INST_W = 100
INST_H = 44
RS_PAD_X = 20
RS_PAD_Y = 12
RS_GAP = 20
ARROW_GAP = 20

# Colors
SVR_STROKE = "#737A82"
SVR_FILL = "#E8EAED"
CLUSTER_STROKE = "#2B1321"
RS_STROKE = "#E23956"
RS_FILL = "#F8CDD6"
INST_STROKE = "#E23956"
INST_FILL_ACTIVE = "#F09CAB"
INST_FILL_STANDBY = "#FDECEF"
LABEL_COLOR = "#E23956"
TEXT_COLOR = "#2B1321"
HINT_COLOR = "#737A82"

# ── Derived positions ─────────────────────────────────
# RS interior: 2 instances side by side with arrow between
rs_inner_w = 2 * INST_W + ARROW_GAP + 2 * RS_PAD_X
rs_inner_h = INST_H + 2 * RS_PAD_Y + 28  # +28 for label row + role labels
RS_W = rs_inner_w
RS_H = rs_inner_h

# Cluster interior: 2 RS stacked + label
cluster_inner_w = RS_W + 2 * CLUSTER_PAD
cluster_inner_h = 2 * RS_H + RS_GAP + 2 * CLUSTER_PAD + 24  # +24 for "Cluster" label

CLUSTER_W = cluster_inner_w
CLUSTER_H = cluster_inner_h

# Servers span the same width as cluster
total_w = CLUSTER_W

# ── Server boxes ──────────────────────────────────────
svr1_x = X0
svr2_x = X0 + total_w / 2
svr_y = Y0

rect("svr1", svr1_x, svr_y, total_w / 2, SVR_H,
     stroke=SVR_STROKE, bg=SVR_FILL, sw=2)
text("svr1_lbl", svr1_x, svr_y, total_w / 2, SVR_H,
     "server 1", size=14, color=SVR_STROKE)

rect("svr2", svr2_x, svr_y, total_w / 2, SVR_H,
     stroke=SVR_STROKE, bg=SVR_FILL, sw=2)
text("svr2_lbl", svr2_x, svr_y, total_w / 2, SVR_H,
     "server 2", size=14, color=SVR_STROKE)

# ── Cluster box (dashed) ─────────────────────────────
cluster_x = X0
cluster_y = svr_y + SVR_H + 10
rect("cluster", cluster_x, cluster_y, CLUSTER_W, CLUSTER_H,
     stroke=CLUSTER_STROKE, bg="transparent", sw=2, ss="dashed")
text("cluster_lbl", cluster_x, cluster_y + 4, CLUSTER_W, 20,
     "Cluster", size=16, color=TEXT_COLOR)

# ── Replica sets ──────────────────────────────────────
def draw_rs(idx, rs_x, rs_y, inst1_name, inst2_name):
    # RS box
    rect(f"rs{idx}", rs_x, rs_y, RS_W, RS_H,
         stroke=RS_STROKE, bg=RS_FILL, sw=1)
    text(f"rs{idx}_lbl", rs_x, rs_y + 2, RS_W, 18,
         f"replica set {idx}", size=13, color=LABEL_COLOR)

    # Instance boxes
    inst1_x = rs_x + RS_PAD_X
    inst2_x = rs_x + RS_PAD_X + INST_W + ARROW_GAP
    inst_y = rs_y + 24

    # Active instance (server 1 side)
    rect(f"inst{idx}_1", inst1_x, inst_y, INST_W, INST_H,
         stroke=INST_STROKE, bg=INST_FILL_ACTIVE, sw=1, roundness=3)
    text(f"inst{idx}_1_lbl", inst1_x, inst_y, INST_W, INST_H,
         inst1_name, size=13, color=LABEL_COLOR)
    text(f"inst{idx}_1_role", inst1_x, inst_y + INST_H + 2, INST_W, 16,
         "active", size=11, color=TEXT_COLOR)

    # Standby instance (server 2 side)
    rect(f"inst{idx}_2", inst2_x, inst_y, INST_W, INST_H,
         stroke=INST_STROKE, bg=INST_FILL_STANDBY, sw=1, roundness=3)
    text(f"inst{idx}_2_lbl", inst2_x, inst_y, INST_W, INST_H,
         inst2_name, size=13, color=LABEL_COLOR)
    text(f"inst{idx}_2_role", inst2_x, inst_y + INST_H + 2, INST_W, 16,
         "standby", size=11, color=TEXT_COLOR)

    # Replication arrow
    arrow_y = inst_y + INST_H / 2
    arrow_x1 = inst1_x + INST_W
    arrow_x2 = inst2_x
    line(f"repl{idx}", arrow_x1 + 2, arrow_y,
         [[0, 0], [arrow_x2 - arrow_x1 - 4, 0]],
         color=RS_STROKE, sw=2, ss="dashed", end_arrow="arrow")

    # "replication" label above arrow
    text(f"repl{idx}_lbl",
         arrow_x1, inst_y - 2, arrow_x2 - arrow_x1, 16,
         "replication", size=10, color=HINT_COLOR)

rs1_x = cluster_x + CLUSTER_PAD
rs1_y = cluster_y + 28
draw_rs(1, rs1_x, rs1_y, "instance 1", "instance 3")

rs2_x = rs1_x
rs2_y = rs1_y + RS_H + RS_GAP
draw_rs(2, rs2_x, rs2_y, "instance 2", "instance 4")

# ── Dashed vertical lines from servers to cluster ─────
# Server 1 center → cluster left half
svr1_cx = svr1_x + total_w / 4
line("sconn1", svr1_cx, svr_y + SVR_H,
     [[0, 0], [0, cluster_y - svr_y - SVR_H]],
     color=SVR_STROKE, sw=1, ss="dashed")

# Server 2 center → cluster right half
svr2_cx = svr2_x + total_w / 4
line("sconn2", svr2_cx, svr_y + SVR_H,
     [[0, 0], [0, cluster_y - svr_y - SVR_H]],
     color=SVR_STROKE, sw=1, ss="dashed")

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
