import React, { useState, useEffect } from 'react';
import { MapPin, Wind, Droplets, ShieldAlert, AlertTriangle, RefreshCcw, CheckCircle2, AlertOctagon, Info, Clock, Check } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { apiUrl } from '../api';

export default function IndiaRealTimeView({ onTriggerToast }) {
  const [locations, setLocations] = useState({});
  const [selectedKey, setSelectedKey] = useState('delhi_ncr');
  const [airData, setAirData] = useState(null);
  const [waterData, setWaterData] = useState(null);
  const [summaryData, setSummaryData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    fetchLocations();
  }, []);

  useEffect(() => {
    if (selectedKey) {
      fetchLocationRealtimeData(selectedKey);
    }
  }, [selectedKey]);

  const fetchLocations = async () => {
    try {
      const res = await fetch(apiUrl('/api/realtime/india-locations'));
      const data = await res.json();
      setLocations(data);
    } catch (err) {
      console.error('Failed to load locations:', err);
    }
  };

  const fetchLocationRealtimeData = async (key) => {
    setLoading(true);
    try {
      const [airRes, waterRes, sumRes] = await Promise.all([
        fetch(apiUrl(`/api/realtime/india-air?location=${key}`)).then(r => r.json()),
        fetch(apiUrl(`/api/realtime/india-water?location=${key}`)).then(r => r.json()),
        fetch(apiUrl('/api/realtime/india-summary')).then(r => r.json())
      ]);

      setAirData(airRes);
      setWaterData(waterRes);
      setSummaryData(sumRes);

      // Trigger Notification Toast if Hazardous AQI or Unsafe Water
      if (airRes?.prediction?.predicted_aqi > 150) {
        onTriggerToast && onTriggerToast({
          title: `HAZARDOUS AIR ALERT: ${airRes.location.name}`,
          message: `Real-time predicted AQI is ${airRes.prediction.predicted_aqi} (${airRes.prediction.aqi_category}). Mask advisories recommended.`,
          category: 'Air Quality Alert',
          severity: 'Critical'
        });
      } else if (waterRes?.prediction?.predicted_class === 0) {
        onTriggerToast && onTriggerToast({
          title: `UNSAFE WATER WARNING: ${waterRes.station_name}`,
          message: `Physicochemical analysis detected NON-POTABLE water quality (${waterRes.prediction.confidence_percentage}% risk factor). Do not consume untreated.`,
          category: 'Water Safety Warning',
          severity: 'Warning'
        });
      }
    } catch (err) {
      console.error('Error fetching India real-time data:', err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handleManualRefresh = () => {
    setRefreshing(true);
    fetchLocationRealtimeData(selectedKey);
  };

  const locInfo = locations[selectedKey] || { name: 'Delhi NCR', state: 'Delhi', type: 'Metropolitan' };
  const airPred = airData?.prediction;
  const waterPred = waterData?.prediction;

  const pollutantChartData = airData ? [
    { name: 'PM2.5', value: airData.input_parameters['PM2.5'], norm: 35 },
    { name: 'PM10', value: airData.input_parameters['PM10'], norm: 150 },
    { name: 'NO2', value: airData.input_parameters['NO2'], norm: 100 },
    { name: 'SO2', value: airData.input_parameters['SO2'], norm: 75 },
    { name: 'O3', value: airData.input_parameters['O3'], norm: 70 },
  ] : [];

  return (
    <div className="space-y-6">
      {/* Header and Location Selector Dropdown */}
      <div className="p-6 rounded-lg bg-white border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-5">
        <div>
          <div className="flex items-center gap-2 text-emerald-800 mb-1">
            <span className="text-xs font-bold uppercase tracking-wider">Continuous Regional Surveillance</span>
          </div>
          <h3 className="text-xl font-bold text-slate-900">India Real-Time Air and Water Monitoring Hub</h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Select an Indian city or rural district to inspect live Open-Meteo atmospheric readings and CPCB-standard physicochemical models.
          </p>
        </div>

        {/* Location Dropdown */}
        <div className="flex items-center gap-3">
          <div className="relative">
            <select
              value={selectedKey}
              onChange={(e) => setSelectedKey(e.target.value)}
              className="appearance-none bg-white border border-slate-300 rounded-md px-4 py-2.5 pr-10 text-xs font-bold text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-700 cursor-pointer shadow-xs"
            >
              <optgroup label="Metropolitan Cities">
                <option value="delhi_ncr">Delhi NCR (Capital Region)</option>
                <option value="mumbai">Mumbai Coastal Zone</option>
                <option value="bengaluru">Bengaluru Tech Corridor</option>
                <option value="kolkata">Kolkata Hooghly Zone</option>
                <option value="chennai">Chennai Coastal City</option>
                <option value="hyderabad">Hyderabad Urban Hub</option>
              </optgroup>
              <optgroup label="Heritage and Industrial Cities">
                <option value="varanasi">Varanasi Ganga River Hub</option>
                <option value="ahmedabad">Ahmedabad Sabarmati Zone</option>
                <option value="pune">Pune Mula-Mutha Zone</option>
                <option value="jaipur">Jaipur Pink City</option>
                <option value="lucknow">Lucknow Gomti Basin</option>
                <option value="patna">Patna Ganga Basin</option>
              </optgroup>
              <optgroup label="Rural and Village Hubs">
                <option value="bundelkhand_village">Bundelkhand Rural Village (MP)</option>
                <option value="punjab_canal_village">Ludhiana Canal Rural Village (Punjab)</option>
                <option value="kutch_village">Kutch Border Village (Gujarat)</option>
              </optgroup>
            </select>
            <MapPin className="w-4 h-4 text-emerald-800 absolute right-3 top-3 pointer-events-none" />
          </div>

          <button
            onClick={handleManualRefresh}
            disabled={refreshing}
            className="p-2.5 rounded-md bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 transition shrink-0"
            title="Refresh Live Sensor Telemetry"
          >
            <RefreshCcw className={`w-4 h-4 ${refreshing ? 'animate-spin text-emerald-800' : ''}`} />
          </button>
        </div>
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-72 text-slate-500 gap-2">
          <RefreshCcw className="w-5 h-5 animate-spin text-emerald-800" />
          <span className="text-sm">Fetching verified sensor streams for {locInfo.name}...</span>
        </div>
      ) : (
        <>
          {/* Main Selected Location Real-Time Gauges */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Real-Time Air Quality Card */}
            <div className="p-6 rounded-lg bg-white border border-slate-200 shadow-sm space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-md bg-emerald-50 text-emerald-800 border border-emerald-200">
                    <Wind className="w-5 h-5" />
                  </div>
                  <div>
                    <h4 className="text-sm font-bold text-slate-900">
                      Ambient Air: {locInfo.name}
                    </h4>
                    <p className="text-[11px] text-slate-500">Source: {airData?.source || 'Open-Meteo European Atmosphere Feed'}</p>
                  </div>
                </div>

                <div className="text-right">
                  <span className="text-[10px] text-slate-400 uppercase font-bold block">Predicted AQI</span>
                  <span className="text-3xl font-extrabold text-slate-900">{airPred?.predicted_aqi}</span>
                </div>
              </div>

              {/* Status Badge & Timestamp */}
              <div className="flex items-center justify-between p-3 rounded-md bg-slate-50 border border-slate-200 text-xs">
                <span className="px-2 py-0.5 rounded-md font-bold bg-yellow-50 text-yellow-900 border border-yellow-300">
                  Category: {airPred?.aqi_category}
                </span>

                <span className="flex items-center gap-1.5 font-mono text-[11px] text-slate-500">
                  <Clock className="w-3.5 h-3.5 text-slate-400" />
                  {airData?.timestamps?.ist || 'Live'}
                </span>
              </div>

              {/* Pollutant Sensor Grid */}
              <div className="grid grid-cols-3 gap-3">
                <div className="p-3 rounded-md bg-slate-50 border border-slate-200 text-center">
                  <span className="text-[10px] text-slate-500 block font-semibold">PM2.5</span>
                  <span className="text-sm font-bold text-slate-900">{airData?.input_parameters['PM2.5']} <span className="text-[10px] font-normal text-slate-500">µg/m³</span></span>
                </div>
                <div className="p-3 rounded-md bg-slate-50 border border-slate-200 text-center">
                  <span className="text-[10px] text-slate-500 block font-semibold">PM10</span>
                  <span className="text-sm font-bold text-slate-900">{airData?.input_parameters['PM10']} <span className="text-[10px] font-normal text-slate-500">µg/m³</span></span>
                </div>
                <div className="p-3 rounded-md bg-slate-50 border border-slate-200 text-center">
                  <span className="text-[10px] text-slate-500 block font-semibold">NO2</span>
                  <span className="text-sm font-bold text-slate-900">{airData?.input_parameters['NO2']} <span className="text-[10px] font-normal text-slate-500">ppb</span></span>
                </div>
              </div>

              {/* Pollutant Chart */}
              <div className="h-44 pt-2">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={pollutantChartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis dataKey="name" stroke="#64748b" fontSize={11} />
                    <YAxis stroke="#64748b" fontSize={11} />
                    <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderColor: '#cbd5e1', borderRadius: '0.375rem', fontSize: '12px' }} />
                    <Bar dataKey="value" fill="#0f766e" radius={[2, 2, 0, 0]} name="Observed Parameter" />
                    <Bar dataKey="norm" fill="#94a3b8" radius={[2, 2, 0, 0]} name="NAAQS Standard" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Real-Time Water Quality Card */}
            <div className="p-6 rounded-lg bg-white border border-slate-200 shadow-sm space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-md bg-teal-50 text-teal-800 border border-teal-200">
                    <Droplets className="w-5 h-5" />
                  </div>
                  <div>
                    <h4 className="text-sm font-bold text-slate-900">
                      Water Supply: {waterData?.station_name}
                    </h4>
                    <p className="text-[11px] text-slate-500">Source: {waterData?.source || 'CPCB Water Quality Framework'}</p>
                  </div>
                </div>

                <div className="text-right">
                  <span className="text-[10px] text-slate-400 uppercase font-bold block">Model Confidence</span>
                  <span className="text-3xl font-extrabold text-slate-900">{waterPred?.confidence_percentage}%</span>
                </div>
              </div>

              {/* Status Badge */}
              <div className="flex items-center justify-between p-3 rounded-md bg-slate-50 border border-slate-200 text-xs">
                {waterPred?.predicted_class === 1 ? (
                  <span className="px-2 py-0.5 rounded-md font-bold bg-emerald-50 text-emerald-900 border border-emerald-300 flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-700" /> Potable (Complies with WHO)
                  </span>
                ) : (
                  <span className="px-2 py-0.5 rounded-md font-bold bg-red-50 text-red-900 border border-red-300 flex items-center gap-1">
                    <ShieldAlert className="w-3.5 h-3.5 text-red-700" /> Non-Potable (Treatment Required)
                  </span>
                )}

                <span className="flex items-center gap-1.5 font-mono text-[11px] text-slate-500">
                  <Clock className="w-3.5 h-3.5 text-slate-400" />
                  {waterData?.timestamps?.ist || 'Live'}
                </span>
              </div>

              {/* Water Parameter Grid */}
              <div className="grid grid-cols-3 gap-3">
                <div className="p-3 rounded-md bg-slate-50 border border-slate-200 text-center">
                  <span className="text-[10px] text-slate-500 block font-semibold">pH Factor</span>
                  <span className="text-sm font-bold text-slate-900">{waterData?.input_parameters['ph']}</span>
                </div>
                <div className="p-3 rounded-md bg-slate-50 border border-slate-200 text-center">
                  <span className="text-[10px] text-slate-500 block font-semibold">Turbidity</span>
                  <span className="text-sm font-bold text-slate-900">{waterData?.input_parameters['Turbidity']} <span className="text-[10px] font-normal text-slate-500">NTU</span></span>
                </div>
                <div className="p-3 rounded-md bg-slate-50 border border-slate-200 text-center">
                  <span className="text-[10px] text-slate-500 block font-semibold">Sulfate</span>
                  <span className="text-sm font-bold text-slate-900">{waterData?.input_parameters['Sulfate']} <span className="text-[10px] font-normal text-slate-500">mg/L</span></span>
                </div>
              </div>

              {/* Location Dynamic Advisory */}
              <div className="p-4 rounded-md bg-slate-50 border border-slate-200 space-y-1">
                <h5 className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
                  <AlertTriangle className="w-3.5 h-3.5 text-amber-700" /> Regional Advisory Directive
                </h5>
                <p className="text-xs text-slate-600 leading-relaxed">
                  {airPred?.predicted_aqi > 150
                    ? `Elevated fine particulates in ${locInfo.name} exceed WHO daily benchmarks. Vulnerable groups should limit strenuous outdoor activity.`
                    : waterPred?.predicted_class === 0
                    ? `Water monitoring station at ${waterData?.station_name} reports elevated dissolved solids or turbidity. Filtration and boiling required before consumption.`
                    : `Environmental parameters in ${locInfo.name} are operating within allowable statutory limits.`}
                </p>
              </div>
            </div>
          </div>

          {/* Nationwide Indian Locations Comparison Matrix */}
          <div className="p-6 rounded-lg bg-white border border-slate-200 shadow-sm space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
              <div>
                <h4 className="text-sm font-bold text-slate-900">Nationwide Surveillance Matrix</h4>
                <p className="text-xs text-slate-500">Live operational overview across 15 monitored Indian urban and rural regions</p>
              </div>
              <span className="text-xs font-bold px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-900 border border-emerald-300 w-fit">
                National Composite EHI: {summaryData?.overall_ehi?.score} / 100
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
              {summaryData?.city_matrix?.map((item) => (
                <button
                  key={item.key}
                  onClick={() => setSelectedKey(item.key)}
                  className={`p-3 rounded-md text-left border transition ${
                    selectedKey === item.key
                      ? 'bg-emerald-50 border-emerald-600 text-slate-900 shadow-xs'
                      : 'bg-white border-slate-200 hover:bg-slate-50 text-slate-700'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-[10px] font-bold text-slate-400 uppercase">{item.state}</span>
                    <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded-md ${
                      item.predicted_aqi > 200 ? 'bg-red-50 text-red-800 border border-red-200' : item.predicted_aqi > 100 ? 'bg-amber-50 text-amber-800 border border-amber-200' : 'bg-emerald-50 text-emerald-800 border border-emerald-200'
                    }`}>
                      AQI {item.predicted_aqi}
                    </span>
                  </div>
                  <h5 className="text-xs font-bold text-slate-900 truncate">{item.name}</h5>
                  <div className="flex items-center justify-between text-[11px] mt-2 text-slate-500">
                    <span>Water: <strong className={item.is_potable ? "text-emerald-800" : "text-red-700"}>{item.is_potable ? "Potable" : "Unsafe"}</strong></span>
                    {item.air_anomaly && <AlertOctagon className="w-3.5 h-3.5 text-amber-600" title="Anomaly Flagged" />}
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Sensor Methodology & Boundaries Notice */}
          <div className="p-4 rounded-lg bg-white border border-slate-200 text-xs text-slate-600 flex items-start gap-3">
            <Info className="w-4 h-4 text-emerald-800 shrink-0 mt-0.5" />
            <div>
              <strong className="text-slate-800">Telemetry Data Provenance:</strong> Real-time atmospheric metrics are ingested continuously from Open-Meteo with CAMS atmospheric chemistry integration. Indian water station physicochemical values represent continuous sensor array telemetry against Indian Standard IS 10500 and WHO benchmarks.
            </div>
          </div>
        </>
      )}
    </div>
  );
}
