import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "ecotrack.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Air Predictions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS air_predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        pm25 REAL,
        pm10 REAL,
        no2 REAL,
        so2 REAL,
        co REAL,
        o3 REAL,
        temperature REAL,
        humidity REAL,
        wind_speed REAL,
        proximity_industrial REAL,
        predicted_aqi REAL,
        aqi_category TEXT,
        is_anomaly INTEGER DEFAULT 0,
        anomaly_score REAL DEFAULT 0.0,
        notes TEXT
    )
    """)
    
    # Water Predictions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS water_predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        ph REAL,
        hardness REAL,
        solids REAL,
        chloramines REAL,
        sulfate REAL,
        conductivity REAL,
        organic_carbon REAL,
        trihalomethanes REAL,
        turbidity REAL,
        predicted_class INTEGER,
        potability_status TEXT,
        probability_potable REAL,
        is_anomaly INTEGER DEFAULT 0,
        anomaly_score REAL DEFAULT 0.0,
        notes TEXT
    )
    """)
    
    # Alerts Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        category TEXT NOT NULL,
        severity TEXT NOT NULL,
        status TEXT DEFAULT 'Active'
    )
    """)
    
    # Recommendations Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        title TEXT NOT NULL,
        recommendation TEXT NOT NULL,
        target_domain TEXT NOT NULL,
        urgency TEXT NOT NULL
    )
    """)
    
    conn.commit()
    conn.close()

def save_air_prediction(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO air_predictions (
        pm25, pm10, no2, so2, co, o3, temperature, humidity, wind_speed, proximity_industrial,
        predicted_aqi, aqi_category, is_anomaly, anomaly_score, notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get('PM2.5'), data.get('PM10'), data.get('NO2'), data.get('SO2'), data.get('CO'), data.get('O3'),
        data.get('Temperature'), data.get('Humidity'), data.get('Wind_Speed'), data.get('Proximity_Industrial'),
        data.get('predicted_aqi'), data.get('aqi_category'), data.get('is_anomaly', 0), data.get('anomaly_score', 0.0),
        data.get('notes', '')
    ))
    record_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return record_id

def save_water_prediction(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO water_predictions (
        ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity,
        predicted_class, potability_status, probability_potable, is_anomaly, anomaly_score, notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get('ph'), data.get('Hardness'), data.get('Solids'), data.get('Chloramines'), data.get('Sulfate'),
        data.get('Conductivity'), data.get('Organic_carbon'), data.get('Trihalomethanes'), data.get('Turbidity'),
        data.get('predicted_class'), data.get('potability_status'), data.get('probability_potable'),
        data.get('is_anomaly', 0), data.get('anomaly_score', 0.0), data.get('notes', '')
    ))
    record_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return record_id

def add_alert(title, message, category, severity):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO alerts (title, message, category, severity)
    VALUES (?, ?, ?, ?)
    """, (title, message, category, severity))
    alert_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return alert_id

def get_recent_air_predictions(limit=50):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM air_predictions ORDER BY id DESC LIMIT ?", (limit,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_recent_water_predictions(limit=50):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM water_predictions ORDER BY id DESC LIMIT ?", (limit,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_alerts(limit=50):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alerts ORDER BY id DESC LIMIT ?", (limit,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def clear_prediction_history():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM air_predictions")
    cursor.execute("DELETE FROM water_predictions")
    cursor.execute("DELETE FROM alerts")
    cursor.execute("DELETE FROM recommendations")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
