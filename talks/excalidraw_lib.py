"""Excalidraw primitives shared by gen_*_compaction.py talk diagrams."""

import json


class Doc:
    def __init__(self, seed_base=800000):
        self.elements = []
        self._seed = seed_base

    def seed(self):
        self._seed += 1
        return self._seed

    def rect(self, eid, x, y, w, h, stroke="#1e1e1e", bg="transparent",
             fill="solid", sw=2, ss="solid", opacity=100, roundness=3):
        self.elements.append({
            "type": "rectangle", "id": eid,
            "x": x, "y": y, "width": w, "height": h,
            "angle": 0, "strokeColor": stroke, "backgroundColor": bg,
            "fillStyle": fill, "strokeWidth": sw, "strokeStyle": ss,
            "roughness": 2, "opacity": opacity,
            "seed": self.seed(), "version": 1, "versionNonce": self.seed(),
            "isDeleted": False, "groupIds": [], "frameId": None,
            "boundElements": None, "updated": 1710000000000,
            "link": None, "locked": False,
            "roundness": {"type": roundness} if roundness else None
        })

    def text(self, eid, x, y, w, h, txt, size=14, color="#1e1e1e",
             family=3, align="center", valign="middle"):
        self.elements.append({
            "type": "text", "id": eid,
            "x": x, "y": y, "width": w, "height": h,
            "angle": 0, "strokeColor": color, "backgroundColor": "transparent",
            "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
            "roughness": 2, "opacity": 100,
            "seed": self.seed(), "version": 1, "versionNonce": self.seed(),
            "isDeleted": False, "groupIds": [], "frameId": None,
            "boundElements": None, "updated": 1710000000000,
            "link": None, "locked": False, "roundness": None,
            "text": txt, "fontSize": size, "fontFamily": family,
            "textAlign": align, "verticalAlign": valign,
            "containerId": None, "originalText": txt, "lineHeight": 1.2
        })

    def line(self, eid, x, y, points, color="#1e1e1e", sw=2, ss="solid",
             end_arrow=None, roughness=2):
        self.elements.append({
            "type": "line", "id": eid,
            "x": x, "y": y,
            "width": max(abs(p[0]) for p in points) or 1,
            "height": max(abs(p[1]) for p in points) or 1,
            "angle": 0, "strokeColor": color, "backgroundColor": "transparent",
            "fillStyle": "solid", "strokeWidth": sw, "strokeStyle": ss,
            "roughness": roughness, "opacity": 100,
            "seed": self.seed(), "version": 1, "versionNonce": self.seed(),
            "isDeleted": False, "groupIds": [], "frameId": None,
            "boundElements": None, "updated": 1710000000000,
            "link": None, "locked": False,
            "roundness": {"type": 2},
            "points": points,
            "lastCommittedPoint": None,
            "startBinding": None, "endBinding": None,
            "startArrowhead": None, "endArrowhead": end_arrow
        })

    def arrow(self, eid, x, y, points, color="#1e1e1e", sw=2, ss="solid", roughness=1):
        self.elements.append({
            "type": "arrow", "id": eid,
            "x": x, "y": y,
            "width": max(abs(p[0]) for p in points) or 1,
            "height": max(abs(p[1]) for p in points) or 1,
            "angle": 0, "strokeColor": color, "backgroundColor": "transparent",
            "fillStyle": "solid", "strokeWidth": sw, "strokeStyle": ss,
            "roughness": roughness, "opacity": 100,
            "seed": self.seed(), "version": 1, "versionNonce": self.seed(),
            "isDeleted": False, "groupIds": [], "frameId": None,
            "boundElements": None, "updated": 1710000000000,
            "link": None, "locked": False,
            "roundness": {"type": 2},
            "points": points,
            "lastCommittedPoint": None,
            "startBinding": None, "endBinding": None,
            "startArrowhead": None, "endArrowhead": "arrow"
        })

    def labeled_rect(self, prefix, x, y, w, h, label, stroke, fill,
                     label_size=13, label_color=None, fill_style="solid",
                     ss="solid", opacity=100):
        self.rect(prefix, x, y, w, h, stroke=stroke, bg=fill,
                  fill=fill_style, sw=1, ss=ss, opacity=opacity)
        self.text(prefix + "_t", x, y, w, h, label, size=label_size,
                  color=label_color or stroke)

    def save(self, outpath):
        doc = {
            "type": "excalidraw",
            "version": 2,
            "source": "https://excalidraw.com",
            "elements": self.elements,
            "appState": {"gridSize": None, "viewBackgroundColor": "transparent"},
            "files": {}
        }
        with open(outpath, "w") as f:
            json.dump(doc, f, indent=2, ensure_ascii=False)
        print(f"Written {len(self.elements)} elements to {outpath}")
