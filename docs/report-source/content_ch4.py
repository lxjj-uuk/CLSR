# -*- coding: utf-8 -*-
"""第 4 章 系统详细设计 的内容填充"""
import copy
from docxlib import Builder
from docx.oxml.ns import qn

FIG = r"E:\CLSR\_work\diagrams"


def _set(tr, idx, text, bold=False):
    tcs = tr.findall(qn('w:tc'))
    if idx < len(tcs):
        Builder._set_tc(tcs[idx], text, bold=bold)


def build_design_table(b, tpl_tbl, d):
    """按模板 9 列结构重建表：类名/所属包/继承/实现/属性/方法/事件"""
    tbl_el = copy.deepcopy(tpl_tbl._tbl)
    trs = tbl_el.findall(qn('w:tr'))
    r_name, r_ext, r_impl = trs[0], trs[1], trs[2]
    attr_hdr, attr_head, attr_tpl = trs[3], trs[4], trs[5]
    meth_hdr, meth_head, meth_tpl = trs[7], trs[8], trs[9]
    evt_hdr, evt_head, evt_tpl = trs[11], trs[12], trs[13]
    for tr in trs:
        tbl_el.remove(tr)
    seq = [r_name, r_ext, r_impl, attr_hdr, attr_head]
    for _ in d["attrs"]:
        seq.append(copy.deepcopy(attr_tpl))
    seq += [meth_hdr, meth_head]
    for _ in d["meths"]:
        seq.append(copy.deepcopy(meth_tpl))
    seq += [evt_hdr, evt_head]
    for _ in d["evts"]:
        seq.append(copy.deepcopy(evt_tpl))
    for tr in seq:
        tbl_el.append(tr)

    _set(r_name, 1, d["cls"])
    _set(r_name, 3, d["pkg"])
    _set(r_ext, 1, d.get("ext", "无"))
    _set(r_impl, 1, d.get("impl", "无"))

    i = 5
    for a in d["attrs"]:
        for j, v in enumerate(a):
            _set(seq[i], j, v)
        i += 1
    i += 2
    for m in d["meths"]:
        for j, v in enumerate(m):
            _set(seq[i], j, v)
        i += 1
    i += 2
    for e in d["evts"]:
        for j, v in enumerate(e):
            _set(seq[i], j, v)
        i += 1
    return tbl_el


SEAT_SERVICE = {
    "cls": "SeatService", "pkg": "com.example.libraryseat.service",
    "ext": "无（普通业务类）", "impl": "无",
    "attrs": [
        ["roomMapper", "ReadingRoomMapper", "—", "Prv（@Autowired 注入）"],
        ["slotMapper", "TimeSlotMapper", "—", "Prv（@Autowired 注入）"],
        ["seatMapper", "SeatMapper", "—", "Prv（@Autowired 注入）"],
        ["reservationMapper", "ReservationMapper", "—", "Prv（@Autowired 注入）"],
    ],
    "meths": [
        ["rooms()", "无", "List<ReadingRoom>", "无", "调用 roomMapper 查询所有状态为开放的阅览室"],
        ["slots()", "无", "List<TimeSlot>", "无", "调用 slotMapper 查询所有启用状态的时段"],
        ["seats(roomId, date, slotId)", "Integer, LocalDate, Integer", "List<SeatVO>", "无", "查询座位列表，逐个统计占用数量并设置 reserved 标记"],
    ],
    "evts": [["无", "无", "无", "本类不定义事件，由 ApiController 的请求驱动"]],
}

RES_SERVICE = {
    "cls": "ReservationService", "pkg": "com.example.libraryseat.service",
    "ext": "无（普通业务类）", "impl": "无",
    "attrs": [
        ["reservationMapper", "ReservationMapper", "—", "Prv（@Autowired 注入）"],
        ["seatMapper", "SeatMapper", "—", "Prv（@Autowired 注入）"],
        ["blacklistMapper", "BlacklistMapper", "—", "Prv（@Autowired 注入）"],
    ],
    "meths": [
        ["reserve(userId, seatId, slotId, date)", "Integer, Integer, Integer, LocalDate", "String", "无（异常回滚事务）", "执行黑名单、座位状态、日期、冲突、重复五重校验并写入预约记录"],
        ["cancel(id, userId)", "Integer, Integer", "String", "无", "将状态为已预约的记录置为已取消并记录取消时间"],
        ["checkIn(id, userId)", "Integer, Integer", "String", "无", "将状态为已预约的记录置为已签到并记录签到时间"],
        ["checkOut(id, userId)", "Integer, Integer", "String", "无", "将状态为已签到的记录置为已完成并记录签退时间"],
        ["generateNo()", "无", "String", "无", "生成 RES + 时间戳 + 3 位随机数的预约单号（私有）"],
    ],
    "evts": [["无", "无", "无", "本类不定义事件，由 ApiController 的请求驱动"]],
}

HOME_VUE = {
    "cls": "Home.vue（选座预约页面）", "pkg": "src/views",
    "ext": "无", "impl": "Vue 3 组合式 API 组件",
    "attrs": [
        ["rooms", "ref([])", "[]", "Prv（组件内状态）"],
        ["slots", "ref([])", "[]", "Prv（组件内状态）"],
        ["seats", "ref([])", "[]", "Prv（组件内状态）"],
        ["roomId / slotId / date", "ref", "null / 当天", "Prv（组件内状态）"],
        ["loading", "ref(false)", "false", "Prv（组件内状态）"],
    ],
    "meths": [
        ["querySeats()", "无", "void", "接口异常", "校验筛选条件后调用 /api/seats 并刷新座位图"],
        ["onSeatClick(seat)", "SeatVO", "void", "用户取消", "弹出确认对话框，确认后调用 /api/reserve"],
        ["seatClass(seat)", "SeatVO", "String", "无", "根据占用与状态返回座位按钮的样式类"],
        ["seatAvailable(seat)", "SeatVO", "Boolean", "无", "判断座位是否可选"],
        ["seatTitle(seat)", "SeatVO", "String", "无", "生成座位悬停提示文本"],
    ],
    "evts": [
        ["点击“查询座位”", "三项筛选条件均已选择", "无", "触发座位查询并渲染座位图"],
        ["点击可选座位", "座位未被预约且状态正常", "SeatVO", "弹出确认框并提交预约请求"],
    ],
}

MY_VUE = {
    "cls": "MyReservations.vue（我的预约页面）", "pkg": "src/views",
    "ext": "无", "impl": "Vue 3 组合式 API 组件",
    "attrs": [
        ["list", "ref([])", "[]", "Prv（组件内状态）"],
        ["loading", "ref(false)", "false", "Prv（组件内状态）"],
        ["statusMap", "Object", "5 种状态映射", "Prv（组件内常量）"],
    ],
    "meths": [
        ["loadList()", "无", "void", "接口异常", "调用 /api/my/reservations 并渲染预约列表"],
        ["onCheckin(row)", "ReservationVO", "void", "用户取消", "二次确认后调用 /api/checkin/{id}"],
        ["onCheckout(row)", "ReservationVO", "void", "用户取消", "二次确认后调用 /api/checkout/{id}"],
        ["onCancel(row)", "ReservationVO", "void", "用户取消", "二次确认后调用 /api/cancel/{id}"],
    ],
    "evts": [
        ["点击“签到”", "记录状态为已预约", "ReservationVO", "弹出确认框，确认后更新为已签到"],
        ["点击“签退”或“取消”", "记录状态为已签到或已预约", "ReservationVO", "弹出确认框，确认后更新状态并刷新列表"],
    ],
}

RES_MAPPER = {
    "cls": "ReservationMapper", "pkg": "com.example.libraryseat.mapper",
    "ext": "无", "impl": "Mapper 接口（MyBatis 代理实现）",
    "attrs": [
        ["无", "—", "—", "接口无实例属性"],
    ],
    "meths": [
        ["countSeatReserved(seatId, date, slotId)", "Integer, LocalDate, Integer", "int", "无", "统计座位在指定日期和时段的有效预约数"],
        ["countUserSlot(userId, date, slotId)", "Integer, LocalDate, Integer", "int", "无", "统计读者在指定日期和时段的预约数，用于防止重复预约"],
        ["findVOByUser(userId)", "Integer", "List<ReservationVO>", "无", "联表查询读者的预约记录（座位号、阅览室、时段名）"],
        ["cancel / checkIn / checkOut(id, userId)", "Integer, Integer", "int", "无", "按 id、user_id 与当前状态更新预约状态与时间戳"],
        ["insert(r)", "Reservation", "int", "无", "新增预约记录并回填主键"],
    ],
    "evts": [["无", "无", "无", "由 Service 层调用驱动"]],
}


def apply(b: Builder):
    # ---------- 4.1 标题 ----------
    b.revise("XX模块详细设计", "座位查询与预约模块详细设计")

    # ---------- 4.1.1 模块职责与功能描述 ----------
    h311 = b.find("模块职责与功能描述")
    empty = h311._p.getnext()
    while empty is not None and empty.tag == qn('w:p') and ''.join(
            t.text or '' for t in empty.findall('.//' + qn('w:t'))).strip() == '':
        break
    b.insert_after(empty, [
        b.p("座位查询与预约模块是学生端的核心模块，负责把阅览室、时段、座位三类静态资源与预约记录这类动态数据组合成可视化的座位分布图，并完成座位预约的全过程校验与写入。模块对外提供 4 个接口：/api/rooms 查询开放的阅览室，/api/slots 查询启用的时段，/api/seats 查询指定阅览室、日期和时段下的座位列表，/api/reserve 提交座位预约。"),
        b.p("模块的主要职责包括：（1）按阅览室、日期、时段三个维度查询座位，并逐个判定座位在该时段的占用状态；（2）把座位实体转换为携带阅览室名称和占用标记的 SeatVO，供前端直接渲染；（3）在预约时完成黑名单、座位状态、日期合法性、座位冲突和用户重复预约五类业务规则校验；（4）生成唯一预约单号，并以事务方式写入预约记录。"),
        b.p("从用户视角看，该模块对应“选座预约”页面：读者先在筛选区选择阅览室、日期和时段，页面下方的座位图以绿色表示可选、灰色表示已预约，并标注带电源的座位；点击可选座位弹出确认对话框，确认后完成预约并刷新座位图。"),
    ])

    # ---------- 4.1.2 模块交互模型 ----------
    b.replace("（该模块分泳道的活动图）", [
        b.p("模块内部的交互过程如图 4.1 所示，活动图按读者、前端页面、后端服务和数据库四条泳道展开。"),
        b.image(FIG + r"\fig4_1_activity_pillow.png", 15.6),
        b.cap_fig("图 4.1 座位查询与预约模块交互活动图"),
        b.p("如图 4.1 所示，查询阶段的流程为“读者设置筛选条件→前端调用座位查询接口→后端鉴权并组装座位视图→数据库查询座位与预约记录→前端渲染座位图”；预约阶段的流程为“读者选座并确认→前端提交预约请求→后端执行预约条件校验→数据库写入预约记录→前端提示成功并刷新座位图”。当预约条件校验不通过时，流程在提示失败原因后结束，读者可返回座位图重新选座。"),
    ])

    # ---------- 4.1.3 模块设计类图 ----------
    b.replace("（画该模块设计阶段的类图", [
        b.p("模块设计阶段的类图如图 4.2 所示，按边界类、控制类、实体类、持久化类和框架类五种角色组织。"),
        b.image(FIG + r"\fig4_2_class.png", 14.2),
        b.cap_fig("图 4.2 座位查询与预约模块设计类图"),
        b.p("边界类 Home.vue 维护页面状态并负责渲染，api/index.js 封装接口调用；控制类 ApiController 接收请求并委派给 SeatService 和 ReservationService；实体类 Seat、SeatVO 和 Reservation 对应数据库表及视图对象，其中 SeatVO 继承 Seat 并增加 roomName 和 reserved 两个属性；持久化类 SeatMapper、ReservationMapper 和 BlacklistMapper 使用 MyBatis 注解完成 SQL 映射；框架类 Result 统一封装响应。类之间的依赖方向始终由上层指向下层，实体类不依赖任何服务类。"),
    ])

    # ---------- 4.1.4 设计类说明 ----------
    b.revise("表4.1 设计类详细说明", "表4.1 设计类详细说明（SeatService）")
    tpl41 = b.find_table("类名")
    first = build_design_table(b, tpl41, SEAT_SERVICE)
    # 用重建后的表替换模板中的空表
    tpl41._tbl.addnext(first)
    tpl41._tbl.getparent().remove(tpl41._tbl)
    ref = first

    for cap, data in [("表4.2 设计类详细说明（ReservationService）", RES_SERVICE),
                      ("表4.3 设计类详细说明（Home.vue）", HOME_VUE)]:
        cap_el = b.cap_tab(cap)
        tbl_el = build_design_table(b, tpl41, data)
        ref.addnext(cap_el)
        cap_el.addnext(tbl_el)
        ref = tbl_el

    # ---------- 4.2 我的预约模块 ----------
    b.revise("XX模块详细设计", "我的预约模块详细设计")
    h42 = b.find("我的预约模块详细设计")
    anchor = h42._p
    # 跳过原模板中的空段
    nxt = anchor.getnext()
    while nxt is not None and nxt.tag == qn('w:p') and not ''.join(
            t.text or '' for t in nxt.findall('.//' + qn('w:t'))).strip():
        anchor = nxt
        nxt = nxt.getnext()

    blocks = [
        b.h3("模块职责与功能描述"),
        b.p("我的预约模块负责预约记录的全生命周期管理，是座位预约业务的闭环环节。模块对外提供 4 个接口：/api/my/reservations 查询本人预约记录，/api/checkin/{id} 签到，/api/checkout/{id} 签退，/api/cancel/{id} 取消预约。"),
        b.p("模块的主要职责包括：（1）联表查询读者的全部预约记录，组装包含座位号、阅览室名、时段名和起止时间的 ReservationVO；（2）按状态渲染不同的操作入口，已预约记录可签到或取消，已签到记录可签退；（3）在状态变更前校验记录归属和当前状态，保证状态按“已预约→已签到→已完成”或“已预约→已取消”的顺序迁移；（4）记录签到、签退和取消的时间戳，为座位使用统计和违约判定提供数据。"),
        b.p("该模块对应“我的预约”页面：列表按预约日期倒序展示预约单号、阅览室、座位、时段、日期和状态标签，操作列根据状态显示“签到/取消”“签退”或“—”，每次操作都经过二次确认，成功后刷新列表。"),
        b.h3("模块交互模型"),
        b.p("模块内部的交互过程如图 4.3 所示，同样按读者、前端页面、后端服务和数据库四条泳道展开。"),
        b.image(FIG + r"\fig4_3_activity_pillow.png", 15.6),
        b.cap_fig("图 4.3 我的预约模块交互活动图"),
        b.p("如图 4.3 所示，进入页面后前端调用预约记录接口，后端联表查询该读者的全部记录并返回视图对象；读者选择签到、签退或取消后，前端弹出确认对话框并提交对应接口；后端校验记录归属与当前状态，通过后更新状态与时间戳，前端提示操作成功并刷新列表。若记录状态不允许该操作，流程在提示“操作失败，当前状态不支持”后结束。"),
        b.h3("模块设计类图"),
        b.p("模块设计阶段的类图如图 4.4 所示。"),
        b.image(FIG + r"\fig4_4_class.png", 7.2),
        b.cap_fig("图 4.4 我的预约模块设计类图"),
        b.p("边界类 MyReservations.vue 维护列表状态并绑定四个操作按钮；控制类 ApiController 把记录查询和状态变更请求分别委派给 ReservationService 的对应方法；实体类 ReservationVO 聚合了展示所需的全部字段，Reservation 保存预约的主键、状态和时间戳；持久化类 ReservationMapper 提供联表查询与条件更新两类 SQL，条件更新时同时限定 id、user_id 和当前状态，从 SQL 层面避免越权与重复提交。"),
        b.h3("设计类说明"),
        b.p("模块中两个关键类的详细说明如表 4.4 和表 4.5 所示。"),
    ]
    cap4 = b.cap_tab("表4.4 设计类详细说明（MyReservations.vue）")
    tbl4 = build_design_table(b, tpl41, MY_VUE)
    cap5 = b.cap_tab("表4.5 设计类详细说明（ReservationMapper）")
    tbl5 = build_design_table(b, tpl41, RES_MAPPER)
    blocks += [cap4, tbl4, cap5, tbl5]
    b.insert_after(anchor, blocks)


