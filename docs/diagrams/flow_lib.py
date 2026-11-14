# -*- coding: utf-8 -*-
"""Minimal flowchart/state/activity diagram engine on Pillow (CJK safe, explicit layout)."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from uml_lib import (Image, ImageDraw, ImageFont, font, draw_text_center, arrow_head,
                     polyline, EDGE, INK, WHITE, HILITE)

GAP = 6


class Node:
    def __init__(self, cx, cy, w, h, kind):
        self.cx, self.cy, self.w, self.h, self.kind = cx, cy, w, h, kind

    @property
    def top(self):
        return (self.cx, self.cy - self.h / 2)

    @property
    def bottom(self):
        return (self.cx, self.cy + self.h / 2)

    @property
    def left(self):
        return (self.cx - self.w / 2, self.cy)

    @property
    def right(self):
        return (self.cx + self.w / 2, self.cy)


class Canvas:
    def __init__(self, w, h):
        self.img = Image.new("RGB", (w, h), WHITE)
        self.d = ImageDraw.Draw(self.img)
        self.w, self.h = w, h

    # ---------- primitives ----------
    def lane(self, x0, x1, title, f, top=20, bottom=None):
        bottom = bottom or self.h - 20
        self.d.rectangle([x0, top, x1, bottom], outline=(70, 84, 96), width=3)
        self.d.rectangle([x0, top, x1, top + 70], outline=(70, 84, 96), width=3, fill=(240, 244, 249))
        draw_text_center(self.d, (x0 + x1) / 2, top + 35, title, f)

    def box(self, cx, cy, w, h, text, f, fill=WHITE, rounded=True, lw=3, line_h=1.35):
        n = Node(cx, cy, w, h, "box")
        box = [int(cx - w / 2), int(cy - h / 2), int(cx + w / 2), int(cy + h / 2)]
        if rounded:
            self.d.rounded_rectangle(box, radius=12, outline=EDGE, width=lw, fill=fill)
        else:
            self.d.rectangle(box, outline=EDGE, width=lw, fill=fill)
        self._multiline(cx, cy, text, f, line_h)
        return n

    def diamond(self, cx, cy, w, h, text, f, fill=WHITE, line_h=1.3):
        n = Node(cx, cy, w, h, "diamond")
        pts = [(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)]
        self.d.polygon(pts, outline=EDGE, fill=fill)
        self.d.line(pts + [pts[0]], fill=EDGE, width=3)
        self._multiline(cx, cy, text, f, line_h)
        return n

    def start(self, cx, cy, r=18):
        self.d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(40, 40, 40))
        return Node(cx, cy, r * 2, r * 2, "start")

    def end(self, cx, cy, r=22):
        self.d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(40, 40, 40), width=3, fill=WHITE)
        self.d.ellipse([cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8], fill=(40, 40, 40))
        return Node(cx, cy, r * 2, r * 2, "end")

    def _multiline(self, cx, cy, text, f, line_h=1.35):
        lines = text.split("\n")
        total = len(lines) * f.size * line_h
        y = cy - total / 2 + f.size * line_h / 2
        for ln in lines:
            draw_text_center(self.d, cx, y, ln, f)
            y += f.size * line_h

    # ---------- edges ----------
    def arrow(self, pts, label=None, f=None, dashed=False, lpos=None, lpad=6,
              head=True, width=2.8, head_size=16, both=False):
        polyline(self.d, pts, dashed=dashed, width=width, head=head, head_size=head_size)
        if both:
            arrow_head(self.d, pts[1], pts[0], size=head_size)
        if label and f:
            if lpos is None:
                # midpoint of the longest segment
                best, bi = -1, 0
                for i in range(len(pts) - 1):
                    ln = math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
                    if ln > best:
                        best, bi = ln, i
                p1, p2 = pts[bi], pts[bi + 1]
                lpos = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
            box = self.d.textbbox((0, 0), label, font=f)
            tw, th = box[2] - box[0], box[3] - box[1]
            x = lpos[0] - tw / 2 - lpad
            y = lpos[1] - th / 2 - lpad / 2
            self.d.rectangle([x, y, x + tw + 2 * lpad, y + th + lpad], fill=WHITE)
            self.d.text((lpos[0] - tw / 2 - box[0], lpos[1] - th / 2 - box[1]), label, font=f, fill=INK)

    def v_arrow(self, a, b, label=None, f=None, lpos=None, dashed=False):
        """node a bottom -> node b top (vertical if same column, elbow otherwise)"""
        if abs(a.cx - b.cx) < 2:
            self.arrow([(a.cx, a.cy + a.h / 2 + GAP), (b.cx, b.cy - b.h / 2 - GAP)], label, f,
                       dashed=dashed, lpos=lpos)
        else:
            mid = (a.cy + a.h / 2 + b.cy - b.h / 2) / 2
            self.arrow([(a.cx, a.cy + a.h / 2 + GAP), (a.cx, mid), (b.cx, mid), (b.cx, b.cy - b.h / 2 - GAP)],
                       label, f, dashed=dashed, lpos=lpos)

    def h_arrow(self, a, b, label=None, f=None, dashed=False, lpos=None):
        """a right -> b left or a left -> b right"""
        if b.cx > a.cx:
            self.arrow([(a.cx + a.w / 2 + GAP, a.cy), (b.cx - b.w / 2 - GAP, b.cy)], label, f,
                       dashed=dashed, lpos=lpos)
        else:
            self.arrow([(a.cx - a.w / 2 - GAP, a.cy), (b.cx + b.w / 2 + GAP, b.cy)], label, f,
                       dashed=dashed, lpos=lpos)

    def save(self, path):
        self.img.save(path, "PNG")
        print("saved", path, self.img.size)

