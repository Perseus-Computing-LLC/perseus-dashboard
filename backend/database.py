import os
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, JSON, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timezone

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/perseus_dashboard"
)

engine = create_engine(DATABASE_URL, pool_size=5, max_overflow=10)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Models ---

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    github_url = Column(String(512), nullable=False)
    name = Column(String(256), nullable=False)
    perseus_config = Column(JSON, default=dict)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_context_at = Column(DateTime, nullable=True)

    context_snapshots = relationship("ContextSnapshot", back_populates="project")
    memory_events = relationship("MemoryEvent", back_populates="project")
    token_analytics = relationship("TokenAnalytics", back_populates="project")


class ContextSnapshot(Base):
    __tablename__ = "context_snapshots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    content = Column(JSON, nullable=False)
    resolved_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    file_count = Column(Integer, default=0)
    token_estimate = Column(Integer, default=0)

    project = relationship("Project", back_populates="context_snapshots")


class MemoryEvent(Base):
    __tablename__ = "memory_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    event_type = Column(String(32), nullable=False)  # store, recall, decay, insight
    fact_key = Column(String(512), nullable=True)
    fact_value = Column(Text, nullable=True)
    confidence = Column(Float, default=0.8)
    session_id = Column(String(128), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    project = relationship("Project", back_populates="memory_events")


class TokenAnalytics(Base):
    __tablename__ = "token_analytics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    session_id = Column(String(128), nullable=True)
    tokens_saved = Column(Integer, default=0)
    tokens_total = Column(Integer, default=0)
    recorded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    project = relationship("Project", back_populates="token_analytics")


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
