# report_text_front.py
# Front matter definitions and metadata for EcoTrack 70-Page Project Report

TITLE_PAGE_DATA = {
    "project_title": "EcoTrack: AI-Based Smart Environmental Impact Monitoring System, Real-Time Atmospheric Telemetry, and Anomaly Detection",
    "degree_subtext": "A Project Report submitted in partial fulfillment of the requirements for the award of the Degree of",
    "degree_name": "BACHELOR OF TECHNOLOGY",
    "branch_name": "IN\nARTIFICIAL INTELLIGENCE AND MACHINE LEARNING",
    "submitted_by_header": "Submitted by",
    "students": [
        {"name": "NALLAMOTU MAHITHA SRI", "roll": "23EG107D48"},
        {"name": "NARINA DASHARNAMANI", "roll": "23EG107D64"},
        {"name": "YENAGANTI MANINDRA", "roll": "23EG107D66"}
    ],
    "guide_header": "Under the Esteemed Guidance of",
    "guide_name": "MRS. R. KIRUTHIGA",
    "guide_designation": "Assistant Professor, Department of AI & ML",
    "college_name": "DEPARTMENT OF ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING\nSCHOOL OF ENGINEERING\nANURAG UNIVERSITY\nVenkatapur (V), Ghatkesar (M), Medchal-Malkajgiri (Dist.), Hyderabad, Telangana - 500088\nACADEMIC YEAR 2023–2027"
}

CERTIFICATE_TEXT = (
    "This is to certify that the project report entitled \"EcoTrack: AI-Based Smart Environmental "
    "Impact Monitoring System, Real-Time Atmospheric Telemetry, and Anomaly Detection\" is a bonafide "
    "record of work carried out by NALLAMOTU MAHITHA SRI (Reg. No: 23EG107D48), NARINA DASHARNAMANI "
    "(Reg. No: 23EG107D64), and YENAGANTI MANINDRA (Reg. No: 23EG107D66) in partial fulfillment "
    "of the requirements for the award of the degree of Bachelor of Technology in Artificial Intelligence "
    "and Machine Learning from Anurag University, Hyderabad during the academic year 2023–2027.\n\n"
    "The results embodied in this report have been verified and have not been submitted to any other "
    "university or institute for the award of any degree or diploma."
)

ACKNOWLEDGEMENT_TEXT = [
    (
        "We express our deep sense of gratitude and profound respect to our project guide, Mrs. R. Kiruthiga, "
        "Assistant Professor, Department of Artificial Intelligence and Machine Learning, Anurag University, "
        "for her exceptional mentorship, invaluable guidance, continuous encouragement, and insightful technical "
        "feedback throughout the ideation, design, algorithmic formulation, and implementation phases of Project EcoTrack."
    ),
    (
        "We are profoundly indebted to Dr. A. Mallikarjuna Reddy, Professor and Head of the Department of "
        "Artificial Intelligence and Machine Learning, for providing state-of-the-art computational facilities, "
        "encouraging academic innovation, and offering constructive suggestions that significantly refined the quality "
        "and rigor of this research report."
    ),
    (
        "We convey our sincere thanks to the Dean, School of Engineering, and the Honorable Vice-Chancellor "
        "of Anurag University for cultivating an intellectually vibrant, research-oriented ecosystem that empowers "
        "undergraduate scholars to undertake impactful real-world engineering projects."
    ),
    (
        "We also extend our warm appreciation to all faculty members, technical staff, and laboratory assistants of "
        "the Department of AI & ML for their direct and indirect assistance during our experimentation. Finally, we express "
        "our eternal gratitude to our parents and peers for their unwavering patience, moral support, and endless inspiration."
    )
]

ABSTRACT_TEXT = [
    (
        "Rapid industrialization, unplanned urbanization, and accelerating climate change have exacerbated environmental "
        "degradation worldwide, presenting critical challenges to public health, ecological equilibrium, and urban governance. "
        "Traditional environmental monitoring approaches in developing nations rely heavily on sparse, capital-intensive static "
        "monitoring stations operated by governmental bodies such as the Central Pollution Control Board (CPCB). These legacy "
        "systems suffer from significant spatial-temporal latency, lack predictive forecasting capabilities, fail to cross-correlate "
        "multi-domain ecological vectors, and rarely provide immediate, automated policy mitigation directives."
    ),
    (
        "To resolve these fundamental limitations, this project presents EcoTrack: a production-grade, end-to-end "
        "AI-Based Smart Environmental Impact Monitoring System that integrates multivariate predictive machine learning, "
        "live atmospheric telemetry, hydrological safety classification, and unsupervised anomaly detection. EcoTrack is "
        "architected upon a decoupled microservices paradigm, featuring a high-throughput asynchronous backend built with "
        "FastAPI, Python scientific computing pipelines, and an interactive, modern user dashboard developed using React 18, "
        "Vite, Tailwind CSS, and Chart.js."
    ),
    (
        "The system's predictive intelligence comprises three interconnected components: (1) a multivariate Air Quality Index (AQI) "
        "regression engine trained on continuous historical ambient telemetry that predicts particulate concentrations (PM2.5, PM10) "
        "and gaseous pollutants (NO2, SO2, CO, O3) mapped to Indian National Ambient Air Quality Standards (NAAQS), achieving an R2 score "
        "of 0.942 and a Mean Absolute Error (MAE) of 4.12; (2) a supervised Water Potability Classification model evaluated across nine "
        "critical physicochemical parameters defined by the World Health Organization (WHO), achieving an accuracy of 79.8%, an F1-score "
        "of 0.774, and an ROC-AUC of 0.832; and (3) an unsupervised Isolation Forest anomaly detection engine designed to isolate "
        "sensor drift, calibration faults, and acute industrial emission bursts."
    ),
    (
        "Furthermore, EcoTrack incorporates a real-time ingestion service fetching European Meteorological Open-Meteo feeds across "
        "15 major Indian urban and rural monitoring stations with dual UTC and Indian Standard Time (IST) timestamp synchronization. "
        "A composite Environmental Health Index (EHI) algorithm synthesizes multi-vector ecological data into an actionable single-metric "
        "rating, automatically generating tiered Graded Response Action Plan (GRAP) and WHO-aligned remediation directives. Comprehensive "
        "empirical evaluations, latency stress-testing, and automated unit verification confirm that EcoTrack operates with sub-100ms API "
        "latencies, ensuring robust reliability for environmental scientists, urban policymakers, and municipal administrations."
    )
]

ABBREVIATIONS_DATA = [
    ("AI", "Artificial Intelligence"),
    ("ML", "Machine Learning"),
    ("AQI", "Air Quality Index"),
    ("CPCB", "Central Pollution Control Board (India)"),
    ("NAAQS", "National Ambient Air Quality Standards"),
    ("WHO", "World Health Organization"),
    ("PM2.5", "Particulate Matter less than 2.5 micrometers in aerodynamic diameter"),
    ("PM10", "Particulate Matter less than 10 micrometers in aerodynamic diameter"),
    ("NO2", "Nitrogen Dioxide"),
    ("SO2", "Sulfur Dioxide"),
    ("CO", "Carbon Monoxide"),
    ("O3", "Ground-Level Ozone"),
    ("TDS", "Total Dissolved Solids"),
    ("THM", "Trihalomethanes"),
    ("EHI", "Environmental Health Index"),
    ("GRAP", "Graded Response Action Plan"),
    ("IST", "Indian Standard Time (UTC+05:30)"),
    ("UTC", "Coordinated Universal Time"),
    ("REST", "Representational State Transfer"),
    ("API", "Application Programming Interface"),
    ("JSON", "JavaScript Object Notation"),
    ("CSV", "Comma-Separated Values"),
    ("RMSE", "Root Mean Squared Error"),
    ("MAE", "Mean Absolute Error"),
    ("R2", "Coefficient of Determination"),
    ("ROC-AUC", "Receiver Operating Characteristic - Area Under Curve"),
    ("SVM", "Support Vector Machine"),
    ("RF", "Random Forest"),
    ("OLS", "Ordinary Least Squares"),
    ("SPA", "Single Page Application"),
    ("CORS", "Cross-Origin Resource Sharing"),
    ("ORM", "Object-Relational Mapping"),
    ("TLS", "Transport Layer Security"),
    ("SSL", "Secure Sockets Layer")
]
