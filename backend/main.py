"""Perseus Dashboard API -- FastAPI backend for H0 Hackathon. Mock data mode."""
from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Perseus Dashboard API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Schemas ---

class ProjectCreate(BaseModel):
    github_url: str
    name: str
    perseus_config: dict = {}

class ServiceStatus(BaseModel):
    name: str
    status: str
    latency_ms: Optional[float] = None

# --- Mock data ---

MOCK_SERVICES = [
    {"name": "CI (GitHub Actions)", "status": "up", "latency_ms": 234},
    {"name": "PostgreSQL (Aurora)", "status": "up", "latency_ms": 12},
    {"name": "Redis Cache", "status": "up", "latency_ms": 3},
    {"name": "API Gateway", "status": "up", "latency_ms": 45},
    {"name": "Docker Registry", "status": "up", "latency_ms": 89},
    {"name": "Sentry (Error Tracking)", "status": "up", "latency_ms": 156},
]

MOCK_MEMORIES = [
    {"id": 1, "event_type": "store", "fact_key": "database.postgres_version", "fact_value": "PostgreSQL 16.3 on Aurora", "confidence": 0.95, "created_at": datetime.now(timezone.utc)},
    {"id": 2, "event_type": "recall", "fact_key": "convention.python_formatter", "fact_value": "black --line-length 88", "confidence": 0.92, "created_at": datetime.now(timezone.utc)},
    {"id": 3, "event_type": "insight", "fact_key": "pattern.api_structure", "fact_value": "FastAPI routes follow /api/resource/{id}/action", "confidence": 0.88, "created_at": datetime.now(timezone.utc)},
    {"id": 4, "event_type": "store", "fact_key": "config.ci_provider", "fact_value": "GitHub Actions with matrix build", "confidence": 0.90, "created_at": datetime.now(timezone.utc)},
    {"id": 5, "event_type": "decay", "fact_key": "preference.old_editor", "fact_value": "vscode (switched to cursor)", "confidence": 0.15, "created_at": datetime.now(timezone.utc)},
]

MOCK_ANALYTICS = [
    {"id": i, "session_id": f"session-{i}", "tokens_saved": s, "tokens_total": u, "recorded_at": datetime.now(timezone.utc)}
    for i, (s, u) in enumerate([(2100, 8500), (1800, 7200), (2400, 9100), (3100, 10400), (1950, 7800)], start=1)
]

# --- Routes ---

@app.get("/api/health")
def health():
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.get("/api/ping")
def ping():
    return {"pong": True}


@app.get("/api/projects")
def list_projects():
    return [{"id": 1, "github_url": "https://github.com/tcconnally/perseus-dashboard", "name": "perseus-dashboard", "created_at": datetime.now(timezone.utc), "last_context_at": None}]


@app.get("/api/projects/{project_id}")
def get_project(project_id: int):
    return {"id": 1, "github_url": "https://github.com/tcconnally/perseus-dashboard", "name": "perseus-dashboard", "created_at": datetime.now(timezone.utc), "last_context_at": None}


@app.get("/api/projects/{project_id}/context")
def get_context(project_id: int):
    return {
        "project_id": project_id,
        "resolved_at": datetime.now(timezone.utc).isoformat(),
        "services": MOCK_SERVICES,
        "context_files": ["AGENTS.md", "pyproject.toml", "docker-compose.yml", "Makefile"],
        "token_estimate": 847,
    }


@app.get("/api/projects/{project_id}/services", response_model=list[ServiceStatus])
def get_services(project_id: int):
    return [ServiceStatus(name=s["name"], status=s["status"], latency_ms=s.get("latency_ms")) for s in MOCK_SERVICES]


@app.get("/api/projects/{project_id}/memories")
def get_memories(project_id: int, limit: int = 50):
    return MOCK_MEMORIES[:limit]


@app.get("/api/projects/{project_id}/analytics/summary")
def get_analytics_summary(project_id: int):
    total_saved = sum(r["tokens_saved"] for r in MOCK_ANALYTICS)
    total_used = sum(r["tokens_total"] for r in MOCK_ANALYTICS)
    return {
        "project_id": project_id,
        "total_tokens_saved": total_saved,
        "total_tokens_used": total_used,
        "savings_ratio": round(total_saved / max(total_used, 1) * 100, 1),
        "total_sessions": len(MOCK_ANALYTICS),
        "snapshot_count": len(MOCK_ANALYTICS),
    }
