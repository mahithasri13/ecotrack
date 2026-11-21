import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split

BASE_DIR = os.path.dirname(__file__)
MODELS_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data")

AIR_MODEL_PATH = os.path.join(MODELS_DIR, "air_quality_best_model.pkl")
AIR_PREP_PATH = os.path.join(MODELS_DIR, "air_quality_preprocessor.pkl")
WATER_MODEL_PATH = os.path.join(MODELS_DIR, "water_potability_best_model.pkl")
WATER_PREP_PATH = os.path.join(MODELS_DIR, "water_potability_preprocessor.pkl")

AIR_DATA_PATH = os.path.join(DATA_DIR, "air_quality.csv")
WATER_DATA_PATH = os.path.join(DATA_DIR, "water_potability.csv")

class MLEngine:
    def __init__(self):
        self.air_model = None
        self.air_prep = None
        self.water_model = None
        self.water_prep = None
        
        self.air_iso_forest = None
        self.water_iso_forest = None
        self.air_stats = {}
        self.water_stats = {}
        
        self.load_models()
        self.fit_anomaly_detectors()

    def load_models(self):
        if os.path.exists(AIR_MODEL_PATH) and os.path.exists(AIR_PREP_PATH):
            self.air_model = joblib.load(AIR_MODEL_PATH)
            self.air_prep = joblib.load(AIR_PREP_PATH)
        else:
            raise FileNotFoundError("Air Quality model artifacts missing.")
            
        if os.path.exists(WATER_MODEL_PATH) and os.path.exists(WATER_PREP_PATH):
            self.water_model = joblib.load(WATER_MODEL_PATH)
            self.water_prep = joblib.load(WATER_PREP_PATH)
        else:
            raise FileNotFoundError("Water Potability model artifacts missing.")

    def fit_anomaly_detectors(self):
        # Air Quality Anomaly Detector
        if os.path.exists(AIR_DATA_PATH):
            df_air = pd.read_csv(AIR_DATA_PATH)
            feature_cols = self.air_prep['feature_names']
            X_air = df_air[feature_cols]
            X_imp = self.air_prep['imputer'].transform(X_air)
            X_scaled = self.air_prep['scaler'].transform(X_imp)
            
            self.air_iso_forest = IsolationForest(contamination=0.05, random_state=42)
            self.air_iso_forest.fit(X_scaled)
            
            # Save distribution stats for Z-score checks
            for col in feature_cols:
                self.air_stats[col] = {
                    'mean': float(df_air[col].mean()),
                    'std': float(df_air[col].std()) if df_air[col].std() > 0 else 1.0,
                    'min': float(df_air[col].min()),
                    'max': float(df_air[col].max())
                }
                
        # Water Quality Anomaly Detector
        if os.path.exists(WATER_DATA_PATH):
            df_water = pd.read_csv(WATER_DATA_PATH)
            feature_cols = self.water_prep['feature_names']
            X_water = df_water[feature_cols]
            X_imp = self.water_prep['imputer'].transform(X_water)
            X_scaled = self.water_prep['scaler'].transform(X_imp)
            
            self.water_iso_forest = IsolationForest(contamination=0.05, random_state=42)
            self.water_iso_forest.fit(X_scaled)
            
            # Save distribution stats
            for col in feature_cols:
                self.water_stats[col] = {
                    'mean': float(df_water[col].mean()),
                    'std': float(df_water[col].std()) if df_water[col].std() > 0 else 1.0,
                    'min': float(df_water[col].min()),
                    'max': float(df_water[col].max())
                }

    def categorize_aqi(self, aqi_val):
        if aqi_val <= 50:
            return "Good", "Green", "Air quality is considered satisfactory, and air pollution poses little or no risk."
        elif aqi_val <= 100:
            return "Moderate", "Yellow", "Air quality is acceptable; however, for some pollutants there may be a moderate health concern."
        elif aqi_val <= 150:
            return "Unhealthy for Sensitive Groups", "Orange", "Members of sensitive groups may experience health effects. The general public is not likely to be affected."
        elif aqi_val <= 200:
            return "Unhealthy", "Red", "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects."
        elif aqi_val <= 300:
            return "Very Unhealthy", "Purple", "Health alert: everyone may experience more serious health effects."
        else:
            return "Hazardous", "Maroon", "Health warnings of emergency conditions. The entire population is more likely to be affected."

    def predict_air_quality(self, input_dict):
        feature_cols = self.air_prep['feature_names']
        input_df = pd.DataFrame([input_dict])
        
        # Ensure all columns exist
        for col in feature_cols:
            if col not in input_df.columns:
                input_df[col] = np.nan
                
        input_df = input_df[feature_cols]
        X_imp = self.air_prep['imputer'].transform(input_df)
        X_scaled = self.air_prep['scaler'].transform(X_imp)
        
        raw_pred = self.air_model.predict(X_scaled)[0]
        aqi_val = max(0.0, round(float(raw_pred), 2))
        category, color, health_desc = self.categorize_aqi(aqi_val)
        
        # Anomaly Detection
        iso_score = self.air_iso_forest.decision_function(X_scaled)[0] if self.air_iso_forest else 0.0
        iso_pred = self.air_iso_forest.predict(X_scaled)[0] if self.air_iso_forest else 1
        
        # Convert decision function score to normalized anomaly degree 0-1
        normalized_anomaly_score = round(float(np.clip((0.2 - iso_score) / 0.5, 0.0, 1.0)), 3)
        
        z_outliers = []
        for col in feature_cols:
            val = input_dict.get(col)
            if val is not None and col in self.air_stats:
                st = self.air_stats[col]
                z = (val - st['mean']) / st['std']
                if abs(z) > 2.8:
                    z_outliers.append(f"{col} value ({val}) deviates significantly (Z={z:.1f}) from average ({st['mean']:.1f})")
                    
        is_anomaly = bool(iso_pred == -1 or len(z_outliers) > 0)
        
        return {
            'predicted_aqi': aqi_val,
            'aqi_category': category,
            'category_color': color,
            'health_description': health_desc,
            'is_anomaly': is_anomaly,
            'anomaly_score': normalized_anomaly_score,
            'anomaly_reasons': z_outliers,
            'processed_features': dict(zip(feature_cols, X_imp[0]))
        }

    def predict_water_potability(self, input_dict):
        feature_cols = self.water_prep['feature_names']
        input_df = pd.DataFrame([input_dict])
        
        for col in feature_cols:
            if col not in input_df.columns:
                input_df[col] = np.nan
                
        input_df = input_df[feature_cols]
        X_imp = self.water_prep['imputer'].transform(input_df)
        X_scaled = self.water_prep['scaler'].transform(X_imp)
        
        pred_class = int(self.water_model.predict(X_scaled)[0])
        prob_potable = float(self.water_model.predict_proba(X_scaled)[0][1]) if hasattr(self.water_model, "predict_proba") else (1.0 if pred_class == 1 else 0.0)
        
        status = "Potable (Safe)" if pred_class == 1 else "Non-Potable (Unsafe)"
        
        # Anomaly Detection
        iso_score = self.water_iso_forest.decision_function(X_scaled)[0] if self.water_iso_forest else 0.0
        iso_pred = self.water_iso_forest.predict(X_scaled)[0] if self.water_iso_forest else 1
        normalized_anomaly_score = round(float(np.clip((0.2 - iso_score) / 0.5, 0.0, 1.0)), 3)
        
        z_outliers = []
        for col in feature_cols:
            val = input_dict.get(col)
            if val is not None and col in self.water_stats:
                st = self.water_stats[col]
                z = (val - st['mean']) / st['std']
                if abs(z) > 2.8:
                    z_outliers.append(f"{col} value ({val}) deviates significantly (Z={z:.1f}) from normal range ({st['min']:.1f}-{st['max']:.1f})")
                    
        is_anomaly = bool(iso_pred == -1 or len(z_outliers) > 0)
        
        return {
            'predicted_class': pred_class,
            'potability_status': status,
            'probability_potable': round(prob_potable, 4),
            'confidence_percentage': round(prob_potable * 100 if pred_class == 1 else (1 - prob_potable) * 100, 2),
            'is_anomaly': is_anomaly,
            'anomaly_score': normalized_anomaly_score,
            'anomaly_reasons': z_outliers,
            'processed_features': dict(zip(feature_cols, X_imp[0]))
        }

    def compute_live_metrics(self):
        metrics = {'air': {}, 'water': {}}
        
        # Air Model Evaluation
        if os.path.exists(AIR_DATA_PATH):
            df_air = pd.read_csv(AIR_DATA_PATH)
            feature_cols = self.air_prep['feature_names']
            X = df_air[feature_cols]
            y = df_air['AQI']
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            X_test_imp = self.air_prep['imputer'].transform(X_test)
            X_test_scaled = self.air_prep['scaler'].transform(X_test_imp)
            
            y_pred = self.air_model.predict(X_test_scaled)
            
            metrics['air'] = {
                'mae': round(float(mean_absolute_error(y_test, y_pred)), 4),
                'mse': round(float(mean_squared_error(y_test, y_pred)), 4),
                'rmse': round(float(np.sqrt(mean_squared_error(y_test, y_pred))), 4),
                'r2_score': round(float(r2_score(y_test, y_pred)), 4),
                'model_name': type(self.air_model).__name__,
                'sample_count': len(df_air)
            }
            
        # Water Model Evaluation
        if os.path.exists(WATER_DATA_PATH):
            df_water = pd.read_csv(WATER_DATA_PATH)
            feature_cols = self.water_prep['feature_names']
            X = df_water[feature_cols]
            y = df_water['Potability']
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            X_test_imp = self.water_prep['imputer'].transform(X_test)
            X_test_scaled = self.water_prep['scaler'].transform(X_test_imp)
            
            y_pred = self.water_model.predict(X_test_scaled)
            y_prob = self.water_model.predict_proba(X_test_scaled)[:, 1] if hasattr(self.water_model, "predict_proba") else y_pred
            
            metrics['water'] = {
                'accuracy': round(float(accuracy_score(y_test, y_pred)), 4),
                'precision': round(float(precision_score(y_test, y_pred, zero_division=0)), 4),
                'recall': round(float(recall_score(y_test, y_pred, zero_division=0)), 4),
                'f1_score': round(float(f1_score(y_test, y_pred, zero_division=0)), 4),
                'roc_auc': round(float(roc_auc_score(y_test, y_prob)), 4),
                'model_name': type(self.water_model).__name__,
                'sample_count': len(df_water)
            }
            
        return metrics

# Instantiated Singleton ML Engine
ml_engine = MLEngine()

if __name__ == '__main__':
    print("Testing ML Engine...")
    air_sample = {
        'PM2.5': 45.0, 'PM10': 85.0, 'NO2': 30.0, 'SO2': 10.0, 'CO': 1.2,
        'O3': 35.0, 'Temperature': 25.0, 'Humidity': 60.0, 'Wind_Speed': 10.0, 'Proximity_Industrial': 12.0
    }
    air_res = ml_engine.predict_air_quality(air_sample)
    print("Air Result:", air_res)
    
    water_sample = {
        'ph': 7.4, 'Hardness': 200.0, 'Solids': 20000.0, 'Chloramines': 7.0,
        'Sulfate': 300.0, 'Conductivity': 420.0, 'Organic_carbon': 14.0,
        'Trihalomethanes': 65.0, 'Turbidity': 3.8
    }
    water_res = ml_engine.predict_water_potability(water_sample)
    print("Water Result:", water_res)
    
    print("Metrics:", ml_engine.compute_live_metrics())
