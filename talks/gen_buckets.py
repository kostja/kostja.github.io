#!/usr/bin/env python3
"""Generate Picodata buckets diagram — unit of data distribution.

Shows:
- 3 replica sets as columns (no container boxes — 1 RS = 1 column)
- Each RS has Leader and Follower (alternating positions for failure domains)
- Both hold the SAME 4 buckets (2×2 grid) — replication visible
- Bucket 2044 in flight from RS 1 → RS 3
- Bucket 2877 in flight from RS 2 → RS 3
- Cross-hatched at source, dashed ghost at destination
- Transfer arrows routed around the outside of the diagram
"""

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
         end_arrow=None, roughness=2):
    elements.append({
        "type": "line", "id": eid,
        "x": x, "y": y,
        "width": max(abs(p[0]) for p in points),
        "height": max(abs(p[1]) for p in points) if any(p[1] for p in points) else 0,
        "angle": 0, "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": sw, "strokeStyle": ss,
        "roughness": roughness, "opacity": 100,
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


def arrow(eid, x, y, points, color="#1e1e1e", sw=2, ss="solid", roughness=1):
    """Arrow element — rendered with arrowhead by excalidraw-to-svg."""
    elements.append({
        "type": "arrow", "id": eid,
        "x": x, "y": y,
        "width": max(abs(p[0]) for p in points),
        "height": max(abs(p[1]) for p in points) if any(p[1] for p in points) else 0,
        "angle": 0, "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": sw, "strokeStyle": ss,
        "roughness": roughness, "opacity": 100,
        "seed": seed(), "version": 1, "versionNonce": seed(),
        "isDeleted": False, "groupIds": [], "frameId": None,
        "boundElements": None, "updated": 1710000000000,
        "link": None, "locked": False,
        "roundness": {"type": 2},
        "points": points,
        "lastCommittedPoint": None,
        "startBinding": None, "endBinding": None,
        "startArrowhead": None, "endArrowhead": "arrow"
    })


# ── Layout ───────────────────────────────────────────
B = 44                    # bucket square side
BGAP = 8                 # gap between buckets
COLS, ROWS = 2, 2

IPAD = 14                # instance internal padding
ILBL = 28                # instance label area height (room for label text)
IGAP = 8                 # gap between label and bucket grid
GRID_W = COLS * B + (COLS - 1) * BGAP    # 96
GRID_H = ROWS * B + (ROWS - 1) * BGAP    # 96
IW = GRID_W + 2 * IPAD                    # 124
IH = ILBL + IGAP + GRID_H + IPAD          # 146

RGAP_REPL = 24           # vertical gap for replication arrow
COL_GAP = 48             # horizontal gap between columns
RS_LBL_H = 28            # RS label height above instances

X0, Y0 = 20, 20

# ── Colors ───────────────────────────────────────────
L_STROKE = "#B91A36";   L_FILL = "#F8CDD6"    # leader
F_STROKE = "#737A82";   F_FILL = "#E8E9EB"    # follower
L3_STROKE = "#2E7D32";  L3_FILL = "#C8E6C9"   # RS3 leader (green)
F3_STROKE = "#66BB6A";  F3_FILL = "#E8F5E9"   # RS3 follower (green)

BK_STROKE = "#B91A36";  BK_FILL = "#F09CAB"   # normal bucket (leader)
BR_STROKE = "#9E9E9E";  BR_FILL = "#CFD3D6"   # replicated bucket (follower)
LV_STROKE = "#E65100";  LV_FILL = "#FFE0B2"   # leaving bucket (cross-hatch)
GH_STROKE = "#43A047"                           # ghost bucket (dashed)

FL_STROKE = "#E65100"                           # transfer arrow color

REPL_C = "#4B7BE5"                              # replication arrow

LBL_C = "#E23956"
LBL3_C = "#2E7D32"
ANNO_C = "#2B1321"

# ── Data ─────────────────────────────────────────────
MOVING1 = 2044  # RS 1 → RS 3
MOVING2 = 2877  # RS 2 → RS 3

rs_data = [
    {"label": "RS 1",  "buckets": [1, 47, MOVING1, 203],
     "moving_idx": [2], "ghost_idx": [], "leader_top": True,
     "lbl_c": LBL_C,
     "l_stroke": L_STROKE, "l_fill": L_FILL,
     "f_stroke": F_STROKE, "f_fill": F_FILL},
    {"label": "RS 2",  "buckets": [742, 1055, 1650, MOVING2],
     "moving_idx": [3], "ghost_idx": [], "leader_top": False,
     "lbl_c": LBL_C,
     "l_stroke": L_STROKE, "l_fill": L_FILL,
     "f_stroke": F_STROKE, "f_fill": F_FILL},
    {"label": "RS 3",  "buckets": [None, None, MOVING1, MOVING2],
     "moving_idx": [], "ghost_idx": [2, 3], "leader_top": True,
     "lbl_c": LBL3_C,
     "l_stroke": L3_STROKE, "l_fill": L3_FILL,
     "f_stroke": F3_STROKE, "f_fill": F3_FILL},
]


def bucket_pos(bx0, by0, idx):
    col = idx % COLS
    row = idx // COLS
    return bx0 + col * (B + BGAP), by0 + row * (B + BGAP)


def draw_bucket(prefix, bx, by, num, bstroke, bfill,
                bss="solid", bfillstyle="solid", bopacity=100):
    rect(f"{prefix}", bx, by, B, B,
         stroke=bstroke, bg=bfill, fill=bfillstyle,
         sw=1, ss=bss, roundness=3, opacity=bopacity)
    text(f"{prefix}_t", bx, by, B, B,
         str(num), size=13, color=bstroke)


def draw_instance(prefix, ix, iy, label, lbl_c, istroke, ifill,
                  buckets, moving_idx, ghost_idx, is_follower):
    rect(f"{prefix}", ix, iy, IW, IH,
         stroke=istroke, bg=ifill, sw=1, roundness=3)
    # Label — positioned well inside the box (14px from top, 20px height)
    text(f"{prefix}_lbl", ix + IPAD, iy + 14, IW - 2 * IPAD, 20,
         label, size=13, color=lbl_c)

    bx0 = ix + IPAD
    by0 = iy + ILBL + IGAP

    for j, bnum in enumerate(buckets):
        bx, by = bucket_pos(bx0, by0, j)
        if bnum is None:
            continue
        if j in ghost_idx:
            draw_bucket(f"{prefix}_g{j}", bx, by, bnum,
                        GH_STROKE, "transparent", bss="dashed")
        elif j in moving_idx:
            op = 60 if is_follower else 100
            draw_bucket(f"{prefix}_m{j}", bx, by, bnum,
                        LV_STROKE, LV_FILL, bfillstyle="cross-hatch",
                        bopacity=op)
        else:
            if is_follower:
                draw_bucket(f"{prefix}_b{j}", bx, by, bnum,
                            BR_STROKE, BR_FILL)
            else:
                draw_bucket(f"{prefix}_b{j}", bx, by, bnum,
                            BK_STROKE, BK_FILL)


# ── Draw columns (no RS container boxes) ────────────
col_xs = []
top_y = Y0 + RS_LBL_H
bot_y = top_y + IH + RGAP_REPL

for i, rs in enumerate(rs_data):
    col_x = X0 + i * (IW + COL_GAP)
    col_xs.append(col_x)

    # RS label above the column
    text(f"rs{i}_lbl", col_x, Y0, IW, RS_LBL_H,
         rs["label"], size=16, color=rs["lbl_c"])

    moving_idx = rs.get("moving_idx", [])
    ghost_idx = rs.get("ghost_idx", [])
    leader_top = rs.get("leader_top", True)

    if leader_top:
        ly, fy = top_y, bot_y
    else:
        fy, ly = top_y, bot_y

    # Leader
    draw_instance(f"rs{i}L", col_x, ly,
                  "★ Leader", rs["l_stroke"],
                  rs["l_stroke"], rs["l_fill"],
                  rs["buckets"], moving_idx, ghost_idx,
                  is_follower=False)

    # Replication arrow (Leader → Follower)
    ax = col_x + IW / 2
    gap_top = top_y + IH + 2
    gap_h = RGAP_REPL - 4
    if leader_top:
        line(f"rs{i}_ra", ax, gap_top, [[0, 0], [0, gap_h]],
             color=REPL_C, sw=1.5, end_arrow="arrow")
    else:
        line(f"rs{i}_ra", ax, gap_top + gap_h, [[0, 0], [0, -gap_h]],
             color=REPL_C, sw=1.5, end_arrow="arrow")
    text(f"rs{i}_rt", ax + 6, gap_top, 50, gap_h,
         "repl.", size=9, color=REPL_C, align="left")

    # Follower
    draw_instance(f"rs{i}F", col_x, fy,
                  "Follower", rs["f_stroke"],
                  rs["f_stroke"], rs["f_fill"],
                  rs["buckets"], moving_idx, ghost_idx,
                  is_follower=True)


# ── Transfer arrows (straight from source to destination) ─
total_h = RS_LBL_H + IH + RGAP_REPL + IH
total_w = col_xs[2] + IW - X0

# Helper: right/left center of a bucket
def bkt_right(col_idx, inst_y, bkt_idx):
    bx0 = col_xs[col_idx] + IPAD
    by0 = inst_y + ILBL + IGAP
    col = bkt_idx % COLS
    row = bkt_idx // COLS
    return bx0 + col * (B + BGAP) + B, by0 + row * (B + BGAP) + B / 2

def bkt_left(col_idx, inst_y, bkt_idx):
    bx0 = col_xs[col_idx] + IPAD
    by0 = inst_y + ILBL + IGAP
    col = bkt_idx % COLS
    row = bkt_idx // COLS
    return bx0 + col * (B + BGAP), by0 + row * (B + BGAP) + B / 2

# Arrow 1: RS1 Leader (top) bucket 2044 → RS3 Leader (top) ghost 2044 (idx 2)
# Straight horizontal (both leaders at top, same y level)
sx1, sy1 = bkt_right(0, top_y, 2)
dx1, dy1 = bkt_left(2, top_y, 2)
arrow("ta1", sx1, sy1,
      [[0, 0], [dx1 - sx1, dy1 - sy1]],
      color=FL_STROKE, sw=1.5, ss="dashed", roughness=0)

# Arrow 2: RS2 Leader (bottom) bucket 2877 → RS3 Leader (top) ghost 2877 (idx 3)
# Straight diagonal (RS2 leader at bottom, RS3 leader at top)
sx2, sy2 = bkt_right(1, bot_y, 3)
dx2, dy2 = bkt_left(2, top_y, 3)
arrow("ta2", sx2, sy2,
      [[0, 0], [dx2 - sx2, dy2 - sy2]],
      color=FL_STROKE, sw=1.5, ss="dashed", roughness=0)

# Labels below the diagram
lbl_y0 = Y0 + total_h + 10
text("rl", X0, lbl_y0, total_w, 16,
     "rebalancing: leader → leader", size=13, color=ANNO_C)
text("rn", X0, lbl_y0 + 18, total_w, 14,
     "follower receives buckets via replication", size=10, color=REPL_C)

# ── Annotations ──────────────────────────────────────
ay0 = lbl_y0 + 36

for k, t in enumerate([
    "3 000 buckets by default — fixed-size units of rebalancing",
    "rebalancing begins when new RS is fully online (RF satisfied)",
    "drivers cache bucket→shard map → queries routed directly",
]):
    text(f"a{k}", X0, ay0 + k * 22, total_w, 20,
         f"• {t}", size=14, color=ANNO_C, align="left", valign="top")


# ── Write ────────────────────────────────────────────
doc = {
    "type": "excalidraw",
    "version": 2,
    "source": "https://excalidraw.com",
    "elements": elements,
    "appState": {"gridSize": None, "viewBackgroundColor": "transparent"},
    "files": {}
}

outpath = "/home/kostja/work/kostja.github.io/assets/img/talks/buckets.excalidraw"
with open(outpath, "w") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)

print(f"Written {len(elements)} elements to {outpath}")
