# app/db/session.py
from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# SQLite file no projeto:
DATABASE_URL = "sqlite:///./job_tracker.db"

# check_same_thread é necessário porque o SQLite tem restrição de thread
# e o FastAPI pode executar em mais de uma thread durante requests.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency do FastAPI: abre uma sessão por request e garante fechamento.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
