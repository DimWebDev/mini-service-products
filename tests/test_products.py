# tests/test_products.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.main import app
from app.database import engine

client = TestClient(app)


@pytest.fixture(autouse=True, scope="function")
def _clean_table():
    """Clear the product table between tests, whatever the DB."""
    with engine.connect() as conn:
        if engine.dialect.name == "sqlite":
            # SQLite: just delete rows; sequence auto-resets with ROWID tables
            conn.execute(text("DELETE FROM product"))
        else:
            # Postgres (and other dialects that support it)
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
