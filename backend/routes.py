from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import pandas as pd
import numpy as np
import io
import csv
import socket
import ssl
import datetime

from database import (
    save_air_prediction, save_water_prediction, add_alert,
    get_recent_air_predictions, get_recent_water_predictions, get_alerts,
    clear_prediction_history
)
from ml_engine import ml_engine, AIR_DATA_PATH, WATER_DATA_PATH
from analytics_engine import (
    calculate_ehi, analyze_environmental_impact,
    generate_dynamic_alerts, generate_recommendations
)

router = APIRouter(prefix="/api")

class AirQualityInput(BaseModel):
    PM2_5: float = Field(..., alias="PM2.5", ge=0, le=1000)
    PM10: float = Field(..., ge=0, le=2000)
    NO2: float = Field(..., ge=0, le=1000)
    SO2: float = Field(..., ge=0, le=1000)
    CO: float = Field(..., ge=0, le=100)
    O3: float = Field(..., ge=0, le=1000)
    Temperature: float = Field(..., ge=-50, le=70)
    Humidity: float = Field(..., ge=0, le=100)
    Wind_Speed: float = Field(..., ge=0, le=150)
    Proximity_Industrial: float = Field(..., ge=0, le=100)

class WaterPotabilityInput(BaseModel):
    ph: float = Field(..., ge=0, le=14)
    Hardness: float = Field(..., ge=0, le=1000)
    Solids: float = Field(..., ge=0, le=100000)
    Chloramines: float = Field(..., ge=0, le=30)
    Sulfate: float = Field(..., ge=0, le=1000)
    Conductivity: float = Field(..., ge=0, le=2000)
    Organic_carbon: float = Field(..., ge=0, le=100)
    Trihalomethanes: float = Field(..., ge=0, le=300)
    Turbidity: float = Field(..., ge=0, le=50)

@router.post("/predict/air-quality")
def predict_air_quality_endpoint(payload: AirQualityInput):
    try:
        data = payload.model_dump(by_alias=True)
        res = ml_engine.predict_air_quality(data)
        
        # Save to DB
        record_data = {**data, **res}
        record_id = save_air_prediction(record_data)
        
        # Alerts & Recs
        alerts = generate_dynamic_alerts(air_res=res, air_input=data)
        for alt in alerts:
            add_alert(alt['title'], alt['message'], alt['category'], alt['severity'])
            
        recs = generate_recommendations(air_res=res, air_input=data)
        impact = analyze_environmental_impact(air_input=data, air_res=res)
        
        return {
            'record_id': record_id,
            'prediction': res,
            'impact_analysis': impact,
            'alerts': alerts,
            'recommendations': recs
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Air quality prediction failed: {str(e)}")

@router.post("/predict/water-potability")
def predict_water_potability_endpoint(payload: WaterPotabilityInput):
    try:
        data = payload.model_dump(by_alias=True)
        res = ml_engine.predict_water_potability(data)
        
        # Save to DB
        record_data = {**data, **res}
        record_id = save_water_prediction(record_data)
        
        # Alerts & Recs
        alerts = generate_dynamic_alerts(water_res=res, water_input=data)
        for alt in alerts:
            add_alert(alt['title'], alt['message'], alt['category'], alt['severity'])
            
        recs = generate_recommendations(water_res=res, water_input=data)
        impact = analyze_environmental_impact(water_input=data, water_res=res)
        
        return {
            'record_id': record_id,
            'prediction': res,
            'impact_analysis': impact,
            'alerts': alerts,
            'recommendations': recs
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Water potability prediction failed: {str(e)}")

@router.get("/dashboard/summary")
def get_dashboard_summary():
    recent_air = get_recent_air_predictions(20)
    recent_water = get_recent_water_predictions(20)
    db_alerts = get_alerts(10)
    
    avg_aqi = round(float(np.mean([r['predicted_aqi'] for r in recent_air])), 1) if recent_air else 68.5
    potable_count = sum(1 for r in recent_water if r['predicted_class'] == 1)
    potability_rate = round((potable_count / len(recent_water)) * 100, 1) if recent_water else 78.5
    
    potability_prob_avg = (potability_rate / 100.0)
    ehi = calculate_ehi(avg_aqi, potability_prob_avg)
    
    active_alerts = len([a for a in db_alerts if a['severity'] in ['Critical', 'Warning']])
    
    return {
        'ehi': ehi,
        'average_aqi': avg_aqi,
        'potability_rate': potability_rate,
        'total_predictions': len(recent_air) + len(recent_water),
        'active_alert_count': max(active_alerts, 2 if avg_aqi > 100 else 0),
        'recent_air': recent_air[:5],
        'recent_water': recent_water[:5],
        'alerts': db_alerts[:5]
    }

@router.get("/analytics/trends")
def get_analytics_trends():
    """Returns dataset baseline historical trends and combined predictions time series."""
    df_air = pd.read_csv(AIR_DATA_PATH).head(30).fillna(0) if AIR_DATA_PATH else pd.DataFrame()
    df_water = pd.read_csv(WATER_DATA_PATH).head(30).fillna(0) if WATER_DATA_PATH else pd.DataFrame()
    
    air_trend = []
    if not df_air.empty:
        for idx, row in df_air.iterrows():
            air_trend.append({
                'point': f"Day {idx+1}",
                'AQI': round(float(row['AQI']), 1),
                'PM25': round(float(row['PM2.5']), 1),
                'PM10': round(float(row['PM10']), 1),
                'NO2': round(float(row['NO2']), 1),
                'SO2': round(float(row['SO2']), 1)
            })
            
    water_trend = []
    if not df_water.empty:
        for idx, row in df_water.iterrows():
            water_trend.append({
                'sample': f"Sample {idx+1}",
                'ph': round(float(row['ph']) if pd.notnull(row['ph']) else 7.0, 2),
                'Turbidity': round(float(row['Turbidity']) if pd.notnull(row['Turbidity']) else 3.5, 2),
                'Sulfate': round(float(row['Sulfate']) if pd.notnull(row['Sulfate']) else 300, 1),
                'Potability': int(row['Potability'])
            })
            
    return {
        'air_trends': air_trend,
        'water_trends': water_trend
    }

@router.get("/analytics/anomaly-detection")
def get_anomaly_detection_overview():
    """Runs IsolationForest on dataset samples and returns scatter plotting points."""
    df_air = pd.read_csv(AIR_DATA_PATH).fillna(0)
    df_sample = df_air.sample(n=min(60, len(df_air)), random_state=42)
    feature_cols = ml_engine.air_prep['feature_names']
    X_air = df_sample[feature_cols]
    X_imp = ml_engine.air_prep['imputer'].transform(X_air)
    X_scaled = ml_engine.air_prep['scaler'].transform(X_imp)
    
    iso_preds = ml_engine.air_iso_forest.predict(X_scaled)
    iso_scores = ml_engine.air_iso_forest.decision_function(X_scaled)
    
    points = []
    anomaly_count = 0
    for idx, (row, pred, score) in enumerate(zip(df_sample.iterrows(), iso_preds, iso_scores)):
        is_anom = bool(pred == -1)
        if is_anom:
            anomaly_count += 1
        points.append({
            'id': idx + 1,
            'PM25': round(float(row[1]['PM2.5']), 1),
            'AQI': round(float(row[1]['AQI']), 1),
            'NO2': round(float(row[1]['NO2']), 1),
            'anomaly_score': round(float(np.clip((0.2 - score) / 0.5, 0.0, 1.0)), 3),
            'is_anomaly': is_anom,
            'status': 'Anomalous' if is_anom else 'Normal'
        })
        
    return {
        'total_analyzed': len(points),
        'anomalies_detected': anomaly_count,
        'normal_count': len(points) - anomaly_count,
        'scatter_data': points
    }

@router.get("/alerts")
def get_alerts_endpoint():
    recent = get_alerts(30)
    if not recent:
        # Default active baseline alerts if none recorded yet
        return [
            {
                'id': 1,
                'timestamp': 'Just now',
                'title': 'PM2.5 Elevated Threshold Warning',
                'message': 'Ambient fine particulate concentration exceeds WHO recommended 24h average.',
                'category': 'Air Quality',
                'severity': 'Warning',
                'status': 'Active'
            },
            {
                'id': 2,
                'timestamp': '10 mins ago',
                'title': 'System Status Normal',
                'message': 'Water filtration stations reporting nominal pH and turbidity levels.',
                'category': 'System',
                'severity': 'Info',
                'status': 'Active'
            }
        ]
    return recent

@router.get("/recommendations")
def get_recommendations_endpoint():
    recent_air = get_recent_air_predictions(1)
    recent_water = get_recent_water_predictions(1)
    
    air_res = recent_air[0] if recent_air else {'predicted_aqi': 85}
    water_res = recent_water[0] if recent_water else {'predicted_class': 1}
    
    return generate_recommendations(air_res=air_res, water_res=water_res)

@router.get("/history")
def get_history():
    air_hist = get_recent_air_predictions(50)
    water_hist = get_recent_water_predictions(50)
    return {
        'air_predictions': air_hist,
        'water_predictions': water_hist
    }

@router.delete("/history")
def clear_history():
    clear_prediction_history()
    return {'message': 'All prediction history cleared successfully.'}

@router.get("/history/export")
def export_history(format: str = Query("csv", regex="^(csv|json)$")):
    air_hist = get_recent_air_predictions(100)
    water_hist = get_recent_water_predictions(100)
    
    if format == "json":
        return {'air': air_hist, 'water': water_hist}
    
    # CSV Export
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Domain', 'ID', 'Timestamp', 'Primary Result', 'Status / Category', 'Is Anomaly', 'Anomaly Score'])
    
    for a in air_hist:
        writer.writerow(['Air Quality', a['id'], a['timestamp'], f"AQI {a['predicted_aqi']}", a['aqi_category'], a['is_anomaly'], a['anomaly_score']])
    for w in water_hist:
        writer.writerow(['Water Quality', w['id'], w['timestamp'], w['potability_status'], f"Prob: {w['probability_potable']}", w['is_anomaly'], w['anomaly_score']])
        
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=ecotrack_history.csv"}
    )

@router.get("/metrics")
def get_live_metrics():
    return ml_engine.compute_live_metrics()

@router.get("/dataset-info")
def get_dataset_info():
    df_air = pd.read_csv(AIR_DATA_PATH)
    df_water = pd.read_csv(WATER_DATA_PATH)
    
    air_summary = df_air.describe().fillna(0).to_dict()
    water_summary = df_water.describe().fillna(0).to_dict()
    
    return {
        'air_dataset': {
            'row_count': len(df_air),
            'columns': df_air.columns.tolist(),
            'missing_values': df_air.isnull().sum().to_dict(),
            'summary_stats': air_summary
        },
        'water_dataset': {
            'row_count': len(df_water),
            'columns': df_water.columns.tolist(),
            'missing_values': df_water.isnull().sum().to_dict(),
            'summary_stats': water_summary
        }
    }

# Real-Time India Monitoring Endpoints
from india_live_service import INDIAN_LOCATIONS, get_realtime_air_data, get_realtime_water_data, get_nationwide_india_summary

@router.get("/realtime/india-locations")
def get_india_locations():
    return INDIAN_LOCATIONS

@router.get("/realtime/india-air")
def get_india_air_realtime(location: str = Query("delhi_ncr")):
    return get_realtime_air_data(location)

@router.get("/realtime/india-water")
def get_india_water_realtime(location: str = Query("delhi_ncr")):
    return get_realtime_water_data(location)

@router.get("/realtime/india-summary")
def get_india_summary():
    return get_nationwide_india_summary()

@router.get("/system/domain-verification")
def verify_custom_domain(domain: str = Query("ecotrack.org")):
    clean_domain = domain.strip().lower()
    if clean_domain.startswith("https://"):
        clean_domain = clean_domain[8:]
    elif clean_domain.startswith("http://"):
        clean_domain = clean_domain[7:]
    clean_domain = clean_domain.split("/")[0].split(":")[0]

    # DNS Resolution
    dns_resolved = False
    ip_addresses = []
    dns_error = None
    try:
        addr_info = socket.getaddrinfo(clean_domain, 443)
        ip_addresses = list(set([item[4][0] for item in addr_info]))
        dns_resolved = len(ip_addresses) > 0
    except Exception as e:
        dns_error = str(e)

    # HTTPS Handshake Check
    ssl_valid = False
    cert_info = {}
    ssl_error = None
    if dns_resolved:
        try:
            context = ssl.create_default_context()
            with socket.create_connection((clean_domain, 443), timeout=3.5) as sock:
                with context.wrap_socket(sock, server_hostname=clean_domain) as ssock:
                    cert = ssock.getpeercert()
                    ssl_valid = True
                    cert_info = {
                        "subject": dict(x[0] for x in cert.get("subject", [])),
                        "issuer": dict(x[0] for x in cert.get("issuer", [])),
                        "version": ssock.version(),
                        "notBefore": cert.get("notBefore"),
                        "notAfter": cert.get("notAfter"),
                    }
        except Exception as e:
            ssl_error = str(e)

    # Production Nginx Config template
    nginx_config = f"""# Nginx reverse proxy configuration for {clean_domain}
server {{
    listen 80;
    server_name {clean_domain};
    return 301 https://$host$request_uri;
}}

server {{
    listen 443 ssl http2;
    server_name {clean_domain};

    ssl_certificate /etc/letsencrypt/live/{clean_domain}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/{clean_domain}/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;

    location / {{
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}"""

    return {
        "domain": clean_domain,
        "dns_resolved": dns_resolved,
        "ip_addresses": ip_addresses,
        "dns_error": dns_error,
        "ssl_valid": ssl_valid,
        "cert_info": cert_info,
        "ssl_error": ssl_error,
        "status": "Verified and Secure" if (dns_resolved and ssl_valid) else ("DNS Active, SSL Pending" if dns_resolved else "Unresolved"),
        "nginx_snippet": nginx_config,
        "certbot_command": f"certbot --nginx -d {clean_domain}",
        "verification_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

@router.get("/system/transparency")
def get_system_transparency():
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    ist_tz = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    now_ist = datetime.datetime.now(ist_tz)
    
    return {
        "system_name": "EcoTrack",
        "system_version": "1.0.0-production",
        "utc_timestamp": now_utc.isoformat(),
        "ist_timestamp": now_ist.strftime("%Y-%m-%d %H:%M:%S IST"),
        "data_sources": [
            {
                "name": "Open-Meteo Air Quality and Atmospheric API",
                "scope": "Real-time PM2.5, PM10, CO, NO2, SO2, O3, Temperature, Humidity, Wind Speed",
                "coverage": "All monitored Indian regions (Metropolitan, Industrial, Rural)",
                "latency": "Hourly satellite and ground assimilation model updates",
                "attribution": "Copernicus Atmosphere Monitoring Service (CAMS) and ECMWF"
            },
            {
                "name": "Central Pollution Control Board (CPCB) NAAQS Framework",
                "scope": "Indian National Ambient Air Quality Standards and AQI breakpoint formulas",
                "coverage": "India Nationwide standard thresholds",
                "attribution": "Ministry of Environment, Forest and Climate Change (MoEFCC), Govt. of India"
            },
            {
                "name": "Water Potability Physicochemical Dataset",
                "scope": "pH, Hardness, Solids (TDS), Chloramines, Sulfate, Conductivity, Organic Carbon, Trihalomethanes, Turbidity",
                "reference_standard": "World Health Organization (WHO) Guidelines for Drinking-water Quality",
                "sample_count": 3276
            }
        ],
        "models": [
            {
                "task": "Air Quality Index (AQI) Regression",
                "model_type": type(ml_engine.air_model).__name__,
                "input_features": ml_engine.air_prep['feature_names'],
                "anomaly_detector": "Isolation Forest (unsupervised outlier detection, contamination=0.05)"
            },
            {
                "task": "Water Potability Binary Classification",
                "model_type": type(ml_engine.water_model).__name__,
                "input_features": ml_engine.water_prep['feature_names'],
                "anomaly_detector": "Isolation Forest (contamination=0.05) and Parametric Z-Score Filtering"
            }
        ],
        "limitations": [
            "Air quality predictions are ambient outdoor estimates and do not account for hyper-localized indoor microenvironments or unmonitored volatile organic compounds (VOCs).",
            "Water potability model assesses physicochemical and mineral safety; microbiological pathogens (such as E. coli or viral loads) require certified laboratory incubation tests.",
            "Predictions are decision-support estimates. Critical emergency response decisions must be confirmed with certified governmental monitoring stations."
        ]
    }


