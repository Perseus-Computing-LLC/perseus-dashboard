'use client';

import { useState, useEffect } from 'react';

const API_URL = ''

interface MemoryEvent {
  id: number;
  event_type: string;
  fact_key?: string;
  fact_value?: string;
  confidence?: number | null;
  created_at: string;
  data_mode?: string;
}

export default function MemoryFeed({ projectId }: { projectId: number }) {
  const [events, setEvents] = useState<MemoryEvent[]>([]);

  useEffect(() => {
    fetch(`${API_URL}/api/projects/${projectId}/memories?limit=20`)
      .then(r => r.json())
      .then(setEvents)
      .catch(() => {});
  }, [projectId]);

  const displayEvents = events;

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
      <h2 className="text-lg font-semibold mb-3">Memory Feed (source-labeled)</h2>
      <div className="card max-h-[400px] overflow-y-auto">
        <div className="space-y-3">
          {displayEvents.length === 0 && (
            <p className="text-sm text-gray-400">No live memory events are available.</p>
          )}
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
                  {event.confidence == null ? 'confidence unavailable' : `${Math.round(event.confidence * 100)}% conf`}
                </span>
              </div>
              <div className="text-[10px] uppercase tracking-wide text-gray-600">
                data mode: {event.data_mode || 'unknown'}
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
