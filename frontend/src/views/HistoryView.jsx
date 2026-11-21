import React, { useState, useEffect } from 'react';
import { History, Download, Trash2, Search, RefreshCcw, Info } from 'lucide-react';
import { apiUrl } from '../api';

export default function HistoryView() {
  const [airHistory, setAirHistory] = useState([]);
  const [waterHistory, setWaterHistory] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [activeTab, setActiveTab] = useState('air');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const response = await fetch(apiUrl('/api/history'));
      const data = await response.json();
      setAirHistory(data.air_predictions || []);
      setWaterHistory(data.water_predictions || []);
    } catch (err) {
      console.error('Failed to fetch history:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleClearHistory = async () => {
    if (window.confirm('Are you sure you want to permanently clear all recorded prediction history?')) {
      try {
        await fetch(apiUrl('/api/history'), { method: 'DELETE' });
        fetchHistory();
      } catch (err) {
        console.error('Clear failed:', err);
      }
    }
  };

  const handleExportCSV = () => {
    window.location.href = apiUrl('/api/history/export?format=csv');
  };

  const filteredAir = airHistory.filter(item =>
    item.aqi_category.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.id.toString().includes(searchTerm)
  );

  const filteredWater = waterHistory.filter(item =>
    item.potability_status.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.id.toString().includes(searchTerm)
  );

  return (
    <div className="space-y-6">
      {/* Controls Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-5 rounded-lg bg-white border border-slate-200 shadow-sm">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <History className="w-5 h-5 text-emerald-800" /> Historical Telemetry and Data Management
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">Auditable repository of real-time inferences, anomaly classifications, and database exports</p>
        </div>

        <div className="flex items-center gap-2.5">
          <button
            onClick={handleExportCSV}
            className="px-3 py-1.5 rounded-md bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 text-xs font-semibold transition flex items-center gap-1.5 shadow-xs"
          >
            <Download className="w-3.5 h-3.5 text-emerald-800" /> Export CSV
          </button>
          <button
            onClick={handleClearHistory}
            className="px-3 py-1.5 rounded-md bg-red-50 border border-red-200 text-red-800 hover:bg-red-100 text-xs font-semibold transition flex items-center gap-1.5"
          >
            <Trash2 className="w-3.5 h-3.5" /> Purge Logs
          </button>
        </div>
      </div>

      {/* Tabs & Search */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-1.5 bg-white p-1 rounded-md border border-slate-200 shadow-xs">
          <button
            onClick={() => setActiveTab('air')}
            className={`px-3 py-1.5 rounded-md text-xs font-bold transition ${
              activeTab === 'air' ? 'bg-[#1b4332] text-white' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Air Quality Inferences ({airHistory.length})
          </button>
          <button
            onClick={() => setActiveTab('water')}
            className={`px-3 py-1.5 rounded-md text-xs font-bold transition ${
              activeTab === 'water' ? 'bg-[#0f766e] text-white' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Water Potability Inferences ({waterHistory.length})
          </button>
        </div>

        <div className="relative w-full sm:w-64">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search records by ID or status..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 rounded-md bg-white border border-slate-300 text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-700 shadow-xs"
          />
        </div>
      </div>

      {/* History Table */}
      <div className="p-5 rounded-lg bg-white border border-slate-200 shadow-sm overflow-x-auto">
        {loading ? (
          <div className="flex items-center justify-center h-48 text-slate-500 gap-2">
            <RefreshCcw className="w-5 h-5 animate-spin text-emerald-800" />
            <span className="text-sm">Querying SQLite prediction repository...</span>
          </div>
        ) : activeTab === 'air' ? (
          filteredAir.length > 0 ? (
            <table className="w-full text-left text-xs text-slate-700">
              <thead className="text-[11px] font-bold text-slate-500 uppercase tracking-wider bg-slate-50 border-b border-slate-200">
                <tr>
                  <th className="p-3">Record ID</th>
                  <th className="p-3">Recorded Timestamp</th>
                  <th className="p-3">Predicted AQI</th>
                  <th className="p-3">Category</th>
                  <th className="p-3">PM2.5 (µg/m³)</th>
                  <th className="p-3">NO2 (ppb)</th>
                  <th className="p-3">Anomaly Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-mono">
                {filteredAir.map((row) => (
                  <tr key={row.id} className="hover:bg-slate-50/80">
                    <td className="p-3 text-slate-500">#{row.id}</td>
                    <td className="p-3 font-sans text-slate-700">{row.timestamp}</td>
                    <td className="p-3 font-bold text-slate-900">{row.predicted_aqi}</td>
                    <td className="p-3 font-sans">
                      <span className="px-2 py-0.5 rounded-md text-[10px] font-semibold bg-slate-100 text-slate-700 border border-slate-200">
                        {row.aqi_category}
                      </span>
                    </td>
                    <td className="p-3 text-slate-600">{row.PM2_5}</td>
                    <td className="p-3 text-slate-600">{row.NO2}</td>
                    <td className="p-3 font-sans">
                      {row.is_anomaly ? (
                        <span className="text-amber-800 font-bold text-[11px] bg-amber-50 px-2 py-0.5 rounded-md border border-amber-200">
                          Outlier (Score: {row.anomaly_score})
                        </span>
                      ) : (
                        <span className="text-emerald-800 text-[11px] font-medium">Nominal</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="py-8 text-center text-xs text-slate-500">
              No air quality records found matching query.
            </div>
          )
        ) : (
          filteredWater.length > 0 ? (
            <table className="w-full text-left text-xs text-slate-700">
              <thead className="text-[11px] font-bold text-slate-500 uppercase tracking-wider bg-slate-50 border-b border-slate-200">
                <tr>
                  <th className="p-3">Record ID</th>
                  <th className="p-3">Recorded Timestamp</th>
                  <th className="p-3">Potability Status</th>
                  <th className="p-3">Confidence</th>
                  <th className="p-3">pH</th>
                  <th className="p-3">Turbidity (NTU)</th>
                  <th className="p-3">Sulfate (mg/L)</th>
                  <th className="p-3">Anomaly Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-mono">
                {filteredWater.map((row) => (
                  <tr key={row.id} className="hover:bg-slate-50/80">
                    <td className="p-3 text-slate-500">#{row.id}</td>
                    <td className="p-3 font-sans text-slate-700">{row.timestamp}</td>
                    <td className="p-3 font-sans">
                      <span className={`px-2 py-0.5 rounded-md text-[10px] font-semibold ${
                        row.predicted_class === 1
                          ? 'bg-emerald-50 text-emerald-900 border border-emerald-300'
                          : 'bg-red-50 text-red-900 border border-red-300'
                      }`}>
                        {row.potability_status}
                      </span>
                    </td>
                    <td className="p-3 text-slate-800 font-bold">{row.confidence_percentage}%</td>
                    <td className="p-3 text-slate-600">{row.ph}</td>
                    <td className="p-3 text-slate-600">{row.Turbidity}</td>
                    <td className="p-3 text-slate-600">{row.Sulfate}</td>
                    <td className="p-3 font-sans">
                      {row.is_anomaly ? (
                        <span className="text-amber-800 font-bold text-[11px] bg-amber-50 px-2 py-0.5 rounded-md border border-amber-200">
                          Outlier (Score: {row.anomaly_score})
                        </span>
                      ) : (
                        <span className="text-emerald-800 text-[11px] font-medium">Nominal</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="py-8 text-center text-xs text-slate-500">
              No water potability records found matching query.
            </div>
          )
        )}
      </div>

      {/* Persistence Note */}
      <div className="p-4 rounded-lg bg-white border border-slate-200 text-xs text-slate-600 flex items-start gap-2.5">
        <Info className="w-4 h-4 text-emerald-800 shrink-0 mt-0.5" />
        <div>
          <strong className="text-slate-800">Storage Architecture:</strong> Inferences are logged transactionally into local SQLite (ecotrack.db). No external cloud database or third-party tracking services are invoked.
        </div>
      </div>
    </div>
  );
}
