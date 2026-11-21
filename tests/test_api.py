import sys
import os
import unittest
from fastapi.testclient import TestClient

# Add backend directory to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "backend"))

from main import app
from database import init_db

class TestEcoTrackAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        cls.client = TestClient(app)

    def test_dashboard_summary(self):
        response = self.client.get("/api/dashboard/summary")
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIn("ehi", json_data)
        self.assertIn("average_aqi", json_data)

    def test_predict_air_quality(self):
        payload = {
            "PM2.5": 25.4,
            "PM10": 45.0,
            "NO2": 15.2,
            "SO2": 8.0,
            "CO": 0.8,
            "O3": 30.0,
            "Temperature": 24.0,
            "Humidity": 55.0,
            "Wind_Speed": 12.0,
            "Proximity_Industrial": 10.0
        }
        response = self.client.post("/api/predict/air-quality", json=payload)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIn("prediction", json_data)
        self.assertIn("predicted_aqi", json_data["prediction"])
        self.assertIn("aqi_category", json_data["prediction"])

    def test_predict_water_potability(self):
        payload = {
            "ph": 7.2,
            "Hardness": 190.0,
            "Solids": 19000.0,
            "Chloramines": 6.8,
            "Sulfate": 310.0,
            "Conductivity": 410.0,
            "Organic_carbon": 13.0,
            "Trihalomethanes": 62.0,
            "Turbidity": 3.6
        }
        response = self.client.post("/api/predict/water-potability", json=payload)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIn("prediction", json_data)
        self.assertIn("predicted_class", json_data["prediction"])
        self.assertIn("potability_status", json_data["prediction"])

    def test_metrics(self):
        response = self.client.get("/api/metrics")
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIn("air", json_data)
        self.assertIn("water", json_data)
        self.assertGreater(json_data["air"]["r2_score"], 0.5)
        self.assertGreater(json_data["water"]["accuracy"], 0.5)

    def test_anomaly_detection(self):
        response = self.client.get("/api/analytics/anomaly-detection")
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIn("scatter_data", json_data)

    def test_domain_verification(self):
        response = self.client.get("/api/system/domain-verification?domain=localhost")
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIn("domain", json_data)
        self.assertIn("dns_resolved", json_data)
        self.assertIn("nginx_snippet", json_data)

    def test_system_transparency(self):
        response = self.client.get("/api/system/transparency")
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data["system_name"], "EcoTrack")
        self.assertIn("data_sources", json_data)
        self.assertIn("limitations", json_data)
        self.assertIn("ist_timestamp", json_data)

    def test_realtime_india_feeds(self):
        response = self.client.get("/api/realtime/india-air?location=delhi_ncr")
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIn("location", json_data)
        self.assertIn("prediction", json_data)
        self.assertIn("timestamps", json_data)

        w_res = self.client.get("/api/realtime/india-water?location=delhi_ncr")
        self.assertEqual(w_res.status_code, 200)
        w_json = w_res.json()
        self.assertIn("station_name", w_json)
        self.assertIn("timestamps", w_json)

if __name__ == '__main__':
    unittest.main()
