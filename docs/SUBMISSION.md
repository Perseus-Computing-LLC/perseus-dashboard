# Perseus Dashboard — H0 Hackathon Submission

## Project Overview

**Name:** Perseus Dashboard
**Tagline:** Source-Labeled Context for AI Coding Agents — inspect what evidence is available.
**Track:** Open Innovation
**Hackathon:** H0: Hack the Zero Stack with Vercel v0 and AWS Databases

## Elevator Pitch (200 chars)

AI coding context goes stale. This prototype defines a source-labeled context and telemetry contract with synthetic fixtures and explicit unavailable states—not live evidence.

## What It Does

Perseus Dashboard prototypes visibility into what their AI coding agents (Claude Code, Cursor, Copilot, Codex) may receive. When an AI agent starts a session, it reads context files (CLAUDE.md, AGENTS.md) that may be out of date. The checked-in build uses repository fixtures and shows:

1. **Synthetic Service Fixture** — the response shape for CI pipelines, databases, APIs, and containers
2. **Source-Labeled Context Snapshot** — what files and facts an evidence collector could provide
3. **Memory Feed** — source-labeled store/recall/decay event shapes
4. **Token Savings Analytics** — explicit unavailable state until paired measured sessions exist

The dashboard eliminates the "what does my agent know?" blind spot that every AI-assisted dev team has.

## How I Built It

### Stack
- **Frontend:** Next.js 14 prototype compatible with **Vercel/v0** — dark-themed dashboard with source labels, service fixture cards, and memory feed timeline
- **Backend:** FastAPI (Python) providing a source-labeled prototype contract for context, service, memory, and analytics
- **Database:** **AWS Aurora PostgreSQL** is the planned production target; this branch uses repository fixtures
- **Context Engine:** Perseus (perseus-ctx) is the planned evidence-producing integration; live workspace resolution is not claimed here

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
AWS Aurora PostgreSQL (Serverless v2) is the intended production database. No live Aurora connection or stored production data is claimed by this branch.

### Vercel v0 Usage
The frontend is a Next.js application compatible with Vercel/v0. It uses:
- App Router for page routing
- Server Components where possible, Client Components for interactivity
- an explicit unavailable state instead of unsupported token-savings visualization
- Tailwind CSS with a custom dark theme matching the GitHub developer aesthetic

## Why Open Innovation Track

Perseus Dashboard doesn't fit neatly into B2C, B2B, or gaming categories. It's a developer tool that creates a new product category: "AI Agent Observability." Every dev team using AI coding assistants needs to know what their agent knows. This is a genuinely new problem that emerged in the last 12 months with the rise of AI coding agents.

The Open Innovation track allows us to test a source-labeled observability contract before connecting live evidence producers through the Vercel v0 + AWS target stack.

## What's Next

1. **Multi-project support** — manage context across an entire GitHub org
2. **Slack/Discord notifications** — alert when a critical service goes down or context goes stale
3. **Drift detection** — compare current context to last session, highlight what changed
4. **Team analytics** — aggregate token savings across the whole team
5. **Agent comparison** — compare how different AI agents (Claude vs Copilot) use context

## Links
- **GitHub:** https://github.com/tcconnally/perseus-dashboard
- **Live Demo:** Not verified by this prototype branch
