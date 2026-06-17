'use client';

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const demoData = [
  { day: 'Mon', saved: 2100, used: 8500 },
  { day: 'Tue', saved: 1800, used: 7200 },
  { day: 'Wed', saved: 2400, used: 9100 },
  { day: 'Thu', saved: 3100, used: 10400 },
  { day: 'Fri', saved: 1950, used: 7800 },
  { day: 'Sat', saved: 800, used: 3200 },
  { day: 'Sun', saved: 697, used: 2800 },
];

export default function TokenChart({ projectId }: { projectId: number }) {
  return (
    <div className="card">
      <ResponsiveContainer width="100%" height={250}>
        <LineChart data={demoData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#30363d" />
          <XAxis dataKey="day" stroke="#8b949e" fontSize={12} />
          <YAxis stroke="#8b949e" fontSize={12} />
          <Tooltip
            contentStyle={{
              background: '#161b22',
              border: '1px solid #30363d',
              borderRadius: '6px',
              color: '#e6edf3',
            }}
          />
          <Line type="monotone" dataKey="saved" stroke="#3fb950" strokeWidth={2} name="Tokens Saved" />
          <Line type="monotone" dataKey="used" stroke="#5c7cfa" strokeWidth={2} name="Tokens Used" />
        </LineChart>
      </ResponsiveContainer>
      <div className="flex gap-6 mt-3 text-xs text-gray-400">
        <div className="flex items-center gap-2">
          <div className="w-3 h-0.5 bg-[#3fb950]" /> Tokens Saved
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-0.5 bg-[#5c7cfa]" /> Tokens Used
        </div>
      </div>
    </div>
  );
}
