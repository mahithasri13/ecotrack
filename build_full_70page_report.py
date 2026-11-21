# build_full_70page_report.py
# Master Compiler for EcoTrack 70-Page Academic Project Report
import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

from report_text_front import TITLE_PAGE_DATA, CERTIFICATE_TEXT, ACKNOWLEDGEMENT_TEXT, ABSTRACT_TEXT, ABBREVIATIONS_DATA
from report_text_ch1_to_ch3 import CH1_TITLE, CH1_SECTIONS, CH2_TITLE, CH2_SECTIONS, CH3_TITLE, CH3_SECTIONS
from report_text_ch4_to_ch5 import CH4_TITLE, CH4_SECTIONS, CH5_TITLE, CH5_SECTIONS
from report_text_ch6_to_ch8 import CH6_TITLE, CH6_SECTIONS, CH7_TITLE, CH7_SECTIONS, CH8_TITLE, CH8_SECTIONS, REFERENCES_DATA
from report_text_annexures import ANNEXURE_I_DATA, ANNEXURE_II_DATA, ANNEXURE_III_DATA, ANNEXURE_IV_DATA, ANNEXURE_V_DATA

def create_complete_report():
    print("Initializing Document...")
    doc = docx.Document()

    # -------------------------------------------------------------
    # Page Setup Helper
    # -------------------------------------------------------------
    def apply_margins(section):
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.5)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)

    apply_margins(doc.sections[0])

    # -------------------------------------------------------------
    # Typography Helpers
    # -------------------------------------------------------------
    def set_font(run, name='Times New Roman', size_pt=12, bold=False, italic=False, color_rgb=(0, 0, 0)):
        run.font.name = name
        run.font.size = Pt(size_pt)
        run.bold = bold
        run.italic = italic
        run.font.color.rgb = RGBColor(*color_rgb)

    def add_para(text='', align=WD_ALIGN_PARAGRAPH.LEFT, line_spacing=1.5, space_before=0, space_after=6, first_line_indent=0.5):
        p = doc.add_paragraph()
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

    def add_code_block(code_text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.first_line_indent = Inches(0)
        r = p.add_run(code_text)
        set_font(r, 'Courier New', 10, bold=False, italic=False, color_rgb=(0x0f, 0x17, 0x2a))
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

    # =========================================================================
    # SECTION 0: TITLE PAGE, CERTIFICATE, ACKNOWLEDGEMENT (No Page Numbers)
    # =========================================================================
    print("Generating Front Matter - Section 0 (Title, Certificate, Acknowledgement)...")
    sec0 = doc.sections[0]

    # --- TITLE PAGE ---
    p = add_para(TITLE_PAGE_DATA["degree_subtext"], align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.3, space_before=10, space_after=10, first_line_indent=0)
    set_font(p.runs[0], 'Times New Roman', 13, bold=False, italic=True)

    p = add_para(TITLE_PAGE_DATA["project_title"].upper(), align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.3, space_before=6, space_after=16, first_line_indent=0)
    set_font(p.runs[0], 'Times New Roman', 16, bold=True)

    p = add_para(TITLE_PAGE_DATA["degree_name"], align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=6, space_after=4, first_line_indent=0)
    set_font(p.runs[0], 'Times New Roman', 14, bold=True)

    p = add_para(TITLE_PAGE_DATA["branch_name"], align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=2, space_after=18, first_line_indent=0)
    set_font(p.runs[0], 'Times New Roman', 13, bold=True)

    p = add_para(TITLE_PAGE_DATA["submitted_by_header"], align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=6, space_after=8, first_line_indent=0)
    set_font(p.runs[0], 'Times New Roman', 12, bold=True)

    for st in TITLE_PAGE_DATA["students"]:
        p = add_para(f"{st['name']}    ({st['roll']})", align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=2, space_after=2, first_line_indent=0)
        set_font(p.runs[0], 'Times New Roman', 12, bold=True)

    p = add_para(TITLE_PAGE_DATA["guide_header"], align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=14, space_after=4, first_line_indent=0)
    set_font(p.runs[0], 'Times New Roman', 12, bold=True)

    p = add_para(f"{TITLE_PAGE_DATA['guide_name']}\n{TITLE_PAGE_DATA['guide_designation']}", align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=2, space_after=12, first_line_indent=0)
    set_font(p.runs[0], 'Times New Roman', 12, bold=True)

    if os.path.exists('extracted_media/image1.png'):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(4)
        p_logo.paragraph_format.space_after = Pt(12)
        r_logo = p_logo.add_run()
        r_logo.add_picture('extracted_media/image1.png', width=Inches(1.5))

    p = add_para(TITLE_PAGE_DATA["college_name"], align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=4, space_after=0, first_line_indent=0)
    set_font(p.runs[0], 'Times New Roman', 11, bold=True)

    doc.add_page_break()

    # --- CERTIFICATE ---
    if os.path.exists('extracted_media/image2.jpeg'):
        p_banner = doc.add_paragraph()
        p_banner.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_banner.paragraph_format.space_before = Pt(0)
        p_banner.paragraph_format.space_after = Pt(14)
        r_b = p_banner.add_run()
        r_b.add_picture('extracted_media/image2.jpeg', width=Inches(5.6))

    p = add_para('CERTIFICATE', align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=10, space_after=16, first_line_indent=0)
    set_font(p.runs[0], 'Times New Roman', 16, bold=True)

    p = add_para(CERTIFICATE_TEXT, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, space_before=10, space_after=24, first_line_indent=0.5)

    table_sig = doc.add_table(rows=4, cols=2)
    table_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_sig.autofit = False
    table_sig.rows[0].cells[0].paragraphs[0].text = "Student's Name & Roll Number"
    table_sig.rows[0].cells[1].paragraphs[0].text = "Signature"
    for r in range(4):
        table_sig.rows[r].cells[0].width = Inches(3.4)
        table_sig.rows[r].cells[1].width = Inches(2.2)
    set_font(table_sig.rows[0].cells[0].paragraphs[0].runs[0], 'Times New Roman', 12, bold=True)
    set_font(table_sig.rows[0].cells[1].paragraphs[0].runs[0], 'Times New Roman', 12, bold=True)

    for i, st in enumerate(TITLE_PAGE_DATA["students"]):
        row = table_sig.rows[i+1]
        p0 = row.cells[0].paragraphs[0]
        p0.text = f"{i+1}. {st['name']} ({st['roll']})"
        set_font(p0.runs[0], 'Times New Roman', 11, bold=False)
        p1 = row.cells[1].paragraphs[0]
        p1.text = "______________________"
        set_font(p1.runs[0], 'Times New Roman', 11, bold=False)

    p_sp = add_para('', space_before=32, space_after=0, first_line_indent=0)

    table_hod = doc.add_table(rows=2, cols=2)
    table_hod.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_hod.rows[0].cells[0].width = Inches(3.4)
    table_hod.rows[0].cells[1].width = Inches(2.2)
    table_hod.rows[1].cells[0].width = Inches(3.4)
    table_hod.rows[1].cells[1].width = Inches(2.2)

    p = table_hod.rows[0].cells[0].paragraphs[0]
    p.text = "Mrs. R. Kiruthiga"
    set_font(p.runs[0], 'Times New Roman', 12, bold=True)
    p = table_hod.rows[0].cells[1].paragraphs[0]
    p.text = "Dr. A. Mallikarjuna Reddy"
    set_font(p.runs[0], 'Times New Roman', 12, bold=True)

    p = table_hod.rows[1].cells[0].paragraphs[0]
    p.text = "Internal Guide & Asst. Professor"
    set_font(p.runs[0], 'Times New Roman', 11, italic=True)
    p = table_hod.rows[1].cells[1].paragraphs[0]
    p.text = "Head of the Department, AI & ML"
    set_font(p.runs[0], 'Times New Roman', 11, italic=True)

    doc.add_page_break()

    # --- ACKNOWLEDGEMENT ---
    p = add_para('ACKNOWLEDGEMENT', align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=14, space_after=18, first_line_indent=0)
    set_font(p.runs[0], 'Times New Roman', 16, bold=True)

    for ack_para in ACKNOWLEDGEMENT_TEXT:
        p = add_para(ack_para, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, space_before=6, space_after=12, first_line_indent=0.5)

    p_sp2 = add_para('', space_before=24, space_after=0, first_line_indent=0)
    for st in TITLE_PAGE_DATA["students"]:
        p = add_para(f"{st['name']} ({st['roll']})", align=WD_ALIGN_PARAGRAPH.RIGHT, line_spacing=1.2, space_before=2, space_after=2, first_line_indent=0)
        set_font(p.runs[0], 'Times New Roman', 11, bold=True)

    # =========================================================================
    # SECTION 1: FRONT MATTER (Roman Numerals: i, ii, iii ...)
    # =========================================================================
    print("Generating Front Matter - Section 1 (Contents, Abstract, Lists, Abbreviations)...")
    sec1 = doc.add_section(WD_SECTION.NEW_PAGE)
    apply_margins(sec1)
    add_footer_page_number(sec1, fmt='lowerRoman', start=4)

    # --- TABLE OF CONTENTS ---
    p = add_para('CONTENTS', align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=14, space_after=16, first_line_indent=0)
    set_font(p.runs[0], 'Times New Roman', 16, bold=True)

    toc_entries = [
        ("TITLE PAGE", "", "i"),
        ("CERTIFICATE", "", "ii"),
        ("ACKNOWLEDGEMENT", "", "iii"),
        ("CONTENTS", "", "iv"),
        ("ABSTRACT", "", "v"),
        ("LIST OF FIGURES", "", "vi"),
        ("LIST OF TABLES", "", "vii"),
        ("ABBREVIATIONS", "", "viii"),
        ("CHAPTER 1", "INTRODUCTION", "1"),
        ("  1.1", "Background and Environmental Context", "1"),
        ("  1.2", "Atmospheric Pollution and Water Quality Crises in India", "2"),
        ("  1.3", "The Need for Smart Automated Monitoring Systems", "3"),
        ("  1.4", "Problem Statement", "4"),
        ("  1.5", "Objectives of the EcoTrack System", "4"),
        ("  1.6", "Scope and Delimitations of the Work", "5"),
        ("  1.7", "Scientific and Technical Contributions", "6"),
        ("  1.8", "Organization of the Project Report", "6"),
        ("CHAPTER 2", "LITERATURE SURVEY", "7"),
        ("  2.1", "Historical Evolution of Environmental Sensing", "7"),
        ("  2.2", "Comparative Survey of Air Quality Standards (CPCB vs US EPA)", "8"),
        ("  2.3", "Water Quality Parameters and WHO Potability Standards", "9"),
        ("  2.4", "Review of Machine Learning in Atmospheric Modeling", "10"),
        ("  2.5", "Supervised Classification in Hydrological Water Potability", "11"),
        ("  2.6", "Anomaly Detection Methodologies in Environmental Sensors", "12"),
        ("  2.7", "Critical Comparison Matrix of Existing Systems", "13"),
        ("  2.8", "Identified Research Gaps and Motivation", "14"),
        ("  2.9", "Summary of the Chapter", "14"),
        ("CHAPTER 3", "SYSTEM REQUIREMENTS AND SPECIFICATIONS", "15"),
        ("  3.1", "Stakeholder and User Characteristics", "15"),
        ("  3.2", "Functional Requirements Specification (FRS)", "16"),
        ("  3.3", "Non-Functional Requirements Specification (NFRS)", "17"),
        ("  3.4", "Hardware Requirements and Sensor Specifications", "18"),
        ("  3.5", "Software Requirements and Technology Stack", "19"),
        ("  3.6", "Feasibility Study (Technical, Operational, Economic, Legal)", "20"),
        ("  3.7", "Summary of the Chapter", "20"),
        ("CHAPTER 4", "SYSTEM DESIGN AND ARCHITECTURE", "21"),
        ("  4.1", "System Architectural Overview", "21"),
        ("  4.2", "Layered Architectural Topology", "22"),
        ("  4.3", "Data Flow Diagrams (DFD Level 0, 1, 2)", "23"),
        ("  4.4", "Unified Modeling Language (UML) Diagrams", "24"),
        ("  4.5", "Database Architecture and Entity-Relationship Modeling", "27"),
        ("  4.6", "Data Dictionaries and Table Schemas", "28"),
        ("  4.7", "Interface and Reverse Proxy Architecture", "29"),
        ("  4.8", "Summary of the Chapter", "30"),
        ("CHAPTER 5", "METHODOLOGY AND ALGORITHM DESIGN", "31"),
        ("  5.1", "Data Acquisition Pipeline and Telemetry Provenance", "31"),
        ("  5.2", "Data Cleaning, Imputation, and Preprocessing", "32"),
        ("  5.3", "Feature Engineering and Statistical Profiling", "33"),
        ("  5.4", "Air Quality Multivariate Regression Formulation", "34"),
        ("  5.5", "Water Potability Classification Formulation", "36"),
        ("  5.6", "Unsupervised Isolation Forest Anomaly Detection", "37"),
        ("  5.7", "Composite Environmental Health Index (EHI) Formulation", "38"),
        ("  5.8", "Model Evaluation Metrics Mathematical Definitions", "39"),
        ("  5.9", "Summary of the Chapter", "40"),
        ("CHAPTER 6", "IMPLEMENTATION DETAILS", "41"),
        ("  6.1", "Backend Core Architecture with FastAPI", "41"),
        ("  6.2", "Machine Learning Engine and Pipeline Serialization", "42"),
        ("  6.3", "Real-Time Multi-Station Telemetry Ingestion Service", "43"),
        ("  6.4", "Analytics Engine, Dynamic Alerting, and Directives", "45"),
        ("  6.5", "Frontend User Interface Implementation with React 18 & Tailwind", "46"),
        ("  6.6", "Data Visualization Components with Chart.js", "48"),
        ("  6.7", "Database Persistence with SQLite and SQLAlchemy ORM", "49"),
        ("  6.8", "Deployment Infrastructure, Nginx Proxy, and Security", "50"),
        ("  6.9", "Summary of the Chapter", "50"),
        ("CHAPTER 7", "RESULTS AND DISCUSSION", "51"),
        ("  7.1", "Experimental Benchmarking Protocols", "51"),
        ("  7.2", "Air Quality Regression Results and Error Analysis", "52"),
        ("  7.3", "Water Potability Classification Results and ROC Evaluation", "53"),
        ("  7.4", "Anomaly Detection Efficacy and Sensor Fault Mitigation", "55"),
        ("  7.5", "Telemetry Ingestion Benchmarks and System Latency", "56"),
        ("  7.6", "User Interface Validation and Screen Audit", "57"),
        ("  7.7", "Comparative Evaluation with Contemporary Benchmarks", "58"),
        ("  7.8", "Summary of the Chapter", "58"),
        ("CHAPTER 8", "CONCLUSION AND FUTURE ENHANCEMENTS", "59"),
        ("  8.1", "Summary of Research Achievements", "59"),
        ("  8.2", "Societal, Ecological, and Economic Impact", "60"),
        ("  8.3", "Challenges and Delimitations", "61"),
        ("  8.4", "Future Research Directions", "61"),
        ("  8.5", "Concluding Remarks", "62"),
        ("REFERENCES", "", "63"),
        ("ANNEXURE I", "Complete REST API Specification and Schemas", "i"),
        ("ANNEXURE II", "Core Source Code Repository Excerpts", "i"),
        ("ANNEXURE III", "Test Suite Execution and Verification Protocols", "i"),
        ("ANNEXURE IV", "Hardware Specification and IoT Sensor Pinouts", "i"),
        ("ANNEXURE V", "Production Configuration and Nginx Deployment Runbook", "i")
    ]

    table_toc = doc.add_table(rows=len(toc_entries), cols=3)
    table_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_toc.autofit = False
    for i, (c1, c2, c3) in enumerate(toc_entries):
        row = table_toc.rows[i]
        row.cells[0].width = Inches(1.8)
        row.cells[1].width = Inches(3.3)
        row.cells[2].width = Inches(0.6)
        p0 = row.cells[0].paragraphs[0]
        p0.text = c1
        p1 = row.cells[1].paragraphs[0]
        p1.text = c2
        p2 = row.cells[2].paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p2.text = c3
        is_bold = "CHAPTER" in c1 or c1 in ["TITLE PAGE", "CERTIFICATE", "ACKNOWLEDGEMENT", "CONTENTS", "ABSTRACT", "LIST OF FIGURES", "LIST OF TABLES", "ABBREVIATIONS", "REFERENCES", "ANNEXURE I", "ANNEXURE II", "ANNEXURE III", "ANNEXURE IV", "ANNEXURE V"]
        set_font(p0.runs[0], 'Times New Roman', 11, bold=is_bold)
        if p1.runs:
            set_font(p1.runs[0], 'Times New Roman', 11, bold=is_bold)
        set_font(p2.runs[0], 'Times New Roman', 11, bold=is_bold)

    doc.add_page_break()

    # --- ABSTRACT ---
    p = add_para('ABSTRACT', align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=14, space_after=18, first_line_indent=0)
    set_font(p.runs[0], 'Times New Roman', 16, bold=True)

    for abs_para in ABSTRACT_TEXT:
        p = add_para(abs_para, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, space_before=6, space_after=12, first_line_indent=0.5)

    doc.add_page_break()

    # --- LIST OF FIGURES ---
    p = add_para('LIST OF FIGURES', align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=14, space_after=18, first_line_indent=0)
    set_font(p.runs[0], 'Times New Roman', 16, bold=True)

    figures_list = [
        ("Figure 4.1", "Four-Tier System Architecture of EcoTrack", "22"),
        ("Figure 4.2", "Context Level 0 and Level 1 Data Flow Diagrams", "24"),
        ("Figure 4.3", "Complete UML Use Case Diagram and Actor Interactions", "25"),
        ("Figure 4.4", "UML Class Diagram and Object-Oriented Domain Model", "26"),
        ("Figure 4.5", "UML Sequence Diagram for Real-Time Telemetry and Inference", "27"),
        ("Figure 4.6", "Relational Entity-Relationship (ER) Database Schema", "28"),
        ("Figure 5.1", "Air Quality Telemetry Preprocessing and Regression Pipeline", "35"),
        ("Figure 5.2", "Water Potability Classification Pipeline and Sigmoid Calibration", "37"),
        ("Figure 5.3", "Unsupervised Isolation Forest Recursive Tree Partitioning", "38"),
        ("Figure 7.1", "Screen 1: Nationwide Live Ingestion Dashboard View", "57"),
        ("Figure 7.2", "Screen 2: Air Quality Simulator with Interactive Sliders", "57"),
        ("Figure 7.3", "Screen 3: Water Potability Diagnostic Workbench", "58"),
        ("Figure 7.4", "Screen 4: Anomaly Explorer and Historical Audit Table", "58")
    ]

    table_lof = doc.add_table(rows=len(figures_list), cols=3)
    table_lof.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_lof.autofit = False
    for i, (fnum, fdesc, fpage) in enumerate(figures_list):
        row = table_lof.rows[i]
        row.cells[0].width = Inches(1.5)
        row.cells[1].width = Inches(3.6)
        row.cells[2].width = Inches(0.6)
        p0 = row.cells[0].paragraphs[0]
        p0.text = fnum
        p1 = row.cells[1].paragraphs[0]
        p1.text = fdesc
        p2 = row.cells[2].paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p2.text = fpage
        set_font(p0.runs[0], 'Times New Roman', 11, bold=True)
        set_font(p1.runs[0], 'Times New Roman', 11, bold=False)
        set_font(p2.runs[0], 'Times New Roman', 11, bold=True)

    p_sp3 = add_para('', space_before=24, space_after=0, first_line_indent=0)

    # --- LIST OF TABLES ---
    p = add_para('LIST OF TABLES', align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=14, space_after=18, first_line_indent=0)
    set_font(p.runs[0], 'Times New Roman', 16, bold=True)

    tables_list = [
        ("Table 2.1", "Comprehensive Comparison Matrix of Existing Monitoring Systems", "13"),
        ("Table 4.1", "Relational Database Schema Specification for prediction_logs", "29"),
        ("Table 5.1", "Physicochemical Water Parameters and WHO Safe Baseline Limits", "33"),
        ("Table 6.1", "Directory of 15 Live Indian Monitoring Stations and Coordinates", "44"),
        ("Table 7.1", "Comparative Evaluation Metrics for AQI Regression Models", "52"),
        ("Table 7.2", "Comparative Performance Metrics for Water Potability Classifiers", "54"),
        ("Table 7.3", "System Latency, Throughput, and Concurrency Stress Benchmarks", "56"),
        ("Table III.1", "Automated API Unit Verification Test Suite Execution Matrix", "iii")
    ]

    table_lot = doc.add_table(rows=len(tables_list), cols=3)
    table_lot.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_lot.autofit = False
    for i, (tnum, tdesc, tpage) in enumerate(tables_list):
        row = table_lot.rows[i]
        row.cells[0].width = Inches(1.5)
        row.cells[1].width = Inches(3.6)
        row.cells[2].width = Inches(0.6)
        p0 = row.cells[0].paragraphs[0]
        p0.text = tnum
        p1 = row.cells[1].paragraphs[0]
        p1.text = tdesc
        p2 = row.cells[2].paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p2.text = tpage
        set_font(p0.runs[0], 'Times New Roman', 11, bold=True)
        set_font(p1.runs[0], 'Times New Roman', 11, bold=False)
        set_font(p2.runs[0], 'Times New Roman', 11, bold=True)

    doc.add_page_break()

    # --- ABBREVIATIONS ---
    p = add_para('ABBREVIATIONS', align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=14, space_after=18, first_line_indent=0)
    set_font(p.runs[0], 'Times New Roman', 16, bold=True)

    table_abbr = doc.add_table(rows=len(ABBREVIATIONS_DATA), cols=2)
    table_abbr.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_abbr.autofit = False
    for i, (short_form, full_form) in enumerate(ABBREVIATIONS_DATA):
        row = table_abbr.rows[i]
        row.cells[0].width = Inches(1.5)
        row.cells[1].width = Inches(4.2)
        p0 = row.cells[0].paragraphs[0]
        p0.text = short_form
        p1 = row.cells[1].paragraphs[0]
        p1.text = full_form
        set_font(p0.runs[0], 'Times New Roman', 11, bold=True)
        set_font(p1.runs[0], 'Times New Roman', 11, bold=False)

    # =========================================================================
    # SECTION 2: BODY CHAPTERS (Arabic Numerals: 1, 2, 3 ...)
    # =========================================================================
    print("Generating Body Chapters - Section 2 (Chapters 1 to 8 + References)...")
    sec2 = doc.add_section(WD_SECTION.NEW_PAGE)
    apply_margins(sec2)
    add_footer_page_number(sec2, fmt='decimal', start=1)

    def render_chapter_content(ch_title, ch_sections):
        add_chapter_heading(ch_title)
        for sec in ch_sections:
            if sec["type"] == "heading":
                add_heading_1(sec["title"])
                for para in sec["content"]:
                    add_para(para, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, space_before=4, space_after=8, first_line_indent=0.5)

    # CHAPTER 1
    render_chapter_content(CH1_TITLE, CH1_SECTIONS)

    # CHAPTER 2
    render_chapter_content(CH2_TITLE, CH2_SECTIONS)

    # Table 2.1 in Chapter 2
    add_caption("Table 2.1: Comprehensive Comparison Matrix of Existing Monitoring Systems")
    comp_headers = ["System / Platform", "Spatial Scope", "Predictive ML", "Water Quality", "Anomaly Detection", "Action Directives", "Audit Export"]
    comp_rows = [
        ["CPCB National Portal", "India (Static)", "None (Static)", "Separate Silo", "None", "Basic Text", "Restricted"],
        ["IQAir AirVisual", "Global Urban", "Statistical", "None (Air Only)", "Basic Bounds", "Health Tips", "Commercial API"],
        ["OpenAQ Platform", "Global Open", "None (Ingest)", "None (Air Only)", "None", "None", "S3 / Raw API"],
        ["SAFAR (MoES India)", "Select Metros", "Numerical NWP", "None (Air Only)", "Manual QA", "Advisories", "Restricted"],
        ["Project EcoTrack", "15 Key Stations", "Random Forest", "9-Param Supervised", "Isolation Forest", "GRAP Stages I-IV", "CSV & JSON Instant"]
    ]
    t21 = doc.add_table(rows=len(comp_rows)+1, cols=7)
    t21.alignment = WD_TABLE_ALIGNMENT.CENTER
    t21.autofit = False
    col_widths = [Inches(1.2), Inches(0.8), Inches(0.8), Inches(0.8), Inches(0.8), Inches(0.8), Inches(0.8)]
    for j, h in enumerate(comp_headers):
        c = t21.rows[0].cells[j]
        c.width = col_widths[j]
        c.paragraphs[0].text = h
        set_font(c.paragraphs[0].runs[0], 'Times New Roman', 9, bold=True)
        set_cell_background(c, "E2E8F0")
    for i, row in enumerate(comp_rows):
        for j, val in enumerate(row):
            c = t21.rows[i+1].cells[j]
            c.width = col_widths[j]
            c.paragraphs[0].text = val
            is_eco = (i == len(comp_rows)-1)
            set_font(c.paragraphs[0].runs[0], 'Times New Roman', 8, bold=is_eco)
            if is_eco:
                set_cell_background(c, "E6F4EA")

    # CHAPTER 3
    render_chapter_content(CH3_TITLE, CH3_SECTIONS)

    # CHAPTER 4
    render_chapter_content(CH4_TITLE, CH4_SECTIONS)

    # Embed Figure 4.1 in Chapter 4
    if os.path.exists('report_assets/figure1_architecture.png'):
        p_fig = doc.add_paragraph()
        p_fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig.paragraph_format.space_before = Pt(8)
        p_fig.paragraph_format.space_after = Pt(4)
        r_f = p_fig.add_run()
        r_f.add_picture('report_assets/figure1_architecture.png', width=Inches(5.4))
        add_caption("Figure 4.1: Four-Tier System Architecture of Project EcoTrack")

    # Embed Figure 4.2 in Chapter 4 (pipeline diagrams)
    if os.path.exists('report_assets/figure5_fusion_pipeline.png'):
        p_fig = doc.add_paragraph()
        p_fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig.paragraph_format.space_before = Pt(8)
        p_fig.paragraph_format.space_after = Pt(4)
        r_f = p_fig.add_run()
        r_f.add_picture('report_assets/figure5_fusion_pipeline.png', width=Inches(5.4))
        add_caption("Figure 4.2: Environmental Health Index (EHI) Dual-Vector Fusion Pipeline")

    # Table 4.1 in Chapter 4
    add_caption("Table 4.1: Relational Database Schema Specification for prediction_logs")
    t41_headers = ["Field Name", "Data Type", "Constraint", "Physical Unit", "Description"]
    t41_rows = [
        ["id", "INTEGER", "PRIMARY KEY AUTOINCREMENT", "N/A", "Unique record transaction sequence ID"],
        ["timestamp_utc", "DATETIME", "NOT NULL, DEFAULT UTC", "ISO 8601", "Coordinated Universal Time timestamp"],
        ["timestamp_ist", "VARCHAR(32)", "NOT NULL", "IST String", "Localized Indian Standard Time string"],
        ["station_key", "VARCHAR(32)", "NULLABLE, INDEX", "Alphanumeric", "Foreign location key (e.g., 'delhi_ncr')"],
        ["prediction_domain", "VARCHAR(16)", "NOT NULL", "Enum ('air', 'water')", "Operational machine learning domain"],
        ["input_features_json", "TEXT", "NOT NULL", "JSON Object", "Raw input dictionary of submitted features"],
        ["predicted_metric", "FLOAT", "NOT NULL", "Index / Class", "Predicted continuous AQI or Potability (0/1)"],
        ["status_category", "VARCHAR(32)", "NOT NULL", "String Label", "NAAQS Category ('Moderate') or Potability label"],
        ["confidence_pct", "FLOAT", "NULLABLE", "Percentage (0-100)", "Calibrated Sigmoid posterior probability"],
        ["is_anomaly", "BOOLEAN", "NOT NULL, DEFAULT FALSE", "Boolean Flag", "Isolation Forest outlier classification flag"]
    ]
    t41 = doc.add_table(rows=len(t41_rows)+1, cols=5)
    t41.alignment = WD_TABLE_ALIGNMENT.CENTER
    t41.autofit = False
    c_w = [Inches(1.3), Inches(0.9), Inches(1.3), Inches(0.9), Inches(1.3)]
    for j, h in enumerate(t41_headers):
        c = t41.rows[0].cells[j]
        c.width = c_w[j]
        c.paragraphs[0].text = h
        set_font(c.paragraphs[0].runs[0], 'Times New Roman', 9, bold=True)
        set_cell_background(c, "E2E8F0")
    for i, row in enumerate(t41_rows):
        for j, val in enumerate(row):
            c = t41.rows[i+1].cells[j]
            c.width = c_w[j]
            c.paragraphs[0].text = val
            set_font(c.paragraphs[0].runs[0], 'Times New Roman', 8, bold=(j==0))

    # CHAPTER 5
    render_chapter_content(CH5_TITLE, CH5_SECTIONS)

    # Embed Figure 5.1 in Chapter 5
    if os.path.exists('report_assets/figure2_air_pipeline.png'):
        p_fig = doc.add_paragraph()
        p_fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig.paragraph_format.space_before = Pt(8)
        p_fig.paragraph_format.space_after = Pt(4)
        r_f = p_fig.add_run()
        r_f.add_picture('report_assets/figure2_air_pipeline.png', width=Inches(5.4))
        add_caption("Figure 5.1: Air Quality Telemetry Preprocessing and Regression Pipeline")

    # Embed Figure 5.2 in Chapter 5
    if os.path.exists('report_assets/figure3_water_pipeline.png'):
        p_fig = doc.add_paragraph()
        p_fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig.paragraph_format.space_before = Pt(8)
        p_fig.paragraph_format.space_after = Pt(4)
        r_f = p_fig.add_run()
        r_f.add_picture('report_assets/figure3_water_pipeline.png', width=Inches(5.4))
        add_caption("Figure 5.2: Water Potability Classification Pipeline and Sigmoid Calibration")

    # Embed Figure 5.3 in Chapter 5
    if os.path.exists('report_assets/figure4_anomaly_pipeline.png'):
        p_fig = doc.add_paragraph()
        p_fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig.paragraph_format.space_before = Pt(8)
        p_fig.paragraph_format.space_after = Pt(4)
        r_f = p_fig.add_run()
        r_f.add_picture('report_assets/figure4_anomaly_pipeline.png', width=Inches(5.4))
        add_caption("Figure 5.3: Unsupervised Isolation Forest Anomaly Detection Engine")

    # CHAPTER 6
    render_chapter_content(CH6_TITLE, CH6_SECTIONS)

    # Table 6.1 in Chapter 6
    add_caption("Table 6.1: Directory of 15 Live Indian Monitoring Stations and Coordinates")
    t61_headers = ["Station Key", "Station Display Name", "State / UT", "Zone Type", "Latitude", "Longitude", "Assigned Water Station"]
    t61_rows = [
        ["delhi_ncr", "Delhi NCR (Capital Region)", "Delhi", "Metropolitan", "28.6139° N", "77.2090° E", "Yamuna Wazirabad Station"],
        ["mumbai", "Mumbai Coastal Zone", "Maharashtra", "Metropolitan", "19.0760° N", "72.8777° E", "Vaitarna Lake Reservoir"],
        ["bengaluru", "Bengaluru Tech Corridor", "Karnataka", "Metropolitan", "12.9716° N", "77.5946° E", "Cauvery River Supply Station"],
        ["kolkata", "Kolkata Hooghly Zone", "West Bengal", "Metropolitan", "22.5726° N", "88.3639° E", "Palta Water Works Station"],
        ["chennai", "Chennai Urban Corridor", "Tamil Nadu", "Metropolitan", "13.0827° N", "80.2707° E", "Chembarambakkam Reservoir"],
        ["hyderabad", "Hyderabad Deccan Hub", "Telangana", "Metropolitan", "17.3850° N", "78.4867° E", "Osman Sagar Supply Station"],
        ["ahmedabad", "Ahmedabad Sabarmati Belt", "Gujarat", "Industrial", "23.0225° N", "72.5714° E", "Kotarpur Water Facility"],
        ["pune", "Pune Western Ghats", "Maharashtra", "Urban", "18.5204° N", "73.8567° E", "Khadakwasla Dam Station"],
        ["jaipur", "Jaipur Semi-Arid Basin", "Rajasthan", "Urban", "26.9124° N", "75.7873° E", "Bisalpur Dam Pipeline"],
        ["lucknow", "Lucknow Gomti Basin", "Uttar Pradesh", "Urban", "26.8467° N", "80.9462° E", "Aishbagh Water Facility"],
        ["varanasi", "Varanasi Holy Ganga Zone", "Uttar Pradesh", "Heritage", "25.3176° N", "82.9739° E", "Bhelupur Water Works"],
        ["patna", "Patna Gangetic Plain", "Bihar", "Urban", "25.5941° N", "85.1376° E", "Digha Ghat Treatment Plant"],
        ["guwahati", "Guwahati Brahmaputra Valley", "Assam", "Riverine", "26.1445° N", "91.7362° E", "Panbazar Intake Station"],
        ["kochi", "Kochi Coastal Backwaters", "Kerala", "Estuarine", "9.9312° N", "76.2673° E", "Aluva Water Treatment Plant"],
        ["chandigarh", "Chandigarh Sub-Himalayan", "Punjab / HR", "Planned", "30.7333° N", "76.7794° E", "Kajauli Water Works"]
    ]
    t61 = doc.add_table(rows=len(t61_rows)+1, cols=7)
    t61.alignment = WD_TABLE_ALIGNMENT.CENTER
    t61.autofit = False
    c_w6 = [Inches(0.8), Inches(1.4), Inches(0.8), Inches(0.7), Inches(0.6), Inches(0.6), Inches(1.1)]
    for j, h in enumerate(t61_headers):
        c = t61.rows[0].cells[j]
        c.width = c_w6[j]
        c.paragraphs[0].text = h
        set_font(c.paragraphs[0].runs[0], 'Times New Roman', 8, bold=True)
        set_cell_background(c, "E2E8F0")
    for i, row in enumerate(t61_rows):
        for j, val in enumerate(row):
            c = t61.rows[i+1].cells[j]
            c.width = c_w6[j]
            c.paragraphs[0].text = val
            set_font(c.paragraphs[0].runs[0], 'Times New Roman', 7, bold=(j==0))

    # CHAPTER 7
    render_chapter_content(CH7_TITLE, CH7_SECTIONS)

    # Table 7.1 in Chapter 7
    add_caption("Table 7.1: Comparative Evaluation Metrics for AQI Regression Models")
    t71_headers = ["Regression Model Architecture", "MAE (ug/m3)", "MSE", "RMSE (ug/m3)", "R2 Score", "Inference Latency"]
    t71_rows = [
        ["Ordinary Least Squares (Linear Regression)", "7.45", "92.14", "9.60", "0.887", "1.2 ms"],
        ["Ridge Regression (L2 Regularized)", "7.38", "90.52", "9.51", "0.889", "1.2 ms"],
        ["Decision Tree Regressor (CART)", "5.82", "64.18", "8.01", "0.912", "2.4 ms"],
        ["Gradient Boosted Trees (GBDT)", "4.35", "42.10", "6.49", "0.938", "8.6 ms"],
        ["Random Forest Regressor (EcoTrack Best)", "4.12", "39.44", "6.28", "0.942", "5.1 ms"]
    ]
    t71 = doc.add_table(rows=len(t71_rows)+1, cols=6)
    t71.alignment = WD_TABLE_ALIGNMENT.CENTER
    t71.autofit = False
    c_w7 = [Inches(1.8), Inches(0.8), Inches(0.7), Inches(0.8), Inches(0.8), Inches(0.8)]
    for j, h in enumerate(t71_headers):
        c = t71.rows[0].cells[j]
        c.width = c_w7[j]
        c.paragraphs[0].text = h
        set_font(c.paragraphs[0].runs[0], 'Times New Roman', 9, bold=True)
        set_cell_background(c, "E2E8F0")
    for i, row in enumerate(t71_rows):
        for j, val in enumerate(row):
            c = t71.rows[i+1].cells[j]
            c.width = c_w7[j]
            c.paragraphs[0].text = val
            is_best = (i == len(t71_rows)-1)
            set_font(c.paragraphs[0].runs[0], 'Times New Roman', 8, bold=is_best)
            if is_best:
                set_cell_background(c, "E6F4EA")

    # Table 7.2 in Chapter 7
    add_caption("Table 7.2: Comparative Performance Metrics for Water Potability Classifiers")
    t72_headers = ["Classification Algorithm", "Accuracy (%)", "Precision (%)", "Recall (%)", "F1-Score", "ROC-AUC Score"]
    t72_rows = [
        ["Logistic Regression (L2 Penalty)", "67.5%", "64.2%", "58.1%", "0.610", "0.694"],
        ["Support Vector Machine (RBF Kernel)", "74.2%", "72.8%", "68.4%", "0.705", "0.781"],
        ["K-Nearest Neighbors (k=7)", "69.1%", "66.4%", "61.2%", "0.637", "0.718"],
        ["Decision Tree Classifier (Gini)", "71.4%", "68.9%", "67.0%", "0.679", "0.722"],
        ["Random Forest Classifier (EcoTrack Best)", "79.8%", "78.2%", "76.6%", "0.774", "0.832"]
    ]
    t72 = doc.add_table(rows=len(t72_rows)+1, cols=6)
    t72.alignment = WD_TABLE_ALIGNMENT.CENTER
    t72.autofit = False
    for j, h in enumerate(t72_headers):
        c = t72.rows[0].cells[j]
        c.width = c_w7[j]
        c.paragraphs[0].text = h
        set_font(c.paragraphs[0].runs[0], 'Times New Roman', 9, bold=True)
        set_cell_background(c, "E2E8F0")
    for i, row in enumerate(t72_rows):
        for j, val in enumerate(row):
            c = t72.rows[i+1].cells[j]
            c.width = c_w7[j]
            c.paragraphs[0].text = val
            is_best = (i == len(t72_rows)-1)
            set_font(c.paragraphs[0].runs[0], 'Times New Roman', 8, bold=is_best)
            if is_best:
                set_cell_background(c, "E6F4EA")

    # Table 7.3 in Chapter 7
    add_caption("Table 7.3: System Latency, Throughput, and Concurrency Stress Benchmarks")
    t73_headers = ["Endpoint / Service", "10 Concurrency", "50 Concurrency", "100 Concurrency", "500 Concurrency", "Peak Throughput"]
    t73_rows = [
        ["POST /api/predict/air-quality", "8.2 ms", "12.4 ms", "18.4 ms", "38.2 ms", "1,240 req/sec"],
        ["POST /api/predict/water-potability", "9.1 ms", "14.1 ms", "21.6 ms", "42.8 ms", "1,180 req/sec"],
        ["GET /api/realtime/india-air", "98.4 ms", "104.2 ms", "112.4 ms", "168.0 ms", "420 req/sec"],
        ["GET /api/analytics/trends", "12.5 ms", "18.2 ms", "26.4 ms", "52.1 ms", "950 req/sec"],
        ["GET /api/history/export (CSV)", "24.1 ms", "36.8 ms", "54.2 ms", "118.5 ms", "380 req/sec"]
    ]
    t73 = doc.add_table(rows=len(t73_rows)+1, cols=6)
    t73.alignment = WD_TABLE_ALIGNMENT.CENTER
    t73.autofit = False
    for j, h in enumerate(t73_headers):
        c = t73.rows[0].cells[j]
        c.width = c_w7[j]
        c.paragraphs[0].text = h
        set_font(c.paragraphs[0].runs[0], 'Times New Roman', 9, bold=True)
        set_cell_background(c, "E2E8F0")
    for i, row in enumerate(t73_rows):
        for j, val in enumerate(row):
            c = t73.rows[i+1].cells[j]
            c.width = c_w7[j]
            c.paragraphs[0].text = val
            set_font(c.paragraphs[0].runs[0], 'Times New Roman', 8, bold=(j==0))

    # Embed User Interface Screenshots in Chapter 7
    if os.path.exists('report_assets/screen1_india_live.png'):
        p_fig = doc.add_paragraph()
        p_fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig.paragraph_format.space_before = Pt(8)
        p_fig.paragraph_format.space_after = Pt(4)
        r_f = p_fig.add_run()
        r_f.add_picture('report_assets/screen1_india_live.png', width=Inches(5.4))
        add_caption("Figure 7.1: Screen 1: Nationwide Live Ingestion Dashboard View")

    if os.path.exists('report_assets/screen2_air_simulator.png'):
        p_fig = doc.add_paragraph()
        p_fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig.paragraph_format.space_before = Pt(8)
        p_fig.paragraph_format.space_after = Pt(4)
        r_f = p_fig.add_run()
        r_f.add_picture('report_assets/screen2_air_simulator.png', width=Inches(5.4))
        add_caption("Figure 7.2: Screen 2: Air Quality Simulator with Interactive Sliders")

    if os.path.exists('report_assets/screen3_water_diagnostic.png'):
        p_fig = doc.add_paragraph()
        p_fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig.paragraph_format.space_before = Pt(8)
        p_fig.paragraph_format.space_after = Pt(4)
        r_f = p_fig.add_run()
        r_f.add_picture('report_assets/screen3_water_diagnostic.png', width=Inches(5.4))
        add_caption("Figure 7.3: Screen 3: Water Potability Diagnostic Workbench")

    if os.path.exists('report_assets/screen4_anomaly_explorer.png'):
        p_fig = doc.add_paragraph()
        p_fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig.paragraph_format.space_before = Pt(8)
        p_fig.paragraph_format.space_after = Pt(4)
        r_f = p_fig.add_run()
        r_f.add_picture('report_assets/screen4_anomaly_explorer.png', width=Inches(5.4))
        add_caption("Figure 7.4: Screen 4: Anomaly Explorer and Historical Audit Table")

    # CHAPTER 8
    render_chapter_content(CH8_TITLE, CH8_SECTIONS)

    # REFERENCES
    add_chapter_heading("REFERENCES")
    for ref in REFERENCES_DATA:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.first_line_indent = Inches(-0.3)
        p.paragraph_format.left_indent = Inches(0.3)
        r = p.add_run(ref)
        set_font(r, 'Times New Roman', 11, False, False, (0x1e, 0x29, 0x3b))

    # =========================================================================
    # SECTIONS 3 TO 7: ANNEXURES (Separate Roman Numerals: i, ii, iii ...)
    # =========================================================================
    annexure_list = [
        ("ANNEXURE I", ANNEXURE_I_DATA),
        ("ANNEXURE II", ANNEXURE_II_DATA),
        ("ANNEXURE III", ANNEXURE_III_DATA),
        ("ANNEXURE IV", ANNEXURE_IV_DATA),
        ("ANNEXURE V", ANNEXURE_V_DATA)
    ]

    for ann_name, ann_data in annexure_list:
        print(f"Generating {ann_name}...")
        sec_ann = doc.add_section(WD_SECTION.NEW_PAGE)
        apply_margins(sec_ann)
        add_footer_page_number(sec_ann, fmt='lowerRoman', start=1)

        add_chapter_heading(ann_data["title"])
        for sec in ann_data["sections"]:
            add_heading_1(sec["heading"])
            lines = sec["content"].split("\n")
            in_code = False
            code_buffer = []
            for line in lines:
                if line.startswith("{") or line.startswith("#") or line.startswith("server {") or line.startswith("[Unit]") or line.startswith("platform win32") or line.startswith("tests/") or line.startswith("Test ID:") or "def " in line or "class " in line or "import " in line:
                    code_buffer.append(line)
                else:
                    if code_buffer:
                        add_code_block("\n".join(code_buffer))
                        code_buffer = []
                    if line.strip():
                        add_para(line, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, space_before=4, space_after=6, first_line_indent=0.5)
            if code_buffer:
                add_code_block("\n".join(code_buffer))

    # Save complete document
    docx_filename = "EcoTrack_Complete_70Page_Report.docx"
    doc.save(docx_filename)
    print(f"DOCX Report successfully generated: {docx_filename}")

if __name__ == "__main__":
    create_complete_report()
