import React from 'react';
import {
  MapPin, LayoutDashboard, Wind, Droplets, Binary, ShieldAlert,
  AlertTriangle, Lightbulb, History, Info, Leaf, Activity, Globe, Scale
} from 'lucide-react';

const navItems = [
  { id: 'india-live', label: 'India Live Monitor', icon: MapPin, badge: 'LIVE' },
  { id: 'dashboard', label: 'Executive Dashboard', icon: LayoutDashboard },
  { id: 'air-quality', label: 'Air Quality Predictor', icon: Wind },
  { id: 'water-quality', label: 'Water Potability', icon: Droplets },
  { id: 'predictions', label: 'Batch Predictions', icon: Binary },
  { id: 'impact', label: 'Environmental Impact', icon: ShieldAlert },
  { id: 'anomaly', label: 'Anomaly Detection', icon: Activity },
  { id: 'alerts', label: 'Alerts and Warnings', icon: AlertTriangle, badge: 'Active' },
  { id: 'recommendations', label: 'Action Recommendations', icon: Lightbulb },
  { id: 'history', label: 'Historical Data', icon: History },
  { id: 'about', label: 'Model Metrics and Data', icon: Info },
  { id: 'domain-verification', label: 'Domain and HTTPS', icon: Globe },
  { id: 'privacy-policy', label: 'Privacy Policy', icon: ShieldAlert },
  { id: 'terms', label: 'Terms and Conditions', icon: Scale }
];

export default function Sidebar({ activeTab, setActiveTab }) {
  return (
    <aside className="w-64 bg-white border-r border-slate-200 flex flex-col shrink-0 h-screen sticky top-0">
      {/* Brand Logo */}
      <div className="p-5 border-b border-slate-200 flex items-center gap-3">
        <div className="w-10 h-10 rounded-lg bg-[#1b4332] flex items-center justify-center shadow-sm">
          <Leaf className="w-5 h-5 text-white" />
        </div>
        <div>
          <h1 className="font-bold text-base text-slate-900 tracking-tight flex items-center gap-1.5">
            EcoTrack <span className="text-[10px] font-semibold px-1.5 py-0.5 rounded-md bg-emerald-100 text-emerald-900 border border-emerald-300">SYSTEM</span>
          </h1>
          <p className="text-[11px] text-slate-500 font-medium">Smart Environmental Impact AI</p>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
        <div className="px-3 py-1.5 text-[10px] font-bold uppercase tracking-wider text-slate-400">
          Surveillance Modules
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center justify-between px-3 py-2 rounded-md text-xs font-medium transition-all ${
                isActive
                  ? 'bg-emerald-50 text-emerald-900 border-l-4 border-[#1b4332] font-semibold'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
              }`}
            >
              <div className="flex items-center gap-2.5">
                <Icon className={`w-4 h-4 ${isActive ? 'text-emerald-800' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded-md ${
                  item.badge === 'LIVE'
                    ? 'bg-emerald-100 text-emerald-800 border border-emerald-300 font-mono'
                    : 'bg-amber-100 text-amber-800 border border-amber-300'
                }`}>
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* System Status Footer */}
      <div className="p-4 border-t border-slate-200 bg-slate-50">
        <div className="flex items-center justify-between text-xs text-slate-600 mb-1">
          <span className="flex items-center gap-1.5 font-medium">
            <span className="w-2 h-2 rounded-full bg-emerald-600"></span>
            India Telemetry Online
          </span>
          <span className="text-slate-400 font-mono text-[10px]">v1.0.0</span>
        </div>
        <p className="text-[10px] text-slate-500">Open-Meteo | CPCB Framework | Scikit-Learn</p>
      </div>
    </aside>
  );
}
