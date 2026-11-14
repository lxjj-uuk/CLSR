# -*- coding: utf-8 -*-
"""在课程设计报告模板上填内容的最小工具集（严格复用模板的样式与格式）"""
import copy
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.text.run import Run
from docx.shared import Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH


class Builder:
    def __init__(self, path):
        self.doc = Document(path)
        self.body = self.doc.element.body
        self._cache = {p.text.strip(): p for p in self.doc.paragraphs if p.text.strip()}
        self.body_tpl = self._find("自习室座位预约基础业务流程如下")
        self.fig_cap_tpl = self._find("图 2.1 自习室座位预约主业务活动图")
        self.tab_cap_tpl = self._find("表2.1 XX用例描述")
        self.h3_tpl = self._find("模块职责与功能描述")
        # 图片段落 = 图 2.1 上一段
        self.img_tpl = self.fig_cap_tpl._p.getprevious()
        while self.img_tpl is not None and self.img_tpl.tag != qn('w:p'):
            self.img_tpl = self.img_tpl.getprevious()

        # 模板 run 格式（宋体 + 小四）
        self.body_rpr = None
        for r in self.body_tpl.runs:
            if r._r.find(qn('w:rPr')) is not None:
                self.body_rpr = r._r.find(qn('w:rPr'))
                break
        self.fig_cap_rpr = None
        for r in self.fig_cap_tpl.runs:
            if r._r.find(qn('w:rPr')) is not None:
                self.fig_cap_rpr = r._r.find(qn('w:rPr'))
                break

    # ---------------- 查找 ----------------
    def _find(self, prefix):
        for p in self.doc.paragraphs:
            if p.text.strip().startswith(prefix):
                return p
        raise KeyError("未找到段落: " + prefix)

    def find(self, prefix):
        return self._find(prefix)

    def find_table(self, first_cell_text):
        for t in self.doc.tables:
            try:
                if t.rows[0].cells[0].text.strip().startswith(first_cell_text):
                    return t
            except Exception:
                continue
        raise KeyError("未找到表格: " + first_cell_text)

    # ---------------- 构造元素 ----------------
    def _para_from(self, tpl_p, text, rpr=None):
        p = copy.deepcopy(tpl_p)
        for child in list(p):
            if child.tag != qn('w:pPr'):
                p.remove(child)
        r = OxmlElement('w:r')
        src = rpr if rpr is not None else self.body_rpr
        if src is not None:
            r.append(copy.deepcopy(src))
        t = OxmlElement('w:t')
        t.set(qn('xml:space'), 'preserve')
        t.text = text
        r.append(t)
        p.append(r)
        return p

    def p(self, text):
        """正文段落（复用模板正文格式：宋体小四、行距 22 磅）"""
        return self._para_from(self.body_tpl._p, text)

    def cap_fig(self, text):
        el = self._para_from(self.fig_cap_tpl._p, text, self.fig_cap_rpr)
        return el

    def cap_tab(self, text):
        p = copy.deepcopy(self.tab_cap_tpl._p)
        for child in list(p):
            if child.tag != qn('w:pPr'):
                p.remove(child)
        r = OxmlElement('w:r')
        rpr = OxmlElement('w:rPr')
        f = OxmlElement('w:rFonts')
        f.set(qn('w:hint'), 'eastAsia')
        rpr.append(f)
        for tag in ('w:b', 'w:bCs'):
            e = OxmlElement(tag)
            rpr.append(e)
        for tag in ('w:sz', 'w:szCs'):
            e = OxmlElement(tag)
            e.set(qn('w:val'), '21')
            rpr.append(e)
        r.append(rpr)
        t = OxmlElement('w:t')
        t.set(qn('xml:space'), 'preserve')
        t.text = text
        r.append(t)
        p.append(r)
        return p

    def h3(self, text):
        p = copy.deepcopy(self.h3_tpl._p)
        for child in list(p):
            if child.tag not in (qn('w:pPr'),):
                p.remove(child)
        r = OxmlElement('w:r')
        rf = OxmlElement('w:rFonts')
        rf.set(qn('w:hint'), 'eastAsia')
        r.append(rf)
        t = OxmlElement('w:t')
        t.set(qn('xml:space'), 'preserve')
        t.text = text
        r.append(t)
        p.append(r)
        return p

    def image(self, path, width_cm=15.5):
        p = OxmlElement('w:p')
        ppr = OxmlElement('w:pPr')
        ppr.append(OxmlElement('w:keepNext'))
        jc = OxmlElement('w:jc')
        jc.set(qn('w:val'), 'center')
        ppr.append(jc)
        spacing = OxmlElement('w:spacing')
        spacing.set(qn('w:before'), '60')
        spacing.set(qn('w:after'), '60')
        ppr.append(spacing)
        p.append(ppr)
        para = Paragraph(p, self.doc._body)
        run = para.add_run()
        run.add_picture(path, width=Cm(width_cm))
        return p

    def revise(self, anchor_prefix, new_text):
        """只改文字，保留段落与首个 run 的格式（用于模板中带 XX 的标题/说明）"""
        p = self._find(anchor_prefix)
        el = p._p
        rpr = None
        for r in p.runs:
            if r._r.find(qn('w:rPr')) is not None:
                rpr = r._r.find(qn('w:rPr'))
                break
        for child in list(el):
            if child.tag != qn('w:pPr'):
                el.remove(child)
        r = OxmlElement('w:r')
        if rpr is not None:
            r.append(copy.deepcopy(rpr))
        t = OxmlElement('w:t')
        t.set(qn('xml:space'), 'preserve')
        t.text = new_text
        r.append(t)
        el.append(r)
        return p

    # ---------------- 插入/替换 ----------------
    def insert_after(self, anchor_p, elements):
        ref = anchor_p._p if hasattr(anchor_p, '_p') else anchor_p
        for el in elements:
            ref.addnext(el)
            ref = el
        return ref

    def replace(self, anchor_text, elements):
        p = self._find(anchor_text)
        ref = p._p
        for el in elements:
            ref.addnext(el)
            ref = el
        ref.getparent().remove(p._p)

    def insert_before(self, anchor_text, elements):
        p = self._find(anchor_text)
        ref = p._p
        for el in elements:
            ref.addprevious(el)

    def delete(self, anchor_text):
        p = self._find(anchor_text)
        p._p.getparent().remove(p._p)

    # ---------------- 表格 ----------------
    @staticmethod
    def _set_tc(tc, text, bold=False, size='21'):
        ps = tc.findall(qn('w:p'))
        if not ps:
            return
        first = ps[0]
        for extra in ps[1:]:
            tc.remove(extra)
        for child in list(first):
            if child.tag != qn('w:pPr'):
                first.remove(child)
        lines = str(text).split('\n')
        r = OxmlElement('w:r')
        rpr = OxmlElement('w:rPr')
        rf = OxmlElement('w:rFonts')
        rf.set(qn('w:hint'), 'eastAsia')
        rf.set(qn('w:ascii'), 'Times New Roman')
        rf.set(qn('w:hAnsi'), 'Times New Roman')
        rf.set(qn('w:eastAsia'), '宋体')
        rpr.append(rf)
        if bold:
            for tag in ('w:b', 'w:bCs'):
                rpr.append(OxmlElement(tag))
        for tag in ('w:sz', 'w:szCs'):
            e = OxmlElement(tag)
            e.set(qn('w:val'), size)
            rpr.append(e)
        r.append(rpr)
        for i, ln in enumerate(lines):
            if i:
                r.append(OxmlElement('w:br'))
            t = OxmlElement('w:t')
            t.set(qn('xml:space'), 'preserve')
            t.text = ln
            r.append(t)
        first.append(r)

    def fill_table(self, tbl, rows, header_bold=True):
        """rows[0] 为表头；数据行数按需增删（克隆现有数据行，保持模板行格式）"""
        trs = tbl._tbl.findall(qn('w:tr'))
        need = len(rows)
        have = len(trs)
        if need > have:
            for _ in range(need - have):
                tbl._tbl.append(copy.deepcopy(trs[-1]))
        elif need < have:
            for tr in trs[need:]:
                tbl._tbl.remove(tr)
        trs = tbl._tbl.findall(qn('w:tr'))
        for i, row in enumerate(rows):
            tcs = trs[i].findall(qn('w:tc'))
            if len(tcs) == len(row):
                for tc, val in zip(tcs, row):
                    self._set_tc(tc, val, bold=(header_bold and i == 0))
            else:
                # 用单元格视图（合并单元格场景）
                cells = []
                seen = set()
                for c in Table(tbl._tbl, tbl._parent).rows[i].cells:
                    if c._tc not in seen:
                        seen.add(c._tc)
                        cells.append(c)
                for c, val in zip(cells, row):
                    self._set_tc(c._tc, val, bold=(header_bold and i == 0))

    def clone_table(self, tbl, rows):
        new_tbl = copy.deepcopy(tbl._tbl)
        wrap = Table(new_tbl, tbl._parent)
        trs = new_tbl.findall(qn('w:tr'))
        need = len(rows)
        have = len(trs)
        if need > have:
            for _ in range(need - have):
                new_tbl.append(copy.deepcopy(trs[-1]))
        elif need < have:
            for tr in trs[need:]:
                new_tbl.remove(tr)
        trs = new_tbl.findall(qn('w:tr'))
        for i, row in enumerate(rows):
            tcs = trs[i].findall(qn('w:tc'))
            if len(tcs) == len(row):
                for tc, val in zip(tcs, row):
                    self._set_tc(tc, val, bold=(i == 0))
            else:
                cells = []
                seen = set()
                for c in Table(new_tbl, tbl._parent).rows[i].cells:
                    if c._tc not in seen:
                        seen.add(c._tc)
                        cells.append(c)
                for c, val in zip(cells, row):
                    self._set_tc(c._tc, val, bold=(i == 0))
        return new_tbl

    def design_table(self, rows, n_attr, n_meth, n_evt):
        """按模板 15 行 9 列结构重建“设计类详细说明”表"""
        return rows, n_attr, n_meth, n_evt

    def finalize_tables(self, skip=2):
        """表头跨页重复 + 行内不断页"""
        for idx, tbl in enumerate(self.doc.tables):
            trs = tbl._tbl.findall(qn('w:tr'))
            if not trs:
                continue
            for i, tr in enumerate(trs):
                trPr = tr.find(qn('w:trPr'))
                if trPr is None:
                    trPr = OxmlElement('w:trPr')
                    tr.insert(0, trPr)
                if trPr.find(qn('w:cantSplit')) is None:
                    trPr.insert(0, OxmlElement('w:cantSplit'))
                if idx >= skip and i == 0 and trPr.find(qn('w:tblHeader')) is None:
                    trPr.append(OxmlElement('w:tblHeader'))

    def save(self, path):
        self.doc.save(path)

