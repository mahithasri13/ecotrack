# report_text_ch4_to_ch5.py
# Chapters 4 and 5 for EcoTrack 70-Page Project Report

CH4_TITLE = "CHAPTER 4\nSYSTEM DESIGN AND ARCHITECTURE"

CH4_SECTIONS = [
    {
        "type": "heading",
        "title": "4.1 SYSTEM ARCHITECTURAL OVERVIEW",
        "content": [
            (
                "Project EcoTrack is designed around a modular, decoupled, four-tier microservices architecture engineered to maximize "
                "concurrency, ensure fault isolation, and provide high computational throughput. The architectural topology establishes "
                "strict separation of concerns between telemetry acquisition, machine learning inference, composite analytical scoring, "
                "relational data persistence, and interactive user visualization."
            ),
            (
                "Figure 4.1 illustrates the comprehensive four-tier system architecture of Project EcoTrack. The system operates across four "
                "tightly coordinated operational layers: (1) Data Ingestion and Telemetry Tier; (2) Core Intelligence and Machine Learning Tier; "
                "(3) Asynchronous Application Backend Tier; and (4) Presentation and Scientific Dashboard Tier."
            )
        ]
    },
    {
        "type": "heading",
        "title": "4.2 LAYERED ARCHITECTURAL TOPOLOGY",
        "content": [
            (
                "1. Data Ingestion and Telemetry Tier: Responsible for the continuous, asynchronous acquisition of environmental parameters. "
                "This layer manages automated HTTP polling of European Meteorological Open-Meteo REST APIs, retrieving hourly atmospheric "
                "variables (temperature, relative humidity, wind speed) and criteria pollutant concentrations (PM2.5, PM10, NO2, SO2, CO, O3) "
                "across 15 designated Indian stations. Additionally, it provides REST ingestion endpoints to accept telemetry streams from "
                "physical edge IoT sensing hardware deployed in field environments."
            ),
            (
                "2. Core Intelligence and Machine Learning Tier: Houses the serialized scientific pipelines and model inference runtime. "
                "Built using Scikit-Learn, NumPy, and Joblib, this tier encapsulates the pre-trained multivariate AQI regression pipeline, "
                "the 9-parameter water potability classification pipeline, the unsupervised Isolation Forest anomaly detection engine, and the "
                "composite Environmental Health Index (EHI) scoring algorithms. Models are loaded into memory during application initialization, "
                "ensuring zero disk I/O latency during real-time inference requests."
            ),
            (
                "3. Asynchronous Application Backend Tier: Implemented in Python using the high-performance FastAPI framework running on the "
                "Uvicorn Asynchronous Server Gateway Interface (ASGI). This layer exposes RESTful HTTP endpoints, enforces strict payload validation "
                "via Pydantic schemas, routes analytical queries, manages dynamic policy directive generation, and interfaces with the underlying "
                "SQLite relational database via SQLAlchemy Object-Relational Mapping (ORM)."
            ),
            (
                "4. Presentation and Scientific Dashboard Tier: A Single Page Application (SPA) built using React 18 and Vite. Styled with Tailwind CSS "
                "and populated with Lucide icons and Chart.js dynamic visualizations, this layer delivers an intuitive, responsive interface "
                "for environmental scientists and municipal operators. It includes interactive simulators, real-time geographic station switchers, "
                "historical audit log explorers, and production domain verification utilities."
            )
        ]
    },
    {
        "type": "heading",
        "title": "4.3 DATA FLOW DIAGRAMS (DFD)",
        "content": [
            (
                "Data Flow Diagrams (DFDs) provide a hierarchical, graphical representation of how information moves through the EcoTrack system, "
                "depicting data sources, functional transformation processes, relational data stores, and external data sinks."
            ),
            (
                "A. Context-Level Diagram (Level 0 DFD):\n"
                "At the macro level, Project EcoTrack acts as a centralized environmental intelligence transformational bubble. Three external entities "
                "interact with the system: (1) External Telemetry Sources (Open-Meteo API and IoT hardware nodes), which supply raw atmospheric "
                "and physicochemical telemetry streams; (2) End Users (Environmental Scientists, Municipal Officers, Citizens), who submit interactive "
                "simulation parameters, query real-time analytics, and receive predictive classifications; and (3) Municipal Regulatory Services, "
                "which receive automated breach alerts and Graded Response Action Plan (GRAP) directives."
            ),
            (
                "B. Level 1 Data Flow Diagram (Modular Decomposition):\n"
                "The Level 1 DFD decomposes the system into six primary transformation processes:\n"
                "- Process 1.0 (Telemetry Ingestion & Timestamping): Ingests external API payloads, parses pollutant fields, attaches dual UTC/IST "
                "timestamps, and stores raw records into the 'Location Telemetry' data store.\n"
                "- Process 2.0 (Payload Validation & Feature Scaling): Validates incoming simulation data against Pydantic schemas and applies "
                "standardized preprocessing transforms using pre-fitted Scikit-Learn transformers.\n"
                "- Process 3.0 (Predictive Machine Learning Inference): Directs scaled feature vectors into serialized models to produce continuous "
                "AQI values, categorical pollutant tiers, and probabilistic water potability verdicts.\n"
                "- Process 4.0 (Unsupervised Anomaly Scoring): Evaluates sensory telemetry across multi-dimensional feature space using Isolation "
                "Forest to flag sensory drift and acute contamination events.\n"
                "- Process 5.0 (Composite EHI & Directive Synthesis): Fuses air and water quality outputs into a 0-100 Environmental Health Index "
                "score, evaluates regulatory thresholds, and generates contextual policy mitigation directives.\n"
                "- Process 6.0 (Persistence, Formatting & Export): Writes transaction records into the 'Historical Logs' SQLite store and formats "
                "JSON responses for the frontend dashboard and CSV export utilities."
            ),
            (
                "C. Level 2 Data Flow Diagram (Algorithmic Processing):\n"
                "The Level 2 DFD details the internal mechanics of Process 3.0 and Process 5.0, illustrating how sub-indices for PM2.5, PM10, "
                "NO2, SO2, CO, and O3 are individually computed, how the maximum sub-index principle determines the governing pollutant, and how "
                "the calibrated Sigmoid function computes water potability confidence."
            )
        ]
    },
    {
        "type": "heading",
        "title": "4.4 UNIFIED MODELING LANGUAGE (UML) DIAGRAMS",
        "content": [
            (
                "To rigorously specify the structural composition and dynamic behavioral interactions of Project EcoTrack, a comprehensive suite "
                "of Unified Modeling Language (UML) diagrams was developed."
            ),
            (
                "4.4.1 Use Case Modeling and Actor Specifications:\n"
                "The Use Case diagram identifies the interactions between system boundaries and external actors. Three primary actors participate:\n"
                "- Environmental Scientist / Analyst: Use cases include 'Simulate Air Quality Scenarios', 'Run Water Potability Diagnostic', "
                "'Inspect Model Performance Metrics', 'Export Historical Telemetry (CSV/JSON)', and 'Configure Anomaly Thresholds'.\n"
                "- Municipal Regulatory Officer: Use cases include 'View Nationwide Dashboard Summary', 'Inspect Local Station Telemetry', "
                "'Receive Automated Threshold Breach Alerts', 'Review GRAP Policy Directives', and 'Execute Emergency Mitigation Protocols'.\n"
                "- System Administrator: Use cases include 'Verify Production Domain & SSL', 'Trigger Manual Model Retraining', 'Purge Historical "
                "Audit Logs', and 'Inspect ASGI System Health'."
            ),
            (
                "4.4.2 Class Diagram and Object-Oriented Domain Model:\n"
                "The Class diagram defines the static object model of the EcoTrack application. Primary classes include:\n"
                "- `MLEngine`: Central singleton encapsulating model loading, preprocessor deserialization, AQI regression, water classification, "
                "and anomaly detection algorithms.\n"
                "- `AnalyticsEngine`: Static mathematical utility implementing `calculate_ehi()`, `analyze_environmental_impact()`, and "
                "`generate_actionable_directives()`.\n"
                "- `IndiaLiveService`: Service class managing the `INDIAN_LOCATIONS` dictionary, Open-Meteo HTTP client, timestamp conversions, "
                "and multi-station aggregation.\n"
                "- `AirQualityInput` and `WaterPotabilityInput`: Pydantic model classes enforcing strict type constraints, field defaults, and "
                "validation rules for incoming JSON payloads.\n"
                "- `PredictionLog` and `AlertRecord`: SQLAlchemy ORM classes mapping application objects to relational SQLite database tables."
            ),
            (
                "4.4.3 Sequence Modeling:\n"
                "Sequence diagrams capture the chronological exchange of messages between objects. Two critical execution scenarios were modeled:\n"
                "- Scenario 1: Air Quality Simulation Workflow: The User initiates a POST request from the React dashboard. The React client "
                "transmits a JSON payload to the FastAPI `/predict/air-quality` endpoint. FastAPI invokes Pydantic validation. The validated object "
                "is passed to `MLEngine.predict_air_quality()`. The model executes feature scaling, runs regression inference, categorizes the AQI "
                "according to CPCB NAAQS, and evaluates anomaly status via Isolation Forest. The result is passed to `AnalyticsEngine` for impact driver "
                "extraction, recorded asynchronously into SQLite via `database.log_prediction()`, and returned as a JSON response to React, which updates "
                "the interactive UI chart.\n"
                "- Scenario 2: Real-Time Multi-Station Ingestion & Alerting Workflow: A timer or client request triggers the `/realtime/india-air` "
                "endpoint. `IndiaLiveService` dispatches an asynchronous HTTP GET to the Open-Meteo API. Upon receiving the meteorological JSON response, "
                "`IndiaLiveService` extracts criteria pollutants, calculates AQI via `MLEngine`, checks breach thresholds against CPCB limits, generates "
                "alert records if thresholds are exceeded, and returns enriched telemetry with dual UTC/IST timestamps."
            ),
            (
                "4.4.4 Activity Modeling:\n"
                "Activity diagrams depict the step-by-step control flow and decision branching of business workflows. The Water Diagnostic Activity "
                "Diagram models: (1) Start node -> (2) Receive 9 physicochemical parameters -> (3) Validate numerical ranges -> (4) Decision Diamond: "
                "Are parameters within physical limits? If No, raise HTTP 422 error and abort; If Yes, proceed -> (5) Apply Scikit-Learn RobustScaler -> "
                "(6) Execute Random Forest Classification -> (7) Compute Sigmoid probability confidence -> (8) Evaluate Potability Decision Diamond: "
                "Is Class == 1? If Yes, set Status to 'Potable (Safe)'; If No, set Status to 'Non-Potable (Unsafe)' -> (9) Formulate WHO-compliant "
                "water boiling/filtration directives -> (10) Persist transaction log -> (11) End node."
            ),
            (
                "4.4.5 State Machine Modeling:\n"
                "The State Machine diagram captures the lifecycle states of an Environmental Monitoring Station. A station transitions through "
                "four defined states: (1) `Active - Optimal`: Telemetry streams normally, AQI < 100, EHI >= 80; (2) `Active - Moderate Warning`: "
                "AQI between 101 and 200, system issues advisory alerts; (3) `Active - Critical Hazard`: AQI > 200 or water non-potable, system "
                "issues mandatory GRAP directives; (4) `Offline - Sensor Drift / Anomaly`: Isolation Forest detects persistent sensory anomalies "
                "or API heartbeat fails, triggering a maintenance alert."
            )
        ]
    },
    {
        "type": "heading",
        "title": "4.5 DATABASE ARCHITECTURE AND ENTITY-RELATIONSHIP (ER) MODELING",
        "content": [
            (
                "EcoTrack utilizes an embedded SQLite relational database managed via SQLAlchemy 2.0 ORM. The relational schema is structured "
                "to provide complete auditability, fast indexing on timestamp and location fields, and seamless historical reporting."
            ),
            (
                "The Entity-Relationship (ER) model comprises three primary relational entities:\n"
                "1. `MonitoringStation`: Stores metadata for the 15 monitored geographical locations, including station unique identifier, "
                "display name, state, geographical latitude, longitude, and assigned water treatment station.\n"
                "2. `PredictionLog`: Stores transaction records of all air quality and water potability simulations and live inferences. "
                "Attributes include record ID (Primary Key), timestamp (UTC & IST), station ID (Foreign Key), prediction domain ('air' or 'water'), "
                "raw input JSON, predicted output (AQI value or potability class), confidence percentage, and anomaly flag.\n"
                "3. `AlertRecord`: Stores automated regulatory breach records. Attributes include alert ID (Primary Key), station ID (Foreign Key), "
                "timestamp, severity level ('Warning', 'Critical', 'Emergency'), triggered pollutant or parameter, breach value, and assigned "
                "policy mitigation directive."
            )
        ]
    },
    {
        "type": "heading",
        "title": "4.6 DATA DICTIONARIES AND TABLE SCHEMAS",
        "content": [
            (
                "A comprehensive Data Dictionary was established to strictly define the attribute names, data types, physical units, "
                "permissible value ranges, and relational constraints across all persistent tables."
            ),
            (
                "Table 4.1 outlines the schema specification for the primary `prediction_logs` table, documenting each attribute's operational role."
            )
        ]
    },
    {
        "type": "heading",
        "title": "4.7 INTERFACE AND REVERSE PROXY ARCHITECTURE",
        "content": [
            (
                "For production deployment, EcoTrack implements a battle-tested reverse proxy architecture. Direct exposure of the Uvicorn ASGI "
                "application to the public internet introduces security risks and suboptimal static file delivery. Therefore, Nginx is deployed as "
                "the front-facing reverse proxy and SSL termination gateway."
            ),
            (
                "Nginx listens on ports 80 (HTTP) and 443 (HTTPS). It automatically redirects all plain HTTP traffic to secure HTTPS using "
                "HTTP 301 Permanent Redirects. Static frontend production assets (HTML, CSS, JavaScript bundles, images) compiled by Vite are served "
                "directly by Nginx from the filesystem with optimized gzip compression and browser caching headers. API requests matching the `/api/` "
                "location prefix are proxied internally to Uvicorn running on `127.0.0.1:8000` via Unix domain sockets or loopback TCP, with "
                "proper `X-Real-IP`, `X-Forwarded-For`, and `X-Forwarded-Proto` headers preserved."
            )
        ]
    },
    {
        "type": "heading",
        "title": "4.8 SUMMARY OF THE CHAPTER",
        "content": [
            (
                "This chapter presented the comprehensive architectural design of Project EcoTrack, encompassing its four-tier topology, "
                "multi-level Data Flow Diagrams, complete UML modeling suite (Use Case, Class, Sequence, Activity, State Machine), relational "
                "ER database schemas, data dictionaries, and production Nginx reverse proxy configuration. This structural blueprint guides "
                "the algorithm design detailed in Chapter 5."
            )
        ]
    }
]

CH5_TITLE = "CHAPTER 5\nMETHODOLOGY AND ALGORITHM DESIGN"

CH5_SECTIONS = [
    {
        "type": "heading",
        "title": "5.1 DATA ACQUISITION PIPELINE AND TELEMETRY PROVENANCE",
        "content": [
            (
                "The scientific validity of any machine learning system depends fundamentally on the authenticity, provenance, and integrity "
                "of its underlying training datasets. Project EcoTrack strictly avoids synthetic data fabrication, utilizing verified empirical "
                "datasets sourced from recognized environmental monitoring institutions."
            ),
            (
                "1. Air Quality Benchmark Dataset: Sourced from the historical continuous air quality monitoring archives of the Central Pollution "
                "Control Board (CPCB) across major Indian industrial and metropolitan centers. The dataset encapsulates 1,000+ validated hourly "
                "observations comprising criteria pollutants: PM2.5, PM10, Nitrogen Dioxide (NO2), Sulfur Dioxide (SO2), Carbon Monoxide (CO), "
                "and Ground-Level Ozone (O3), coupled with calibrated reference AQI values computed according to official CPCB NAAQS guidelines."
            ),
            (
                "2. Drinking Water Potability Benchmark Dataset: Sourced from published municipal water quality surveillance records compiled "
                "against World Health Organization (WHO) Drinking-water Quality Guidelines. The dataset contains 3,276 individual water sample "
                "records evaluated across nine physicochemical parameters: pH, Hardness, Total Dissolved Solids, Chloramines, Sulfate, "
                "Electrical Conductivity, Total Organic Carbon, Trihalomethanes, and Turbidity, with binary ground-truth labels indicating "
                "biological and chemical potability (1 = Potable, 0 = Non-Potable)."
            ),
            (
                "3. Real-Time Telemetry Stream: Sourced dynamically via the Open-Meteo European Meteorological Service API. Open-Meteo integrates "
                "high-resolution numerical weather prediction models (including the Copernicus Atmosphere Monitoring Service - CAMS, ECMWF IFS, "
                "and NOAA GFS) to deliver real-time atmospheric pollutant concentrations and weather variables at 11 km spatial resolution across "
                "India."
            )
        ]
    },
    {
        "type": "heading",
        "title": "5.2 DATA CLEANING, IMPUTATION, AND PREPROCESSING",
        "content": [
            (
                "Raw environmental datasets collected in the field frequently exhibit data quality defects, including missing values due to "
                "sensor downtime, transient recording errors, extreme outliers, and dimensional scale disparities. EcoTrack implements a rigorous "
                "multi-stage preprocessing pipeline."
            ),
            (
                "A. Missing Value Imputation:\n"
                "In the water potability dataset, missing observations were detected in three physicochemical attributes: Sulfate (24.1% missing), "
                "pH (14.9% missing), and Trihalomethanes (4.9% missing). Because environmental parameters frequently exhibit skewed distributions, "
                "standard mean imputation introduces severe distributional bias. EcoTrack employs a Median Imputation strategy for skewed features "
                "and Group-Median Imputation conditioned on potability class labels during offline exploration, preserving the underlying variance "
                "without data leakage."
            ),
            (
                "B. Feature Scaling and Normalization:\n"
                "Different environmental parameters operate across vastly disparate physical magnitudes. For example, Total Dissolved Solids "
                "ranges from 300 to 50,000 ppm, whereas Turbidity ranges from 1 to 7 NTU, and pH spans 0 to 14. If supplied to distance-based or "
                "gradient-based algorithms without transformation, high-magnitude features disproportionately dominate the cost function. "
                "EcoTrack deploys Scikit-Learn's `RobustScaler` and `StandardScaler` transformations. RobustScaler removes the median and scales "
                "the data according to the Interquartile Range (IQR = Q3 - Q1), making feature scaling highly resilient to extreme pollution outliers."
            )
        ]
    },
    {
        "type": "heading",
        "title": "5.3 FEATURE ENGINEERING AND STATISTICAL PROFILING",
        "content": [
            (
                "To optimize model expressiveness and enhance predictive accuracy, domain-specific feature engineering was conducted on atmospheric "
                "and hydrological feature spaces."
            ),
            (
                "For atmospheric modeling, the ratio between fine and coarse particulate matter (PM_ratio = PM2.5 / PM10) was formulated. Under normal "
                "crustal dust conditions, PM_ratio ranges between 0.3 and 0.5. However, during combustion-dominated smog episodes (vehicular exhaust, "
                "biomass burning), PM_ratio surges above 0.75, providing a powerful non-linear signature for severe AQI elevation."
            ),
            (
                "For water potability modeling, an Mineral Mineralization Index (MMI) was engineered by computing the normalized product of Electrical "
                "Conductivity and Total Dissolved Solids. Furthermore, interaction terms between pH and Chloramines were generated, capturing the chemical "
                "equilibrium governing the formation of hypochlorous acid versus hypochlorite ions during municipal water disinfection."
            )
        ]
    },
    {
        "type": "heading",
        "title": "5.4 AIR QUALITY MULTIVARIATE REGRESSION FORMULATION",
        "content": [
            (
                "Air Quality Index (AQI) prediction is formulated as a continuous multivariate regression problem. Given a vector of ambient criteria "
                "pollutant concentrations x = [PM2.5, PM10, NO2, SO2, CO, O3]^T in R^6, the objective is to learn a mapping function f: R^6 -> R "
                "that predicts the continuous scalar AQI value y with minimal generalization error."
            ),
            (
                "Three distinct regression architectures were formulated, implemented, and benchmarked:"
            ),
            (
                "5.4.1 Ordinary Least Squares and Ridge Regularization:\n"
                "The baseline linear regression model expresses the predicted AQI as a linear combination of input pollutants: "
                "y_hat = w_0 + sum_{i=1}^6 w_i * x_i. To prevent multicollinearity between correlated pollutants (such as PM2.5 and PM10), "
                "L2 Tikhonov Regularization (Ridge Regression) was applied, minimizing the penalized residual sum of squares: "
                "J(w) = sum_{k=1}^N (y_k - y_hat_k)^2 + lambda * ||w||_2^2, where lambda > 0 controls regularization strength."
            ),
            (
                "5.4.2 Random Forest Regression Ensemble:\n"
                "To capture complex non-linear pollutant interactions, an ensemble of B = 100 de-correlated decision trees was constructed. "
                "Each tree T_b is trained on a bootstrap sample drawn with replacement from the training set. At each split, a random subset of "
                "m = sqrt(p) features is considered. The final ensemble prediction is computed via bootstrap aggregation (bagging): "
                "y_hat_{RF} = (1 / B) * sum_{b=1}^B T_b(x). Random Forest provides intrinsic resistance to overfitting and computes empirical "
                "feature importance rankings based on mean decrease in node impurity."
            ),
            (
                "5.4.3 Gradient Boosted Decision Trees:\n"
                "As an advanced alternative, Gradient Boosting sequentially constructs decision trees in a stage-wise additive manner, fitting "
                "each subsequent tree to the negative gradient (pseudo-residuals) of the squared error loss function: "
                "r_{ik} = - [d L(y_i, f(x_i)) / d f(x_i)]. GBDT achieves sharp boundary delineation across extreme breakpoint transitions."
            )
        ]
    },
    {
        "type": "heading",
        "title": "5.5 WATER POTABILITY CLASSIFICATION FORMULATION",
        "content": [
            (
                "Drinking water safety is formulated as a supervised binary classification problem. Given a vector of nine physicochemical measurements "
                "z in R^9, the objective is to predict the discrete potability class y in {0, 1}, where y = 1 denotes water meeting WHO potability "
                "standards and y = 0 denotes non-potable or contaminated water."
            ),
            (
                "Three classification models were developed and compared:"
            ),
            (
                "5.5.1 Regularized Logistic Regression:\n"
                "Models the posterior class probability via the Sigmoid logistic link function: "
                "P(y=1 | z) = 1 / (1 + exp(- (w^T * z + b))). While computationally efficient and highly interpretable, linear logistic regression "
                "exhibits limited capacity when separating non-linearly intertwined chemical clusters."
            ),
            (
                "5.5.2 Support Vector Machines with RBF Kernel:\n"
                "Maps input vectors into an infinite-dimensional Hilbert feature space using the Radial Basis Function (RBF) kernel: "
                "K(z_i, z_j) = exp(- gamma * ||z_i - z_j||^2). The dual optimization problem constructs a maximal-margin hyperplane separating potable "
                "from non-potable samples while penalizing slack margin violations via soft-margin parameter C."
            ),
            (
                "5.5.3 Random Forest Classifier:\n"
                "A non-parametric ensemble of 150 randomized decision trees utilizing Gini impurity as the split criterion: "
                "Gini(D) = 1 - sum_{c=0}^1 (p_c)^2. The ensemble averages individual tree probability estimates, producing calibrated posterior "
                "confidence scores: Conf(z) = (1 / B) * sum_{b=1}^B P_b(y=1 | z) * 100%. This model was selected as the production classifier "
                "due to superior cross-validated F1-score and robustness against missing feature imputations."
            )
        ]
    },
    {
        "type": "heading",
        "title": "5.6 UNSUPERVISED ISOLATION FOREST ANOMALY DETECTION",
        "content": [
            (
                "To ensure reliable sensory data quality, EcoTrack implements an unsupervised Isolation Forest (iForest) anomaly detection model. "
                "Unlike density-based or distance-based anomaly detectors (e.g., Local Outlier Factor or One-Class SVM) which exhibit O(n^2) computational "
                "complexity, Isolation Forest isolates anomalies explicitly using recursive tree partitioning with linear O(n) complexity."
            ),
            (
                "Algorithm Execution Principle:\n"
                "1. Given an unlabeled telemetry dataset X = {x_1, ..., x_n} of p dimensions, an ensemble of t = 100 Isolation Trees (iTrees) is built.\n"
                "2. To construct each iTree, a random sub-sample X' subset of X (size psi = 256) is recursively partitioned by randomly selecting "
                "an attribute q and a random split value p between min(q) and max(q) until either: (a) the tree reaches maximum depth limit "
                "h_max = ceil(log_2(psi)); (b) |X'| <= 1; or (c) all data points in X' have identical values.\n"
                "3. Path Length Calculation: The path length h(x) of an observation x is measured as the number of edges traversed from the root node "
                "to an external leaf node in an iTree.\n"
                "4. Anomaly Score Derivation: The anomaly score s(x, psi) is formulated as: "
                "s(x, psi) = 2^(- E(h(x)) / c(psi)), where E(h(x)) is the average path length across all t trees, and c(psi) is the average path "
                "length of unsuccessful searches in a Binary Search Tree: c(psi) = 2 * (ln(psi - 1) + 0.5772156649) - (2 * (psi - 1) / psi).\n"
                "5. Interpretation:\n"
                "- If s -> 1.0 (average path length is very short), the instance is classified as a severe anomaly (Score = -1).\n"
                "- If s < 0.5 (average path length is long), the instance is classified as a normal inlier (Score = +1)."
            )
        ]
    },
    {
        "type": "heading",
        "title": "5.7 COMPOSITE ENVIRONMENTAL HEALTH INDEX (EHI) FORMULATION",
        "content": [
            (
                "A primary scientific innovation of Project EcoTrack is the synthesis of atmospheric and hydrological vectors into a unified "
                "Environmental Health Index (EHI). The EHI is a normalized scalar score ranging from 0 to 100, where 100 represents pristine "
                "environmental quality and 0 represents acute ecological toxicity."
            ),
            (
                "Mathematical Formulation:\n"
                "EHI = w_{air} * S_{air}(AQI) + w_{water} * S_{water}(P_{potable})\n"
                "where w_{air} = 0.50 and w_{water} = 0.50 represent equal stakeholder weighting across atmospheric and aquatic domains."
            ),
            (
                "The air quality sub-score S_{air} is computed as a bounded inverse linear transform of the predicted AQI:\n"
                "S_{air}(AQI) = max(0.0, min(100.0, 100.0 - (AQI / 3.0)))\n"
                "- For AQI <= 25 (pristine ambient air), S_{air} = 100.0.\n"
                "- For AQI = 150 (moderate pollution), S_{air} = 50.0.\n"
                "- For AQI >= 300 (severe hazardous smog), S_{air} = 0.0."
            ),
            (
                "The water quality sub-score S_{water} is derived directly from the calibrated posterior potability probability:\n"
                "S_{water}(P_{potable}) = max(0.0, min(100.0, P_{potable} * 100.0))\n"
                "- For P_{potable} >= 0.80 (certified safe drinking water), S_{water} >= 80.0.\n"
                "- For P_{potable} <= 0.20 (heavily contaminated supply), S_{water} <= 20.0."
            ),
            (
                "Tiered Health Classifications:\n"
                "- EHI >= 80.0: Optimal Environmental Quality (Emerald Status)\n"
                "- 60.0 <= EHI < 80.0: Moderate Quality (Yellow Advisory)\n"
                "- 40.0 <= EHI < 60.0: Degraded Environment (Orange Warning)\n"
                "- EHI < 40.0: Critical Ecological Risk (Red Emergency Mandate)"
            )
        ]
    },
    {
        "type": "heading",
        "title": "5.8 MODEL EVALUATION METRICS MATHEMATICAL DEFINITIONS",
        "content": [
            (
                "To guarantee rigorous empirical evaluation, standard mathematical loss functions and performance metrics were implemented:"
            ),
            (
                "A. Regression Evaluation Metrics (Air Quality):\n"
                "1. Mean Absolute Error (MAE): Measures the average magnitude of absolute prediction errors:\n"
                "MAE = (1 / N) * sum_{i=1}^N |y_i - y_hat_i|\n"
                "2. Root Mean Squared Error (RMSE): Penalizes large outlier errors more heavily due to quadratic squaring:\n"
                "RMSE = sqrt((1 / N) * sum_{i=1}^N (y_i - y_hat_i)^2)\n"
                "3. Coefficient of Determination (R2): Quantifies the proportion of target variance explained by model features:\n"
                "R2 = 1 - [sum_{i=1}^N (y_i - y_hat_i)^2 / sum_{i=1}^N (y_i - y_bar)^2]"
            ),
            (
                "B. Classification Evaluation Metrics (Water Potability):\n"
                "1. Accuracy: Overall fraction of correct classifications: Acc = (TP + TN) / (TP + TN + FP + FN)\n"
                "2. Precision: Exactness of potable predictions: Prec = TP / (TP + FP)\n"
                "3. Recall (Sensitivity): Completeness of detected potable instances: Rec = TP / (TP + FN)\n"
                "4. F1-Score: Harmonic mean of precision and recall: F1 = 2 * (Prec * Rec) / (Prec + Rec)\n"
                "5. Area Under the ROC Curve (ROC-AUC): Evaluates the trade-off between True Positive Rate and False Positive Rate across all thresholds."
            )
        ]
    },
    {
        "type": "heading",
        "title": "5.9 SUMMARY OF THE CHAPTER",
        "content": [
            (
                "This chapter articulated the mathematical and algorithmic methodology powering Project EcoTrack. It detailed data provenance, "
                "preprocessing pipelines, multivariate AQI regression, Random Forest water potability classification, Isolation Forest anomaly scoring, "
                "the composite Environmental Health Index formulation, and evaluation metric equations. These formulations are directly realized in the "
                "implementation detailed in Chapter 6."
            )
        ]
    }
]
