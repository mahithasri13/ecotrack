import React from 'react';
import { ShieldAlert, AlertTriangle, Activity, CheckCircle, Info } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

export default function EnvironmentalImpactView() {
  const airImpactData = [
    { name: 'PM2.5', importance: 0.35, risk: 'High' },
    { name: 'PM10', importance: 0.22, risk: 'High' },
    { name: 'NO2', importance: 0.18, risk: 'Moderate' },
    { name: 'SO2', importance: 0.12, risk: 'Moderate' },
    { name: 'CO', importance: 0.08, risk: 'Low' },
    { name: 'O3', importance: 0.05, risk: 'Low' },
  ];

  const waterImpactData = [
    { name: 'Sulfate', importance: 0.28, risk: 'High' },
    { name: 'pH', importance: 0.24, risk: 'High' },
    { name: 'Chloramines', importance: 0.18, risk: 'Moderate' },
    { name: 'Solids (TDS)', importance: 0.14, risk: 'Moderate' },
    { name: 'Turbidity', importance: 0.10, risk: 'Low' },
    { name: 'Trihalomethanes', importance: 0.06, risk: 'Low' },
  ];

  return (
    <div className="space-y-6">
      {/* View Title */}
      <div className="p-5 rounded-lg bg-white border border-slate-200 shadow-sm">
        <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
          <ShieldAlert className="w-5 h-5 text-emerald-800" /> Environmental Impact and Feature Sensitivity Analysis
        </h3>
        <p className="text-xs text-slate-500 mt-0.5">Statistical parameter sensitivity, feature contribution weights, and ecosystem vulnerability indicators</p>
      </div>

      {/* Feature Contribution Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Air Quality Feature Importance */}
        <div className="p-5 rounded-lg bg-white border border-slate-200 shadow-sm space-y-3">
          <div className="border-b border-slate-100 pb-2">
            <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider">Air Quality Regression Sensitivity Weights</h4>
            <p className="text-[11px] text-slate-500">Relative contribution of atmospheric constituents to predicted AQI</p>
          </div>
          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={airImpactData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis type="number" stroke="#64748b" fontSize={11} domain={[0, 0.4]} />
                <YAxis dataKey="name" type="category" stroke="#64748b" fontSize={11} width={70} />
                <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderColor: '#cbd5e1', borderRadius: '0.375rem', fontSize: '12px' }} />
                <Bar dataKey="importance" fill="#1b4332" radius={[0, 2, 2, 0]} name="Sensitivity Weight" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Water Quality Feature Importance */}
        <div className="p-5 rounded-lg bg-white border border-slate-200 shadow-sm space-y-3">
          <div className="border-b border-slate-100 pb-2">
            <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider">Water Potability Gini Importance Weights</h4>
            <p className="text-[11px] text-slate-500">Gradient boosted decision tree feature splits across 3,276 samples</p>
          </div>
          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={waterImpactData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis type="number" stroke="#64748b" fontSize={11} domain={[0, 0.35]} />
                <YAxis dataKey="name" type="category" stroke="#64748b" fontSize={11} width={90} />
                <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderColor: '#cbd5e1', borderRadius: '0.375rem', fontSize: '12px' }} />
                <Bar dataKey="importance" fill="#0f766e" radius={[0, 2, 2, 0]} name="Importance Factor" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Risk Matrix Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <div className="p-5 rounded-lg bg-white border border-slate-200 shadow-sm space-y-2">
          <div className="flex items-center justify-between text-xs font-bold text-slate-700">
            <span>Public Health Exposure Risk</span>
            <span className="px-2 py-0.5 rounded-md bg-amber-50 text-amber-900 border border-amber-300">Moderate</span>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            Fine particulates (PM2.5) contribute to 35% of model predictive variance, correlating with upper respiratory stress indices.
          </p>
        </div>

        <div className="p-5 rounded-lg bg-white border border-slate-200 shadow-sm space-y-2">
          <div className="flex items-center justify-between text-xs font-bold text-slate-700">
            <span>Water Infrastructure Vulnerability</span>
            <span className="px-2 py-0.5 rounded-md bg-emerald-50 text-emerald-900 border border-emerald-300">Low</span>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            Sulfate and pH factors across baseline municipal reservoirs currently satisfy metallic conduit corrosion thresholds.
          </p>
        </div>

        <div className="p-5 rounded-lg bg-white border border-slate-200 shadow-sm space-y-2">
          <div className="flex items-center justify-between text-xs font-bold text-slate-700">
            <span>Vegetation and Smog Sensitivity</span>
            <span className="px-2 py-0.5 rounded-md bg-amber-50 text-amber-900 border border-amber-300">Moderate</span>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            Nitrogen Dioxide concentrations in urban basins drive ground-level ozone formation, impacting regional flora and crops.
          </p>
        </div>
      </div>

      {/* Methodology and Scope */}
      <div className="p-4 rounded-lg bg-white border border-slate-200 text-xs text-slate-600 flex items-start gap-2.5">
        <Info className="w-4 h-4 text-emerald-800 shrink-0 mt-0.5" />
        <div>
          <strong className="text-slate-800">Analytical Methodology:</strong> Feature contribution rankings reflect standardized coefficients in linear regression and mean decrease in impurity (MDI) across GradientBoosting ensemble trees.
        </div>
      </div>
    </div>
  );
}
