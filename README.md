# EcoTrack: AI-Based Smart Environmental Impact Monitoring System

EcoTrack is a production-grade, scientific environmental monitoring system that uses machine learning to analyze environmental data, detect abnormal conditions, and predict environmental health risks.

## Key Capabilities

- **Real-Time Air Quality Monitoring and AQI Prediction**: Multivariate regression models for particulate matter (PM2.5, PM10) and gaseous pollutants (NO2, SO2, CO, O3) mapped to Indian National Ambient Air Quality Standards (NAAQS).
- **Water Potability Prediction**: Supervised classification predicting drinking water safety across 9 physicochemical attributes against World Health Organization (WHO) standards.
- **Location-Based Monitoring Across India**: Live atmospheric data ingestion via Open-Meteo European Meteorological Feeds across 15 metropolitan, heritage, and rural monitoring stations with local IST timestamps.
- **Anomaly Detection**: Unsupervised Isolation Forest outlier detection identifying sensor drift, calibration faults, and acute emission anomalies.
- **Automated Alerts and Actionable Directives**: Dynamic threshold breach notifications and policy mitigation directives.
- **Verified Empirical Metrics**: Model performance scores (R2, MAE, RMSE, Accuracy, F1-Score, ROC-AUC) computed live directly from train-test splits on genuine datasets (zero hardcoding or fabrication).
- **Pre-Launch Production Readiness**: Domain and HTTPS verification workbench, Nginx reverse proxy configuration generator, scientific SVG favicon, Privacy Policy, and Terms and Conditions pages.

## Design Philosophy

- Clean scientific dashboard with crisp white surfaces (`#ffffff`), forest green (`#1b4332`), teal (`#0f766e`), and charcoal (`#1e293b`).
- Zero purple gradients, zero pill-shaped buttons, zero emojis, and zero em dashes.
- Fully transparent data provenance, timestamps, and model scope limitations.

## Getting Started

### 1. Backend Service

```bash
cd backend
pip install -r requirements.txt
python main.py
```
FastAPI runs on `http://127.0.0.1:8000` with interactive API docs at `/docs`.

### 2. Frontend Application

```bash
cd frontend
npm install
npm run build
```
The FastAPI backend serves the production frontend build directly from `frontend/dist`.

### 3. Running Verification Suite

```bash
python tests/test_api.py
```
# ecotrack
# ecotrack
