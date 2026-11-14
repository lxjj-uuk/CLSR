# -*- coding: utf-8 -*-
"""图 3.6 用户界面状态图"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flow_lib import Canvas, font, WHITE, HILITE, draw_text_center

W, H = 1740, 1460
cv = Canvas(W, H)
f_node = font(31, "song")
f_lab = font(25, "song")
f_title = font(34, "hei")
d = cv.d


def txt(cx, cy, s, f, pad=7):
    draw_text_center(d, cx, cy, s, f)


draw_text_center(d, W / 2, 42, "本人负责功能的界面状态图", f_title)

XM, XD = 560, 1330
start = cv.start(XM, 105)
login = cv.box(XM, 220, 320, 84, "登录界面", f_node)
select = cv.box(XM, 450, 340, 98, "选座预约界面\n（座位图已加载）", f_node, fill=HILITE)
d1 = cv.box(XD, 440, 300, 88, "预约确认对话框", f_node)
myres = cv.box(XM, 800, 340, 98, "我的预约界面\n（预约记录列表）", f_node, fill=HILITE)
d2 = cv.box(XD, 650, 330, 96, "签到 / 签退\n确认对话框", f_node)
d4 = cv.box(XD, 960, 300, 88, "取消预约对话框", f_node)
notices = cv.box(XM, 1080, 340, 92, "馆内公告界面\n（公告列表）", f_node)
detail = cv.box(XM, 1275, 320, 84, "公告详情界面", f_node)

# 主流程
cv.arrow([(start.cx, start.cy + 25), (login.cx, login.cy - 43)], None, f_lab)
cv.v_arrow(login, select, "登录成功 / 写入令牌并跳转", f_lab, lpos=(XM + 190, 335))
cv.v_arrow(select, myres, "点击“我的预约”", f_lab, lpos=(XM + 175, 655))
cv.v_arrow(myres, notices, "点击“馆内公告”", f_lab, lpos=(XM + 175, 945))
cv.v_arrow(notices, detail, "点击公告标题", f_lab, lpos=(XM + 160, 1190))
cv.arrow([(detail.cx - 160, detail.cy - 43), (detail.cx - 160, notices.cy + 47)], "返回", f_lab,
         lpos=(XM - 250, 1190))

# 登录自环
cv.arrow([(login.cx + 160, login.cy - 20), (login.cx + 218, login.cy - 20),
          (login.cx + 218, login.cy - 56), (login.cx + 162, login.cy - 56)], None, f_lab)
d.text((login.cx + 236, login.cy - 56), "账号或密码错误", font=f_lab, fill=(34, 34, 34))

# 选座 <-> 预约确认
cv.arrow([(select.right[0] + 8, select.cy), (d1.left[0] - 8, d1.cy)], None, f_lab, both=True)
txt((select.right[0] + d1.left[0]) / 2, select.cy - 52, "点击可选座位", f_lab)
txt((select.right[0] + d1.left[0]) / 2, select.cy + 92, "取消 / 确认预约（提示结果并刷新座位图）", f_lab)

# 我的预约 <-> 签到/签退
cv.arrow([(myres.right[0] + 8, myres.cy - 20), (d2.left[0] - 8, d2.cy + 18)], None, f_lab, both=True)
txt((myres.right[0] + d2.left[0]) / 2 - 25, myres.cy - 145, "点击“签到”或“签退”", f_lab)
txt((myres.right[0] + d2.left[0]) / 2 + 45, myres.cy - 72, "取消 / 确定（状态更新为已签到或已完成）", f_lab)

# 我的预约 <-> 取消预约
cv.arrow([(myres.right[0] + 8, myres.cy + 20), (d4.left[0] - 8, d4.cy - 18)], None, f_lab, both=True)
txt((myres.right[0] + d4.left[0]) / 2 + 10, myres.cy + 72, "点击“取消”", f_lab)
txt((myres.right[0] + d4.left[0]) / 2 + 60, myres.cy + 132, "再想想 / 确定取消", f_lab)

# 退出登录：我的预约 -> 登录界面
cv.arrow([(myres.left[0] - 6, myres.cy + 20), (myres.left[0] - 130, myres.cy + 20),
          (myres.left[0] - 130, login.cy + 8), (login.left[0] - 6, login.cy + 8)],
         "退出登录 / 清除令牌", f_lab, lpos=(myres.left[0] - 268, myres.cy - 250))

cv.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fig3_6_state_pillow.png"))

