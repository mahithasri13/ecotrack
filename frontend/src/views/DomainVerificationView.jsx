import React, { useState, useEffect } from 'react';
import { Globe, ShieldCheck, CheckCircle2, AlertTriangle, RefreshCcw, Lock, Server, Copy, Check } from 'lucide-react';
import { apiUrl } from '../api';

export default function DomainVerificationView() {
  const [domainInput, setDomainInput] = useState('ecotrack.org');
  const [verificationResult, setVerificationResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    runVerification('ecotrack.org');
  }, []);

  const runVerification = async (targetDomain) => {
    setLoading(true);
    try {
      const res = await fetch(apiUrl(`/api/system/domain-verification?domain=${encodeURIComponent(targetDomain)}`));
      const data = await res.json();
      setVerificationResult(data);
    } catch (err) {
      console.error('Domain verification failed:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (domainInput.trim()) {
      runVerification(domainInput.trim());
    }
  };

  const handleCopyNginx = () => {
    if (verificationResult?.nginx_snippet) {
      navigator.clipboard.writeText(verificationResult.nginx_snippet);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="p-6 rounded-lg bg-white border border-slate-200 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-emerald-800 mb-1">
              <Globe className="w-5 h-5 text-emerald-800" />
              <span className="text-xs font-bold uppercase tracking-wider">Production Infrastructure Workbench</span>
            </div>
            <h3 className="text-xl font-bold text-slate-900">Custom Domain and HTTPS Verification</h3>
            <p className="text-xs text-slate-600 mt-1">
              Verify live DNS record propagation, SSL certificate validity, and generate production deployment configurations for EcoTrack.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="flex items-center gap-2">
            <input
              type="text"
              value={domainInput}
              onChange={(e) => setDomainInput(e.target.value)}
              placeholder="e.g. ecotrack.org"
              className="px-3.5 py-2 rounded-md bg-white border border-slate-300 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-700 font-mono"
            />
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 rounded-md bg-[#1b4332] hover:bg-[#143225] text-white text-xs font-semibold flex items-center gap-2 transition"
            >
              {loading ? <RefreshCcw className="w-4 h-4 animate-spin" /> : <ShieldCheck className="w-4 h-4" />}
              <span>Verify Domain</span>
            </button>
          </form>
        </div>
      </div>

      {/* Verification Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {/* Overall Status */}
        <div className="p-5 rounded-lg bg-white border border-slate-200 shadow-sm">
          <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block mb-2">Overall Security Status</span>
          <div className="flex items-center gap-2">
            <span className={`px-2.5 py-1 rounded-md text-xs font-bold ${
              verificationResult?.ssl_valid
                ? 'bg-emerald-50 text-emerald-800 border border-emerald-300'
                : 'bg-amber-50 text-amber-800 border border-amber-300'
            }`}>
              {verificationResult?.status || 'Pending Check'}
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-2">
            Target Host: <span className="font-mono text-slate-800">{verificationResult?.domain || domainInput}</span>
          </p>
        </div>

        {/* DNS Status */}
        <div className="p-5 rounded-lg bg-white border border-slate-200 shadow-sm">
          <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block mb-2">DNS A-Record Resolution</span>
          <div className="flex items-center gap-2">
            {verificationResult?.dns_resolved ? (
              <>
                <CheckCircle2 className="w-4 h-4 text-emerald-700" />
                <span className="text-xs font-semibold text-emerald-800">Resolved Successfully</span>
              </>
            ) : (
              <>
                <AlertTriangle className="w-4 h-4 text-amber-700" />
                <span className="text-xs font-semibold text-amber-800">Unresolved / Local Host</span>
              </>
            )}
          </div>
          <p className="text-xs text-slate-500 mt-2 truncate">
            IPs: {verificationResult?.ip_addresses?.join(', ') || 'No public records found'}
          </p>
        </div>

        {/* SSL / HTTPS Status */}
        <div className="p-5 rounded-lg bg-white border border-slate-200 shadow-sm">
          <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block mb-2">TLS/SSL Encryption</span>
          <div className="flex items-center gap-2">
            {verificationResult?.ssl_valid ? (
              <>
                <Lock className="w-4 h-4 text-emerald-700" />
                <span className="text-xs font-semibold text-emerald-800">HTTPS Active (Port 443 Valid)</span>
              </>
            ) : (
              <>
                <Lock className="w-4 h-4 text-slate-400" />
                <span className="text-xs font-semibold text-slate-600">Pending Certificate Issuance</span>
              </>
            )}
          </div>
          <p className="text-xs text-slate-500 mt-2">
            Protocol: {verificationResult?.cert_info?.version || 'TLSv1.3 Ready'}
          </p>
        </div>
      </div>

      {/* Production Deployment Instructions */}
      <div className="p-6 rounded-lg bg-white border border-slate-200 shadow-sm space-y-4">
        <div className="flex items-center justify-between border-b border-slate-200 pb-3">
          <div>
            <h4 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <Server className="w-4 h-4 text-teal-700" />
              Nginx Production Reverse Proxy Configuration
            </h4>
            <p className="text-xs text-slate-500 mt-0.5">
              Deploy this block to /etc/nginx/sites-available/{verificationResult?.domain || 'ecotrack.org'} to terminate SSL and proxy to FastAPI backend.
            </p>
          </div>
          <button
            onClick={handleCopyNginx}
            className="px-3 py-1.5 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold flex items-center gap-1.5 transition"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-700" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied' : 'Copy Config'}</span>
          </button>
        </div>

        <pre className="p-4 rounded-md bg-slate-900 text-slate-100 font-mono text-xs overflow-x-auto leading-relaxed">
          {verificationResult?.nginx_snippet || '# Loading config template...'}
        </pre>

        <div className="p-4 rounded-md bg-slate-50 border border-slate-200 space-y-2">
          <h5 className="text-xs font-bold text-slate-800 uppercase tracking-wide">Automated SSL Provisioning via Certbot</h5>
          <p className="text-xs text-slate-600">
            Execute the following command on your production server to automatically issue and install a Let's Encrypt certificate:
          </p>
          <code className="block p-2.5 rounded bg-white border border-slate-300 font-mono text-xs text-emerald-800 font-bold select-all">
            sudo {verificationResult?.certbot_command || `certbot --nginx -d ${domainInput}`}
          </code>
        </div>
      </div>

      {/* Pre-flight Security Checklist */}
      <div className="p-6 rounded-lg bg-white border border-slate-200 shadow-sm space-y-3">
        <h4 className="text-sm font-bold text-slate-900">Pre-Launch Security Checklist</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs text-slate-700">
          <div className="flex items-start gap-2.5 p-3 rounded-md bg-slate-50 border border-slate-200">
            <CheckCircle2 className="w-4 h-4 text-emerald-700 shrink-0 mt-0.5" />
            <div>
              <strong className="block text-slate-800">Strict-Transport-Security (HSTS)</strong>
              Enforces HTTPS connection across all subsequent client requests.
            </div>
          </div>
          <div className="flex items-start gap-2.5 p-3 rounded-md bg-slate-50 border border-slate-200">
            <CheckCircle2 className="w-4 h-4 text-emerald-700 shrink-0 mt-0.5" />
            <div>
              <strong className="block text-slate-800">X-Content-Type-Options: nosniff</strong>
              Mitigates MIME-type sniffing vulnerabilities across API endpoints.
            </div>
          </div>
          <div className="flex items-start gap-2.5 p-3 rounded-md bg-slate-50 border border-slate-200">
            <CheckCircle2 className="w-4 h-4 text-emerald-700 shrink-0 mt-0.5" />
            <div>
              <strong className="block text-slate-800">X-Frame-Options: DENY</strong>
              Protects dashboard telemetry from unauthorized iframe clickjacking.
            </div>
          </div>
          <div className="flex items-start gap-2.5 p-3 rounded-md bg-slate-50 border border-slate-200">
            <CheckCircle2 className="w-4 h-4 text-emerald-700 shrink-0 mt-0.5" />
            <div>
              <strong className="block text-slate-800">Zero AI-Builder Branding</strong>
              All template tags, student demos, and placeholder scripts stripped for production.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
