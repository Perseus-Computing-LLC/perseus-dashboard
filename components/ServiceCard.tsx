export default function ServiceCard({ name, status, latency_ms }: {
  name: string;
  status: string;
  latency_ms?: number;
}) {
  const isUp = status === 'up';
  return (
    <div className="card flex items-center justify-between">
      <div>
        <div className="font-medium text-sm">{name}</div>
        <div className="text-xs text-gray-500 mt-1">
          {isUp ? `${latency_ms}ms` : 'unreachable'}
        </div>
      </div>
      <span className={`px-2 py-0.5 rounded text-xs font-medium ${isUp ? 'badge-up' : 'badge-down'}`}>
        {isUp ? 'UP' : 'DOWN'}
      </span>
    </div>
  );
}
