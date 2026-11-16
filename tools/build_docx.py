# -*- coding: utf-8 -*-
"""把学习路线 Markdown 转成手机上好看、好读的 DOCX（供微信发送用）。"""
import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

CJK_FONT = "微软雅黑"
MONO_FONT = "Consolas"
ACCENT = RGBColor(0x1F, 0x4E, 0x79)
ACCENT2 = RGBColor(0x2E, 0x75, 0xB6)
GRAY = RGBColor(0x59, 0x59, 0x59)


def set_cjk(run_or_style, font=CJK_FONT):
    """同时设置西文与中文字体，否则中文会回退到宋体。"""
    rpr = run_or_style.element.get_or_add_rPr() if hasattr(run_or_style, "element") else run_or_style._r.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:ascii"), font)
    rfonts.set(qn("w:hAnsi"), font)
    rfonts.set(qn("w:eastAsia"), font)


def shade(element_pr, color):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color)
    element_pr.append(shd)


def bottom_rule(paragraph, color="1F4E79", size=8):
    ppr = paragraph._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), str(size))
    bottom.set(qn("w:space"), "4")
    bottom.set(qn("w:color"), color)
    borders.append(bottom)
    ppr.append(borders)


INLINE = re.compile(r"(\*\*.+?\*\*|`[^`]+`|~~.+?~~)")


def add_inline(paragraph, text, size=None):
    for token in INLINE.split(text):
        if not token:
            continue
        if token.startswith("**") and token.endswith("**") and len(token) > 4:
            run = paragraph.add_run(token[2:-2])
            run.bold = True
        elif token.startswith("~~") and token.endswith("~~") and len(token) > 4:
            run = paragraph.add_run(token[2:-2])
            run.font.strike = True
            run.font.color.rgb = GRAY
        elif token.startswith("`") and token.endswith("`") and len(token) > 2:
            run = paragraph.add_run(token[1:-1])
            run.font.name = MONO_FONT
            run.font.size = Pt(9)
            run.font.color.rgb = RGBColor(0xB0, 0x30, 0x60)
            shade(run._r.get_or_add_rPr(), "F4F4F4")
        else:
            run = paragraph.add_run(token)
        if size:
            run.font.size = Pt(size)


def is_table_sep(line):
    stripped = line.strip().strip("|")
    if not stripped:
        return False
    return all(part.strip().replace("-", "").replace(":", "") == "" and "-" in part for part in stripped.split("|"))


def split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def build_heading(doc, text, level):
    p = doc.add_paragraph(style=f"Heading {min(level, 4)}")
    add_inline(p, text)
    return p


def build_table(doc, rows):
    cols = max(len(r) for r in rows)
    table = doc.add_table(rows=len(rows), cols=cols)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True
    for r_idx, row in enumerate(rows):
        for c_idx in range(cols):
            cell = table.cell(r_idx, c_idx)
            cell.text = ""
            para = cell.paragraphs[0]
            para.paragraph_format.space_before = Pt(2)
            para.paragraph_format.space_after = Pt(2)
            add_inline(para, row[c_idx] if c_idx < len(row) else "", size=9)
            if r_idx == 0:
                for run in para.runs:
                    run.bold = True
                shade(cell._tc.get_or_add_tcPr(), "D9E2F3")
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return table


def convert(md_path, doc, first_section):
    lines = md_path.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.3)
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(8)
            p.paragraph_format.line_spacing = 1.05
            shade(p._p.get_or_add_pPr(), "F5F5F5")
            for idx, cl in enumerate(code_lines):
                run = p.add_run(cl if cl else " ")
                run.font.name = MONO_FONT
                run.font.size = Pt(8.5)
                if idx < len(code_lines) - 1:
                    run.add_break()
            i += 1
            continue

        if stripped.startswith("|") and i + 1 < len(lines) and is_table_sep(lines[i + 1]):
            rows = [split_row(stripped)]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i].strip()))
                i += 1
            build_table(doc, rows)
            continue

        heading = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if heading:
            level = len(heading.group(1))
            text = heading.group(2).strip()
            if level == 1:
                p = doc.add_paragraph()
                p.add_run().add_break(WD_BREAK.PAGE)
                p = build_heading(doc, text, 1)
                p.paragraph_format.space_before = Pt(6)
                p.paragraph_format.space_after = Pt(10)
                for run in p.runs:
                    run.font.size = Pt(17)
                    run.font.color.rgb = ACCENT
                bottom_rule(p)
            elif level == 2:
                p = build_heading(doc, text, 2)
                for run in p.runs:
                    run.font.size = Pt(13.5)
                    run.font.color.rgb = ACCENT2
            else:
                p = build_heading(doc, text, level)
                for run in p.runs:
                    run.font.size = Pt(11.5)
                    run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
            i += 1
            continue

        if re.fullmatch(r"-{3,}|\*{3,}", stripped):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            bottom_rule(p, color="BFBFBF", size=4)
            i += 1
            continue

        if stripped.startswith(">"):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.5)
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            add_inline(p, stripped.lstrip("> ").strip())
            for run in p.runs:
                if not run.font.strike:
                    run.font.color.rgb = GRAY
                    run.italic = True
            shade(p._p.get_or_add_pPr(), "F7F7F7")
            i += 1
            continue

        checked = re.match(r"^-\s+\[([ xX])\]\s*(.*)$", stripped)
        if checked:
            p = doc.add_paragraph(style="List Bullet")
            p.paragraph_format.space_after = Pt(2)
            mark = "☑ " if checked.group(1).lower() == "x" else "☐ "
            run = p.add_run(mark)
            run.font.name = "Segoe UI Symbol"
            add_inline(p, checked.group(2))
            if checked.group(1).lower() == "x":
                for r in p.runs[1:]:
                    r.font.color.rgb = GRAY
            i += 1
            continue

        bullet = re.match(r"^[-*]\s+(.*)$", stripped)
        if bullet:
            p = doc.add_paragraph(style="List Bullet")
            p.paragraph_format.space_after = Pt(2)
            add_inline(p, bullet.group(1))
            i += 1
            continue

        numbered = re.match(r"^(\d+)[.、]\s+(.*)$", stripped)
        if numbered:
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.72)
            p.paragraph_format.first_line_indent = Cm(-0.72)
            p.paragraph_format.space_after = Pt(3)
            run = p.add_run(f"{numbered.group(1)}. ")
            run.bold = True
            add_inline(p, numbered.group(2))
            i += 1
            continue

        if not stripped:
            i += 1
            continue

        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(6)
        add_inline(p, stripped)
        i += 1


def main():
    workspace = Path(__file__).resolve().parent.parent
    out = workspace / "编程学习路线图_手机版.docx"

    doc = Document()
    section = doc.sections[0]
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(2.2)
    section.right_margin = Cm(2.2)

    normal = doc.styles["Normal"]
    normal.font.name = CJK_FONT
    normal.font.size = Pt(10.5)
    set_cjk(normal)
    normal.paragraph_format.line_spacing = 1.35

    for name in ["Heading 1", "Heading 2", "Heading 3", "Heading 4"]:
        style = doc.styles[name]
        style.font.name = CJK_FONT
        set_cjk(style)

    # 封面
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.paragraph_format.space_before = Pt(90)
    run = title.add_run("从零到独立开发")
    run.font.size = Pt(30)
    run.bold = True
    run.font.color.rgb = ACCENT

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = sub.add_run("编程学习路线图 · 2026 版")
    run.font.size = Pt(15)
    run.font.color.rgb = ACCENT2

    meta = doc.add_paragraph()
    meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    meta.paragraph_format.space_before = Pt(24)
    run = meta.add_run("目标：看懂 GitHub 项目 → 独立开发 → 拓宽职业选择\n生成日期：2026-11-16")
    run.font.size = Pt(10)
    run.font.color.rgb = GRAY

    first = doc.add_paragraph()
    first.alignment = WD_ALIGN_PARAGRAPH.CENTER
    first.paragraph_format.space_before = Pt(110)
    run = first.add_run("每次调整计划前，先回来看这份文件，别凭记忆改。")
    run.font.size = Pt(9.5)
    run.font.color.rgb = GRAY
    run.italic = True

    first_section = [True]
    convert(workspace / "编程学习路线图.md", doc, first_section)
    convert(workspace / "每周复盘模板.md", doc, first_section)

    doc.save(out)
    print(f"SAVED {out}  {out.stat().st_size} bytes")


if __name__ == "__main__":
    sys.exit(main())
