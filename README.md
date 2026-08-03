# Perseus Dashboard

**Context Dashboard Prototype for AI Coding Agents** — inspect the context and telemetry contract without confusing fixtures for live evidence.

Built for **H0: Hack the Zero Stack** (June 29, 2026). Target stack: Vercel v0 + AWS Aurora PostgreSQL; this branch is fixture-backed.

## Problem

AI coding agents (Claude Code, Cursor, Copilot, Codex) use stale context files. Your CLAUDE.md goes out of date within hours. You don't know what your agent "knows" — leading to hallucinations, repeated mistakes, and wasted tokens on discovery.

## Solution

The current repository ships a clearly labeled synthetic fixture backend. It shows:
- **Synthetic service-health fixtures** — not live CI, database, API, or container status
- **Fixture context snapshot** — not an authoritative current agent context
- **Unavailable token-savings analytics** — measured values require an evidence-producing collector
- **Source-labeled memory feed** — fixture events are not persisted user memory
- **Drift detection** — what's changed since the agent last looked

Every fixture response includes `data_mode: "synthetic"`, source, and observation
metadata. A future live mode must provide a read-only collector, source revision,
observation time, and reproducible measurement evidence before presenting live
health or token-savings claims.

## Architecture

```
┌─────────────────────┐
│  Vercel v0 Frontend │  Next.js + shadcn/ui
│  (Dashboard UI)     │
└────────┬────────────┘
         │ REST fixture contract
┌────────▼────────────┐
│  FastAPI Backend    │  Source-labeled fixtures
│  (planned collector)│
└────────┬────────────┘
         │ planned database adapter
┌────────▼────────────┐
│  AWS Aurora         │  PostgreSQL (planned target)
│  (Memory + Analytics│
└─────────────────────┘
```

## Quick Start

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Hackathon

**H0: Hack the Zero Stack** — $80,000 in prizes
- Required: Vercel v0 + AWS Database
- This project targets: Vercel v0 (frontend) + AWS Aurora PostgreSQL (planned backend)
- Track: Open Innovation
- Deadline: June 29, 2026

## License

MIT — see LICENSE file.
