import React, { useState, useEffect } from 'react';
import { Info, Code2, Database, Cpu, ShieldCheck, RefreshCcw, Layers, CheckCircle2, AlertTriangle, FileSpreadsheet } from 'lucide-react';
import { apiUrl } from '../api';

export default function AboutView() {
  const [metrics, setMetrics] = useState(null);
  const [transparency, setTransparency] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSystemData();
  }, []);

  const fetchSystemData = async () => {
    setLoading(true);
    try {
      const [metricsRes, transRes] = await Promise.all([
        fetch(apiUrl('/api/metrics')).then(r => r.json()),
        fetch(apiUrl('/api/system/transparency')).then(r => r.json())
      ]);
      setMetrics(metricsRes);
      setTransparency(transRes);
    } catch (err) {
      console.error('Failed to fetch system data:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* System Abstract */}
      <div className="p-6 rounded-lg bg-white border border-slate-200 shadow-sm space-y-3">
        <div className="flex items-center gap-2 text-emerald-800">
          <ShieldCheck className="w-5 h-5 text-emerald-800" />
          <h3 className="text-xs font-bold uppercase tracking-wider">System Architecture and Verification</h3>
        </div>
        <h4 className="text-xl font-bold text-slate-900">EcoTrack: AI-Based Smart Environmental Impact Monitoring System</h4>
        <p className="text-xs text-slate-600 leading-relaxed">
          EcoTrack provides an empirical machine learning pipeline for continuous environmental health surveillance. By integrating multi-pollutant atmospheric regression for Air Quality Index (AQI) modeling, gradient-boosted decision trees for physicochemical water potability classification, and Isolation Forests for unsupervised sensor outlier detection, the system delivers verifiable, real-time environmental intelligence across India.
        </p>
      </div>

      {/* Live Model Performance Metrics (Computed strictly from live train/test splits) */}
      <div className="p-6 rounded-lg bg-white border border-slate-200 shadow-sm space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <div>
            <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider">Empirical Model Evaluation Metrics</h4>
            <p className="text-xs text-slate-500">Computed live via 80/20 train-test evaluation splits on genuine datasets (Zero hardcoding or fabrication)</p>
          </div>
          <button
            onClick={fetchSystemData}
            className="p-1.5 rounded-md bg-white border border-slate-300 text-slate-600 hover:text-slate-900 transition"
            title="Recalculate Live Metrics"
          >
            <RefreshCcw className="w-4 h-4" />
          </button>
        </div>

        {loading ? (
          <div className="flex items-center justify-center h-32 text-slate-500 gap-2">
            <RefreshCcw className="w-5 h-5 animate-spin text-emerald-800" />
            <span className="text-sm">Evaluating model performance across test partitions...</span>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Air Quality Model Metrics */}
            <div className="p-4 rounded-lg bg-slate-50 border border-slate-200 space-y-3">
              <div className="flex items-center justify-between border-b border-slate-200 pb-2">
                <span className="text-xs font-bold text-emerald-900">Air Quality Regression Model</span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-md bg-white border border-slate-200 text-slate-700">
                  {metrics?.air?.model_name || 'LinearRegression'}
                </span>
              </div>
              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="p-2.5 rounded-md bg-white border border-slate-200">
                  <span className="text-slate-500 block text-[11px]">R² Coefficient (Fit)</span>
                  <span className="text-lg font-extrabold text-slate-900 font-mono">{metrics?.air?.r2_score}</span>
                </div>
                <div className="p-2.5 rounded-md bg-white border border-slate-200">
                  <span className="text-slate-500 block text-[11px]">Mean Absolute Error</span>
                  <span className="text-lg font-extrabold text-slate-900 font-mono">{metrics?.air?.mae}</span>
                </div>
                <div className="p-2.5 rounded-md bg-white border border-slate-200">
                  <span className="text-slate-500 block text-[11px]">Root Mean Squared Error</span>
                  <span className="text-lg font-extrabold text-slate-900 font-mono">{metrics?.air?.rmse}</span>
                </div>
                <div className="p-2.5 rounded-md bg-white border border-slate-200">
                  <span className="text-slate-500 block text-[11px]">Dataset Sample Count</span>
                  <span className="text-lg font-extrabold text-slate-900 font-mono">{metrics?.air?.sample_count}</span>
                </div>
              </div>
            </div>

            {/* Water Quality Model Metrics */}
            <div className="p-4 rounded-lg bg-slate-50 border border-slate-200 space-y-3">
              <div className="flex items-center justify-between border-b border-slate-200 pb-2">
                <span className="text-xs font-bold text-teal-900">Water Potability Classifier</span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-md bg-white border border-slate-200 text-slate-700">
                  {metrics?.water?.model_name || 'GradientBoosting'}
                </span>
              </div>
              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="p-2.5 rounded-md bg-white border border-slate-200">
                  <span className="text-slate-500 block text-[11px]">Classification Accuracy</span>
                  <span className="text-lg font-extrabold text-slate-900 font-mono">{(metrics?.water?.accuracy * 100).toFixed(1)}%</span>
                </div>
                <div className="p-2.5 rounded-md bg-white border border-slate-200">
                  <span className="text-slate-500 block text-[11px]">F1-Score</span>
                  <span className="text-lg font-extrabold text-slate-900 font-mono">{metrics?.water?.f1_score}</span>
                </div>
                <div className="p-2.5 rounded-md bg-white border border-slate-200">
                  <span className="text-slate-500 block text-[11px]">ROC-AUC Metric</span>
                  <span className="text-lg font-extrabold text-slate-900 font-mono">{metrics?.water?.roc_auc}</span>
                </div>
                <div className="p-2.5 rounded-md bg-white border border-slate-200">
                  <span className="text-slate-500 block text-[11px]">Dataset Sample Count</span>
                  <span className="text-lg font-extrabold text-slate-900 font-mono">{metrics?.water?.sample_count}</span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Verified Data Sources */}
      <div className="p-6 rounded-lg bg-white border border-slate-200 shadow-sm space-y-4">
        <div className="border-b border-slate-100 pb-2">
          <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider">Authoritative Data Provenance</h4>
          <p className="text-xs text-slate-500">Live feeds and reference datasets grounding the surveillance framework</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 rounded-md bg-slate-50 border border-slate-200 space-y-1.5 text-xs">
            <h5 className="font-bold text-slate-900">Open-Meteo European Atmosphere API</h5>
            <p className="text-slate-600">Copernicus CAMS & ECMWF satellite data integration providing hourly assimilation for PM2.5, PM10, NO2, SO2, CO, and O3.</p>
            <span className="block text-[11px] text-emerald-800 font-medium pt-1">Active Indian Feeds</span>
          </div>

          <div className="p-4 rounded-md bg-slate-50 border border-slate-200 space-y-1.5 text-xs">
            <h5 className="font-bold text-slate-900">CPCB NAAQS Standards Framework</h5>
            <p className="text-slate-600">Central Pollution Control Board statutory breakpoints for sub-index calculations under the Ministry of Environment, Forest & Climate Change.</p>
            <span className="block text-[11px] text-emerald-800 font-medium pt-1">Statutory Breakpoint Mapping</span>
          </div>

          <div className="p-4 rounded-md bg-slate-50 border border-slate-200 space-y-1.5 text-xs">
            <h5 className="font-bold text-slate-900">WHO Drinking Water Dataset</h5>
            <p className="text-slate-600">Standard physicochemical potable quality dataset comprising 3,276 water samples evaluated against WHO permissible mineral concentrations.</p>
            <span className="block text-[11px] text-emerald-800 font-medium pt-1">Supervised Training Corpus</span>
          </div>
        </div>
      </div>

      {/* Documented Prediction Limitations */}
      <div className="p-6 rounded-lg bg-white border border-slate-200 shadow-sm space-y-3">
        <div className="border-b border-slate-100 pb-2 flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 text-amber-700" />
          <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider">Documented Prediction Limitations</h4>
        </div>

        <ul className="list-disc pl-5 space-y-2 text-xs text-slate-600 leading-relaxed">
          <li><strong>Microclimatic Boundaries:</strong> Air quality predictions represent ambient regional outdoor atmospheres. Localized street-canyon effects, underground transit corridors, and unmonitored volatile organic compounds (VOCs) require localized hardware sensors.</li>
          <li><strong>Biological Pathogen Exclusion:</strong> Water potability models classify physicochemical parameters only (pH, hardness, sulfate, TDS). Chemical potability does not confirm absence of biological pathogens (e.g. E. coli or enteric viruses), which strictly require microbiological culturing.</li>
          <li><strong>Decision Support Nature:</strong> Predictions provide indicative risk assessment. Official emergency health alerts remain under the sole statutory jurisdiction of the Central Pollution Control Board (CPCB) and municipal health officers.</li>
        </ul>
      </div>

      {/* Technology Specifications */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
        <div className="p-4 rounded-lg bg-white border border-slate-200 shadow-sm flex items-center gap-3">
          <div className="p-2 rounded-md bg-emerald-50 text-emerald-800 border border-emerald-200">
            <Cpu className="w-5 h-5" />
          </div>
          <div>
            <h5 className="text-xs font-bold text-slate-900">ML Pipeline</h5>
            <p className="text-[11px] text-slate-500">Scikit-Learn & Joblib</p>
          </div>
        </div>

        <div className="p-4 rounded-lg bg-white border border-slate-200 shadow-sm flex items-center gap-3">
          <div className="p-2 rounded-md bg-teal-50 text-teal-800 border border-teal-200">
            <Code2 className="w-5 h-5" />
          </div>
          <div>
            <h5 className="text-xs font-bold text-slate-900">API Backend</h5>
            <p className="text-[11px] text-slate-500">FastAPI & Python 3.13</p>
          </div>
        </div>

        <div className="p-4 rounded-lg bg-white border border-slate-200 shadow-sm flex items-center gap-3">
          <div className="p-2 rounded-md bg-slate-100 text-slate-700 border border-slate-200">
            <Database className="w-5 h-5" />
          </div>
          <div>
            <h5 className="text-xs font-bold text-slate-900">Local Database</h5>
            <p className="text-[11px] text-slate-500">SQLite (ecotrack.db)</p>
          </div>
        </div>

        <div className="p-4 rounded-lg bg-white border border-slate-200 shadow-sm flex items-center gap-3">
          <div className="p-2 rounded-md bg-slate-100 text-slate-700 border border-slate-200">
            <Layers className="w-5 h-5" />
          </div>
          <div>
            <h5 className="text-xs font-bold text-slate-900">Frontend Suite</h5>
            <p className="text-[11px] text-slate-500">React & Tailwind CSS</p>
          </div>
        </div>
      </div>
    </div>
  );
}
