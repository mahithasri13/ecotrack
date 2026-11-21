import React, { useState, useEffect } from 'react';
import { apiUrl } from '../api';
import { Lightbulb, CheckCircle2, RefreshCcw, Info } from 'lucide-react';

export default function RecommendationsView() {
  const [recs, setRecs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRecs();
  }, []);

  const fetchRecs = async () => {
    setLoading(true);
    try {
      const response = await fetch(apiUrl('/api/recommendations'));
      const data = await response.json();
      setRecs(data);
    } catch (err) {
      console.error('Failed to fetch recommendations:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Title Header */}
      <div className="flex items-center justify-between p-5 rounded-lg bg-white border border-slate-200 shadow-sm">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Lightbulb className="w-5 h-5 text-emerald-800" /> Actionable Policy and Public Health Directives
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">Automated mitigation measures derived from real-time model inferences and WHO environmental criteria</p>
        </div>
        <button
          onClick={fetchRecs}
          className="p-2 rounded-md bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 transition"
          title="Refresh Advisory Directives"
        >
          <RefreshCcw className="w-4 h-4" />
        </button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-64 text-slate-500 gap-2">
          <RefreshCcw className="w-5 h-5 animate-spin text-emerald-800" />
          <span className="text-sm">Synthesizing environmental advisory directives...</span>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {recs.map((item, idx) => (
            <div key={idx} className="p-5 rounded-lg bg-white border border-slate-200 shadow-sm space-y-3 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-bold text-emerald-800 flex items-center gap-1.5">
                    <Lightbulb className="w-4 h-4 text-emerald-700" /> {item.target_domain} Protocol
                  </span>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-md ${
                    item.urgency === 'High' ? 'bg-red-50 text-red-800 border border-red-200' : 'bg-amber-50 text-amber-800 border border-amber-200'
                  }`}>
                    {item.urgency} Urgency
                  </span>
                </div>
                <h4 className="text-sm font-bold text-slate-900 mb-1.5">{item.title}</h4>
                <p className="text-xs text-slate-600 leading-relaxed">{item.recommendation}</p>
              </div>

              <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                <span className="flex items-center gap-1 text-emerald-800 font-medium">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-700" /> Statutory Rule Engine
                </span>
                <span className="text-[11px] font-mono text-slate-400">CPCB / WHO Alignment</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Advisory Scope */}
      <div className="p-4 rounded-lg bg-white border border-slate-200 text-xs text-slate-600 flex items-start gap-2.5">
        <Info className="w-4 h-4 text-emerald-800 shrink-0 mt-0.5" />
        <div>
          <strong className="text-slate-800">Operational Disclaimer:</strong> Advisory measures are algorithmic recommendations for municipal and industrial operators. Emergency evacuation or industrial shutdown orders must be ratified through certified municipal environmental authorities.
        </div>
      </div>
    </div>
  );
}
