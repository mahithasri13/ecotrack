import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import NotificationToast from './components/NotificationToast';
import IndiaRealTimeView from './views/IndiaRealTimeView';
import DashboardView from './views/DashboardView';
import AirQualityView from './views/AirQualityView';
import WaterQualityView from './views/WaterQualityView';
import PredictionsView from './views/PredictionsView';
import EnvironmentalImpactView from './views/EnvironmentalImpactView';
import AnomalyDetectionView from './views/AnomalyDetectionView';
import AlertsView from './views/AlertsView';
import RecommendationsView from './views/RecommendationsView';
import HistoryView from './views/HistoryView';
import AboutView from './views/AboutView';
import DomainVerificationView from './views/DomainVerificationView';
import PrivacyPolicyView from './views/PrivacyPolicyView';
import TermsAndConditionsView from './views/TermsAndConditionsView';

export default function App() {
  const [activeTab, setActiveTab] = useState('india-live');
  const [activeToastAlert, setActiveToastAlert] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  const handleRefresh = () => {
    setRefreshKey(prev => prev + 1);
  };

  const handleTriggerToast = (alertObj) => {
    setActiveToastAlert(alertObj);
  };

  const renderView = () => {
    switch (activeTab) {
      case 'india-live':
        return <IndiaRealTimeView key={refreshKey} onTriggerToast={handleTriggerToast} />;
      case 'dashboard':
        return <DashboardView key={refreshKey} onNavigate={(tab) => setActiveTab(tab)} />;
      case 'air-quality':
        return <AirQualityView key={refreshKey} />;
      case 'water-quality':
        return <WaterQualityView key={refreshKey} />;
      case 'predictions':
        return <PredictionsView key={refreshKey} />;
      case 'impact':
        return <EnvironmentalImpactView key={refreshKey} />;
      case 'anomaly':
        return <AnomalyDetectionView key={refreshKey} />;
      case 'alerts':
        return <AlertsView key={refreshKey} />;
      case 'recommendations':
        return <RecommendationsView key={refreshKey} />;
      case 'history':
        return <HistoryView key={refreshKey} />;
      case 'about':
        return <AboutView key={refreshKey} />;
      case 'domain-verification':
        return <DomainVerificationView key={refreshKey} />;
      case 'privacy-policy':
        return <PrivacyPolicyView key={refreshKey} />;
      case 'terms':
        return <TermsAndConditionsView key={refreshKey} />;
      default:
        return <IndiaRealTimeView key={refreshKey} onTriggerToast={handleTriggerToast} />;
    }
  };

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden font-sans text-slate-800">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <Header activeTab={activeTab} onRefresh={handleRefresh} />

        <main className="flex-1 overflow-y-auto p-6 space-y-8">
          {renderView()}

          {/* Scientific Institutional Footer */}
          <footer className="mt-12 pt-6 border-t border-slate-200 text-xs text-slate-500 flex flex-col md:flex-row items-center justify-between gap-4">
            <div>
              <p className="font-semibold text-slate-700">EcoTrack - AI Environmental Impact Monitoring System</p>
              <p className="text-[11px] text-slate-500 mt-0.5">
                Verified telemetry sources: Open-Meteo European Weather Feed, CPCB National Air Quality Standards, WHO Potability Guidelines.
              </p>
            </div>

            <div className="flex items-center gap-4 text-xs font-medium">
              <button
                onClick={() => setActiveTab('privacy-policy')}
                className="hover:text-emerald-800 transition"
              >
                Privacy Policy
              </button>
              <span className="text-slate-300">|</span>
              <button
                onClick={() => setActiveTab('terms')}
                className="hover:text-emerald-800 transition"
              >
                Terms and Conditions
              </button>
              <span className="text-slate-300">|</span>
              <button
                onClick={() => setActiveTab('domain-verification')}
                className="hover:text-emerald-800 transition"
              >
                Domain and HTTPS
              </button>
            </div>
          </footer>
        </main>
      </div>

      {/* Real-Time Notification Toast Popup */}
      <NotificationToast
        alert={activeToastAlert}
        onClose={() => setActiveToastAlert(null)}
      />
    </div>
  );
}
