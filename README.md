# Perseus Dashboard

**Live Context Dashboard for AI Coding Agents** — see exactly what your AI knows about your codebase, in real time.

Built for **H0: Hack the Zero Stack** (June 29, 2026). Stack: Vercel v0 + AWS Aurora PostgreSQL.

## Problem

AI coding agents (Claude Code, Cursor, Copilot, Codex) use stale context files. Your CLAUDE.md goes out of date within hours. You don't know what your agent "knows" — leading to hallucinations, repeated mistakes, and wasted tokens on discovery.

## Solution

Perseus Dashboard connects to any project's Perseus install and shows:
- **Live service health** — CI, databases, APIs, containers
- **Current context snapshot** — what the agent will see right now
- **Token savings analytics** — how many tokens Perseus saved this week
- **Memory recall feed** — what facts the agent remembered from past sessions
- **Drift detection** — what's changed since the agent last looked

## Architecture

```
┌─────────────────────┐
│  Vercel v0 Frontend │  Next.js + shadcn/ui
│  (Dashboard UI)     │
└────────┬────────────┘
         │ REST + WebSocket
┌────────▼────────────┐
│  Perseus API        │  FastAPI + perseus-ctx
│  (Context Engine)   │
└────────┬────────────┘
         │ psycopg2
┌────────▼────────────┐
│  AWS Aurora         │  PostgreSQL (serverless)
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
- This project uses: Vercel v0 (frontend) + AWS Aurora PostgreSQL (backend)
- Track: Open Innovation
- Deadline: June 29, 2026

## License

MIT — see LICENSE file.
