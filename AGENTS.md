# Perseus Dashboard — Project context for AI agents

## Purpose
Perseus Dashboard is a web UI that shows developers what their AI coding agents know about their codebase. Built for H0: Hack the Zero Stack (Vercel v0 + AWS Aurora PostgreSQL).

## Stack
- Frontend: Next.js + shadcn/ui (deployed on Vercel/v0)
- Backend: FastAPI (Python)
- Database: AWS Aurora PostgreSQL
- Context Engine: Perseus (perseus-ctx)

## How to run
```bash
# Backend
cd backend && pip install -r requirements.txt && uvicorn main:app --reload

# Frontend
cd frontend && npm install && npm run dev
```

## Hackathon requirements
- Must use Vercel v0 or Vercel for frontend deployment
- Must use AWS Aurora PostgreSQL, Aurora DSQL, or DynamoDB
- Track: Open Innovation
- Deadline: June 29, 2026
