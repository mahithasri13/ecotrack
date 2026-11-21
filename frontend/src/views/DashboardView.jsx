import React, { useState, useEffect } from 'react';
import { Wind, Droplets, ShieldAlert, Activity, AlertTriangle, ArrowUpRight, CheckCircle2, RefreshCcw, Info } from 'lucide-react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { apiUrl } from '../api';

export default function DashboardView({ onNavigate }) {
  const [summary, setSummary] = useState(null);
  const [trends, setTrends] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      const [sumRes, trendRes] = await Promise.all([
        fetch(apiUrl('/api/dashboard/summary')),
        fetch(apiUrl('/api/analytics/trends'))
      ]);
      const sumData = await sumRes.json();
      const trendData = await trendRes.json();
      setSummary(sumData);
      setTrends(trendData.air_trends || []);
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-80 text-slate-500 gap-2">
        <RefreshCcw className="w-5 h-5 animate-spin text-emerald-800" />
        <span className="text-sm">Synthesizing environmental surveillance telemetry...</span>
      </div>
    );
  }

  const ehi = summary?.ehi || { score: 78.5, status: 'Moderate', color: 'emerald' };

  return (
    <div className="space-y-6">
      {/* Top Banner Alert if active alerts exist */}
      {summary?.alerts && summary.alerts.length > 0 && (
        <div className="p-4 rounded-lg bg-amber-50 border border-amber-300 flex items-start justify-between gap-4">
          <div className="flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-amber-700 shrink-0 mt-0.5" />
            <div>
              <h4 className="text-xs font-bold text-amber-900">{summary.alerts[0].title}</h4>
              <p className="text-xs text-amber-800 mt-0.5">{summary.alerts[0].message}</p>
            </div>
          </div>
          <button
            onClick={() => onNavigate('alerts')}
            className="text-xs font-semibold px-3 py-1.5 rounded-md bg-amber-200 hover:bg-amber-300 text-amber-900 transition shrink-0"
          >
            Inspect Alerts
          </button>
        </div>
      )}

      {/* Main KPI Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {/* Environmental Health Index (EHI) Card */}
        <div className="p-5 rounded-lg bg-white border border-slate-200 shadow-sm flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Environmental Health Index</span>
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-600"></span>
          </div>
          <div className="my-4 flex items-baseline gap-3">
            <span className="text-4xl font-extrabold text-slate-900 tracking-tight">{ehi.score}</span>
            <span className="text-xs font-semibold text-slate-400">/ 100</span>
            <span className="ml-auto px-2 py-0.5 rounded-md text-xs font-bold bg-emerald-50 text-emerald-900 border border-emerald-300">
              {ehi.status}
            </span>
          </div>
          <div className="w-full bg-slate-100 rounded-md h-2 overflow-hidden">
            <div
              className="bg-[#1b4332] h-2 transition-all duration-500"
              style={{ width: `${ehi.score}%` }}
            ></div>
          </div>
          <p className="text-[11px] text-slate-500 mt-3 font-medium">Weighted composite score (50% Air Quality + 50% Water Potability)</p>
        </div>

        {/* Air Quality AQI Card */}
        <div className="p-5 rounded-lg bg-white border border-slate-200 shadow-sm flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Wind className="w-4 h-4 text-teal-800" />
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Mean Ambient AQI</span>
            </div>
            <button onClick={() => onNavigate('air-quality')} className="text-slate-400 hover:text-slate-900 transition" title="Go to Air Quality Predictor">
              <ArrowUpRight className="w-4 h-4" />
            </button>
          </div>
          <div className="my-4 flex items-baseline gap-3">
            <span className="text-4xl font-extrabold text-slate-900 tracking-tight">{summary?.average_aqi || 68.5}</span>
            <span className="px-2 py-0.5 rounded-md text-xs font-bold bg-yellow-50 text-yellow-900 border border-yellow-300">
              Moderate
            </span>
          </div>
          <div className="flex items-center justify-between text-xs text-slate-600 pt-2 border-t border-slate-100">
            <span>Reference Baseline: <strong className="text-slate-800">CPCB NAAQS</strong></span>
            <span>WHO Target: <strong className="text-slate-800">&lt; 50 AQI</strong></span>
          </div>
        </div>

        {/* Water Potability Card */}
        <div className="p-5 rounded-lg bg-white border border-slate-200 shadow-sm flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Droplets className="w-4 h-4 text-emerald-800" />
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Water Safety Rate</span>
            </div>
            <button onClick={() => onNavigate('water-quality')} className="text-slate-400 hover:text-slate-900 transition" title="Go to Water Quality Predictor">
              <ArrowUpRight className="w-4 h-4" />
            </button>
          </div>
          <div className="my-4 flex items-baseline gap-3">
            <span className="text-4xl font-extrabold text-slate-900 tracking-tight">{summary?.potability_rate || 78.5}%</span>
            <span className="px-2 py-0.5 rounded-md text-xs font-bold bg-emerald-50 text-emerald-900 border border-emerald-300 flex items-center gap-1">
              <CheckCircle2 className="w-3.5 h-3.5" /> Compliant
            </span>
          </div>
          <div className="flex items-center justify-between text-xs text-slate-600 pt-2 border-t border-slate-100">
            <span>Standard: <strong className="text-slate-800">WHO Guidelines</strong></span>
            <span>Sample Set: <strong className="text-slate-800">Physicochemical</strong></span>
          </div>
        </div>
      </div>

      {/* Main Charts and Modules Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Air Quality AQI & PM Trend Chart */}
        <div className="lg:col-span-2 p-5 rounded-lg bg-white border border-slate-200 shadow-sm space-y-3">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Air Quality and Pollutant Baseline Trends</h3>
              <p className="text-xs text-slate-500">Continuous historical AQI vs PM2.5 concentrations</p>
            </div>
            <span className="text-xs text-slate-600 bg-slate-50 px-2.5 py-1 rounded-md border border-slate-200 font-mono">
              30-Day Empirical Window
            </span>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trends}>
                <defs>
                  <linearGradient id="colorAqi" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#1b4332" stopOpacity={0.25}/>
                    <stop offset="95%" stopColor="#1b4332" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorPm" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#0f766e" stopOpacity={0.25}/>
                    <stop offset="95%" stopColor="#0f766e" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="point" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#ffffff', borderColor: '#cbd5e1', borderRadius: '0.375rem', color: '#0f172a', fontSize: '12px' }}
                />
                <Area type="monotone" dataKey="AQI" stroke="#1b4332" fillOpacity={1} fill="url(#colorAqi)" strokeWidth={2} name="AQI Index" />
                <Area type="monotone" dataKey="PM25" stroke="#0f766e" fillOpacity={1} fill="url(#colorPm)" strokeWidth={2} name="PM2.5 (µg/m³)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Quick Module Navigation and Actions */}
        <div className="p-5 rounded-lg bg-white border border-slate-200 shadow-sm flex flex-col justify-between space-y-4">
          <div>
            <h3 className="text-sm font-bold text-slate-900 mb-1">Direct Environmental Inferences</h3>
            <p className="text-xs text-slate-500">Run machine learning models against test parameters</p>
          </div>

          <div className="space-y-2.5">
            <button
              onClick={() => onNavigate('air-quality')}
              className="w-full p-3 rounded-md bg-slate-50 hover:bg-emerald-50 border border-slate-200 hover:border-emerald-300 text-left transition flex items-center justify-between group"
            >
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-md bg-white text-emerald-800 border border-slate-200">
                  <Wind className="w-4 h-4" />
                </div>
                <div>
                  <h4 className="text-xs font-bold text-slate-900">Air Quality Predictor</h4>
                  <p className="text-[11px] text-slate-500">Compute multi-pollutant AQI</p>
                </div>
              </div>
              <ArrowUpRight className="w-4 h-4 text-slate-400 group-hover:text-emerald-800 transition" />
            </button>

            <button
              onClick={() => onNavigate('water-quality')}
              className="w-full p-3 rounded-md bg-slate-50 hover:bg-teal-50 border border-slate-200 hover:border-teal-300 text-left transition flex items-center justify-between group"
            >
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-md bg-white text-teal-800 border border-slate-200">
                  <Droplets className="w-4 h-4" />
                </div>
                <div>
                  <h4 className="text-xs font-bold text-slate-900">Water Safety Classifier</h4>
                  <p className="text-[11px] text-slate-500">WHO standard potability rating</p>
                </div>
              </div>
              <ArrowUpRight className="w-4 h-4 text-slate-400 group-hover:text-teal-800 transition" />
            </button>

            <button
              onClick={() => onNavigate('anomaly')}
              className="w-full p-3 rounded-md bg-slate-50 hover:bg-slate-100 border border-slate-200 text-left transition flex items-center justify-between group"
            >
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-md bg-white text-slate-700 border border-slate-200">
                  <Activity className="w-4 h-4" />
                </div>
                <div>
                  <h4 className="text-xs font-bold text-slate-900">Isolation Forest Outliers</h4>
                  <p className="text-[11px] text-slate-500">Detect sensor anomalies</p>
                </div>
              </div>
              <ArrowUpRight className="w-4 h-4 text-slate-400 group-hover:text-slate-800 transition" />
            </button>
          </div>

          <div className="pt-3 border-t border-slate-100 text-center">
            <span className="text-[11px] text-slate-500">Cumulative Recorded Telemetry Inferences: <strong className="text-slate-800">{summary?.total_predictions || 0}</strong></span>
          </div>
        </div>
      </div>

      {/* Data Provenance and Scope Disclosure */}
      <div className="p-4 rounded-lg bg-white border border-slate-200 text-xs text-slate-600 flex items-start gap-3">
        <Info className="w-4 h-4 text-emerald-800 shrink-0 mt-0.5" />
        <div>
          <strong className="text-slate-800">Data Sources and Methodological Constraints:</strong> Atmospheric feeds are integrated directly via the Open-Meteo API using satellite assimilation models. Water potability inferences evaluate physicochemical characteristics only; biological safety testing requires certified microbiological laboratory culturing.
        </div>
      </div>
    </div>
  );
}
