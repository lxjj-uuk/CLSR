# -*- coding: utf-8 -*-
"""Lightweight UML drawing helpers built on Pillow (CJK-safe)."""
import math
from PIL import Image, ImageDraw, ImageFont

SIMSONG = r"C:\Windows\Fonts\simsun.ttc"
HEI = r"C:\Windows\Fonts\simhei.ttf"
YAHEI = r"C:\Windows\Fonts\msyh.ttc"
YAHEI_B = r"C:\Windows\Fonts\msyhbd.ttc"

INK = (34, 34, 34)
EDGE = (60, 60, 60)
WHITE = (255, 255, 255)
HILITE = (255, 243, 190)


def font(size, kind="song"):
    path = SIMSONG if kind == "song" else (HEI if kind == "hei" else (YAHEI_B if kind == "yahei_b" else YAHEI))
    return ImageFont.truetype(path, size)


def text_size(draw, s, f):
    box = draw.textbbox((0, 0), s, font=f)
    return box[2] - box[0], box[3] - box[1], box


def draw_text_center(draw, cx, cy, s, f, fill=INK):
    if not s:
        return
    box = draw.textbbox((0, 0), s, font=f)
    w, h = box[2] - box[0], box[3] - box[1]
    draw.text((cx - w / 2 - box[0], cy - h / 2 - box[1]), s, font=f, fill=fill)


def arrow_head(draw, p_from, p_to, color=EDGE, size=17, half=6.5):
    ang = math.atan2(p_to[1] - p_from[1], p_to[0] - p_from[0])
    bx = p_to[0] - size * math.cos(ang)
    by = p_to[1] - size * math.sin(ang)
    left = (bx + half * math.sin(ang), by - half * math.cos(ang))
    right = (bx - half * math.sin(ang), by + half * math.cos(ang))
    draw.polygon([tuple(map(int, p_to)), left, right], fill=color)


def polyline(draw, pts, color=EDGE, width=2.6, dashed=False, head=True, dash=(12, 9), head_size=17):
    pts = [tuple(map(float, p)) for p in pts]
    w = int(round(width))
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i + 1]
        if dashed:
            total = math.hypot(x2 - x1, y2 - y1)
            if total == 0:
                continue
            dx, dy = (x2 - x1) / total, (y2 - y1) / total
            pos = 0.0
            on = True
            while pos < total:
                seg = dash[0] if on else dash[1]
                seg = min(seg, total - pos)
                if on:
                    draw.line([(x1 + dx * pos, y1 + dy * pos),
                               (x1 + dx * (pos + seg), y1 + dy * (pos + seg))],
                              fill=color, width=w)
                pos += seg
                on = not on
        else:
            draw.line([(x1, y1), (x2, y2)], fill=color, width=w)
    if head:
        arrow_head(draw, pts[-2], pts[-1], color=color, size=head_size)


def draw_actor(draw, cx, cy, label, f, h=150, color=EDGE):
    """Stick figure centred at (cx, cy); label placed below."""
    top = cy - h / 2
    r = h * 0.13
    head_cy = top + r
    draw.ellipse([int(cx - r), int(head_cy - r), int(cx + r), int(head_cy + r)],
                 outline=color, width=3, fill=WHITE)
    body_top = head_cy + r
    body_bot = top + h * 0.62
    draw.line([(cx, body_top), (cx, body_bot)], fill=color, width=3)
    arm_y = body_top + (body_bot - body_top) * 0.28
    draw.line([(cx - h * 0.20, arm_y), (cx + h * 0.20, arm_y)], fill=color, width=3)
    draw.line([(cx, body_bot), (cx - h * 0.17, top + h)], fill=color, width=3)
    draw.line([(cx, body_bot), (cx + h * 0.17, top + h)], fill=color, width=3)
    lines = label.split("\n")
    yy = top + h + f.size * 0.62
    for ln in lines:
        draw_text_center(draw, cx, yy, ln, f)
        yy += f.size * 1.2


def draw_usecase(draw, cx, cy, w, h, label, f, fill=WHITE, max_chars=None):
    draw.ellipse([int(cx - w / 2), int(cy - h / 2), int(cx + w / 2), int(cy + h / 2)],
                 outline=EDGE, width=3, fill=fill)
    if max_chars and len(label) > max_chars:
        mid = len(label) // 2
        draw_text_center(draw, cx, cy - f.size * 0.62, label[:mid], f)
        draw_text_center(draw, cx, cy + f.size * 0.62, label[mid:], f)
    else:
        draw_text_center(draw, cx, cy, label, f)


def new_canvas(w, h):
    img = Image.new("RGB", (w, h), WHITE)
    return img, ImageDraw.Draw(img)
