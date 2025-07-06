# tests/conftest.py
"""
Put test-only environment variables in effect *before* your application package
is imported and make sure the tables exist for the SQLite test DB.
"""
from pathlib import Path
import os
from dotenv import load_dotenv
import pytest

# ── load `.env.test` ──────────────────────────────────────────────────────────
here = Path(__file__).resolve().parent          # tests/
for dotfile in (here.parent / ".env.test", here / ".env.test"):
    if dotfile.exists():
        load_dotenv(dotfile, override=True)
        break

# flag so code can tell it runs under pytest
os.environ.setdefault("TESTING", "1")

# ── create the schema once for the whole session ─────────────────────────────
from app.database import init_db

@pytest.fixture(scope="session", autouse=True)
def _create_sqlite_schema():
    """Create all tables in the (SQLite) test DB before the first test."""
    init_db()
    yield
