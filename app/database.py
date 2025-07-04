# app/database.py
import os
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel, Session

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set – see .env")

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

def init_db() -> None:
    """Create tables once at startup (no Alembic)."""
    SQLModel.metadata.create_all(engine)

# ─── THIS is the corrected dependency ──────────────────────────────────────
def get_session():
    """
    FastAPI dependency ‒ yields a live Session object.
    FastAPI will handle the generator: open → yield → close.
    """
    session = Session(engine)
    try:
        yield session            # <-- FastAPI injects *this* into your route
    finally:
        session.close()
