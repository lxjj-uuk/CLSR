# -*- coding: utf-8 -*-
"""把各章内容装配到课程设计报告模板上"""
import copy
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from docxlib import Builder
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import content_ch2
import content_ch3
import content_ch4
import content_ch5_6

TEMPLATE = r"E:\xwechat_files\wxid_rkuxu3u0bplw22_d8f7\msg\file\2026-10\学号-姓名-软件工程课程设计-报告(2).docx"
OUT = r"E:\CLSR\_work\report_draft.docx"


def replace_in_cell(cell, old, new):
    for p in cell.paragraphs:
        if old in p.text:
            runs = p.runs
            rpr = None
            for r in runs:
                if r._r.find(qn('w:rPr')) is not None:
                    rpr = r._r.find(qn('w:rPr'))
                    break
            text = p.text.replace(old, new)
            for child in list(p._p):
                if child.tag != qn('w:pPr'):
                    p._p.remove(child)
            r = OxmlElement('w:r')
            if rpr is not None:
                r.append(copy.deepcopy(rpr))
            t = OxmlElement('w:t')
            t.set(qn('xml:space'), 'preserve')
            t.text = text
            r.append(t)
            p._p.append(r)
            return True
    return False


def fix_task_sheet(b):
    t = b.doc.tables[0]
    # 题目
    for row in t.rows:
        cells = row.cells
        for i, c in enumerate(cells):
            if c.text.strip() == '题目' and i + 1 < len(cells):
                nxt = cells[i + 1]
                if not nxt.text.strip():
                    for p in nxt.paragraphs:
                        if not p.runs:
                            r = p.add_run('校园图书馆座位预约系统')
                            r.font.name = '宋体'
                            r._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
                            break
                break
    # 任务书中的 XX、XX 部分
    for row in t.rows:
        for c in row.cells:
            if 'XX、XX部分' in c.text:
                replace_in_cell(c, 'XX、XX部分', '座位查询与预约（座位查询、座位预约）、我的预约（预约记录查询、签到、签退、取消预约）')


def fix_settings(b):
    s = b.doc.settings.element
    uf = s.find(qn('w:updateFields'))
    if uf is None:
        uf = OxmlElement('w:updateFields')
        s.append(uf)
    uf.set(qn('w:val'), 'true')


def drop_empty_numbered(b):
    """删除参考文献后多余的空编号段落"""
    for p in list(b.doc.paragraphs):
        if p.text.strip():
            continue
        ppr = p._p.find(qn('w:pPr'))
        if ppr is None:
            continue
        numpr = ppr.find(qn('w:numPr'))
        if numpr is None:
            continue
        nid = numpr.find(qn('w:numId'))
        if nid is not None and nid.get(qn('w:val')) == '4':
            p._p.getparent().remove(p._p)


def drop_empty_before(b, heading_prefix):
    """删除标题前的空段（避免整页空白），跳过带分节符的段落"""
    p = b.find(heading_prefix)
    el = p._p.getprevious()
    while el is not None and el.tag == qn('w:p'):
        txt = ''.join(t.text or '' for t in el.findall('.//' + qn('w:t'))).strip()
        if txt:
            break
        ppr = el.find(qn('w:pPr'))
        if ppr is not None and ppr.find(qn('w:sectPr')) is not None:
            break
        prev = el.getprevious()
        el.getparent().remove(el)
        el = prev


def main():
    b = Builder(TEMPLATE)
    content_ch2.apply(b)
    content_ch3.apply(b)
    content_ch4.apply(b)

    blocks, tests, tbl51 = content_ch5_6.apply(b)
    cap51 = b.cap_tab("表5.1 本人负责接口的功能测试用例及结果")
    tbl = b.clone_table(tbl51, tests)
    b.replace("（按功能自行设计三级标题）", blocks + [cap51, tbl])

    content_ch5_6.apply_tail(b)
    fix_task_sheet(b)
    drop_empty_numbered(b)
    drop_empty_before(b, "结论")
    b.finalize_tables(skip=2)
    fix_settings(b)
    b.save(OUT)
    print("saved", OUT)
    print("paragraphs:", len(b.doc.paragraphs), "tables:", len(b.doc.tables))


if __name__ == '__main__':
    main()

