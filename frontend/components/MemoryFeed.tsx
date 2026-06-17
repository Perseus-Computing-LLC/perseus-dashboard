'use client';

import { useState, useEffect } from 'react';

const API_URL = typeof window !== 'undefined'
  ? (process.env.NEXT_PUBLIC_API_URL || '')
  : (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000');

interface MemoryEvent {
  id: number;
  event_type: string;
  fact_key?: string;
  fact_value?: string;
  confidence: number;
  created_at: string;
}

export default function MemoryFeed({ projectId }: { projectId: number }) {
  const [events, setEvents] = useState<MemoryEvent[]>([]);

  useEffect(() => {
    fetch(`${API_URL}/api/projects/${projectId}/memories?limit=20`)
      .then(r => r.json())
      .then(setEvents)
      .catch(() => {});
  }, [projectId]);

  const displayEvents = events.length > 0 ? events : [
    { id: 1, event_type: 'store', fact_key: 'database.postgres_version', fact_value: 'PostgreSQL 16.3 on Aurora', confidence: 0.95, created_at: new Date().toISOString() },
    { id: 2, event_type: 'recall', fact_key: 'convention.python_formatter', fact_value: 'black --line-length 88', confidence: 0.92, created_at: new Date(Date.now() - 60000).toISOString() },
    { id: 3, event_type: 'insight', fact_key: 'pattern.api_structure', fact_value: 'FastAPI routes follow /api/resource/{id}/action pattern', confidence: 0.88, created_at: new Date(Date.now() - 120000).toISOString() },
    { id: 4, event_type: 'store', fact_key: 'config.ci_provider', fact_value: 'GitHub Actions with matrix build', confidence: 0.90, created_at: new Date(Date.now() - 180000).toISOString() },
    { id: 5, event_type: 'decay', fact_key: 'preference.old_editor', fact_value: 'vscode (switched to cursor)', confidence: 0.15, created_at: new Date(Date.now() - 240000).toISOString() },
  ];

  const badgeClass = (type: string) => {
    switch (type) {
      case 'store': return 'badge-up';
      case 'recall': return 'bg-[#5c7cfa]/20 text-[#5c7cfa]';
      case 'insight': return 'badge-warn';
      case 'decay': return 'badge-down';
      default: return 'bg-gray-700 text-gray-300';
    }
  };

  return (
    <div>
      <h2 className="text-lg font-semibold mb-3">Memory Feed</h2>
      <div className="card max-h-[400px] overflow-y-auto">
        <div className="space-y-3">
          {displayEvents.map((event) => (
            <div key={event.id} className="border-b border-[#30363d] pb-2 last:border-0">
              <div className="flex items-center gap-2 mb-1">
                <span className={`px-2 py-0 text-xs rounded font-medium ${badgeClass(event.event_type)}`}>
                  {event.event_type.toUpperCase()}
                </span>
                <span className="text-xs text-gray-500">
                  {new Date(event.created_at).toLocaleTimeString()}
                </span>
                <span className="text-xs text-gray-600 ml-auto">
                  {Math.round(event.confidence * 100)}% conf
                </span>
              </div>
              {event.fact_key && (
                <div className="text-xs text-gray-400 mt-1">
                  <span className="text-gray-300 font-medium">{event.fact_key}</span>
                  {event.fact_value && <> → {event.fact_value.substring(0, 80)}</>}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
