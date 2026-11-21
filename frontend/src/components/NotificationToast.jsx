import React from 'react';
import { AlertTriangle, ShieldAlert, X } from 'lucide-react';

export default function NotificationToast({ alert, onClose }) {
  if (!alert) return null;

  const isCritical = alert.severity === 'Critical';
  const isWarning = alert.severity === 'Warning';

  const borderColor = isCritical ? 'border-l-4 border-l-red-600' : (isWarning ? 'border-l-4 border-l-amber-600' : 'border-l-4 border-l-emerald-600');
  const iconColor = isCritical ? 'text-red-700 bg-red-50' : (isWarning ? 'text-amber-700 bg-amber-50' : 'text-emerald-700 bg-emerald-50');

  return (
    <div className="fixed bottom-6 right-6 z-50 max-w-md">
      <div className={`p-4 rounded-lg shadow-lg border border-slate-200 bg-white flex items-start gap-3 ${borderColor}`}>
        <div className={`p-2 rounded-md shrink-0 ${iconColor}`}>
          {isCritical ? <ShieldAlert className="w-5 h-5" /> : <AlertTriangle className="w-5 h-5" />}
        </div>
        
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between gap-2">
            <span className="text-[10px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded-md bg-slate-100 text-slate-700 border border-slate-200">
              {alert.category || 'Environmental Alert'}
            </span>
            <span className="text-[10px] text-slate-400 font-mono">AUTOMATED TELEMETRY</span>
          </div>
          <h4 className="text-xs font-bold text-slate-900 mt-1 leading-snug">{alert.title}</h4>
          <p className="text-xs text-slate-600 mt-0.5 leading-relaxed">{alert.message}</p>
        </div>

        <button
          onClick={onClose}
          className="p-1 rounded-md hover:bg-slate-100 text-slate-400 hover:text-slate-700 transition shrink-0"
          title="Dismiss Alert"
        >
          <X className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
