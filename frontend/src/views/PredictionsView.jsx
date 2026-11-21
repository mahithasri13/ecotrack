import React, { useState } from 'react';
import { apiUrl } from '../api';
import { Binary, Play, CheckCircle2, AlertOctagon, RefreshCcw, Info } from 'lucide-react';

const BATCH_AIR_SAMPLES = [
  { name: 'Urban Commercial Center', PM2_5: 22.4, PM10: 45.0, NO2: 24.5, SO2: 6.2, CO: 0.9, O3: 32.0, Temperature: 23.0, Humidity: 52.0, Wind_Speed: 11.0, Proximity_Industrial: 12.0 },
  { name: 'Industrial Smelting Zone', PM2_5: 115.0, PM10: 195.0, NO2: 78.0, SO2: 42.0, CO: 4.1, O3: 88.0, Temperature: 33.0, Humidity: 28.0, Wind_Speed: 3.5, Proximity_Industrial: 0.8 },
  { name: 'Highland Ecological Reserve', PM2_5: 6.2, PM10: 12.0, NO2: 4.1, SO2: 1.5, CO: 0.2, O3: 15.0, Temperature: 18.0, Humidity: 65.0, Wind_Speed: 18.0, Proximity_Industrial: 45.0 }
];

const BATCH_WATER_SAMPLES = [
  { name: 'Municipal Storage Reservoir A', ph: 7.3, Hardness: 185.0, Solids: 16500.0, Chloramines: 6.4, Sulfate: 305.0, Conductivity: 400.0, Organic_carbon: 11.5, Trihalomethanes: 55.0, Turbidity: 3.4 },
  { name: 'Industrial Runoff Canal B', ph: 5.2, Hardness: 310.0, Solids: 42000.0, Chloramines: 12.0, Sulfate: 440.0, Conductivity: 680.0, Organic_carbon: 28.0, Trihalomethanes: 125.0, Turbidity: 8.2 },
  { name: 'Rural Community Deep Borewell C', ph: 7.8, Hardness: 240.0, Solids: 22000.0, Chloramines: 7.8, Sulfate: 350.0, Conductivity: 460.0, Organic_carbon: 15.0, Trihalomethanes: 72.0, Turbidity: 4.1 }
];

export default function PredictionsView() {
  const [airResults, setAirResults] = useState([]);
  const [waterResults, setWaterResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const runBatchPredictions = async () => {
    setLoading(true);
    try {
      const airProms = BATCH_AIR_SAMPLES.map(sample =>
        fetch(apiUrl('/api/predict/air-quality'), {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            "PM2.5": sample.PM2_5, "PM10": sample.PM10, "NO2": sample.NO2, "SO2": sample.SO2, "CO": sample.CO,
            "O3": sample.O3, "Temperature": sample.Temperature, "Humidity": sample.Humidity,
            "Wind_Speed": sample.Wind_Speed, "Proximity_Industrial": sample.Proximity_Industrial
          })
        }).then(res => res.json())
      );

      const waterProms = BATCH_WATER_SAMPLES.map(sample =>
        fetch(apiUrl('/api/predict/water-potability'), {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(sample)
        }).then(res => res.json())
      );

      const aRes = await Promise.all(airProms);
      const wRes = await Promise.all(waterProms);

      setAirResults(aRes.map((r, i) => ({ ...r, sampleName: BATCH_AIR_SAMPLES[i].name })));
      setWaterResults(wRes.map((r, i) => ({ ...r, sampleName: BATCH_WATER_SAMPLES[i].name })));
    } catch (err) {
      console.error('Batch error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-5 rounded-lg bg-white border border-slate-200 shadow-sm">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Binary className="w-5 h-5 text-emerald-800" /> Multi-Sample Batch Inference Suite
          </h3>
          <p className="text-xs text-slate-500">Run parallel model evaluations across diverse geographical and industrial station profiles</p>
        </div>
        <button
          onClick={runBatchPredictions}
          disabled={loading}
          className="px-4 py-2 rounded-md bg-[#1b4332] hover:bg-[#143225] text-white font-semibold text-xs transition flex items-center gap-2 shadow-xs"
        >
          {loading ? <RefreshCcw className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4 fill-white" />}
          <span>{loading ? 'Evaluating Array...' : 'Run Parallel Inferences'}</span>
        </button>
      </div>

      {/* Grid of Results */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Air Quality Batch Results */}
        <div className="p-5 rounded-lg bg-white border border-slate-200 shadow-sm space-y-3">
          <div className="border-b border-slate-100 pb-2 flex items-center justify-between">
            <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider">
              Air Quality Test Matrix
            </h4>
            <span className="text-[10px] text-slate-400 font-mono">3 Sample Cohorts</span>
          </div>
          {airResults.length > 0 ? (
            <div className="space-y-2.5">
              {airResults.map((item, idx) => (
                <div key={idx} className="p-3 rounded-md bg-slate-50 border border-slate-200 flex items-center justify-between text-xs">
                  <div>
                    <h5 className="font-bold text-slate-900">{item.sampleName}</h5>
                    <p className="text-[11px] text-slate-500 mt-0.5">Predicted AQI: <strong className="text-emerald-800 font-mono">{item.prediction.predicted_aqi}</strong></p>
                  </div>
                  <span className="px-2 py-0.5 rounded-md font-bold text-[11px] bg-yellow-50 text-yellow-900 border border-yellow-300">
                    {item.prediction.aqi_category}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <div className="py-8 text-center text-xs text-slate-500">
              Select 'Run Parallel Inferences' to evaluate air quality test vectors.
            </div>
          )}
        </div>

        {/* Water Quality Batch Results */}
        <div className="p-5 rounded-lg bg-white border border-slate-200 shadow-sm space-y-3">
          <div className="border-b border-slate-100 pb-2 flex items-center justify-between">
            <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider">
              Water Potability Test Matrix
            </h4>
            <span className="text-[10px] text-slate-400 font-mono">3 Station Cohorts</span>
          </div>
          {waterResults.length > 0 ? (
            <div className="space-y-2.5">
              {waterResults.map((item, idx) => (
                <div key={idx} className="p-3 rounded-md bg-slate-50 border border-slate-200 flex items-center justify-between text-xs">
                  <div>
                    <h5 className="font-bold text-slate-900">{item.sampleName}</h5>
                    <p className="text-[11px] text-slate-500 mt-0.5">Potability Probability: <strong className="text-teal-800 font-mono">{(item.prediction.probability_potable * 100).toFixed(1)}%</strong></p>
                  </div>
                  <span className={`px-2 py-0.5 rounded-md font-bold text-[11px] ${
                    item.prediction.predicted_class === 1
                      ? 'bg-emerald-50 text-emerald-900 border border-emerald-300'
                      : 'bg-red-50 text-red-900 border border-red-300'
                  }`}>
                    {item.prediction.potability_status}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <div className="py-8 text-center text-xs text-slate-500">
              Select 'Run Parallel Inferences' to evaluate water physicochemical cohorts.
            </div>
          )}
        </div>
      </div>

      {/* Information Disclosure */}
      <div className="p-4 rounded-lg bg-white border border-slate-200 text-xs text-slate-600 flex items-start gap-2.5">
        <Info className="w-4 h-4 text-emerald-800 shrink-0 mt-0.5" />
        <div>
          <strong className="text-slate-800">Batch Evaluation Note:</strong> Each inference pipeline transforms features using fitted StandardScaler and SimpleImputer artifacts before computing model predictions and Isolation Forest anomaly scores.
        </div>
      </div>
    </div>
  );
}
