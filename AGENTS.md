# Perseus Dashboard — Project context for AI agents

## Purpose
Perseus Dashboard is a source-labeled web UI prototype for showing what evidence AI coding agents may receive. Built for H0: Hack the Zero Stack; Vercel v0 + AWS Aurora PostgreSQL are target integrations.

## Stack
- Frontend: Next.js + shadcn/ui (compatible with Vercel/v0; deployment unverified)
- Backend: FastAPI (Python)
- Database: AWS Aurora PostgreSQL (planned target; fixture backend currently)
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
