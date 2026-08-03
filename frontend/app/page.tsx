'use client';

import { useState, useEffect } from 'react';
import ServiceCard from '@/components/ServiceCard';
import ContextPanel from '@/components/ContextPanel';
import MemoryFeed from '@/components/MemoryFeed';
import TokenChart from '@/components/TokenChart';

const API_URL = ''

interface ServiceStatus {
  name: string;
  status: string;
  latency_ms?: number;
  data_mode?: string;
}

interface AnalyticsSummary {
  data_mode?: string;
  metric_status?: string;
  total_saved?: number | null;
  observed_at?: string;
}

export default function DashboardPage() {
  const [services, setServices] = useState<ServiceStatus[]>([]);
  const [context, setContext] = useState<any>(null);
  const [analytics, setAnalytics] = useState<AnalyticsSummary | null>(null);
  const [memoryCount, setMemoryCount] = useState<number | null>(null);
  const [dataMode, setDataMode] = useState('unavailable');
  const [loading, setLoading] = useState(true);
  const projectId = 1; // Demo project

  useEffect(() => {
    async function fetchData() {
      try {
        const [svcRes, ctxRes, analyticsRes, memoriesRes] = await Promise.all([
          fetch(`${API_URL}/api/projects/${projectId}/services`),
          fetch(`${API_URL}/api/projects/${projectId}/context`),
          fetch(`${API_URL}/api/projects/${projectId}/analytics/summary`),
          fetch(`${API_URL}/api/projects/${projectId}/memories?limit=50`),
        ]);
        if (svcRes.ok) {
          const nextServices = await svcRes.json();
          setServices(nextServices);
          if (nextServices[0]?.data_mode) setDataMode(nextServices[0].data_mode);
        }
        if (ctxRes.ok) {
          const nextContext = await ctxRes.json();
          setContext(nextContext);
          if (nextContext.data_mode) setDataMode(nextContext.data_mode);
        }
        if (analyticsRes.ok) {
          const nextAnalytics = await analyticsRes.json();
          setAnalytics(nextAnalytics);
          if (nextAnalytics.data_mode) setDataMode(nextAnalytics.data_mode);
        }
        if (memoriesRes.ok) setMemoryCount((await memoriesRes.json()).length);
      } catch (e) {
        console.log('Dashboard telemetry unavailable');
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  const displayServices = services;
  const upCount = displayServices.filter(s => s.status === 'up').length;

  return (
    <div>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">perseus-dashboard</h1>
        <p className="text-gray-400">
          Context telemetry &middot; Data mode: {dataMode} &middot;{' '}
          Last observed: {context?.observed_at ? new Date(context.observed_at).toLocaleString() : 'unavailable'}
        </p>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-4 gap-4 mb-8">
        <div className="card">
          <div className="text-sm text-gray-400 mb-1">Services</div>
          <div className="text-2xl font-bold text-[#3fb950]">{displayServices.length ? `${upCount}/${displayServices.length} UP` : '—'}</div>
        </div>
        <div className="card">
          <div className="text-sm text-gray-400 mb-1">Context Files</div>
          <div className="text-2xl font-bold">{context?.context_files?.length ?? '—'}</div>
        </div>
        <div className="card">
          <div className="text-sm text-gray-400 mb-1">Tokens Saved</div>
          <div className="text-2xl font-bold text-[#5c7cfa]">{analytics?.total_saved ?? '—'}</div>
        </div>
        <div className="card">
          <div className="text-sm text-gray-400 mb-1">Active Memories</div>
          <div className="text-2xl font-bold text-[#d2991d]">{memoryCount ?? '—'}</div>
        </div>
      </div>

      {/* Services Grid */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-3">Synthetic Service Fixture</h2>
        <div className="grid grid-cols-3 gap-3">
          {displayServices.length === 0 && <div className="card text-sm text-gray-400">No live service telemetry is available.</div>}
          {displayServices.map((svc) => (
            <ServiceCard key={svc.name} name={svc.name} status={svc.status} latency_ms={svc.latency_ms} />
          ))}
        </div>
      </div>

      {/* Two-column: Context + Memory */}
      <div className="grid grid-cols-2 gap-6 mb-8">
        <ContextPanel context={context} />
        <MemoryFeed projectId={projectId} />
      </div>

      {/* Analytics Chart */}
      <div>
        <h2 className="text-lg font-semibold mb-3">Token Savings (Last 7 Days · synthetic fixture)</h2>
        <TokenChart metricStatus={analytics?.metric_status} totalSaved={analytics?.total_saved} />
      </div>
    </div>
  );
}
