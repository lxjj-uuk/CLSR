# -*- coding: utf-8 -*-
"""图 2.2 系统用例图（手工排版，比例适合 A4 正文）"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from uml_lib import *

W, H = 2500, 1680
img, d = new_canvas(W, H)
f_uc = font(46, "song")
f_actor = font(40, "song")
f_title = font(50, "hei")
f_note = font(33, "song")
f_inc = font(30, "song")


def txt_bg(cx, cy, s, f, fill=INK, pad=8):
    box = d.textbbox((0, 0), s, font=f)
    w, h = box[2] - box[0], box[3] - box[1]
    d.rectangle([cx - w / 2 - pad, cy - h / 2 - pad * 0.5,
                 cx + w / 2 + pad, cy + h / 2 + pad * 0.5], fill=WHITE)
    d.text((cx - w / 2 - box[0], cy - h / 2 - box[1]), s, font=f, fill=fill)


def txt_rot(cx, cy, s, f):
    box = f.getbbox(s)
    w, h = box[2] - box[0], box[3] - box[1]
    tmp = Image.new("RGB", (w + 10, h + 10), WHITE)
    ImageDraw.Draw(tmp).text((5 - box[0], 5 - box[1]), s, font=f, fill=INK)
    tmp = tmp.rotate(90, expand=True)
    img.paste(tmp, (int(cx - tmp.width / 2), int(cy - tmp.height / 2)))


# 系统边界
BL, BT, BR, BB = 300, 55, 1930, 1560
d.rectangle([BL, BT, BR, BB], outline=(55, 71, 79), width=3)
draw_text_center(d, (BL + BR) / 2, BT + 40, "校园图书馆座位预约系统", f_title)

LH, LW = 116, 500
LX, RX = 800, 1600
ys = [185 + i * 152 for i in range(9)]

left = [("用户登录", False), ("座位查询", True), ("座位预约", True), ("取消预约", True),
        ("座位签到", True), ("座位签退", True), ("查看我的预约", True), ("浏览馆内公告", False)]
right = [("后台登录", False), ("阅览室信息管理", False), ("座位信息维护", False), ("预约记录核验", False),
         ("违约与黑名单管理", False), ("公告发布管理", False), ("用户与权限管理", False),
         ("系统参数配置", False), ("数据备份与日志", False)]


def fan(ax, ay, targets, col_x, sign):
    for i, off in targets:
        polyline(d, [(ax, ay + off), (col_x + sign * (LW / 2 + 4), ys[i])], width=2.4, head_size=16)


ACT_L = (145, 720)
fan(ACT_L[0] + 40, ACT_L[1], [(i, (i - 4) * 7) for i in range(8)], LX, -1)

ACT_R1 = (2140, 420)
fan(ACT_R1[0] - 40, ACT_R1[1], [(i, (i - 2) * 8) for i in range(6)], RX, +1)

ACT_R2 = (2140, 1180)
fan(ACT_R2[0] - 40, ACT_R2[1], [(i, off) for i, off in zip([0, 6, 7, 8], [-18, 6, 18, 30])], RX, +1)


def include(src_y, channel_x):
    polyline(d, [(LX + LW / 2, src_y), (channel_x, src_y), (channel_x, ys[0] + 8),
                 (LX + LW / 2 + 3, ys[0] + 8)], width=2.2, dashed=True, head_size=14, dash=(11, 8))


include(ys[2], LX + LW / 2 + 52)
include(ys[6], LX + LW / 2 + 104)

# 用例椭圆
for i, (label, mine) in enumerate(left):
    draw_usecase(d, LX, ys[i], LW, LH, label, f_uc, fill=HILITE if mine else WHITE)
for i, (label, mine) in enumerate(right):
    draw_usecase(d, RX, ys[i], LW, LH, label, f_uc, fill=HILITE if mine else WHITE)

# «include» 竖排标注
txt_rot(LX + LW / 2 + 60, (ys[0] + ys[2]) / 2 + 40, "«include»", f_inc)
txt_rot(LX + LW / 2 + 148, (ys[0] + ys[6]) / 2 + 55, "«include»", f_inc)

# 参与者
draw_actor(d, ACT_L[0], ACT_L[1], "", f_actor, h=160)
txt_bg(ACT_L[0] + 30, ACT_L[1] + 130, "学生 / 教职工", f_actor)
txt_bg(ACT_L[0] + 30, ACT_L[1] + 182, "（读者）", f_actor)

draw_actor(d, ACT_R1[0], ACT_R1[1], "", f_actor, h=160)
d.text((ACT_R1[0] + 52, ACT_R1[1] - 22), "自习室管理员", font=f_actor, fill=INK)

draw_actor(d, ACT_R2[0], ACT_R2[1], "", f_actor, h=160)
d.text((ACT_R2[0] + 52, ACT_R2[1] - 22), "系统管理员", font=f_actor, fill=INK)

# 图例
lg_x, lg_y = 480, 1505
d.rounded_rectangle([lg_x, lg_y - 22, lg_x + 62, lg_y + 22], radius=5, outline=EDGE, width=2, fill=HILITE)
d.text((lg_x + 82, lg_y - 19), "注：黄色底色的用例为本人负责设计、实现与说明的部分。", font=f_note, fill=INK)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fig2_2_usecase_pillow.png")
img.save(out, "PNG")
print("saved", out, img.size)

