export default function ContextPanel({ context }: { context: any }) {
  if (!context) {
    return (
      <div>
        <h2 className="text-lg font-semibold mb-3">Live Context Snapshot</h2>
        <div className="card text-sm text-gray-400">
          <p className="mb-2">Context will appear here when the API is connected.</p>
          <p>Demo files: AGENTS.md, pyproject.toml, docker-compose.yml, Makefile</p>
        </div>
      </div>
    );
  }

  return (
    <div>
      <h2 className="text-lg font-semibold mb-3">Live Context Snapshot</h2>
      <div className="card">
        <div className="text-xs text-gray-500 mb-3">
          Resolved at: {new Date(context.resolved_at).toLocaleString()} &middot;
          Token estimate: {context.token_estimate?.toLocaleString()}
        </div>
        <div className="space-y-2">
          <h3 className="text-sm font-medium text-gray-300">Services ({context.services?.length || 0})</h3>
          <ul className="text-xs text-gray-400 space-y-1">
            {context.services?.map((s: any) => (
              <li key={s.name}>● {s.name}: <span className={s.status === 'up' ? 'text-[#3fb950]' : 'text-[#f85149]'}>{s.status}</span></li>
            ))}
          </ul>
          <h3 className="text-sm font-medium text-gray-300 mt-3">Context Files</h3>
          <ul className="text-xs text-gray-400 space-y-1">
            {context.context_files?.map((f: string) => (
              <li key={f}>📄 {f}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
