import React, { useState } from 'react';
import { Wind, Gauge, AlertOctagon, RefreshCcw, AlertTriangle, Info, CheckCircle2 } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { apiUrl } from '../api';

const PRESETS = [
  {
    name: 'Clean Ambient Air',
    data: { PM2_5: 14.5, PM10: 28.0, NO2: 12.0, SO2: 4.5, CO: 0.5, O3: 22.0, Temperature: 21.0, Humidity: 50.0, Wind_Speed: 14.0, Proximity_Industrial: 18.0 }
  },
  {
    name: 'Industrial Corridor',
    data: { PM2_5: 88.5, PM10: 165.0, NO2: 65.0, SO2: 38.0, CO: 3.2, O3: 75.0, Temperature: 32.0, Humidity: 35.0, Wind_Speed: 4.5, Proximity_Industrial: 1.2 }
  },
  {
    name: 'Smog Inversion Event',
    data: { PM2_5: 285.0, PM10: 410.0, NO2: 110.0, SO2: 55.0, CO: 6.8, O3: 105.0, Temperature: 38.0, Humidity: 18.0, Wind_Speed: 2.0, Proximity_Industrial: 8.0 }
  }
];

export default function AirQualityView() {
  const [formData, setFormData] = useState(PRESETS[0].data);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (field, val) => {
    setFormData(prev => ({ ...prev, [field]: parseFloat(val) || 0 }));
  };

  const applyPreset = (preset) => {
    setFormData(preset.data);
    setResult(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const payload = {
      "PM2.5": formData.PM2_5,
      "PM10": formData.PM10,
      "NO2": formData.NO2,
      "SO2": formData.SO2,
      "CO": formData.CO,
      "O3": formData.O3,
      "Temperature": formData.Temperature,
      "Humidity": formData.Humidity,
      "Wind_Speed": formData.Wind_Speed,
      "Proximity_Industrial": formData.Proximity_Industrial
    };

    try {
      const response = await fetch(apiUrl('/api/predict/air-quality'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!response.ok) {
        throw new Error('API server returned prediction error');
      }
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'Failed to calculate AQI prediction.');
    } finally {
      setLoading(false);
    }
  };

  const chartData = [
    { name: 'PM2.5', value: formData.PM2_5, norm: 35 },
    { name: 'PM10', value: formData.PM10, norm: 150 },
    { name: 'NO2', value: formData.NO2, norm: 100 },
    { name: 'SO2', value: formData.SO2, norm: 75 },
    { name: 'CO (x10)', value: formData.CO * 10, norm: 90 },
    { name: 'O3', value: formData.O3, norm: 70 },
  ];

  return (
    <div className="space-y-6">
      {/* Header and Preset Scenarios */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-5 rounded-lg bg-white border border-slate-200 shadow-sm">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Wind className="w-5 h-5 text-emerald-800" /> Air Quality Prediction Engine
          </h3>
          <p className="text-xs text-slate-500">Multivariate regression pipeline trained on ambient particulate and meteorological parameters</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold text-slate-500">Benchmark Presets:</span>
          {PRESETS.map((preset, idx) => (
            <button
              key={idx}
              onClick={() => applyPreset(preset)}
              className="text-xs font-medium px-3 py-1.5 rounded-md bg-slate-50 border border-slate-200 hover:bg-emerald-50 hover:border-emerald-300 text-slate-700 transition"
            >
              {preset.name}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Input Form Column */}
        <form onSubmit={handleSubmit} className="lg:col-span-6 p-6 rounded-lg bg-white border border-slate-200 shadow-sm space-y-4">
          <div className="border-b border-slate-100 pb-2 flex items-center justify-between">
            <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider">
              Atmospheric and Meteorological Parameters
            </h4>
            <span className="text-[10px] text-slate-400 font-mono">10 Feature Vector</span>
          </div>

          <div className="grid grid-cols-2 gap-3.5">
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">PM2.5 (µg/m³)</label>
              <input
                type="number"
                step="0.1"
                value={formData.PM2_5}
                onChange={(e) => handleInputChange('PM2_5', e.target.value)}
                className="w-full px-3 py-1.5 rounded-md bg-white border border-slate-300 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-700"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">PM10 (µg/m³)</label>
              <input
                type="number"
                step="0.1"
                value={formData.PM10}
                onChange={(e) => handleInputChange('PM10', e.target.value)}
                className="w-full px-3 py-1.5 rounded-md bg-white border border-slate-300 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-700"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">NO2 (ppb)</label>
              <input
                type="number"
                step="0.1"
                value={formData.NO2}
                onChange={(e) => handleInputChange('NO2', e.target.value)}
                className="w-full px-3 py-1.5 rounded-md bg-white border border-slate-300 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-700"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">SO2 (ppb)</label>
              <input
                type="number"
                step="0.1"
                value={formData.SO2}
                onChange={(e) => handleInputChange('SO2', e.target.value)}
                className="w-full px-3 py-1.5 rounded-md bg-white border border-slate-300 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-700"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">CO (ppm)</label>
              <input
                type="number"
                step="0.1"
                value={formData.CO}
                onChange={(e) => handleInputChange('CO', e.target.value)}
                className="w-full px-3 py-1.5 rounded-md bg-white border border-slate-300 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-700"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">O3 (ppb)</label>
              <input
                type="number"
                step="0.1"
                value={formData.O3}
                onChange={(e) => handleInputChange('O3', e.target.value)}
                className="w-full px-3 py-1.5 rounded-md bg-white border border-slate-300 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-700"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">Temperature (°C)</label>
              <input
                type="number"
                step="0.1"
                value={formData.Temperature}
                onChange={(e) => handleInputChange('Temperature', e.target.value)}
                className="w-full px-3 py-1.5 rounded-md bg-white border border-slate-300 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-700"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">Relative Humidity (%)</label>
              <input
                type="number"
                step="0.1"
                value={formData.Humidity}
                onChange={(e) => handleInputChange('Humidity', e.target.value)}
                className="w-full px-3 py-1.5 rounded-md bg-white border border-slate-300 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-700"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">Wind Speed (km/h)</label>
              <input
                type="number"
                step="0.1"
                value={formData.Wind_Speed}
                onChange={(e) => handleInputChange('Wind_Speed', e.target.value)}
                className="w-full px-3 py-1.5 rounded-md bg-white border border-slate-300 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-700"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">Proximity Industrial (km)</label>
              <input
                type="number"
                step="0.1"
                value={formData.Proximity_Industrial}
                onChange={(e) => handleInputChange('Proximity_Industrial', e.target.value)}
                className="w-full px-3 py-1.5 rounded-md bg-white border border-slate-300 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-700"
                required
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 rounded-md bg-[#1b4332] hover:bg-[#143225] font-semibold text-white shadow-xs transition flex items-center justify-center gap-2 text-xs"
          >
            {loading ? <RefreshCcw className="w-4 h-4 animate-spin" /> : <Gauge className="w-4 h-4" />}
            <span>{loading ? 'Evaluating Model Inferences...' : 'Compute AQI and Health Impact'}</span>
          </button>
        </form>

        {/* Results and Visualizations Column */}
        <div className="lg:col-span-6 space-y-6">
          {error && (
            <div className="p-4 rounded-md bg-red-50 border border-red-300 text-red-800 text-xs flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {result ? (
            <div className="p-6 rounded-lg bg-white border border-slate-200 shadow-sm space-y-5">
              {/* Main AQI Score Header */}
              <div className="flex items-center justify-between pb-4 border-b border-slate-100">
                <div>
                  <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Predicted Index</span>
                  <div className="flex items-baseline gap-3 mt-1">
                    <span className="text-4xl font-extrabold text-slate-900">{result.prediction.predicted_aqi}</span>
                    <span className="px-2.5 py-0.5 rounded-md text-xs font-bold bg-yellow-50 text-yellow-900 border border-yellow-300">
                      {result.prediction.aqi_category}
                    </span>
                  </div>
                </div>

                {result.prediction.is_anomaly && (
                  <div className="px-2.5 py-1 rounded-md bg-amber-50 border border-amber-300 text-amber-800 text-xs font-semibold flex items-center gap-1.5">
                    <AlertOctagon className="w-4 h-4" /> Anomaly Detected
                  </div>
                )}
              </div>

              {/* Health Advisory */}
              <div className="p-3.5 rounded-md bg-slate-50 border border-slate-200">
                <h5 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-1">Health Advisory</h5>
                <p className="text-xs text-slate-600 leading-relaxed">{result.prediction.health_description}</p>
              </div>

              {/* Pollutant Bar Visualization */}
              <div>
                <h5 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">Parameter Distribution vs NAAQS Thresholds</h5>
                <div className="h-44">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                      <XAxis dataKey="name" stroke="#64748b" fontSize={11} />
                      <YAxis stroke="#64748b" fontSize={11} />
                      <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderColor: '#cbd5e1', borderRadius: '0.375rem', fontSize: '12px' }} />
                      <Bar dataKey="value" fill="#0f766e" radius={[2, 2, 0, 0]} name="Evaluated Level" />
                      <Bar dataKey="norm" fill="#94a3b8" radius={[2, 2, 0, 0]} name="Benchmark Limit" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          ) : (
            <div className="p-8 rounded-lg bg-white border border-slate-200 shadow-sm text-center space-y-3">
              <div className="w-10 h-10 rounded-md bg-emerald-50 text-emerald-800 mx-auto flex items-center justify-center border border-emerald-200">
                <Wind className="w-5 h-5" />
              </div>
              <h4 className="text-sm font-bold text-slate-900">Model Ready for Atmospheric Inferences</h4>
              <p className="text-xs text-slate-500 max-w-sm mx-auto">
                Modify parameters or select a benchmark scenario above to compute air quality index and anomaly degree.
              </p>
            </div>
          )}

          {/* Model Scope and Limitations */}
          <div className="p-4 rounded-lg bg-white border border-slate-200 text-xs text-slate-600 flex items-start gap-2.5">
            <Info className="w-4 h-4 text-emerald-800 shrink-0 mt-0.5" />
            <div>
              <strong className="text-slate-800">Prediction Limitations:</strong> Regression output calculates ambient regional outdoor AQI. Hyper-localized indoor spaces, underground metro passages, and unmonitored industrial VOCs require site-specific physical monitors.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
