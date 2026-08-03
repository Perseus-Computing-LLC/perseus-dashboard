# The Token Tax: How Much Context Discovery Costs Your AI Agent (And How to Eliminate It)

Every AI coding session starts the same way. You open Claude Code or Cursor, ask a question about your project, and the agent spends 3-5 turns just figuring out where it is. It checks what services are running. It reads your config files. It runs `docker ps` and `git status`. By the time it's oriented, you've burned 2,000-5,000 tokens on questions you already knew the answers to.

This is the **Token Tax** — the cold-start discovery cost that every AI-assisted developer pays, every session, forever. And most people don't even realize they're paying it.

## Measuring the Tax

I benchmarked this with a typical mid-size Python project (FastAPI backend, PostgreSQL, Docker Compose, CI pipeline). The agent needed to understand:

- What services are running and their health
- Which config files exist and their contents
- What the project structure looks like
- Any conventions or preferences from previous sessions
- Test status and coverage

**Without pre-resolved context:** agents may need repeated discovery calls before the first useful answer; no universal token count is claimed here.

**With Perseus resolving context before the agent reads it:** the intended workflow is to provide a bounded, source-labeled context before reasoning. Live savings require paired raw session artifacts.

## What Perseus Does

[Perseus](https://github.com/tcconnally/perseus) is a "resolve-before-context" engine. Instead of giving your AI assistant only static instructions, Perseus is designed to resolve workspace state into plain facts *before* the assistant reads it. This repository does not claim a live collector run:

```
Without Perseus:    "Port is 3001 (check .env)"     ← may be stale
With Perseus:       "Port: 3001 | Service: UP"       ← target source-labeled shape
```

It works with any MCP-compatible assistant: Claude Desktop, Cursor, Copilot, Hermes Agent. One `pip install perseus-ctx` and your agent stops rediscovering what hasn't changed.

## The Numbers

```
Cold vs Warm render:      published estimate only (120ms / 15ms)
Token reduction:          unavailable without paired raw sessions
P99 overhead:             unavailable
Gauntlet v2 reliability:  not claimed by this dashboard fixture
```

Any token-savings estimate requires paired before/after sessions with model, provider, run, and artifact provenance.

## Why This Matters Beyond Tokens

Token savings are nice, but the real cost isn't tokens — it's developer attention. Every time your agent asks "let me check what's running" or "let me read your config," you're waiting. Multiply that by 10 sessions a day, across a team of 5 engineers, and you're losing hours a week to orientation that could be pre-resolved.

Perseus aims to reduce orientation work. A connected evidence-producing collector would let an agent start with source-labeled service, config, memory, and convention context.

## Try It

```bash
pip install perseus-ctx
cd your-project
perseus quickstart
```

That's it. Your AI agent just got context-aware. No more cold starts. No more token tax. No more waiting for your agent to figure out what you already know.

---

*Perseus is MIT-licensed, patent pending, and open source at [github.com/tcconnally/perseus](https://github.com/tcconnally/perseus). Read more at [perseus.observer](https://perseus.observer).*

---

*This post is part of the [Proof of Usefulness Hackathon](https://proofofusefulness.com) by HackerNoon — scoring projects on real-world utility, not pitch decks.*
