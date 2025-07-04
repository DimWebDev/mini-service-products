import os, time, uuid, subprocess, textwrap
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(autouse=True, scope="function")
def _clean_table():
    """Truncate table between tests to keep state isolated."""
    from sqlalchemy import text
    from app.database import engine
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE product RESTART IDENTITY"))
        conn.commit()
    yield

def test_create_then_list():
    data = {"name": "Book", "price": 9.99}
    r = client.post("/products", json=data)
    assert r.status_code == 201
    product = r.json()
    assert product["name"] == "Book"
    assert product["id"] == 1

    r2 = client.get("/products")
    assert r2.status_code == 200
    assert len(r2.json()) == 1
