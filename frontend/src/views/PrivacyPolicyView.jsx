import React from 'react';
import { ShieldCheck, FileText, Database, Lock, EyeOff } from 'lucide-react';

export default function PrivacyPolicyView() {
  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header Banner */}
      <div className="p-6 rounded-lg bg-white border border-slate-200 shadow-sm">
        <div className="flex items-center gap-2 text-emerald-800 mb-2">
          <ShieldCheck className="w-5 h-5 text-emerald-800" />
          <span className="text-xs font-bold uppercase tracking-wider">Regulatory Compliance</span>
        </div>
        <h2 className="text-2xl font-bold text-slate-900">EcoTrack Privacy Policy</h2>
        <p className="text-xs text-slate-500 mt-1">
          Effective Date: October 11, 2026 | System Version: 1.0.0-production
        </p>
      </div>

      {/* Main Content Sections */}
      <div className="p-8 rounded-lg bg-white border border-slate-200 shadow-sm space-y-6 text-sm text-slate-700 leading-relaxed">
        <section className="space-y-2">
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <FileText className="w-4 h-4 text-emerald-800" />
            1. Overview and Scope
          </h3>
          <p>
            EcoTrack is an AI-based smart environmental impact monitoring system designed for real-time air quality surveillance, water potability analysis, and environmental risk assessment. This Privacy Policy outlines how environmental telemetry and user-submitted data parameters are handled, stored, and processed across the platform.
          </p>
        </section>

        <section className="space-y-2">
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Database className="w-4 h-4 text-emerald-800" />
            2. Data Collection and Telemetry Processing
          </h3>
          <p>
            EcoTrack does not collect, harvest, or monetize personally identifiable information (PII). The platform processes only environmental, meteorological, and physicochemical data points, specifically:
          </p>
          <ul className="list-disc pl-5 space-y-1 text-slate-600">
            <li><strong>Atmospheric Data:</strong> Particulate matter (PM2.5, PM10), Nitrogen Dioxide (NO2), Sulfur Dioxide (SO2), Carbon Monoxide (CO), Ozone (O3), ambient temperature, relative humidity, and wind speed.</li>
            <li><strong>Physicochemical Water Data:</strong> pH, hardness, total dissolved solids (TDS), chloramines, sulfate, electrical conductivity, total organic carbon, trihalomethanes, and nephelometric turbidity.</li>
            <li><strong>Geographic Coordinates:</strong> Regional latitude and longitude identifiers for continuous monitoring stations across India.</li>
          </ul>
        </section>

        <section className="space-y-2">
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Lock className="w-4 h-4 text-emerald-800" />
            3. Local Storage and Data Retention
          </h3>
          <p>
            Prediction records generated via user simulation or API queries are recorded in an encrypted SQLite database stored locally within the host server infrastructure. Users maintain full sovereignty over their logged data and can export all records to CSV or clear historical logs permanently at any time via the History Management console.
          </p>
        </section>

        <section className="space-y-2">
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <EyeOff className="w-4 h-4 text-emerald-800" />
            4. Third-Party Integrations and External Feeds
          </h3>
          <p>
            Real-time atmospheric telemetry is retrieved dynamically from Open-Meteo European Meteorological APIs (Copernicus CAMS and ECMWF assimilation). Queries to these third-party endpoints transmit only geographic coordinates and do not include user identities, tracking tokens, or client cookies.
          </p>
        </section>

        <section className="space-y-2">
          <h3 className="text-base font-bold text-slate-900">5. Security Standards</h3>
          <p>
            All network communication is secured using TLS 1.3 encryption over HTTPS with strict HTTP response headers (Strict-Transport-Security, X-Content-Type-Options: nosniff, X-Frame-Options: DENY). We apply industry-standard isolation to prevent cross-site scripting and unauthorized telemetry scraping.
          </p>
        </section>

        <section className="space-y-2 border-t border-slate-200 pt-4">
          <h3 className="text-base font-bold text-slate-900">6. Inquiries and Contact</h3>
          <p className="text-slate-600">
            For technical inquiries or data sovereignty questions regarding the EcoTrack platform, contact the deployment administrators at <span className="font-mono text-emerald-800">compliance@ecotrack.org</span>.
          </p>
        </section>
      </div>
    </div>
  );
}
