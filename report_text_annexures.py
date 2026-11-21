# report_text_annexures.py
# Annexures I to V for EcoTrack 70-Page Project Report

ANNEXURE_I_DATA = {
    "title": "ANNEXURE I\nCOMPLETE REST API SPECIFICATION AND JSON DATA CONTRACTS",
    "sections": [
        {
            "heading": "I.1 OVERVIEW OF REST INTERFACES",
            "content": (
                "The EcoTrack backend exposes a fully documented, high-throughput RESTful API conforming to the OpenAPI 3.1.0 specification. "
                "All state-modifying requests require JSON payloads validated against strict Pydantic v2 schemas. Responses are delivered with "
                "standard HTTP status codes and ISO 8601 timestamps."
            )
        },
        {
            "heading": "I.2 PREDICTIVE INFERENCE ENDPOINTS",
            "content": (
                "Endpoint: POST /api/predict/air-quality\n"
                "Description: Evaluates multivariate atmospheric criteria pollutants, returning continuous predicted AQI, NAAQS category, "
                "Isolation Forest anomaly status, and primary risk driver.\n\n"
                "Sample Request Payload:\n"
                "{\n"
                "  \"PM2_5\": 84.5,\n"
                "  \"PM10\": 142.0,\n"
                "  \"NO2\": 42.1,\n"
                "  \"SO2\": 18.6,\n"
                "  \"CO\": 1.15,\n"
                "  \"O3\": 32.4\n"
                "}\n\n"
                "Sample Response Payload:\n"
                "{\n"
                "  \"predicted_aqi\": 165.2,\n"
                "  \"category\": \"Moderate\",\n"
                "  \"color_code\": \"yellow\",\n"
                "  \"primary_pollutant\": \"PM2.5\",\n"
                "  \"is_anomaly\": false,\n"
                "  \"anomaly_score\": 0.62,\n"
                "  \"grap_directive\": \"GRAP Stage I: Mechanized sweeping and dust suppression active.\"\n"
                "}\n\n"
                "Endpoint: POST /api/predict/water-potability\n"
                "Description: Evaluates nine physicochemical drinking water parameters against WHO standards, returning binary potability "
                "classification and calibrated posterior confidence.\n\n"
                "Sample Request Payload:\n"
                "{\n"
                "  \"ph\": 7.25,\n"
                "  \"Hardness\": 195.4,\n"
                "  \"Solids\": 18450.2,\n"
                "  \"Chloramines\": 6.85,\n"
                "  \"Sulfate\": 320.1,\n"
                "  \"Conductivity\": 420.5,\n"
                "  \"Organic_carbon\": 12.4,\n"
                "  \"Trihalomethanes\": 62.1,\n"
                "  \"Turbidity\": 3.85\n"
                "}\n\n"
                "Sample Response Payload:\n"
                "{\n"
                "  \"potability_verdict\": \"Potable (Safe)\",\n"
                "  \"potability_code\": 1,\n"
                "  \"confidence_percentage\": 82.4,\n"
                "  \"is_anomaly\": false,\n"
                "  \"advisory\": \"Water parameters comply with WHO drinking standards. Routine municipal disinfection sufficient.\"\n"
                "}"
            )
        },
        {
            "heading": "I.3 REAL-TIME TELEMETRY AND NATIONWIDE AGGREGATION ENDPOINTS",
            "content": (
                "Endpoint: GET /api/realtime/india-air?location=delhi_ncr\n"
                "Description: Fetches live atmospheric telemetry for specified Indian monitoring station, incorporating dual UTC/IST timestamps.\n\n"
                "Sample Response Payload:\n"
                "{\n"
                "  \"location_key\": \"delhi_ncr\",\n"
                "  \"station_name\": \"Delhi NCR (Capital Region)\",\n"
                "  \"state\": \"Delhi\",\n"
                "  \"coordinates\": {\"latitude\": 28.6139, \"longitude\": 77.2090},\n"
                "  \"timestamps\": {\n"
                "    \"utc\": \"2026-11-16T06:15:00Z\",\n"
                "    \"ist\": \"16 Nov 2026, 11:45:00 AM IST\"\n"
                "  },\n"
                "  \"measurements\": {\n"
                "    \"PM2_5\": 168.4,\n"
                "    \"PM10\": 285.2,\n"
                "    \"NO2\": 68.1,\n"
                "    \"SO2\": 24.5,\n"
                "    \"CO\": 2.3,\n"
                "    \"O3\": 48.0\n"
                "  },\n"
                "  \"predicted_aqi\": 312.8,\n"
                "  \"category\": \"Very Poor\",\n"
                "  \"grap_stage\": \"Stage II\"\n"
                "}\n\n"
                "Endpoint: GET /api/realtime/india-summary\n"
                "Description: Returns national aggregate metrics across all 15 stations, including average AQI, potability compliance rate, "
                "and active critical warnings."
            )
        }
    ]
}

ANNEXURE_II_DATA = {
    "title": "ANNEXURE II\nCORE SOURCE CODE REPOSITORY EXCERPTS",
    "sections": [
        {
            "heading": "II.1 FASTAPI BACKEND ENTRYPOINT (backend/main.py)",
            "content": (
                "# =====================================================================\n"
                "# EcoTrack: FastAPI Backend Application Entrypoint\n"
                "# =====================================================================\n"
                "import os\n"
                "import uvicorn\n"
                "from fastapi import FastAPI\n"
                "from fastapi.middleware.cors import CORSMiddleware\n"
                "from fastapi.staticfiles import StaticFiles\n"
                "from routes import router\n"
                "from ml_engine import ml_engine\n"
                "from database import init_db\n\n"
                "app = FastAPI(\n"
                "    title='EcoTrack Scientific Environmental API',\n"
                "    version='2.0.0',\n"
                "    description='High-performance environmental telemetry and predictive intelligence'\n"
                ")\n\n"
                "# CORS Configuration\n"
                "app.add_middleware(\n"
                "    CORSMiddleware,\n"
                "    allow_origins=['*'],\n"
                "    allow_credentials=True,\n"
                "    allow_methods=['*'],\n"
                "    allow_headers=['*'],\n"
                ")\n\n"
                "@app.on_event('startup')\n"
                "def startup_event():\n"
                "    init_db()\n"
                "    ml_engine.load_models()\n"
                "    ml_engine.fit_anomaly_detectors()\n"
                "    print('EcoTrack backend initialized successfully with pre-warmed models.')\n\n"
                "app.include_router(router, prefix='/api')\n\n"
                "if __name__ == '__main__':\n"
                "    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)\n"
            )
        },
        {
            "heading": "II.2 MACHINE LEARNING RUNTIME ENGINE (backend/ml_engine.py Excerpt)",
            "content": (
                "# =====================================================================\n"
                "# EcoTrack: Machine Learning Inference Core\n"
                "# =====================================================================\n"
                "import joblib\n"
                "import numpy as np\n"
                "import pandas as pd\n"
                "from sklearn.ensemble import IsolationForest\n\n"
                "class MLEngine:\n"
                "    def __init__(self):\n"
                "        self.air_model = None\n"
                "        self.air_preprocessor = None\n"
                "        self.water_model = None\n"
                "        self.water_preprocessor = None\n"
                "        self.isolation_forest = None\n\n"
                "    def load_models(self):\n"
                "        self.air_model = joblib.load('models/air_quality_best_model.pkl')\n"
                "        self.air_preprocessor = joblib.load('models/air_quality_preprocessor.pkl')\n"
                "        self.water_model = joblib.load('models/water_potability_best_model.pkl')\n"
                "        self.water_preprocessor = joblib.load('models/water_potability_preprocessor.pkl')\n\n"
                "    def predict_air_quality(self, input_dict):\n"
                "        features = np.array([[input_dict['PM2_5'], input_dict['PM10'], input_dict['NO2'],\n"
                "                              input_dict['SO2'], input_dict['CO'], input_dict['O3']]])\n"
                "        X_scaled = self.air_preprocessor.transform(features)\n"
                "        predicted_aqi = float(self.air_model.predict(X_scaled)[0])\n"
                "        category, color = self.categorize_aqi(predicted_aqi)\n"
                "        is_anomaly = bool(self.isolation_forest.predict(features)[0] == -1)\n"
                "        return {\n"
                "            'predicted_aqi': round(predicted_aqi, 1),\n"
                "            'category': category,\n"
                "            'color_code': color,\n"
                "            'is_anomaly': is_anomaly\n"
                "        }\n"
            )
        },
        {
            "heading": "II.3 COMPOSITE ENVIRONMENTAL HEALTH INDEX (backend/analytics_engine.py Excerpt)",
            "content": (
                "# =====================================================================\n"
                "# EcoTrack: Composite Environmental Health Index (EHI)\n"
                "# =====================================================================\n"
                "def calculate_ehi(aqi_val: float, potability_prob: float) -> dict:\n"
                "    air_score = max(0.0, min(100.0, 100.0 - (aqi_val / 3.0)))\n"
                "    water_score = max(0.0, min(100.0, potability_prob * 100.0))\n"
                "    overall_ehi = round(0.50 * air_score + 0.50 * water_score, 1)\n\n"
                "    if overall_ehi >= 80.0:\n"
                "        status, color = 'Optimal', 'emerald'\n"
                "    elif overall_ehi >= 60.0:\n"
                "        status, color = 'Moderate', 'yellow'\n"
                "    elif overall_ehi >= 40.0:\n"
                "        status, color = 'Degraded', 'orange'\n"
                "    else:\n"
                "        status, color = 'Critical Risk', 'red'\n\n"
                "    return {\n"
                "        'score': overall_ehi,\n"
                "        'air_score': round(air_score, 1),\n"
                "        'water_score': round(water_score, 1),\n"
                "        'status': status,\n"
                "        'color': color\n"
                "    }\n"
            )
        }
    ]
}

ANNEXURE_III_DATA = {
    "title": "ANNEXURE III\nTEST SUITE EXECUTION AND VERIFICATION PROTOCOLS",
    "sections": [
        {
            "heading": "III.1 UNIT TESTING MATRIX AND AUTOMATION SUITE",
            "content": (
                "EcoTrack maintains a fully automated verification test suite implemented in `tests/test_api.py` utilizing pytest and "
                "FastAPI's TestClient. All 18 automated test cases execute cleanly on pull requests, ensuring continuous integration (CI) integrity."
            )
        },
        {
            "heading": "III.2 AUTOMATED TEST CASE SPECIFICATIONS (TABLE)",
            "content": (
                "Test ID: TC-01 | Test Description: Air Quality Normal Prediction | Input: Standard CPCB inputs | Expected: 200 OK, valid AQI float | Status: PASS\n"
                "Test ID: TC-02 | Test Description: Air Quality Boundary (Extreme High) | Input: PM2.5 = 999.0 | Expected: 200 OK, Severe AQI > 400 | Status: PASS\n"
                "Test ID: TC-03 | Test Description: Air Quality Negative Value Rejection | Input: PM2.5 = -15.0 | Expected: 422 Unprocessable Entity | Status: PASS\n"
                "Test ID: TC-04 | Test Description: Water Potability Normal Safe Sample | Input: Neutral pH 7.2, Turbidity 2.1 | Expected: 200 OK, Potable = 1 | Status: PASS\n"
                "Test ID: TC-05 | Test Description: Water Potability Toxic THM Spike | Input: THM = 150.0 ug/L | Expected: 200 OK, Non-Potable = 0 | Status: PASS\n"
                "Test ID: TC-06 | Test Description: Live India Station Retrieval | Input: location = 'delhi_ncr' | Expected: 200 OK, dual UTC/IST timestamps | Status: PASS\n"
                "Test ID: TC-07 | Test Description: Invalid Station Fallback | Input: location = 'unknown_xyz' | Expected: 200 OK, fallback to Delhi NCR | Status: PASS\n"
                "Test ID: TC-08 | Test Description: Isolation Forest Outlier Trigger | Input: Out-of-distribution point | Expected: is_anomaly = True | Status: PASS\n"
                "Test ID: TC-09 | Test Description: Historical Log Export Format | Input: format = 'csv' | Expected: text/csv Content-Type, valid rows | Status: PASS\n"
                "Test ID: TC-10 | Test Description: Historical Log Purge Authorization | Input: DELETE /api/history | Expected: 200 OK, count reset to 0 | Status: PASS\n"
                "Test ID: TC-11 | Test Description: Domain Verification Workbench | Input: domain = 'ecotrack.org' | Expected: 200 OK, DNS & SSL report | Status: PASS\n"
                "Test ID: TC-12 | Test Description: Composite EHI Mathematical Bounds | Input: AQI = 0, Water Prob = 1.0 | Expected: EHI = 100.0, Optimal | Status: PASS"
            )
        },
        {
            "heading": "III.3 TEST EXECUTION LOG OUTPUT",
            "content": (
                "============================= test session starts ==============================\n"
                "platform win32 -- Python 3.10.12, pytest-8.1.1, pluggy-1.4.0\n"
                "rootdir: C:\\Users\\ADMIN\\OneDrive\\Desktop\\MiniProject\\UI_dashboard\n"
                "collected 18 items\n\n"
                "tests/test_api.py::test_health_check PASSED                               [ 5%]\n"
                "tests/test_api.py::test_air_prediction_nominal PASSED                      [ 11%]\n"
                "tests/test_api.py::test_air_prediction_severe PASSED                       [ 16%]\n"
                "tests/test_api.py::test_air_validation_negative_input PASSED               [ 22%]\n"
                "tests/test_api.py::test_water_prediction_safe PASSED                       [ 27%]\n"
                "tests/test_api.py::test_water_prediction_contaminated PASSED               [ 33%]\n"
                "tests/test_api.py::test_water_validation_missing_fields PASSED             [ 38%]\n"
                "tests/test_api.py::test_india_locations_list PASSED                        [ 44%]\n"
                "tests/test_api.py::test_india_air_live_feed PASSED                         [ 50%]\n"
                "tests/test_api.py::test_india_air_invalid_location_fallback PASSED         [ 55%]\n"
                "tests/test_api.py::test_india_summary_aggregate PASSED                     [ 61%]\n"
                "tests/test_api.py::test_anomaly_detection_pipeline PASSED                  [ 66%]\n"
                "tests/test_api.py::test_ehi_calculation_edge_cases PASSED                  [ 72%]\n"
                "tests/test_api.py::test_database_persistence_and_retrieval PASSED          [ 77%]\n"
                "tests/test_api.py::test_history_csv_export PASSED                           [ 83%]\n"
                "tests/test_api.py::test_history_json_export PASSED                          [ 88%]\n"
                "tests/test_api.py::test_domain_verification_utility PASSED                  [ 94%]\n"
                "tests/test_api.py::test_system_transparency_metadata PASSED                [100%]\n\n"
                "============================== 18 passed in 2.45s =============================="
            )
        }
    ]
}

ANNEXURE_IV_DATA = {
    "title": "ANNEXURE IV\nHARDWARE SPECIFICATION AND IOT SENSOR PINOUTS",
    "sections": [
        {
            "heading": "IV.1 EDGE SENSING HARDWARE ARCHITECTURE",
            "content": (
                "Project EcoTrack defines a standardized physical hardware sensing node specification engineered around the Espressif "
                "ESP32-WROOM-32 microcontroller. The edge node captures ambient atmospheric and hydrological readings, converts analog "
                "signals via 12-bit ADCs, packages readings into JSON payloads, and transmits telemetry over Wi-Fi/4G to the FastAPI ingestion service."
            )
        },
        {
            "heading": "IV.2 COMPONENT WIRING AND PINOUT MATRIX",
            "content": (
                "1. Espressif ESP32 Node Pin Connections:\n"
                "- Pin 3V3 / VIN: 5.0V external regulated DC input.\n"
                "- Pin GND: Common system ground reference.\n"
                "- Pin GPIO 16 (RX2): Nova Fitness SDS011 TX Pin (UART Serial Communication).\n"
                "- Pin GPIO 17 (TX2): Nova Fitness SDS011 RX Pin (UART Serial Communication).\n"
                "- Pin GPIO 34 (ADC1_CH6): Winsen MQ-135 Multi-Gas Analog Output (V_in = 0.0 to 3.3V).\n"
                "- Pin GPIO 35 (ADC1_CH7): Winsen MQ-7 Carbon Monoxide Analog Output.\n"
                "- Pin GPIO 32 (ADC1_CH4): DFRobot Gravity Analog pH Sensor Signal.\n"
                "- Pin GPIO 33 (ADC1_CH5): DFRobot Gravity Analog TDS Sensor Signal.\n"
                "- Pin GPIO 21 (SDA) / GPIO 22 (SCL): I2C Bus for optional OLED local status display."
            )
        },
        {
            "heading": "IV.3 EMBEDDED C/C++ ARDUINO TELEMETRY TRANSMITTER EXCERPT",
            "content": (
                "#include <WiFi.h>\n"
                "#include <HTTPClient.h>\n"
                "#include <ArduinoJson.h>\n\n"
                "const char* ssid = \"MUNICIPAL_IOT_NET\";\n"
                "const char* password = \"EcoSecure#2026\";\n"
                "const char* serverUrl = \"http://ecotrack.org/api/predict/air-quality\";\n\n"
                "void setup() {\n"
                "    Serial.begin(115200);\n"
                "    WiFi.begin(ssid, password);\n"
                "    while (WiFi.status() != WL_CONNECTED) { delay(500); }\n"
                "}\n\n"
                "void loop() {\n"
                "    if (WiFi.status() == WL_CONNECTED) {\n"
                "        HTTPClient http;\n"
                "        http.begin(serverUrl);\n"
                "        http.addHeader(\"Content-Type\", \"application/json\");\n\n"
                "        StaticJsonDocument<256> doc;\n"
                "        doc[\"PM2_5\"] = readSDS011_PM25();\n"
                "        doc[\"PM10\"] = readSDS011_PM10();\n"
                "        doc[\"NO2\"] = readMQ135_NO2();\n"
                "        doc[\"SO2\"] = readMQ135_SO2();\n"
                "        doc[\"CO\"] = readMQ7_CO();\n"
                "        doc[\"O3\"] = 25.0;\n\n"
                "        String requestBody;\n"
                "        serializeJson(doc, requestBody);\n"
                "        int httpCode = http.POST(requestBody);\n"
                "        http.end();\n"
                "    }\n"
                "    delay(60000); // 1-minute transmission interval\n"
                "}"
            )
        }
    ]
}

ANNEXURE_V_DATA = {
    "title": "ANNEXURE V\nPRODUCTION CONFIGURATION AND NGINX DEPLOYMENT RUNBOOK",
    "sections": [
        {
            "heading": "V.1 SYSTEMD SERVICE UNIT CONFIGURATION (/etc/systemd/system/ecotrack.service)",
            "content": (
                "[Unit]\n"
                "Description=EcoTrack Production FastAPI ASGI Service\n"
                "After=network.target\n\n"
                "[Service]\n"
                "User=www-data\n"
                "Group=www-data\n"
                "WorkingDirectory=/var/www/ecotrack/backend\n"
                "Environment=\"PATH=/var/www/ecotrack/venv/bin\"\n"
                "ExecStart=/var/www/ecotrack/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 --workers 4 --proxy-headers\n"
                "Restart=always\n"
                "RestartSec=5\n\n"
                "[Install]\n"
                "WantedBy=multi-user.target"
            )
        },
        {
            "heading": "V.2 NGINX REVERSE PROXY AND SSL CONFIGURATION (/etc/nginx/sites-available/ecotrack.conf)",
            "content": (
                "server {\n"
                "    listen 80;\n"
                "    server_name ecotrack.org www.ecotrack.org;\n"
                "    return 301 https://$host$request_uri;\n"
                "}\n\n"
                "server {\n"
                "    listen 443 ssl http2;\n"
                "    server_name ecotrack.org www.ecotrack.org;\n\n"
                "    ssl_certificate /etc/letsencrypt/live/ecotrack.org/fullchain.pem;\n"
                "    ssl_certificate_key /etc/letsencrypt/live/ecotrack.org/privkey.pem;\n"
                "    ssl_protocols TLSv1.2 TLSv1.3;\n"
                "    ssl_ciphers HIGH:!aNULL:!MD5;\n\n"
                "    # Production Frontend Static Assets\n"
                "    location / {\n"
                "        root /var/www/ecotrack/frontend/dist;\n"
                "        index index.html;\n"
                "        try_files $uri $uri/ /index.html;\n"
                "        gzip on;\n"
                "        gzip_types text/plain text/css application/json application/javascript;\n"
                "    }\n\n"
                "    # API Reverse Proxy Routing\n"
                "    location /api/ {\n"
                "        proxy_pass http://127.0.0.1:8000/api/;\n"
                "        proxy_set_header Host $host;\n"
                "        proxy_set_header X-Real-IP $remote_addr;\n"
                "        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n"
                "        proxy_set_header X-Forwarded-Proto $scheme;\n"
                "        proxy_connect_timeout 60s;\n"
                "        proxy_read_timeout 60s;\n"
                "    }\n"
                "}"
            )
        },
        {
            "heading": "V.3 DEPLOYMENT COMMAND EXECUTION WORKFLOW",
            "content": (
                "# 1. Clone repository and set permissions\n"
                "cd /var/www && git clone https://github.com/ecotrack-org/ecotrack.git\n"
                "sudo chown -R www-data:www-data /var/www/ecotrack\n\n"
                "# 2. Build Python backend virtual environment\n"
                "cd /var/www/ecotrack/backend\n"
                "python3 -m venv venv && source venv/bin/activate\n"
                "pip install --upgrade pip && pip install -r requirements.txt\n\n"
                "# 3. Build frontend single page application\n"
                "cd /var/www/ecotrack/frontend\n"
                "npm install && npm run build\n\n"
                "# 4. Activate Systemd daemon and Nginx\n"
                "sudo systemctl daemon-reload\n"
                "sudo systemctl enable ecotrack.service && sudo systemctl start ecotrack.service\n"
                "sudo ln -s /etc/nginx/sites-available/ecotrack.conf /etc/nginx/sites-enabled/\n"
                "sudo nginx -t && sudo systemctl reload nginx"
            )
        }
    ]
}
