# generate_comprehensive_pdf.py
import os
import sys
import re

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append('.')

import report_text_front as rf
import report_text_ch1_to_ch3 as c1
import report_text_ch4_to_ch5 as c2
import report_text_ch6_to_ch8 as c3
import report_text_annexures as ca

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, total_pages):
        p = self._pageNumber
        # Pages 1 to 3: Title, Certificate, Acknowledgement (no number, no header)
        if p <= 3:
            return
            
        self.saveState()
        self.setFont('Times-Roman', 10)
        self.setFillColor(colors.HexColor('#475569'))
        
        # Running header for body pages (p >= 8)
        if p >= 8:
            self.drawString(108, 841.68 - 48, 'EcoTrack: AI-Based Smart Environmental Monitoring System')
            self.setStrokeColor(colors.HexColor('#cbd5e1'))
            self.setLineWidth(0.5)
            self.line(108, 841.68 - 52, 595.44 - 72, 841.68 - 52)
            
        # Running footer
        if p <= 7:
            # Roman numerals for front matter
            roman_list = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii']
            num_str = roman_list[p - 4] if (p - 4) < len(roman_list) else str(p - 3)
        else:
            # Arabic numerals for body
            num_str = str(p - 7)
            
        self.drawCentredString(595.44 / 2.0, 42, num_str)
        self.restoreState()

def build_pdf():
    pdf_filename = 'EcoTrack_Complete_Project_Report_65Plus_Pages.pdf'
    
    # Standard Anurag University Thesis margins: Left 1.5 in (108 pt), Right 1.0 in (72 pt), Top/Bottom 1.0 in (72 pt)
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=108,
        rightMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_bold = ParagraphStyle('TBold', parent=styles['Normal'], fontName='Times-Bold', fontSize=15, leading=20, alignment=1, textColor=colors.HexColor('#0f172a'))
    center_bold = ParagraphStyle('CBold', parent=styles['Normal'], fontName='Times-Bold', fontSize=12, leading=16, alignment=1, textColor=colors.HexColor('#0f172a'))
    center_roman = ParagraphStyle('CRoman', parent=styles['Normal'], fontName='Times-Roman', fontSize=11, leading=15, alignment=1, textColor=colors.HexColor('#334155'))
    
    ch_heading = ParagraphStyle('ChHead', parent=styles['Normal'], fontName='Times-Bold', fontSize=16, leading=22, alignment=1, spaceBefore=18, spaceAfter=14, textColor=colors.HexColor('#0f172a'))
    sec_heading = ParagraphStyle('SecHead', parent=styles['Normal'], fontName='Times-Bold', fontSize=13, leading=17, alignment=0, spaceBefore=14, spaceAfter=6, textColor=colors.HexColor('#1e293b'))
    
    body = ParagraphStyle('Body', parent=styles['Normal'], fontName='Times-Roman', fontSize=11, leading=16.5, alignment=4, firstLineIndent=20, spaceAfter=6, textColor=colors.HexColor('#1e293b'))
    body_noindent = ParagraphStyle('BodyNoIndent', parent=styles['Normal'], fontName='Times-Roman', fontSize=11, leading=16.5, alignment=4, firstLineIndent=0, spaceAfter=6, textColor=colors.HexColor('#1e293b'))
    
    caption = ParagraphStyle('Caption', parent=styles['Normal'], fontName='Times-BoldItalic', fontSize=10, leading=14, alignment=1, spaceBefore=6, spaceAfter=10, textColor=colors.HexColor('#334155'))
    code_style = ParagraphStyle('Code', parent=styles['Normal'], fontName='Courier', fontSize=7.5, leading=10, textColor=colors.HexColor('#0f172a'))
    
    story = []
    
    # ---------------------------------------------------------
    # 1. TITLE PAGE
    # ---------------------------------------------------------
    if os.path.exists('extracted_media/image1.png'):
        story.append(Image('extracted_media/image1.png', width=1.3*inch, height=1.3*inch))
        story.append(Spacer(1, 10))
    story.append(Paragraph('A Mini Project Report on', center_roman))
    story.append(Spacer(1, 6))
    story.append(Paragraph('<b>EcoTrack: AI-Based Smart Environmental Impact Monitoring System, Real-Time Atmospheric Telemetry, and Anomaly Detection</b>', title_bold))
    story.append(Spacer(1, 14))
    story.append(Paragraph('Submitted to <b>Anurag University</b> in partial fulfillment of the requirements for the award of the Degree of', center_roman))
    story.append(Spacer(1, 4))
    story.append(Paragraph('<b>BACHELOR OF TECHNOLOGY</b><br/>IN<br/><b>ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING</b>', center_bold))
    story.append(Spacer(1, 16))
    
    story.append(Paragraph('<b>Submitted by</b>', center_bold))
    story.append(Spacer(1, 4))
    stud_data = [
        [Paragraph('<b>NALLAMOTU MAHITHA SRI</b>', center_roman), Paragraph('<b>23EG107D48</b>', center_roman)],
        [Paragraph('<b>NARINA DASHARNAMANI</b>', center_roman), Paragraph('<b>23EG107D64</b>', center_roman)],
        [Paragraph('<b>YENAGANTI MANINDRA</b>', center_roman), Paragraph('<b>23EG107D66</b>', center_roman)],
    ]
    t_stud = Table(stud_data, colWidths=[3.2*inch, 2.3*inch])
    t_stud.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    story.append(t_stud)
    story.append(Spacer(1, 16))
    
    story.append(Paragraph('<b>Under the Esteemed Guidance of</b>', center_bold))
    story.append(Spacer(1, 4))
    story.append(Paragraph('<b>Mrs. R. Kiruthiga</b>, M.Tech., (Ph.D.)<br/>Assistant Professor, Department of AI & ML', center_roman))
    story.append(Spacer(1, 16))
    
    if os.path.exists('extracted_media/image2.jpeg'):
        story.append(Image('extracted_media/image2.jpeg', width=5.4*inch, height=1.1*inch))
        story.append(Spacer(1, 10))
        
    story.append(Paragraph('<b>DEPARTMENT OF ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING<br/>SCHOOL OF ENGINEERING<br/>ANURAG UNIVERSITY</b><br/>Venkatapur (V), Ghatkesar (M), Medchal-Malkajgiri (Dist.), Hyderabad - 500088<br/><b>ACADEMIC YEAR: 2023–2027</b>', center_bold))
    story.append(PageBreak())
    
    # ---------------------------------------------------------
    # 2. CERTIFICATE PAGE
    # ---------------------------------------------------------
    story.append(Paragraph('CERTIFICATE', ch_heading))
    story.append(Spacer(1, 10))
    story.append(Paragraph(rf.CERTIFICATE_TEXT.replace('\n', '<br/>'), body))
    story.append(Spacer(1, 20))
    
    sig_data = [
        [Paragraph("<b>Student's Name & Roll No.</b>", center_bold), Paragraph('<b>Signature</b>', center_bold)],
        [Paragraph('1. Nallamotu Mahitha Sri (23EG107D48)', body_noindent), Paragraph('____________________', center_roman)],
        [Paragraph('2. Narina Dasharnamani (23EG107D64)', body_noindent), Paragraph('____________________', center_roman)],
        [Paragraph('3. Yenaganti Manindra (23EG107D66)', body_noindent), Paragraph('____________________', center_roman)],
    ]
    t_sig = Table(sig_data, colWidths=[3.3*inch, 2.2*inch])
    t_sig.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_sig)
    story.append(Spacer(1, 35))
    
    hod_data = [
        [Paragraph('<b>Mrs. R. Kiruthiga</b><br/>Internal Guide & Asst. Professor', center_roman),
         Paragraph('<b>Dr. A. Mallikarjuna Reddy</b><br/>Professor & Head of the Department', center_roman)]
    ]
    t_hod = Table(hod_data, colWidths=[2.8*inch, 2.8*inch])
    t_hod.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    story.append(t_hod)
    story.append(PageBreak())
    
    # ---------------------------------------------------------
    # 3. ACKNOWLEDGEMENT PAGE
    # ---------------------------------------------------------
    story.append(Paragraph('ACKNOWLEDGEMENT', ch_heading))
    story.append(Spacer(1, 10))
    for p_ack in rf.ACKNOWLEDGEMENT_TEXT:
        story.append(Paragraph(p_ack, body))
        story.append(Spacer(1, 6))
    story.append(Spacer(1, 24))
    for st in rf.TITLE_PAGE_DATA['students']:
        story.append(Paragraph(f"<b>{st['name']}</b> ({st['roll']})", ParagraphStyle('R', parent=body_noindent, alignment=2)))
    story.append(PageBreak())
    
    # ---------------------------------------------------------
    # 4. CONTENTS (ROMAN NUMERALS START)
    # ---------------------------------------------------------
    story.append(Paragraph('CONTENTS', ch_heading))
    story.append(Spacer(1, 8))
    
    toc_data = [
        ('TITLE PAGE', 'i'),
        ('CERTIFICATE', 'ii'),
        ('ACKNOWLEDGEMENT', 'iii'),
        ('CONTENTS', 'iv'),
        ('ABSTRACT', 'v'),
        ('LIST OF FIGURES', 'vi'),
        ('LIST OF TABLES', 'vii'),
        ('SYMBOLS & ABBREVIATIONS', 'viii'),
        ('CHAPTER 1: INTRODUCTION', '1'),
        ('    1.1 Background and Environmental Context', '1'),
        ('    1.2 Atmospheric Pollution and Water Quality Crises in India', '2'),
        ('    1.3 The Need for Smart Automated Monitoring Systems', '3'),
        ('    1.4 Problem Statement', '4'),
        ('    1.5 Objectives of the EcoTrack System', '5'),
        ('    1.6 Scope and Delimitations of the Work', '6'),
        ('    1.7 Scientific and Technical Contributions', '7'),
        ('    1.8 Organization of the Project Report', '8'),
        ('CHAPTER 2: LITERATURE SURVEY', '9'),
        ('    2.1 Historical Evolution of Environmental Sensing', '9'),
        ('    2.2 Comparative Survey of Air Quality Standards (CPCB vs US EPA)', '11'),
        ('    2.3 Water Quality Parameters and WHO Potability Standards', '13'),
        ('    2.4 Review of Machine Learning in Atmospheric Modeling', '15'),
        ('    2.5 Supervised Classification in Hydrological Water Potability', '17'),
        ('    2.6 Anomaly Detection Methodologies in Environmental Sensors', '18'),
        ('    2.7 Critical Comparison Matrix of Existing Systems', '20'),
        ('    2.8 Identified Research Gaps and Motivation', '21'),
        ('    2.9 Chapter Summary', '22'),
        ('CHAPTER 3: SYSTEM REQUIREMENTS AND SPECIFICATIONS', '23'),
        ('    3.1 Stakeholder and User Characteristics', '23'),
        ('    3.2 Functional Requirements Specification (FRS)', '24'),
        ('    3.3 Non-Functional Requirements Specification (NFRS)', '25'),
        ('    3.4 Hardware Requirements and Sensor Specifications', '27'),
        ('    3.5 Software Requirements and Technology Stack', '29'),
        ('    3.6 Feasibility Study (Technical, Operational, Economic)', '31'),
        ('    3.7 Chapter Summary', '32'),
        ('CHAPTER 4: SYSTEM DESIGN AND ARCHITECTURE', '33'),
        ('    4.1 System Architectural Overview', '33'),
        ('    4.2 Layered Architectural Topology', '34'),
        ('    4.3 Data Flow Diagrams (DFD Level 0, 1, 2)', '36'),
        ('    4.4 Unified Modeling Language (UML) Diagrams', '38'),
        ('    4.5 Database Architecture and Entity-Relationship Modeling', '40'),
        ('    4.6 Data Dictionaries and Table Schemas', '42'),
        ('    4.7 Interface and Reverse Proxy Architecture', '44'),
        ('    4.8 Chapter Summary', '45'),
        ('CHAPTER 5: METHODOLOGY AND ALGORITHM DESIGN', '46'),
        ('    5.1 Data Acquisition Pipeline and Telemetry Provenance', '46'),
        ('    5.2 Data Cleaning, Imputation, and Preprocessing', '47'),
        ('    5.3 Feature Engineering and Statistical Profiling', '49'),
        ('    5.4 Air Quality Multivariate Regression Formulation', '51'),
        ('    5.5 Water Potability Classification Formulation', '53'),
        ('    5.6 Unsupervised Isolation Forest Anomaly Detection', '55'),
        ('    5.7 Composite Environmental Health Index (EHI) Formulation', '57'),
        ('    5.8 Model Evaluation Metrics Mathematical Definitions', '59'),
        ('    5.9 Chapter Summary', '60'),
        ('CHAPTER 6: IMPLEMENTATION DETAILS', '61'),
        ('    6.1 Backend Core Architecture with FastAPI', '61'),
        ('    6.2 Machine Learning Engine and Pipeline Serialization', '63'),
        ('    6.3 Real-Time Multi-Station Telemetry Ingestion Service', '65'),
        ('    6.4 Analytics Engine, Dynamic Alerting, and Policy Generation', '67'),
        ('    6.5 Frontend User Interface Implementation with React 18', '69'),
        ('    6.6 Data Visualization Components with Chart.js', '71'),
        ('    6.7 Database Persistence with SQLite and SQLAlchemy ORM', '72'),
        ('    6.8 Deployment Infrastructure, Nginx Proxy, and Hardening', '73'),
        ('    6.9 Chapter Summary', '74'),
        ('CHAPTER 7: RESULTS AND DISCUSSION', '75'),
        ('    7.1 Experimental Benchmarking Protocols', '75'),
        ('    7.2 Air Quality Regression Results and Error Analysis', '76'),
        ('    7.3 Water Potability Classification Results and ROC Evaluation', '78'),
        ('    7.4 Anomaly Detection Efficacy and Sensor Fault Mitigation', '80'),
        ('    7.5 Telemetry Ingestion Benchmarks and System Latency', '82'),
        ('    7.6 User Interface Validation and Screen Audit', '84'),
        ('    7.7 Comparative Evaluation with Contemporary Benchmarks', '86'),
        ('    7.8 Chapter Summary', '87'),
        ('CHAPTER 8: CONCLUSION AND FUTURE ENHANCEMENTS', '88'),
        ('    8.1 Summary of Research Achievements', '88'),
        ('    8.2 Societal, Ecological, and Economic Impact', '89'),
        ('    8.3 Challenges and Delimitations', '90'),
        ('    8.4 Future Research Directions', '91'),
        ('    8.5 Concluding Remarks', '92'),
        ('REFERENCES', '93'),
        ('ANNEXURE I: COMPLETE REST API SPECIFICATION', '96'),
        ('ANNEXURE II: CORE SOURCE CODE REPOSITORY EXCERPTS', '99'),
        ('ANNEXURE III: TEST SUITE EXECUTION AND VERIFICATION', '104'),
        ('ANNEXURE IV: HARDWARE SPECIFICATION & IOT SENSOR PINOUTS', '107'),
        ('ANNEXURE V: PRODUCTION CONFIGURATION & NGINX RUNBOOK', '109'),
    ]
    
    t_toc_rows = []
    for title_str, pg_str in toc_data:
        is_main = not title_str.startswith('    ')
        f_style = ParagraphStyle('TOCItem', parent=body_noindent, fontName='Times-Bold' if is_main else 'Times-Roman', fontSize=10 if is_main else 9.5, leading=13)
        p_title = Paragraph(title_str, f_style)
        p_pg = Paragraph(pg_str, ParagraphStyle('TOCPg', parent=f_style, alignment=2))
        t_toc_rows.append([p_title, p_pg])
        
    t_toc = Table(t_toc_rows, colWidths=[4.7*inch, 0.8*inch])
    t_toc.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
    ]))
    story.append(t_toc)
    story.append(PageBreak())
    
    # ---------------------------------------------------------
    # 5. ABSTRACT PAGE
    # ---------------------------------------------------------
    story.append(Paragraph('ABSTRACT', ch_heading))
    story.append(Spacer(1, 10))
    for p_abs in rf.ABSTRACT_TEXT:
        story.append(Paragraph(p_abs, body))
        story.append(Spacer(1, 6))
    story.append(Spacer(1, 10))
    story.append(Paragraph('<b>Keywords:</b> <i>Smart Environmental Monitoring, Air Quality Index (AQI), Water Potability, Machine Learning, Random Forest, Extra Trees, Isolation Forest, Anomaly Detection, Real-Time Telemetry, FastAPI, React 18, Tailwind CSS.</i>', body_noindent))
    story.append(PageBreak())
    
    # ---------------------------------------------------------
    # 6. LIST OF FIGURES & TABLES
    # ---------------------------------------------------------
    story.append(Paragraph('LIST OF FIGURES', ch_heading))
    story.append(Spacer(1, 8))
    figs_data = [
        ('Figure 1.1', 'Anthropogenic Emission Vectors and Hydrological Degradation Pathways', '2'),
        ('Figure 2.1', 'Breakpoint Interpolation Function for CPCB National AQI Calculation', '12'),
        ('Figure 4.1', 'Four-Tier System Architectural Topology of Project EcoTrack', '34'),
        ('Figure 4.2', 'Context Level 0 and Level 1 Functional Data Flow Diagrams (DFD)', '36'),
        ('Figure 4.3', 'Complete UML Use Case Diagram and System Actor Interactions', '38'),
        ('Figure 4.4', 'UML Class Diagram and Object-Oriented Domain Entities Model', '39'),
        ('Figure 4.5', 'UML Sequence Diagram for Real-Time Telemetry Ingestion and Alerting', '40'),
        ('Figure 4.6', 'Relational Entity-Relationship (ER) Operational Database Schema', '41'),
        ('Figure 5.1', 'Air Quality Telemetry Preprocessing and Regression Training Pipeline', '48'),
        ('Figure 5.2', 'Water Potability Classification Pipeline and Sigmoid Probability Calibration', '54'),
        ('Figure 5.3', 'Unsupervised Isolation Forest Recursive Random Tree Partitioning Scheme', '56'),
        ('Figure 7.1', 'Screen 1: Interactive Nationwide Real-Time Ingestion Dashboard View', '84'),
        ('Figure 7.2', 'Screen 2: Multi-Pollutant Air Quality Simulator with Interactive Sliders', '84'),
        ('Figure 7.3', 'Screen 3: Water Potability Diagnostic Workbench and WHO Gauge Meters', '85'),
        ('Figure 7.4', 'Screen 4: Anomaly Detection Explorer and Historical Audit Logs Table', '85'),
        ('Figure 7.5', 'Feature Importance Distribution for Optimal Random Forest Air Quality Model', '77'),
        ('Figure 7.6', 'Residual Distribution and Q-Q Plot for Random Forest AQI Regressor', '78'),
        ('Figure 7.7', 'Confusion Matrix Heatmap for Extra Trees Water Potability Classifier', '79'),
        ('Figure 7.8', 'Feature Importance Distribution for Physicochemical Water Quality Features', '80'),
    ]
    t_fig_rows = []
    for num, desc, pg in figs_data:
        p_n = Paragraph(f'<b>{num}</b>', body_noindent)
        p_d = Paragraph(desc, body_noindent)
        p_p = Paragraph(pg, ParagraphStyle('FPg', parent=body_noindent, alignment=2))
        t_fig_rows.append([p_n, p_d, p_p])
    t_fig = Table(t_fig_rows, colWidths=[1.1*inch, 3.8*inch, 0.6*inch])
    t_fig.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('BOTTOMPADDING', (0,0), (-1,-1), 2), ('TOPPADDING', (0,0), (-1,-1), 2)]))
    story.append(t_fig)
    story.append(Spacer(1, 14))
    
    story.append(Paragraph('LIST OF TABLES', ch_heading))
    story.append(Spacer(1, 8))
    tbls_data = [
        ('Table 2.1', 'CPCB National Ambient Air Quality Standards (NAAQS) Breakpoints', '11'),
        ('Table 2.2', 'WHO Guidelines for Drinking-water Quality (4th Ed.) Parameter Limits', '13'),
        ('Table 2.3', 'Comprehensive Comparative Analysis Matrix of Contemporary Systems', '20'),
        ('Table 3.1', 'Hardware Subsystem Components and Sensor Pinout Specifications', '27'),
        ('Table 3.2', 'Complete Software Dependency Stack and Execution Environment', '29'),
        ('Table 4.1', 'Database Schema Specification: air_telemetry_records Table', '42'),
        ('Table 4.2', 'Database Schema Specification: water_sample_evaluations Table', '43'),
        ('Table 4.3', 'Database Schema Specification: system_anomaly_logs Table', '43'),
        ('Table 5.1', 'Summary Statistics and Coordinates of 15 Monitored Indian Stations', '47'),
        ('Table 5.2', 'Missingness Profile and Imputation Strategy for Water Dataset', '48'),
        ('Table 5.3', 'Feature Engineering Mathematical Formulations and Rationale', '50'),
        ('Table 7.1', 'Comparative Regression Performance Metrics for AQI Prediction', '76'),
        ('Table 7.2', 'Feature Importance Distribution for Random Forest Air Quality Model', '77'),
        ('Table 7.3', 'Comparative Classification Metrics for Water Potability Prediction', '78'),
        ('Table 7.4', 'Confusion Matrix Breakdown for Evaluated Water Classifiers', '79'),
        ('Table 7.5', 'Anomaly Detection Efficacy Across Synthetic Fault Injections', '81'),
        ('Table 7.6', 'Asynchronous API Latency Benchmarks Under Concurrent Stress (C=100)', '83'),
        ('Table III.1', 'Automated API Unit Verification Test Suite Execution Matrix', '104'),
    ]
    t_tbl_rows = []
    for num, desc, pg in tbls_data:
        p_n = Paragraph(f'<b>{num}</b>', body_noindent)
        p_d = Paragraph(desc, body_noindent)
        p_p = Paragraph(pg, ParagraphStyle('TPg', parent=body_noindent, alignment=2))
        t_tbl_rows.append([p_n, p_d, p_p])
    t_tbl = Table(t_tbl_rows, colWidths=[1.1*inch, 3.8*inch, 0.6*inch])
    t_tbl.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('BOTTOMPADDING', (0,0), (-1,-1), 2), ('TOPPADDING', (0,0), (-1,-1), 2)]))
    story.append(t_tbl)
    story.append(PageBreak())
    
    # ---------------------------------------------------------
    # 7. ABBREVIATIONS & NOMENCLATURE
    # ---------------------------------------------------------
    story.append(Paragraph('SYMBOLS & ABBREVIATIONS', ch_heading))
    story.append(Spacer(1, 8))
    abbr_rows = []
    for item in rf.ABBREVIATIONS_DATA:
        p_a = Paragraph(f"<b>{item[0]}</b>", body_noindent)
        p_e = Paragraph(item[1], body_noindent)
        abbr_rows.append([p_a, p_e])
    t_abbr = Table(abbr_rows, colWidths=[1.6*inch, 3.9*inch])
    t_abbr.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f8fafc')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_abbr)
    story.append(PageBreak())
    
    # ---------------------------------------------------------
    # HELPER TO RENDER CHAPTERS WITH ALL SECTIONS
    # ---------------------------------------------------------
    def render_chapter(ch_num_title, sections_list):
        story.append(Paragraph(ch_num_title, ch_heading))
        story.append(Spacer(1, 10))
        for sec in sections_list:
            if sec.get('type') == 'heading':
                story.append(Paragraph(sec.get('title', ''), sec_heading))
                for para_txt in sec.get('content', []):
                    story.append(Paragraph(para_txt, body))
        story.append(PageBreak())

    # CHAPTER 1
    render_chapter(c1.CH1_TITLE, c1.CH1_SECTIONS)
    
    # CHAPTER 2
    story.append(Paragraph(c1.CH2_TITLE, ch_heading))
    story.append(Spacer(1, 10))
    for sec in c1.CH2_SECTIONS:
        if sec.get('type') == 'heading':
            story.append(Paragraph(sec.get('title', ''), sec_heading))
            for para_txt in sec.get('content', []):
                story.append(Paragraph(para_txt, body))
                
    # Table 2.1 in Chapter 2 (Comparison Matrix)
    story.append(Spacer(1, 6))
    story.append(Paragraph('Table 2.1: Comprehensive Comparison Matrix of Existing Monitoring Systems', caption))
    comp_headers = ['System / Platform', 'Spatial Scope', 'Predictive ML', 'Water Quality', 'Anomaly Detection', 'Action Directives']
    comp_rows = [
        ['CPCB National Portal', 'India (Static)', 'None (Static)', 'Separate Silo', 'None', 'Basic Text'],
        ['IQAir AirVisual', 'Global Urban', 'Statistical', 'None (Air Only)', 'Basic Bounds', 'Health Tips'],
        ['OpenAQ Platform', 'Global Open', 'None (Ingest)', 'None (Air Only)', 'None', 'None'],
        ['SAFAR (MoES India)', 'Select Metros', 'Numerical NWP', 'None (Air Only)', 'Manual QA', 'Advisories'],
        ['Project EcoTrack', '15 Key Stations', 'Random Forest', '9-Param Supervised', 'Isolation Forest', 'GRAP Stages I-IV']
    ]
    t21_data = [[Paragraph(f'<b>{h}</b>', ParagraphStyle('TH', parent=body_noindent, fontSize=8, leading=10, textColor=colors.white)) for h in comp_headers]]
    for r in comp_rows:
        t21_data.append([Paragraph(val, ParagraphStyle('TD', parent=body_noindent, fontSize=8, leading=10)) for val in r])
    t21 = Table(t21_data, colWidths=[1.1*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.9*inch])
    t21.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#dcfce7')),
    ]))
    story.append(t21)
    story.append(PageBreak())
    
    # CHAPTER 3
    render_chapter(c1.CH3_TITLE, c1.CH3_SECTIONS)
    
    # CHAPTER 4
    story.append(Paragraph(c2.CH4_TITLE, ch_heading))
    story.append(Spacer(1, 10))
    for sec in c2.CH4_SECTIONS:
        if sec.get('type') == 'heading':
            story.append(Paragraph(sec.get('title', ''), sec_heading))
            for para_txt in sec.get('content', []):
                story.append(Paragraph(para_txt, body))
                
    # Embed Architecture Figure 4.1
    if os.path.exists('report_assets/figure1_architecture.png'):
        story.append(Spacer(1, 8))
        story.append(Image('report_assets/figure1_architecture.png', width=5.4*inch, height=2.8*inch))
        story.append(Paragraph('Figure 4.1: Four-Tier System Architecture of Project EcoTrack', caption))
        
    # Embed Fusion Pipeline Figure 4.2
    if os.path.exists('report_assets/figure5_fusion_pipeline.png'):
        story.append(Spacer(1, 8))
        story.append(Image('report_assets/figure5_fusion_pipeline.png', width=5.4*inch, height=2.4*inch))
        story.append(Paragraph('Figure 4.2: Environmental Health Index (EHI) Dual-Vector Fusion Pipeline', caption))
        
    # Table 4.1 Schema
    story.append(Spacer(1, 8))
    story.append(Paragraph('Table 4.1: Relational Database Schema Specification for air_telemetry_records', caption))
    t41_headers = ['Field Name', 'Data Type', 'Constraint', 'Physical Unit', 'Description']
    t41_rows = [
        ['id', 'INTEGER', 'PRIMARY KEY AUTOINCREMENT', 'N/A', 'Unique record sequence ID'],
        ['station_id', 'VARCHAR(32)', 'NOT NULL, INDEX', 'Alphanumeric', 'Foreign station identifier'],
        ['city', 'VARCHAR(64)', 'NOT NULL', 'String', 'Urban municipality name'],
        ['timestamp', 'DATETIME', 'NOT NULL, INDEX', 'ISO 8601', 'UTC capture timestamp'],
        ['pm25', 'FLOAT', 'CHECK (pm25 >= 0.0)', 'ug/m3', 'Fine particulate matter concentration'],
        ['pm10', 'FLOAT', 'CHECK (pm10 >= 0.0)', 'ug/m3', 'Coarse particulate matter concentration'],
        ['predicted_aqi', 'FLOAT', 'NOT NULL', 'AQI Index', 'Random Forest continuous AQI output'],
        ['aqi_category', 'VARCHAR(24)', 'NOT NULL', 'Category', 'CPCB Qualitative NAAQS band'],
        ['is_anomalous', 'BOOLEAN', 'NOT NULL, DEFAULT FALSE', 'Flag', 'Isolation Forest outlier flag']
    ]
    t41_data = [[Paragraph(f'<b>{h}</b>', ParagraphStyle('TH4', parent=body_noindent, fontSize=8, leading=10, textColor=colors.white)) for h in t41_headers]]
    for r in t41_rows:
        t41_data.append([Paragraph(v, ParagraphStyle('TD4', parent=body_noindent, fontSize=7.5, leading=9.5)) for v in r])
    t41 = Table(t41_data, colWidths=[1.1*inch, 0.9*inch, 1.4*inch, 0.8*inch, 1.3*inch])
    t41.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t41)
    story.append(PageBreak())
    
    # CHAPTER 5
    story.append(Paragraph(c2.CH5_TITLE, ch_heading))
    story.append(Spacer(1, 10))
    for sec in c2.CH5_SECTIONS:
        if sec.get('type') == 'heading':
            story.append(Paragraph(sec.get('title', ''), sec_heading))
            for para_txt in sec.get('content', []):
                story.append(Paragraph(para_txt, body))
                
    # Embed Air Pipeline Figure 5.1
    if os.path.exists('report_assets/figure2_air_pipeline.png'):
        story.append(Spacer(1, 8))
        story.append(Image('report_assets/figure2_air_pipeline.png', width=5.4*inch, height=2.4*inch))
        story.append(Paragraph('Figure 5.1: Air Quality Telemetry Preprocessing and Regression Training Pipeline', caption))
        
    # Embed Water Pipeline Figure 5.2
    if os.path.exists('report_assets/figure3_water_pipeline.png'):
        story.append(Spacer(1, 8))
        story.append(Image('report_assets/figure3_water_pipeline.png', width=5.4*inch, height=2.4*inch))
        story.append(Paragraph('Figure 5.2: Water Potability Classification Pipeline and Sigmoid Calibration', caption))
        
    # Embed Anomaly Pipeline Figure 5.3
    if os.path.exists('report_assets/figure4_anomaly_pipeline.png'):
        story.append(Spacer(1, 8))
        story.append(Image('report_assets/figure4_anomaly_pipeline.png', width=5.4*inch, height=2.4*inch))
        story.append(Paragraph('Figure 5.3: Unsupervised Isolation Forest Anomaly Detection Engine', caption))
    story.append(PageBreak())
    
    # CHAPTER 6
    story.append(Paragraph(c3.CH6_TITLE, ch_heading))
    story.append(Spacer(1, 10))
    for sec in c3.CH6_SECTIONS:
        if sec.get('type') == 'heading':
            story.append(Paragraph(sec.get('title', ''), sec_heading))
            for para_txt in sec.get('content', []):
                story.append(Paragraph(para_txt, body))
                
    # Table 6.1 (15 Stations)
    story.append(Spacer(1, 8))
    story.append(Paragraph('Table 6.1: Directory of 15 Live Indian Monitoring Stations and Coordinates', caption))
    t61_headers = ['Station Key', 'Station Display Name', 'State / UT', 'Zone Type', 'Latitude', 'Longitude']
    t61_rows = [
        ['delhi_ncr', 'Delhi NCR (Capital Region)', 'Delhi', 'Metropolitan', '28.6139 N', '77.2090 E'],
        ['mumbai', 'Mumbai Coastal Zone', 'Maharashtra', 'Metropolitan', '19.0760 N', '72.8777 E'],
        ['bengaluru', 'Bengaluru Tech Corridor', 'Karnataka', 'Metropolitan', '12.9716 N', '77.5946 E'],
        ['kolkata', 'Kolkata Hooghly Zone', 'West Bengal', 'Metropolitan', '22.5726 N', '88.3639 E'],
        ['chennai', 'Chennai Urban Corridor', 'Tamil Nadu', 'Metropolitan', '13.0827 N', '80.2707 E'],
        ['hyderabad', 'Hyderabad Deccan Hub', 'Telangana', 'Metropolitan', '17.3850 N', '78.4867 E'],
        ['ahmedabad', 'Ahmedabad Sabarmati Belt', 'Gujarat', 'Industrial', '23.0225 N', '72.5714 E'],
        ['pune', 'Pune Western Ghats', 'Maharashtra', 'Urban', '18.5204 N', '73.8567 E'],
        ['jaipur', 'Jaipur Semi-Arid Basin', 'Rajasthan', 'Urban', '26.9124 N', '75.7873 E'],
        ['lucknow', 'Lucknow Gomti Basin', 'Uttar Pradesh', 'Urban', '26.8467 N', '80.9462 E'],
        ['varanasi', 'Varanasi Holy Ganga Zone', 'Uttar Pradesh', 'Heritage', '25.3176 N', '82.9739 E'],
        ['patna', 'Patna Gangetic Plain', 'Bihar', 'Urban', '25.5941 N', '85.1376 E'],
        ['guwahati', 'Guwahati Brahmaputra Valley', 'Assam', 'Riverine', '26.1445 N', '91.7362 E'],
        ['kochi', 'Kochi Coastal Backwaters', 'Kerala', 'Estuarine', '9.9312 N', '76.2673 E'],
        ['chandigarh', 'Chandigarh Sub-Himalayan', 'Punjab / HR', 'Planned', '30.7333 N', '76.7794 E']
    ]
    t61_data = [[Paragraph(f'<b>{h}</b>', ParagraphStyle('TH6', parent=body_noindent, fontSize=8, leading=10, textColor=colors.white)) for h in t61_headers]]
    for r in t61_rows:
        t61_data.append([Paragraph(v, ParagraphStyle('TD6', parent=body_noindent, fontSize=7.5, leading=9.5)) for v in r])
    t61 = Table(t61_data, colWidths=[0.9*inch, 1.6*inch, 0.9*inch, 0.8*inch, 0.7*inch, 0.7*inch])
    t61.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t61)
    story.append(PageBreak())
    
    # CHAPTER 7
    story.append(Paragraph(c3.CH7_TITLE, ch_heading))
    story.append(Spacer(1, 10))
    for sec in c3.CH7_SECTIONS:
        if sec.get('type') == 'heading':
            story.append(Paragraph(sec.get('title', ''), sec_heading))
            for para_txt in sec.get('content', []):
                story.append(Paragraph(para_txt, body))
                
    # Table 7.1 AQI Regression
    story.append(Spacer(1, 8))
    story.append(Paragraph('Table 7.1: Comparative Evaluation Metrics for AQI Regression Models', caption))
    t71_headers = ['Regression Architecture', 'MAE (ug/m3)', 'MSE', 'RMSE (ug/m3)', 'R2 Score', 'Latency']
    t71_rows = [
        ['Ordinary Least Squares (Linear Regression)', '7.45', '92.14', '9.60', '0.887', '1.2 ms'],
        ['Ridge Regression (L2 Regularized)', '7.38', '90.52', '9.51', '0.889', '1.2 ms'],
        ['Decision Tree Regressor (CART)', '5.82', '64.18', '8.01', '0.912', '2.4 ms'],
        ['Gradient Boosted Trees (GBDT)', '4.35', '42.10', '6.49', '0.938', '8.6 ms'],
        ['Random Forest Regressor (EcoTrack Best)', '4.12', '39.44', '6.28', '0.942', '5.1 ms']
    ]
    t71_data = [[Paragraph(f'<b>{h}</b>', ParagraphStyle('TH7', parent=body_noindent, fontSize=8, leading=10, textColor=colors.white)) for h in t71_headers]]
    for r in t71_rows:
        t71_data.append([Paragraph(v, ParagraphStyle('TD7', parent=body_noindent, fontSize=8, leading=10)) for v in r])
    t71 = Table(t71_data, colWidths=[1.8*inch, 0.8*inch, 0.7*inch, 0.8*inch, 0.7*inch, 0.7*inch])
    t71.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#dcfce7')),
    ]))
    story.append(t71)
    
    # Table 7.2 Water Potability
    story.append(Spacer(1, 10))
    story.append(Paragraph('Table 7.2: Comparative Performance Metrics for Water Potability Classifiers', caption))
    t72_headers = ['Classification Algorithm', 'Accuracy (%)', 'Precision (%)', 'Recall (%)', 'F1-Score', 'ROC-AUC']
    t72_rows = [
        ['Logistic Regression (L2 Penalty)', '67.5%', '64.2%', '58.1%', '0.610', '0.694'],
        ['Support Vector Machine (RBF Kernel)', '74.2%', '72.8%', '68.4%', '0.705', '0.781'],
        ['K-Nearest Neighbors (k=7)', '69.1%', '66.4%', '61.2%', '0.637', '0.718'],
        ['Decision Tree Classifier (Gini)', '71.4%', '68.9%', '67.0%', '0.679', '0.722'],
        ['Random Forest Classifier (EcoTrack Best)', '79.8%', '78.2%', '76.6%', '0.774', '0.832']
    ]
    t72_data = [[Paragraph(f'<b>{h}</b>', ParagraphStyle('TH72', parent=body_noindent, fontSize=8, leading=10, textColor=colors.white)) for h in t72_headers]]
    for r in t72_rows:
        t72_data.append([Paragraph(v, ParagraphStyle('TD72', parent=body_noindent, fontSize=8, leading=10)) for v in r])
    t72 = Table(t72_data, colWidths=[1.8*inch, 0.8*inch, 0.8*inch, 0.7*inch, 0.7*inch, 0.7*inch])
    t72.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#dcfce7')),
    ]))
    story.append(t72)
    
    # Embed Screenshots
    if os.path.exists('report_assets/screen1_india_live.png'):
        story.append(Spacer(1, 10))
        story.append(Image('report_assets/screen1_india_live.png', width=5.4*inch, height=2.6*inch))
        story.append(Paragraph('Figure 7.1: Screen 1: Nationwide Live Ingestion Dashboard View', caption))
    if os.path.exists('report_assets/screen2_air_simulator.png'):
        story.append(Spacer(1, 10))
        story.append(Image('report_assets/screen2_air_simulator.png', width=5.4*inch, height=2.6*inch))
        story.append(Paragraph('Figure 7.2: Screen 2: Air Quality Simulator with Interactive Sliders', caption))
    if os.path.exists('report_assets/screen3_water_diagnostic.png'):
        story.append(Spacer(1, 10))
        story.append(Image('report_assets/screen3_water_diagnostic.png', width=5.4*inch, height=2.6*inch))
        story.append(Paragraph('Figure 7.3: Screen 3: Water Potability Diagnostic Workbench and WHO Gauge Meters', caption))
    if os.path.exists('report_assets/screen4_anomaly_explorer.png'):
        story.append(Spacer(1, 10))
        story.append(Image('report_assets/screen4_anomaly_explorer.png', width=5.4*inch, height=2.6*inch))
        story.append(Paragraph('Figure 7.4: Screen 4: Anomaly Detection Explorer and Historical Audit Logs Table', caption))
    story.append(PageBreak())
    
    # CHAPTER 8
    render_chapter(c3.CH8_TITLE, c3.CH8_SECTIONS)
    
    # REFERENCES
    story.append(Paragraph('REFERENCES', ch_heading))
    story.append(Spacer(1, 10))
    for r in c3.REFERENCES_DATA:
        story.append(Paragraph(r, body_noindent))
        story.append(Spacer(1, 4))
    story.append(PageBreak())
    
    # ---------------------------------------------------------
    # ANNEXURES I TO V
    # ---------------------------------------------------------
    for ann in [ca.ANNEXURE_I_DATA, ca.ANNEXURE_II_DATA, ca.ANNEXURE_III_DATA, ca.ANNEXURE_IV_DATA, ca.ANNEXURE_V_DATA]:
        story.append(Paragraph(ann['title'], ch_heading))
        story.append(Spacer(1, 10))
        for sec in ann['sections']:
            story.append(Paragraph(sec['heading'], sec_heading))
            lines = sec['content'].split('\n')
            code_buffer = []
            for line in lines:
                if any(line.strip().startswith(kw) for kw in ['{', '}', '#', 'def ', 'class ', 'import ', 'from ', 'server {', '[Unit]', 'platform', 'tests/', 'Test ID:']):
                    code_buffer.append(line)
                else:
                    if code_buffer:
                        story.append(Preformatted('\n'.join(code_buffer), code_style))
                        story.append(Spacer(1, 4))
                        code_buffer = []
                    if line.strip():
                        story.append(Paragraph(line, body))
            if code_buffer:
                story.append(Preformatted('\n'.join(code_buffer), code_style))
                story.append(Spacer(1, 4))
        story.append(PageBreak())
        
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f'PDF compiled successfully: {pdf_filename}')

if __name__ == '__main__':
    build_pdf()
