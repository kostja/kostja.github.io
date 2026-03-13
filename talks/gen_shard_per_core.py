#!/usr/bin/env python3
"""Generate 'Shard-per-core: a new architecture trend' Excalidraw diagram
with embedded runtime logos."""

import json, base64, hashlib

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


def image(eid, file_id, x, y, w, h):
    elements.append({
        "type": "image", "id": eid,
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": "transparent",
        "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 0, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100,
        "seed": seed(), "version": 1, "versionNonce": seed(),
        "isDeleted": False, "groupIds": [], "frameId": None,
        "boundElements": None, "updated": 1710000000000,
        "link": None, "locked": False, "roundness": None,
        "fileId": file_id,
        "status": "saved", "scale": [1, 1]
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


def load_png(path):
    """Load PNG, return (base64_data, file_id, width, height)."""
    with open(path, "rb") as f:
        data = f.read()
    b64 = base64.standard_b64encode(data).decode("ascii")
    file_id = hashlib.sha1(data).hexdigest()
    from PIL import Image
    import io
    img = Image.open(io.BytesIO(data))
    return b64, file_id, img.width, img.height


# ── Load logos ──────────────────────────────────────────
files = {}
logos = {}
for name, path in [
    ("go", "/tmp/logo_go_final.png"),
    ("tokio", "/tmp/logo_tokio_final.png"),
    ("seastar", "/tmp/logo_seastar_final.png"),
    ("picodata", "/tmp/logo_picodata_final.png"),
]:
    b64, fid, w, h = load_png(path)
    files[fid] = {
        "mimeType": "image/png",
        "id": fid,
        "dataURL": f"data:image/png;base64,{b64}",
        "created": 1710000000000,
        "lastRetrieved": 1710000000000
    }
    logos[name] = {"file_id": fid, "w": w, "h": h}


# ── Layout ──────────────────────────────────────────────
BOX_W = 190
BOX_H = 110  # taller to fit logo
BOX_GAP = 25
X0 = 20
Y0 = 20
TOTAL_W = 4 * BOX_W + 3 * BOX_GAP  # 835

LOGO_DISPLAY_H = 24  # display height for logos in the box

RUNTIMES = [
    {"name": "Go runtime", "lang": "Go", "users": "Kubernetes, Docker",
     "stroke": "#2B1321", "fill": "#E8E9EB", "sw": 2, "logo": "go"},
    {"name": "Tokio", "lang": "Rust", "users": "Cloudflare, Discord",
     "stroke": "#2B1321", "fill": "#E8E9EB", "sw": 2, "logo": "tokio"},
    {"name": "Seastar", "lang": "C++", "users": "ScyllaDB, Redpanda",
     "stroke": "#2B1321", "fill": "#E8E9EB", "sw": 2, "logo": "seastar"},
    {"name": "Picodata", "lang": "Rust", "users": "in-memory distributed DB",
     "stroke": "#E23956", "fill": "#F09CAB", "sw": 3, "logo": "picodata"},
]

# ── Boxes with logos ────────────────────────────────────
for i, rt in enumerate(RUNTIMES):
    bx = X0 + i * (BOX_W + BOX_GAP)

    rect(f"box_{i}", bx, Y0, BOX_W, BOX_H,
         stroke=rt["stroke"], bg=rt["fill"], fill="solid", sw=rt["sw"])

    # Logo centered at top of box
    logo = logos[rt["logo"]]
    scale = LOGO_DISPLAY_H / logo["h"]
    logo_w = logo["w"] * scale
    logo_x = bx + (BOX_W - logo_w) / 2
    logo_y = Y0 + 10
    image(f"logo_{i}", logo["file_id"], logo_x, logo_y,
          logo_w, LOGO_DISPLAY_H)

    # Language below logo
    text(f"lang_{i}", bx, Y0 + 42, BOX_W, 16.8,
         rt["lang"], size=14, color="#2B1321")

    # Notable users
    text(f"users_{i}", bx, Y0 + 64, BOX_W, 16.8,
         rt["users"], size=12, color="#737A82")


# ── Connecting line below boxes ─────────────────────────
LINE_Y = Y0 + BOX_H + 25
line_x1 = X0 + BOX_W / 2
line_x2 = X0 + 3 * (BOX_W + BOX_GAP) + BOX_W / 2
line("banner_line", line_x1, LINE_Y,
     [[0, 0], [line_x2 - line_x1, 0]],
     color="#2B1321", sw=2)

# Small ticks
for i in range(4):
    tx = X0 + i * (BOX_W + BOX_GAP) + BOX_W / 2
    line(f"tick_{i}", tx, LINE_Y - 5,
         [[0, 0], [0, 10]], color="#2B1321", sw=2)

# Banner text
BANNER_Y = LINE_Y + 15
text("banner_text", X0, BANNER_Y, TOTAL_W, 16.8,
     "message-passing, per-core isolation, no shared state",
     size=14, color="#2B1321")


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
    "files": files
}

outpath = "/home/kostja/work/kostja.github.io/assets/img/talks/shard_per_core_trend.excalidraw"
with open(outpath, "w") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)

print(f"Written {len(elements)} elements to {outpath}")
