#!/usr/bin/env python3
"""Generate PostgreSQL ecosystem logo diagram for slide 9.

Shows logos of tools/frameworks that work with Picodata via PostgreSQL
wire protocol, organized in a hub-and-spoke layout with PostgreSQL
elephant logo at center.
"""

import json, base64, hashlib, os

elements = []
_seed = 1100000


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
LOGO_DIR = "/tmp/pg_logos"

LOGO_FILES = {
    "postgresql": "postgresql.png",
    "dbeaver": "dbeaver.png",
    "datagrip": "datagrip.png",
    "python": "python.png",
    "django": "django.png",
    "sqlalchemy": "sqlalchemy.png",
    "apachespark": "apachespark.png",
    "grafana": "grafana.png",
    "metabase": "metabase.png",
    "gnubash": "gnubash.png",
    "go": "go.png",
    "rust": "rust.png",
    "spring": "spring.png",
    "hibernate": "hibernate.png",
    "picodata": "picodata.png",
}

for name, filename in LOGO_FILES.items():
    path = os.path.join(LOGO_DIR, filename)
    if not os.path.exists(path):
        print(f"WARNING: {path} not found, skipping")
        continue
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
# Grid of tool cards, grouped into rows by category
# Each card has: logo + label below

CARD_W = 90
CARD_H = 70
CARD_GAP_X = 10
CARD_GAP_Y = 10
LOGO_H = 30  # display height for logos
X0, Y0 = 20, 20

# Category colors
PG_STROKE = "#4169E1"   # PostgreSQL blue
PG_FILL = "#DBE6FA"
TOOL_STROKE = "#737A82"
TOOL_FILL = "#E8EAED"
DRIVER_STROKE = "#E23956"
DRIVER_FILL = "#F8CDD6"

# Row definitions: (category_label, stroke, fill, items)
# items: [(logo_key, display_label), ...]
ROWS = [
    ("PostgreSQL ecosystem — works out of the box",
     PG_STROKE, None, [
        ("postgresql", "PostgreSQL"),
        ("gnubash", "psql"),
        ("dbeaver", "DBeaver"),
        ("datagrip", "DataGrip"),
        ("python", "psycopg2"),
        ("sqlalchemy", "SQLAlchemy"),
        ("django", "Django ORM"),
        ("spring", "Spring/JDBC"),
        ("hibernate", "Hibernate"),
        ("apachespark", "Spark"),
        ("grafana", "Grafana"),
        ("metabase", "Metabase"),
    ]),
]

# ── Draw section header + cards ─────────────────────────
y = Y0
for section_label, sec_stroke, sec_fill, items in ROWS:
    # Section header
    total_w = len(items) * (CARD_W + CARD_GAP_X) - CARD_GAP_X
    text(f"sec_hdr", X0, y, total_w, 20,
         section_label, size=14, color=sec_stroke, align="left")
    y += 26

    # Draw cards
    x = X0
    for i, (logo_key, label) in enumerate(items):
        # Card background
        card_stroke = TOOL_STROKE
        card_fill = TOOL_FILL
        # PostgreSQL gets its own color
        if logo_key == "postgresql":
            card_stroke = PG_STROKE
            card_fill = PG_FILL

        rect(f"card_{logo_key}", x, y, CARD_W, CARD_H,
             stroke=card_stroke, bg=card_fill, sw=1, roundness=3,
             roughness=1)

        # Logo centered in card
        if logo_key in logos:
            logo = logos[logo_key]
            scale = LOGO_H / logo["h"]
            logo_w = logo["w"] * scale
            logo_x = x + (CARD_W - logo_w) / 2
            logo_y = y + 6
            image(f"img_{logo_key}", logo["file_id"],
                  logo_x, logo_y, logo_w, LOGO_H)

        # Label below logo
        text(f"lbl_{logo_key}", x, y + LOGO_H + 10, CARD_W, 16,
             label, size=11, color="#2B1321")

        x += CARD_W + CARD_GAP_X

    y += CARD_H + CARD_GAP_Y

# ── Picodata native drivers section ────────────────────
y += 4
native_label = "Picodata-native drivers — shard-aware, topology-aware"
text("native_hdr", X0, y, 600, 20,
     native_label, size=14, color=DRIVER_STROKE, align="left")
y += 26

NATIVE_ITEMS = [
    ("go", "Go"),
    ("rust", "Rust"),
    ("spring", "JDBC"),
]

x = X0
for i, (logo_key, label) in enumerate(NATIVE_ITEMS):
    rect(f"ncard_{logo_key}", x, y, CARD_W, CARD_H,
         stroke=DRIVER_STROKE, bg=DRIVER_FILL, sw=1, roundness=3,
         roughness=1)

    if logo_key in logos:
        logo = logos[logo_key]
        scale = LOGO_H / logo["h"]
        logo_w = logo["w"] * scale
        logo_x = x + (CARD_W - logo_w) / 2
        logo_y = y + 6
        image(f"nimg_{logo_key}", logo["file_id"],
              logo_x, logo_y, logo_w, LOGO_H)

    text(f"nlbl_{logo_key}", x, y + LOGO_H + 10, CARD_W, 16,
         label, size=11, color="#2B1321")

    x += CARD_W + CARD_GAP_X

# Add explanation text next to native drivers
explain_x = x + 10
text("explain", explain_x, y + 5, 400, 16,
     "Cache the bucket→shard map", size=13, color="#737A82", align="left")
text("explain2", explain_x, y + 24, 400, 16,
     "Route queries to the right node", size=13, color="#737A82", align="left")
text("explain3", explain_x, y + 43, 400, 16,
     "Auto-refresh topology on changes", size=13, color="#737A82", align="left")

# ── Bottom tagline ──────────────────────────────────────
y += CARD_H + 20
text("tagline", X0, y, 700, 20,
     "PostgreSQL compatibility = easy migration, instant adoption",
     size=16, color="#E23956", align="left")


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

outpath = "/home/kostja/work/kostja.github.io/assets/img/talks/pg_ecosystem.excalidraw"
with open(outpath, "w") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)

print(f"Written {len(elements)} elements ({len(files)} images) to {outpath}")
