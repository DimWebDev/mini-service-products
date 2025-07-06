# tests/test_products.py

import pytest
# TestClient lets us simulate HTTP requests against our FastAPI app
from fastapi.testclient import TestClient
# We need raw SQL execution to clear tables between tests
from sqlalchemy import text

# Import our FastAPI application and the database engine
from app.main import app
from app.database import engine

# Create a TestClient instance for the entire module to reuse
client = TestClient(app)


@pytest.fixture(autouse=True, scope="function")
def _clean_table():
    """
    Pytest fixture that runs before each test function (autouse=True).
    It ensures the `product` table is empty, whether we're on SQLite or Postgres.
    """
    # Open a direct connection to the test database
    with engine.connect() as conn:
        # Branch by dialect name
        if engine.dialect.name == "sqlite":
            # SQLite: deleting rows is enough, ROWID auto-increment
            conn.execute(text("DELETE FROM product"))
        else:
            # Postgres (and similar): TRUNCATE resets identity as well
            conn.execute(text("TRUNCATE TABLE product RESTART IDENTITY"))
        # Make sure changes are committed
        conn.commit()
    # Yield back to the test; after the test, connection is closed automatically
    yield


def test_create_then_list():
    """
    1. POST a new product
    2. Verify we get HTTP 201 and correct payload
    3. GET the list of products and verify exactly one item
    """
    # Define request payload
    data = {"name": "Book", "price": 9.99}

    # 1) Create the product
    r = client.post("/products", json=data)
    # Assert we got "Created"
    assert r.status_code == 201

    # Parse JSON response
    product = r.json()
    # Check that name matches
    assert product["name"] == "Book"
    # First product should have id=1 since our table was empty
    assert product["id"] == 1

    # 2) List all products
    r2 = client.get("/products")
    # Assert OK
    assert r2.status_code == 200
    # Body should be a list of length exactly one
    assert len(r2.json()) == 1
