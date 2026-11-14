# -*- coding: utf-8 -*-
"""图 4.1 / 图 4.3 模块交互活动图（泳道，手工排版）"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flow_lib import Canvas, font, WHITE, HILITE, draw_text_center

HERE = os.path.dirname(os.path.abspath(__file__))
f_title = font(34, "hei")
f_node = font(30, "song")
f_lab = font(25, "song")

LANES = [(20, 440, "读者"), (440, 860, "前端页面"), (860, 1280, "后端服务"), (1280, 1700, "数据库")]
CX = [230, 650, 1070, 1490]
BW, BH = 350, 104


def base(title, h):
    cv = Canvas(1720, h)
    draw_text_center(cv.d, 860, 40, title, f_title)
    for (x0, x1, name) in LANES:
        cv.lane(x0, x1, name, f_node, top=75, bottom=h - 25)
    return cv


# ============ 图 4.1 座位查询与预约 ============
cv = base("座位查询与预约模块交互活动图", 2010)

n1 = cv.box(CX[0], 250, BW, BH, "选择阅览室、\n预约日期与时段", f_node)
n2 = cv.box(CX[1], 400, BW, BH, "调用座位查询接口\n/api/seats", f_node)
n3 = cv.box(CX[2], 550, BW, BH, "校验 JWT 令牌并\n组装座位视图 SeatVO", f_node)
n4 = cv.box(CX[3], 700, BW, BH, "查询座位记录及\n该时段有效预约", f_node)
n5 = cv.box(CX[1], 850, BW, BH, "渲染座位分布图\n（可选/已预约/维修）", f_node)
n6 = cv.box(CX[0], 1000, BW, BH, "浏览座位图并\n在确认框中确认预约", f_node)
n7 = cv.box(CX[1], 1150, BW, BH, "提交预约请求\n/api/reserve", f_node)
n8 = cv.diamond(CX[2], 1330, 300, 130, "预约条件\n校验通过？", f_node)
n9 = cv.box(CX[2], 1480, BW, BH, "生成预约单号并\n写入预约记录", f_node)
n10 = cv.box(CX[3], 1630, BW, BH, "新增预约记录\n（状态：已预约）", f_node)
n11 = cv.box(CX[1], 1780, BW, BH, "提示“预约成功”\n并刷新座位图", f_node)
n12 = cv.end(CX[0], 1900)
nf = cv.box(CX[1], 1480, BW, BH, "提示失败原因\n（黑名单/维修/冲突）", f_node)
ne = cv.end(CX[1], 1620)

cv.v_arrow(n1, n2)
cv.v_arrow(n2, n3)
cv.v_arrow(n3, n4)
cv.v_arrow(n4, n5)
cv.v_arrow(n5, n6)
cv.v_arrow(n6, n7)
cv.arrow([(n7.cx, n7.cy + BH / 2 + 6), (n7.cx, 1228), (n8.cx, 1228), (n8.cx, n8.cy - 66)])  # to diamond top
cv.arrow([(n8.left[0] - 4, n8.cy), (nf.cx, n8.cy), (nf.cx, nf.cy - BH / 2 - 6)], "否", f_lab,
         lpos=(nf.cx - 55, n8.cy - 22))
cv.arrow([(n8.cx, n8.cy + 66), (n9.cx, n9.cy - BH / 2 - 6)], "是", f_lab, lpos=(n9.cx + 45, (n8.cy + 66 + n9.cy - 58) / 2))
cv.v_arrow(n9, n10)
cv.v_arrow(n10, n11)
cv.v_arrow(n11, n12)
cv.arrow([(nf.cx, nf.cy + BH / 2 + 6), (ne.cx, ne.cy - 24)], None, f_lab)

cv.save(os.path.join(HERE, "fig4_1_activity_pillow.png"))

# ============ 图 4.3 我的预约（预约记录管理） ============
cv = base("我的预约模块交互活动图", 2010)

m1 = cv.box(CX[0], 250, BW, BH, "进入“我的预约”\n页面", f_node)
m2 = cv.box(CX[1], 400, BW, BH, "调用预约记录接口\n/api/my/reservations", f_node)
m3 = cv.box(CX[2], 550, BW, BH, "校验令牌并查询\n本人预约记录", f_node)
m4 = cv.box(CX[3], 700, BW, BH, "联表查询预约、\n座位、阅览室、时段", f_node)
m5 = cv.box(CX[1], 850, BW, BH, "渲染预约列表\n（按状态显示标签）", f_node)
m6 = cv.box(CX[0], 1000, BW, BH, "选择签到、签退\n或取消预约", f_node)
m7 = cv.box(CX[1], 1150, BW, BH, "弹出确认对话框并\n提交操作请求", f_node)
m8 = cv.diamond(CX[2], 1330, 340, 130, "预约归属与\n状态是否允许？", f_node)
m9 = cv.box(CX[2], 1480, BW, BH, "更新预约状态与\n签到签退时间", f_node)
m10 = cv.box(CX[3], 1630, BW, BH, "更新 reservation\n表 status 字段", f_node)
m11 = cv.box(CX[1], 1780, BW, BH, "提示操作成功并\n刷新预约列表", f_node)
m12 = cv.end(CX[0], 1900)
mf = cv.box(CX[1], 1480, BW, BH, "提示“操作失败”，\n当前状态不支持", f_node)
me = cv.end(CX[1], 1620)

cv.v_arrow(m1, m2)
cv.v_arrow(m2, m3)
cv.v_arrow(m3, m4)
cv.v_arrow(m4, m5)
cv.v_arrow(m5, m6)
cv.v_arrow(m6, m7)
cv.arrow([(m7.cx, m7.cy + BH / 2 + 6), (m7.cx, 1228), (m8.cx, 1228), (m8.cx, m8.cy - 66)])
cv.arrow([(m8.left[0] - 4, m8.cy), (mf.cx, m8.cy), (mf.cx, mf.cy - BH / 2 - 6)], "否", f_lab,
         lpos=(mf.cx - 55, m8.cy - 22))
cv.arrow([(m8.cx, m8.cy + 66), (m9.cx, m9.cy - BH / 2 - 6)], "是", f_lab, lpos=(m9.cx + 45, (m8.cy + 66 + m9.cy - 58) / 2))
cv.v_arrow(m9, m10)
cv.v_arrow(m10, m11)
cv.v_arrow(m11, m12)
cv.arrow([(mf.cx, mf.cy + BH / 2 + 6), (me.cx, me.cy - 24)], None, f_lab)

cv.save(os.path.join(HERE, "fig4_3_activity_pillow.png"))

