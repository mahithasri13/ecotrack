import React, { useState } from 'react';
import { Droplets, ShieldCheck, ShieldAlert, RefreshCcw, AlertTriangle, Info, CheckCircle2 } from 'lucide-react';
import { apiUrl } from '../api';

const WATER_PRESETS = [
  {
    name: 'Treated Municipal Supply',
    data: { ph: 7.4, Hardness: 175.0, Solids: 14000.0, Chloramines: 6.2, Sulfate: 290.0, Conductivity: 380.0, Organic_carbon: 10.5, Trihalomethanes: 52.0, Turbidity: 3.2 }
  },
  {
    name: 'Urban Groundwater Borewell',
    data: { ph: 7.1, Hardness: 210.0, Solids: 21000.0, Chloramines: 7.5, Sulfate: 330.0, Conductivity: 430.0, Organic_carbon: 14.2, Trihalomethanes: 68.0, Turbidity: 3.9 }
  },
  {
    name: 'Untreated Effluent Discharge',
    data: { ph: 4.8, Hardness: 340.0, Solids: 48000.0, Chloramines: 13.5, Sulfate: 460.0, Conductivity: 720.0, Organic_carbon: 32.0, Trihalomethanes: 140.0, Turbidity: 8.8 }
  }
];

export default function WaterQualityView() {
  const [formData, setFormData] = useState(WATER_PRESETS[0].data);
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

    try {
      const response = await fetch(apiUrl('/api/predict/water-potability'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      if (!response.ok) {
        throw new Error('API server returned classification error');
      }
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'Failed to calculate water potability.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header and Scenario Presets */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-5 rounded-lg bg-white border border-slate-200 shadow-sm">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Droplets className="w-5 h-5 text-teal-800" /> Water Potability Classification Engine
          </h3>
          <p className="text-xs text-slate-500">Supervised machine learning model classifying drinking safety against WHO statutory standards</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold text-slate-500">Benchmark Presets:</span>
          {WATER_PRESETS.map((preset, idx) => (
            <button
              key={idx}
              onClick={() => applyPreset(preset)}
              className="text-xs font-medium px-3 py-1.5 rounded-md bg-slate-50 border border-slate-200 hover:bg-teal-50 hover:border-teal-300 text-slate-700 transition"
            >
              {preset.name}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Form Column */}
        <form onSubmit={handleSubmit} className="lg:col-span-6 p-6 rounded-lg bg-white border border-slate-200 shadow-sm space-y-4">
          <div className="border-b border-slate-100 pb-2 flex items-center justify-between">
            <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider">
              Physicochemical Water Parameters
            </h4>
            <span className="text-[10px] text-slate-400 font-mono">9 Parameter Matrix</span>
          </div>

          <div className="grid grid-cols-2 gap-3.5">
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">pH Factor (6.5 - 8.5 WHO)</label>
              <input
                type="number"
                step="0.01"
                value={formData.ph}
                onChange={(e) => handleInputChange('ph', e.target.value)}
                className="w-full px-3 py-1.5 rounded-md bg-white border border-slate-300 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-700"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">Hardness (mg/L CaCO3)</label>
              <input
                type="number"
                step="0.1"
                value={formData.Hardness}
                onChange={(e) => handleInputChange('Hardness', e.target.value)}
                className="w-full px-3 py-1.5 rounded-md bg-white border border-slate-300 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-700"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">Solids / TDS (ppm)</label>
              <input
                type="number"
                step="1"
                value={formData.Solids}
                onChange={(e) => handleInputChange('Solids', e.target.value)}
                className="w-full px-3 py-1.5 rounded-md bg-white border border-slate-300 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-700"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">Chloramines (ppm)</label>
              <input
                type="number"
                step="0.1"
                value={formData.Chloramines}
                onChange={(e) => handleInputChange('Chloramines', e.target.value)}
                className="w-full px-3 py-1.5 rounded-md bg-white border border-slate-300 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-700"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">Sulfate (mg/L)</label>
              <input
                type="number"
                step="0.1"
                value={formData.Sulfate}
                onChange={(e) => handleInputChange('Sulfate', e.target.value)}
                className="w-full px-3 py-1.5 rounded-md bg-white border border-slate-300 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-700"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">Conductivity (μS/cm)</label>
              <input
                type="number"
                step="0.1"
                value={formData.Conductivity}
                onChange={(e) => handleInputChange('Conductivity', e.target.value)}
                className="w-full px-3 py-1.5 rounded-md bg-white border border-slate-300 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-700"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">Organic Carbon (ppm)</label>
              <input
                type="number"
                step="0.1"
                value={formData.Organic_carbon}
                onChange={(e) => handleInputChange('Organic_carbon', e.target.value)}
                className="w-full px-3 py-1.5 rounded-md bg-white border border-slate-300 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-700"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">Trihalomethanes (μg/L)</label>
              <input
                type="number"
                step="0.1"
                value={formData.Trihalomethanes}
                onChange={(e) => handleInputChange('Trihalomethanes', e.target.value)}
                className="w-full px-3 py-1.5 rounded-md bg-white border border-slate-300 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-700"
                required
              />
            </div>
            <div className="col-span-2">
              <label className="block text-xs font-medium text-slate-600 mb-1">Turbidity (NTU)</label>
              <input
                type="number"
                step="0.1"
                value={formData.Turbidity}
                onChange={(e) => handleInputChange('Turbidity', e.target.value)}
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
            {loading ? <RefreshCcw className="w-4 h-4 animate-spin" /> : <Droplets className="w-4 h-4" />}
            <span>{loading ? 'Executing Classifier...' : 'Assess Drinking Safety and Potability'}</span>
          </button>
        </form>

        {/* Results Column */}
        <div className="lg:col-span-6 space-y-6">
          {error && (
            <div className="p-4 rounded-md bg-red-50 border border-red-300 text-red-800 text-xs flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {result ? (
            <div className="p-6 rounded-lg bg-white border border-slate-200 shadow-sm space-y-5">
              <div className="flex items-center justify-between pb-4 border-b border-slate-100">
                <div>
                  <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Classification Result</span>
                  <div className="flex items-center gap-3 mt-1">
                    {result.prediction.predicted_class === 1 ? (
                      <span className="px-3 py-1 rounded-md text-xs font-bold bg-emerald-50 text-emerald-900 border border-emerald-300 flex items-center gap-1.5">
                        <ShieldCheck className="w-4 h-4 text-emerald-700" /> {result.prediction.potability_status}
                      </span>
                    ) : (
                      <span className="px-3 py-1 rounded-md text-xs font-bold bg-red-50 text-red-900 border border-red-300 flex items-center gap-1.5">
                        <ShieldAlert className="w-4 h-4 text-red-700" /> {result.prediction.potability_status}
                      </span>
                    )}
                  </div>
                </div>

                <div className="text-right">
                  <span className="text-xs text-slate-400 font-semibold block">Model Confidence</span>
                  <span className="text-2xl font-extrabold text-slate-900">{result.prediction.confidence_percentage}%</span>
                </div>
              </div>

              {/* WHO Compliance Grid */}
              <div>
                <h5 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2.5">WHO Guideline Compliance Verification</h5>
                <div className="space-y-2">
                  <div className="flex items-center justify-between p-2.5 rounded-md bg-slate-50 border border-slate-200 text-xs">
                    <span className="text-slate-600 font-medium">pH Safe Window (6.5 - 8.5)</span>
                    <span className={formData.ph >= 6.5 && formData.ph <= 8.5 ? "text-emerald-800 font-bold" : "text-red-700 font-bold"}>
                      {formData.ph} ({formData.ph >= 6.5 && formData.ph <= 8.5 ? "COMPLIANT" : "VIOLATION"})
                    </span>
                  </div>
                  <div className="flex items-center justify-between p-2.5 rounded-md bg-slate-50 border border-slate-200 text-xs">
                    <span className="text-slate-600 font-medium">Turbidity Benchmark (&lt; 5.0 NTU)</span>
                    <span className={formData.Turbidity <= 5.0 ? "text-emerald-800 font-bold" : "text-red-700 font-bold"}>
                      {formData.Turbidity} NTU ({formData.Turbidity <= 5.0 ? "COMPLIANT" : "VIOLATION"})
                    </span>
                  </div>
                  <div className="flex items-center justify-between p-2.5 rounded-md bg-slate-50 border border-slate-200 text-xs">
                    <span className="text-slate-600 font-medium">Sulfate Recommendation (&lt; 350 mg/L)</span>
                    <span className={formData.Sulfate <= 350 ? "text-emerald-800 font-bold" : "text-amber-800 font-bold"}>
                      {formData.Sulfate} mg/L ({formData.Sulfate <= 350 ? "COMPLIANT" : "ELEVATED"})
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="p-8 rounded-lg bg-white border border-slate-200 shadow-sm text-center space-y-3">
              <div className="w-10 h-10 rounded-md bg-teal-50 text-teal-800 mx-auto flex items-center justify-center border border-teal-200">
                <Droplets className="w-5 h-5" />
              </div>
              <h4 className="text-sm font-bold text-slate-900">Classifier Ready for Water Potability Inferences</h4>
              <p className="text-xs text-slate-500 max-w-sm mx-auto">
                Input the 9 chemical and physical attributes or pick a benchmark preset above to evaluate drinking suitability.
              </p>
            </div>
          )}

          {/* Explicit Microbiological Limitation Warning */}
          <div className="p-4 rounded-lg bg-white border border-slate-200 text-xs text-slate-600 flex items-start gap-2.5">
            <Info className="w-4 h-4 text-emerald-800 shrink-0 mt-0.5" />
            <div>
              <strong className="text-slate-800">Critical Scientific Limitation:</strong> This machine learning classification assesses physicochemical mineral properties only. Chemical potability does not guarantee freedom from microbiological pathogens (E. coli, coliform bacteria, or viral loads). Water disinfection and certified incubation testing remain mandatory for municipal supply certification.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
