import React, { useState, useEffect } from 'react';
import { RefreshCw, Server, ShieldCheck, Clock, Lock } from 'lucide-react';

export default function Header({ activeTab, onRefresh }) {
  const [timeString, setTimeString] = useState('');

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      // Indian Standard Time formatting
      const istString = now.toLocaleTimeString('en-IN', {
        timeZone: 'Asia/Kolkata',
        hour12: true,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      });
      setTimeString(`${istString} IST`);
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  const titles = {
    'india-live': 'India Real-Time Environmental Surveillance',
    'dashboard': 'Executive Environmental Health Dashboard',
    'air-quality': 'Air Quality Index (AQI) Prediction Engine',
    'water-quality': 'Water Potability Assessment Classifier',
    'predictions': 'Batch Sensor Array Inferences',
    'impact': 'Environmental Impact and Feature Sensitivity',
    'anomaly': 'Isolation Forest Outlier Detection',
    'alerts': 'Real-Time Alert and Threshold Breach Log',
    'recommendations': 'Actionable Mitigation and Regulatory Directives',
    'history': 'Historical Telemetry and Export Console',
    'about': 'Model Performance Metrics and Data Provenance',
    'domain-verification': 'Custom Domain and HTTPS Verification',
    'privacy-policy': 'EcoTrack Privacy Policy',
    'terms': 'Terms and Conditions'
  };

  const descriptions = {
    'india-live': 'Continuous Open-Meteo atmospheric telemetry and CPCB water quality parameters across Indian stations',
    'dashboard': 'Synthesized Environmental Health Index (EHI), national averages, and active threat matrices',
    'air-quality': 'Regression modeling for particulate concentrations (PM2.5, PM10) and gaseous pollutants',
    'water-quality': 'Supervised classification for drinking water safety against WHO threshold metrics',
    'predictions': 'Multi-sample simulation and evaluation across synthetic and industrial scenarios',
    'impact': 'Empirical feature importance and environmental hazard weighting',
    'anomaly': 'Unsupervised machine learning for identifying sensor drift and abnormal emissions',
    'alerts': 'Automated notifications for WHO and CPCB standard violations',
    'recommendations': 'Targeted municipal, industrial, and public safety advisory directives',
    'history': 'Auditable SQLite prediction repository with CSV export and purge controls',
    'about': 'Live train-test evaluation scores (R2, MAE, RMSE, Accuracy, F1, ROC-AUC) and citations',
    'domain-verification': 'Live DNS A-record verification, SSL certificate handshake, and Nginx production deployment',
    'privacy-policy': 'Data collection disclosure, telemetry handling, and client privacy guarantees',
    'terms': 'Operational framework, machine learning limitation notices, and legal disclaimers'
  };

  return (
    <header className="h-16 border-b border-slate-200 bg-white px-6 flex items-center justify-between sticky top-0 z-10">
      <div>
        <h2 className="text-base font-bold text-slate-900 tracking-tight">
          {titles[activeTab] || 'EcoTrack Environmental Surveillance'}
        </h2>
        <p className="text-xs text-slate-500 font-normal">
          {descriptions[activeTab] || 'Scientific Environmental Health Surveillance System'}
        </p>
      </div>

      <div className="flex items-center gap-3">
        {/* Live IST Clock */}
        <div className="hidden lg:flex items-center gap-1.5 px-2.5 py-1.5 rounded-md bg-slate-50 border border-slate-200 text-xs text-slate-700 font-mono">
          <Clock className="w-3.5 h-3.5 text-emerald-800" />
          <span>{timeString || 'Loading IST...'}</span>
        </div>

        {/* Backend Connectivity Status */}
        <div className="hidden sm:flex items-center gap-2 px-2.5 py-1.5 rounded-md bg-slate-50 border border-slate-200 text-xs text-slate-700">
          <Server className="w-3.5 h-3.5 text-emerald-700" />
          <span>Backend: <strong className="text-emerald-800 font-semibold font-mono">{import.meta.env.VITE_API_URL ? 'Render service' : 'Local proxy'}</strong></span>
        </div>

        {/* HTTPS / Protection Status */}
        <div className="flex items-center gap-1.5 text-xs text-emerald-800 bg-emerald-50 px-2.5 py-1.5 rounded-md border border-emerald-200 font-medium">
          <Lock className="w-3.5 h-3.5 text-emerald-700" />
          <span>HTTPS / ML Active</span>
        </div>

        {/* Refresh Button */}
        <button
          onClick={onRefresh}
          className="p-2 rounded-md bg-white border border-slate-300 text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition shadow-xs"
          title="Refresh Current View Telemetry"
        >
          <RefreshCw className="w-4 h-4" />
        </button>
      </div>
    </header>
  );
}
