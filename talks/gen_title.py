#!/usr/bin/env python3
"""Generate title slide: Picodata — Shard-Per-Core In-Memory Database."""

import json, hashlib, base64, io

elements = []
_seed = 1400000


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


def image(eid, file_id, x, y, w, h):
    elements.append({
        "type": "image", "id": eid,
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": "transparent",
        "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 2, "opacity": 100,
        "seed": seed(), "version": 1, "versionNonce": seed(),
        "isDeleted": False, "groupIds": [], "frameId": None,
        "boundElements": None, "updated": 1710000000000,
        "link": None, "locked": False, "roundness": None,
        "fileId": file_id,
        "status": "saved", "scale": [1, 1]
    })


# ── Load Picodata logo ────────────────────────────────
logo_path = "/home/kostja/work/kostja.github.io/assets/img/talks/picodata_logo.png"
with open(logo_path, "rb") as f:
    logo_data = f.read()
logo_b64 = base64.standard_b64encode(logo_data).decode("ascii")
logo_fid = hashlib.sha1(logo_data).hexdigest()

from PIL import Image
img = Image.open(io.BytesIO(logo_data))
logo_orig_w, logo_orig_h = img.width, img.height

files = {
    logo_fid: {
        "mimeType": "image/png",
        "id": logo_fid,
        "dataURL": f"data:image/png;base64,{logo_b64}",
        "created": 1710000000000,
        "lastRetrieved": 1710000000000
    }
}

# ── Layout constants ──────────────────────────────────
X0, Y0 = 20, 20
TOTAL_W = 480

# ── Picodata logo (centered, ~220px wide) ─────────────
LOGO_W = 220
LOGO_H = logo_orig_h * LOGO_W / logo_orig_w
logo_x = X0 + (TOTAL_W - LOGO_W) / 2

image("logo", logo_fid, logo_x, Y0, LOGO_W, LOGO_H)

# ── Title text ────────────────────────────────────────
TITLE_GAP = 30
TITLE_SIZE = 24
LINE_H = int(TITLE_SIZE * 1.2)
title_y = Y0 + LOGO_H + TITLE_GAP

text("title_l1", X0, title_y, TOTAL_W, LINE_H,
     "Shard-Per-Core", size=TITLE_SIZE, color="#E23956")
text("title_l2", X0, title_y + LINE_H + 4, TOTAL_W, LINE_H,
     "In-Memory Database", size=TITLE_SIZE, color="#2B1321")

# ── Decorative tier squares (foreshadow the 4 tiers) ──
SQ_Y = title_y + 2 * LINE_H + 4 + 20
SQ_SIZE = 12;  SQ_GAP = 8
TIER_COLORS = [
    ("#E23956", "#F8CDD6"),   # hot storage
    ("#FF611D", "#FFE0D0"),   # cold storage
    ("#16222E", "#CFD3D6"),   # compute
    ("#737A82", "#E8EAED"),   # arbiter
]
total_sq_w = len(TIER_COLORS) * SQ_SIZE + (len(TIER_COLORS) - 1) * SQ_GAP
sq_x = X0 + (TOTAL_W - total_sq_w) / 2

for i, (stroke, fill) in enumerate(TIER_COLORS):
    rect(f"sq_{i}",
         sq_x + i * (SQ_SIZE + SQ_GAP), SQ_Y, SQ_SIZE, SQ_SIZE,
         stroke=stroke, bg=fill, sw=1, roundness=0)

# ── Speaker name & role ───────────────────────────────
NAME_Y = SQ_Y + SQ_SIZE + 20
text("speaker", X0, NAME_Y, TOTAL_W, 24,
     "Kostja Osipov", size=18, color="#2B1321")
text("role", X0, NAME_Y + 28, TOTAL_W, 18,
     "Co-Founder, Picodata \u00b7 Managing Director R&D, Arenadata",
     size=13, color="#737A82")

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
    "files": files
}

outpath = "/home/kostja/work/kostja.github.io/assets/img/talks/title.excalidraw"
with open(outpath, "w") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)

print(f"Written {len(elements)} elements to {outpath}")
