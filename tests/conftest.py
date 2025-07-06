# tests/conftest.py

"""
Put test-only environment variables in effect *before* your application package
is imported and make sure the tables exist for the SQLite test DB.
"""

# We need to manipulate file paths
from pathlib import Path
# We need to set environment variables
import os
# To load .env files
from dotenv import load_dotenv
# Pytest is used for fixtures
import pytest

# ────────────────────────────────────────────────────────────────────────────────
# Step 1: Locate and load our `.env.test` file so that pytest runs against SQLite
# ────────────────────────────────────────────────────────────────────────────────

# Identify this file's directory: tests/
here = Path(__file__).resolve().parent

# We will look for `.env.test` first at the repo root, then inside tests/
for dotfile in (
        here.parent / ".env.test",  # ../.env.test (repo-root/.env.test)
        here / ".env.test",         # tests/.env.test
):
    if dotfile.exists():
        # Load its key/value pairs into os.environ, overriding any existing ones
        load_dotenv(dotfile, override=True)
        break  # stop after the first match

# Mark that we are in a testing context; optional but handy if your code
# needs to branch behavior under tests. E.g. skip certain startup hooks.
os.environ.setdefault("TESTING", "1")


# ────────────────────────────────────────────────────────────────────────────────
# Step 2: Ensure that our test database actually has tables before any tests run
# ────────────────────────────────────────────────────────────────────────────────

# We import and call our application’s `init_db` helper, which creates
# all SQLModel tables on the bound engine (now pointed at SQLite via .env.test).
from app.database import init_db

@pytest.fixture(scope="session", autouse=True)
def _create_sqlite_schema():
    """
    Pytest session-scoped fixture that runs exactly once before any tests.

    It invokes `init_db()`, which:
      - Reads DATABASE_URL (now SQLite from .env.test)
      - Calls SQLModel.metadata.create_all(engine)
    so all tables (including `product`) exist in the test database.
    """
    init_db()   # Create all tables
    yield       # Let the test session proceed
    # (no teardown needed; the SQLite file can be left or removed manually)
