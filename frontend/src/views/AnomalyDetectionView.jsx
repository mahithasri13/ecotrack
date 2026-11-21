import React, { useState, useEffect } from 'react';
import { Activity, AlertOctagon, CheckCircle2, RefreshCcw, Info } from 'lucide-react';
import { ResponsiveContainer, ScatterChart, Scatter, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { apiUrl } from '../api';

export default function AnomalyDetectionView() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnomalyData();
  }, []);

  const fetchAnomalyData = async () => {
    setLoading(true);
    try {
      const response = await fetch(apiUrl('/api/analytics/anomaly-detection'));
      const json = await response.json();
      setData(json);
    } catch (err) {
      console.error('Failed to fetch anomaly data:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-80 text-slate-500 gap-2">
        <RefreshCcw className="w-5 h-5 animate-spin text-emerald-800" />
        <span className="text-sm">Executing Isolation Forest unsupervised outlier analysis...</span>
      </div>
    );
  }

  const normalPoints = data?.scatter_data?.filter(p => !p.is_anomaly) || [];
  const anomalyPoints = data?.scatter_data?.filter(p => p.is_anomaly) || [];

  return (
    <div className="space-y-6">
      {/* Title */}
      <div className="flex items-center justify-between p-5 rounded-lg bg-white border border-slate-200 shadow-sm">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Activity className="w-5 h-5 text-emerald-800" /> Isolation Forest Anomaly Detection
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">Unsupervised outlier classification to flag sensor drift, calibration faults, and illegal emissions</p>
        </div>
        <button
          onClick={fetchAnomalyData}
          className="p-2 rounded-md bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 transition"
          title="Re-run Anomaly Detector"
        >
          <RefreshCcw className="w-4 h-4" />
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <div className="p-5 rounded-lg bg-white border border-slate-200 shadow-sm">
          <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Evaluated Cohort</span>
          <div className="text-3xl font-extrabold text-slate-900 mt-2">{data?.total_analyzed || 0}</div>
          <p className="text-[11px] text-slate-500 mt-1">Multi-sensor vectors</p>
        </div>
        <div className="p-5 rounded-lg bg-white border border-slate-200 shadow-sm">
          <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Normal Distribution</span>
          <div className="text-3xl font-extrabold text-emerald-800 mt-2 flex items-center gap-2">
            <CheckCircle2 className="w-5 h-5 text-emerald-700" /> {data?.normal_count || 0}
          </div>
          <p className="text-[11px] text-slate-500 mt-1">Within standard deviation bounds</p>
        </div>
        <div className="p-5 rounded-lg bg-white border border-slate-200 shadow-sm">
          <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Flagged Outliers</span>
          <div className="text-3xl font-extrabold text-amber-800 mt-2 flex items-center gap-2">
            <AlertOctagon className="w-5 h-5 text-amber-700" /> {data?.anomalies_detected || 0}
          </div>
          <p className="text-[11px] text-slate-500 mt-1">Significant anomaly score (&gt; 0.6)</p>
        </div>
      </div>

      {/* Scatter Plot Chart */}
      <div className="p-5 rounded-lg bg-white border border-slate-200 shadow-sm space-y-3">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-2">
          <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider">
            Multivariate Cluster Projection (PM2.5 vs AQI Outlier Detection)
          </h4>
          <div className="flex items-center gap-4 text-xs">
            <span className="flex items-center gap-1.5 text-slate-700 font-medium">
              <span className="w-2.5 h-2.5 rounded-sm bg-[#0f766e]"></span> Normal Baseline
            </span>
            <span className="flex items-center gap-1.5 text-amber-900 font-medium">
              <span className="w-2.5 h-2.5 rounded-sm bg-[#d97706]"></span> Outlier Deviation
            </span>
          </div>
        </div>

        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <ScatterChart margin={{ top: 10, right: 10, bottom: 10, left: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="PM25" name="PM2.5" unit="µg/m³" stroke="#64748b" fontSize={11} />
              <YAxis dataKey="AQI" name="AQI Index" stroke="#64748b" fontSize={11} />
              <Tooltip cursor={{ strokeDasharray: '3 3' }} contentStyle={{ backgroundColor: '#ffffff', borderColor: '#cbd5e1', borderRadius: '0.375rem', fontSize: '12px' }} />
              <Scatter name="Normal Readings" data={normalPoints} fill="#0f766e" />
              <Scatter name="Anomalous Readings" data={anomalyPoints} fill="#d97706" />
            </ScatterChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Flagged Anomalies Log */}
      <div className="p-5 rounded-lg bg-white border border-slate-200 shadow-sm space-y-3">
        <div className="border-b border-slate-100 pb-2">
          <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider">Identified Outlier Records</h4>
          <p className="text-[11px] text-slate-500">Readings classified as anomalous by Isolation Forest isolation paths</p>
        </div>
        {anomalyPoints.length > 0 ? (
          <div className="space-y-2">
            {anomalyPoints.map((pt, i) => (
              <div key={i} className="p-3 rounded-md bg-slate-50 border border-slate-200 flex items-center justify-between text-xs">
                <div className="flex items-center gap-3">
                  <AlertOctagon className="w-4 h-4 text-amber-700" />
                  <span className="text-slate-700">Sample #{pt.id} : PM2.5 = <strong>{pt.PM25} µg/m³</strong>, AQI = <strong>{pt.AQI}</strong></span>
                </div>
                <span className="px-2 py-0.5 rounded-md bg-amber-50 text-amber-900 border border-amber-300 font-bold font-mono">
                  Anomaly Score: {pt.anomaly_score}
                </span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-slate-500 italic py-4">No statistical anomalies currently detected in sample cohort.</p>
        )}
      </div>

      {/* Model Information */}
      <div className="p-4 rounded-lg bg-white border border-slate-200 text-xs text-slate-600 flex items-start gap-2.5">
        <Info className="w-4 h-4 text-emerald-800 shrink-0 mt-0.5" />
        <div>
          <strong className="text-slate-800">Unsupervised Algorithm:</strong> Scikit-learn IsolationForest (contamination=0.05, n_estimators=100). The model isolates abnormal instances by recursively partitioning randomly selected features. Shorter path lengths signify higher outlier probability.
        </div>
      </div>
    </div>
  );
}
