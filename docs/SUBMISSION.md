# Perseus Dashboard — H0 Hackathon Submission

## Project Overview

**Name:** Perseus Dashboard
**Tagline:** Live Context for AI Coding Agents — see exactly what your AI knows about your codebase.
**Track:** Open Innovation
**Hackathon:** H0: Hack the Zero Stack with Vercel v0 and AWS Databases

## Elevator Pitch (200 chars)

Your AI agent's context goes stale within hours. Perseus Dashboard shows you exactly what your agent knows — live service health, context snapshots, memory feed, and token savings. Built on Vercel v0 + AWS Aurora PostgreSQL.

## What It Does

Perseus Dashboard gives developer teams real-time visibility into what their AI coding agents (Claude Code, Cursor, Copilot, Codex) "know" about their codebase. When an AI agent starts a session, it reads context files (CLAUDE.md, AGENTS.md) that are already hours or days out of date. Perseus Dashboard connects directly to the Perseus context engine and shows:

1. **Live Service Health** — CI pipelines, databases, APIs, and containers — are they up or down right now?
2. **Current Context Snapshot** — what files and facts will the agent see when it starts its next session?
3. **Memory Feed** — what facts did the agent store, recall, and let decay across sessions?
4. **Token Savings Analytics** — how many tokens did Perseus save by pre-resolving workspace state?

The dashboard eliminates the "what does my agent know?" blind spot that every AI-assisted dev team has.

## How I Built It

### Stack
- **Frontend:** Next.js 14 deployed on **Vercel v0** — dark-themed dashboard with real-time data visualization (Recharts), responsive service health cards, and memory feed timeline
- **Backend:** FastAPI (Python) providing REST endpoints for context resolution, service health, memory events, and token analytics
- **Database:** **AWS Aurora PostgreSQL** — stores projects, context snapshots, memory events, and token analytics with full relational schema
- **Context Engine:** Perseus (perseus-ctx) — resolves live workspace state before the agent sees it, eliminating cold-start discovery

### Architecture
```
Vercel v0 Frontend (Next.js + Tailwind)
    ↓ REST API + polling
FastAPI Backend (Python)
    ↓ psycopg2 + SQLAlchemy
AWS Aurora PostgreSQL
    ↑ reads/writes
Perseus Context Engine (CLI/lib)
```

### Database Schema (Aurora PostgreSQL)
- `projects` — GitHub URL, name, Perseus config
- `context_snapshots` — JSONB content, file count, token estimate, timestamp
- `memory_events` — store/recall/decay/insight events with confidence scores
- `token_analytics` — tokens saved per session, timestamped

### AWS Aurora Proof
The database runs on AWS Aurora PostgreSQL (Serverless v2). All project data, context snapshots, memory events, and analytics are stored in Aurora tables with proper foreign key relationships, indexing, and connection pooling.

### Vercel v0 Usage
The frontend is a Next.js application generated and deployed on Vercel. It uses:
- App Router for page routing
- Server Components where possible, Client Components for interactivity
- Recharts for token savings visualization
- Tailwind CSS with a custom dark theme matching the GitHub developer aesthetic

## Why Open Innovation Track

Perseus Dashboard doesn't fit neatly into B2C, B2B, or gaming categories. It's a developer tool that creates a new product category: "AI Agent Observability." Every dev team using AI coding assistants needs to know what their agent knows. This is a genuinely new problem that emerged in the last 12 months with the rise of AI coding agents.

The Open Innovation track allows us to submit something that pushes the boundaries of what's possible with the Vercel v0 + AWS stack — building a real-time observability layer for the AI-assisted development workflow.

## What's Next

1. **Multi-project support** — manage context across an entire GitHub org
2. **Slack/Discord notifications** — alert when a critical service goes down or context goes stale
3. **Drift detection** — compare current context to last session, highlight what changed
4. **Team analytics** — aggregate token savings across the whole team
5. **Agent comparison** — compare how different AI agents (Claude vs Copilot) use context

## Links
- **GitHub:** https://github.com/tcconnally/perseus-dashboard
- **Live Demo:** https://perseus-dashboard.vercel.app
