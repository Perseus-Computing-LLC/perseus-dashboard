'use client';

export default function TokenChart({ metricStatus, totalSaved }: { metricStatus?: string; totalSaved?: number | null }) {
  return (
    <div className="card">
      <div className="min-h-[250px] flex items-center justify-center text-center">
        <div>
          <div className="text-lg font-semibold text-gray-300">Token savings unavailable</div>
          <p className="mt-2 text-xs text-gray-500">
            No paired measured before/after session artifact is available.
            {metricStatus ? ` Metric status: ${metricStatus}.` : ''}
          </p>
          {totalSaved != null && <p className="mt-2 text-sm text-gray-400">Observed total: {totalSaved}</p>}
        </div>
      </div>
    </div>
  );
}
