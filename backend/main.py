"""Perseus Dashboard API -- FastAPI backend for H0 Hackathon."""
from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

app = FastAPI(title="Perseus Dashboard API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ServiceStatus(BaseModel):
    name: str
    status: str
    latency_ms: Optional[float] = None

MOCK_SERVICES = [
    {"name": "CI (GitHub Actions)", "status": "up", "latency_ms": 234},
    {"name": "PostgreSQL (Aurora)", "status": "up", "latency_ms": 12},
    {"name": "Redis Cache", "status": "up", "latency_ms": 3},
    {"name": "API Gateway", "status": "up", "latency_ms": 45},
    {"name": "Docker Registry", "status": "up", "latency_ms": 89},
    {"name": "Sentry (Error Tracking)", "status": "up", "latency_ms": 156},
]

def now_iso():
    return datetime.now(timezone.utc).isoformat()

@app.get("/api/health")
def health():
    return {"status": "ok", "now": now_iso()}

@app.get("/api/ping")
def ping():
    return {"pong": True, "now": now_iso()}

@app.get("/api/projects")
def list_projects():
    return [{"id": 1, "name": "perseus-dashboard", "now": now_iso()}]

@app.get("/api/projects/{project_id}")
def get_project(project_id: int):
    return {"id": project_id, "name": "perseus-dashboard", "now": now_iso()}

@app.get("/api/projects/{project_id}/services", response_model=list[ServiceStatus])
def get_services(project_id: int):
    return [ServiceStatus(**s) for s in MOCK_SERVICES]

@app.get("/api/projects/{project_id}/context")
def get_context(project_id: int):
    return {"project_id": project_id, "now": now_iso(), "services": MOCK_SERVICES, "files": ["AGENTS.md"]}

@app.get("/api/projects/{project_id}/memories")
def get_memories(project_id: int, limit: int = 50):
    return [{"id": 1, "event_type": "store", "now": now_iso()}]

@app.get("/api/projects/{project_id}/analytics/summary")
def get_analytics_summary(project_id: int):
    return {"project_id": project_id, "total_saved": 12847, "now": now_iso()}
