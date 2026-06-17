import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Perseus Dashboard — Live Context for AI Agents',
  description: 'See exactly what your AI coding agents know about your codebase — live, always current.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen">
        <nav className="border-b border-[#30363d] bg-[#0d1117] px-6 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-xl font-bold text-[#5c7cfa]">&#9670;</span>
            <span className="font-semibold text-lg">Perseus Dashboard</span>
            <span className="text-xs text-gray-500 ml-2">H0 Hackathon</span>
          </div>
          <div className="flex items-center gap-4 text-sm text-gray-400">
            <a href="/" className="hover:text-white transition">Dashboard</a>
            <a href="/context" className="hover:text-white transition">Context</a>
            <a href="/memory" className="hover:text-white transition">Memory</a>
            <a href="/analytics" className="hover:text-white transition">Analytics</a>
          </div>
        </nav>
        <main className="p-6 max-w-7xl mx-auto">{children}</main>
      </body>
    </html>
  );
}
