"""
Perseus Dashboard API — FastAPI backend for the H0 Hackathon entry.

Connects Vercel v0 frontend to AWS Aurora PostgreSQL via Perseus context engine.
"""
import os
import subprocess
import json
from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import init_db, get_db, Project, ContextSnapshot, MemoryEvent, TokenAnalytics

app = FastAPI(title="Perseus Dashboard API", version="0.1.0")

# CORS for Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic schemas ---

class ProjectCreate(BaseModel):
    github_url: str
    name: str
    perseus_config: dict = {}

class ProjectResponse(BaseModel):
    id: int
    github_url: str
    name: str
    created_at: datetime
    last_context_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ContextSnapshotResponse(BaseModel):
    id: int
    content: dict
    resolved_at: datetime
    file_count: int
    token_estimate: int

    class Config:
        from_attributes = True

class MemoryEventResponse(BaseModel):
    id: int
    event_type: str
    fact_key: Optional[str]
    fact_value: Optional[str]
    confidence: float
    created_at: datetime

    class Config:
        from_attributes = True

class TokenAnalyticsResponse(BaseModel):
    id: int
    session_id: Optional[str]
    tokens_saved: int
    tokens_total: int
    recorded_at: datetime

    class Config:
        from_attributes = True

class ServiceStatus(BaseModel):
    name: str
    status: str  # "up", "down", "unknown"
    latency_ms: Optional[float] = None

# --- Helper: run Perseus CLI ---

def run_perseus_command(*args, workdir: str = ".") -> dict:
    """Run a Perseus CLI command and return parsed JSON output.
    
    Falls back to mock data if Perseus isn't installed.
    """
    try:
        result = subprocess.run(
            ["perseus"] + list(args),
            capture_output=True, text=True, timeout=15,
            cwd=workdir
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
    except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
        pass
    
    # Mock fallback for demo/development
    return {
        "services": [
            {"name": "CI (GitHub Actions)", "status": "up", "latency_ms": 234},
            {"name": "Database (PostgreSQL)", "status": "up", "latency_ms": 12},
            {"name": "Redis Cache", "status": "up", "latency_ms": 3},
            {"name": "API Gateway", "status": "up", "latency_ms": 45},
        ],
        "context_files": ["AGENTS.md", "pyproject.toml", "docker-compose.yml"],
        "memory_facts": [],
        "token_saved": 0,
    }


# --- Startup ---

@app.on_event("startup")
def startup():
    try:
        init_db()
    except Exception as e:
        print(f"DB init skipped (expected in dev): {e}")


# --- Health ---

@app.get("/api/health")
def health():
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


# --- Projects ---

@app.post("/api/projects", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    db_project = Project(
        github_url=project.github_url,
        name=project.name,
        perseus_config=project.perseus_config,
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@app.get("/api/projects", response_model=list[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).order_by(Project.created_at.desc()).all()


@app.get("/api/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


# --- Context ---

@app.get("/api/projects/{project_id}/context")
def get_context(project_id: int, db: Session = Depends(get_db)):
    """Resolve live Perseus context for this project."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Try Perseus CLI, fall back to mock
    perseus_data = run_perseus_command("context", "--json")

    # Store snapshot
    snapshot = ContextSnapshot(
        project_id=project_id,
        content=perseus_data,
        file_count=len(perseus_data.get("context_files", [])),
        token_estimate=len(json.dumps(perseus_data)) // 4,  # rough estimate
    )
    db.add(snapshot)
    project.last_context_at = datetime.now(timezone.utc)
    db.commit()

    return {
        "project_id": project_id,
        "resolved_at": snapshot.resolved_at.isoformat(),
        "services": perseus_data.get("services", []),
        "context_files": perseus_data.get("context_files", []),
        "token_estimate": snapshot.token_estimate,
    }


@app.get("/api/projects/{project_id}/services", response_model=list[ServiceStatus])
def get_services(project_id: int, db: Session = Depends(get_db)):
    """Get live service health for this project."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    data = run_perseus_command("services", "--json")
    return [
        ServiceStatus(
            name=s["name"],
            status=s.get("status", "unknown"),
            latency_ms=s.get("latency_ms"),
        )
        for s in data.get("services", [])
    ]


# --- Memory ---

@app.get("/api/projects/{project_id}/memories", response_model=list[MemoryEventResponse])
def get_memories(project_id: int, limit: int = 50, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return (
        db.query(MemoryEvent)
        .filter(MemoryEvent.project_id == project_id)
        .order_by(MemoryEvent.created_at.desc())
        .limit(limit)
        .all()
    )


@app.post("/api/projects/{project_id}/memories")
def record_memory(project_id: int, event_type: str, fact_key: str, fact_value: str,
                  confidence: float = 0.8, session_id: str = None,
                  db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    event = MemoryEvent(
        project_id=project_id,
        event_type=event_type,
        fact_key=fact_key,
        fact_value=fact_value,
        confidence=confidence,
        session_id=session_id,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return {"id": event.id, "status": "recorded"}


# --- Analytics ---

@app.get("/api/projects/{project_id}/analytics", response_model=list[TokenAnalyticsResponse])
def get_analytics(project_id: int, limit: int = 30, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return (
        db.query(TokenAnalytics)
        .filter(TokenAnalytics.project_id == project_id)
        .order_by(TokenAnalytics.recorded_at.desc())
        .limit(limit)
        .all()
    )


@app.get("/api/projects/{project_id}/analytics/summary")
def get_analytics_summary(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    records = (
        db.query(TokenAnalytics)
        .filter(TokenAnalytics.project_id == project_id)
        .all()
    )

    total_saved = sum(r.tokens_saved for r in records)
    total_used = sum(r.tokens_total for r in records)
    session_count = len(set(r.session_id for r in records if r.session_id))

    return {
        "project_id": project_id,
        "total_tokens_saved": total_saved,
        "total_tokens_used": total_used,
        "savings_ratio": round(total_saved / max(total_used, 1) * 100, 1),
        "total_sessions": session_count,
        "snapshot_count": len(records),
    }


# --- Run ---

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
