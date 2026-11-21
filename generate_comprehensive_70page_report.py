import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def create_report():
    doc = docx.Document()

    # Set page setup for all initial sections
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.5)
        s.right_margin = Inches(1.0)
        s.page_width = Inches(8.27)
        s.page_height = Inches(11.69)

    # Styles
    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)

    def set_font(run, name='Times New Roman', size_pt=12, bold=False, italic=False, color_rgb=(0, 0, 0)):
        run.font.name = name
        run.font.size = Pt(size_pt)
        run.bold = bold
        run.italic = italic
        run.font.color.rgb = RGBColor(*color_rgb)

    def add_para(text='', style='Normal', align=WD_ALIGN_PARAGRAPH.LEFT, line_spacing=1.5, space_before=0, space_after=6, first_line_indent=0.5):
        p = doc.add_paragraph(style=style)
        p.alignment = align
        p.paragraph_format.line_spacing = line_spacing
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        if first_line_indent > 0 and align in [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.JUSTIFY]:
            p.paragraph_format.first_line_indent = Inches(first_line_indent)
        else:
            p.paragraph_format.first_line_indent = Inches(0)
        if text:
            r = p.add_run(text)
            set_font(r, 'Times New Roman', 12, False, False, (0x1e, 0x29, 0x3b))
        return p

    def add_chapter_heading(title_text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(12)
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.page_break_before = True
        r = p.add_run(title_text.upper())
        set_font(r, 'Times New Roman', 16, bold=True, italic=False, color_rgb=(0, 0, 0))
        return p

    def add_heading_1(title_text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.first_line_indent = Inches(0)
        r = p.add_run(title_text.upper())
        set_font(r, 'Times New Roman', 14, bold=True, italic=False, color_rgb=(0, 0, 0))
        return p

    def add_subheading(title_text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.first_line_indent = Inches(0)
        r = p.add_run(title_text)
        set_font(r, 'Times New Roman', 14, bold=True, italic=False, color_rgb=(0, 0, 0))
        return p

    def add_sub_subheading(title_text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.first_line_indent = Inches(0)
        r = p.add_run(title_text)
        set_font(r, 'Times New Roman', 12, bold=True, italic=False, color_rgb=(0, 0, 0))
        return p

    def add_caption(caption_text, align=WD_ALIGN_PARAGRAPH.CENTER):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(10)
        p.paragraph_format.first_line_indent = Inches(0)
        r = p.add_run(caption_text)
        set_font(r, 'Times New Roman', 12, bold=True, italic=True, color_rgb=(0, 0, 0))
        return p

    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def add_footer_page_number(section, fmt='decimal', start=1):
        sectPr = section._sectPr
        for child in list(sectPr):
            if child.tag.endswith('pgNumType'):
                sectPr.remove(child)
        pgNumType = OxmlElement('w:pgNumType')
        pgNumType.set(qn('w:fmt'), fmt)
        if start is not None:
            pgNumType.set(qn('w:start'), str(start))
        sectPr.append(pgNumType)

        footer = section.footer
        footer.is_linked_to_previous = False
        p = footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.text = ''
        r = p.add_run()
        fld1 = OxmlElement('w:fldChar')
        fld1.set(qn('w:fldCharType'), 'begin')
        instr = OxmlElement('w:instrText')
        instr.set(qn('xml:space'), 'preserve')
        instr.text = ' PAGE '
        fld2 = OxmlElement('w:fldChar')
        fld2.set(qn('w:fldCharType'), 'separate')
        t = OxmlElement('w:t')
        t.text = '1'
        fld3 = OxmlElement('w:fldChar')
        fld3.set(qn('w:fldCharType'), 'end')
        r._r.extend([fld1, instr, fld2, t, fld3])
        set_font(r, 'Times New Roman', 12, False, False, (0, 0, 0))

    print("Setup completed successfully.")
    return doc

if __name__ == "__main__":
    create_report()
