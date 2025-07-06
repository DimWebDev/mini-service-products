# app/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session

from .database import get_session, init_db
from .models import Product
from . import crud


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs once at startup, then once at shutdown.

    We create all tables before the first request, mirroring the
    old @app.on_event("startup") behaviour.
    """
    init_db()          # ↞ old startup hook
    yield              # ----- application runs here -----
    # (optional) add shutdown logic after yield


app = FastAPI(
    title="Mini-Service Products",
    version="0.1.0",
    docs_url="/docs",
    lifespan=lifespan,   # ↞ new!
)

# ─────────────────────────── Routes ─────────────────────────────────────────


@app.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(prod: Product, db: Session = Depends(get_session)):
    return crud.create_product(db, prod)


@app.get("/products", response_model=list[Product])
def read_products(db: Session = Depends(get_session)):
    return crud.list_products(db)


@app.delete("/products/{pid}", status_code=status.HTTP_204_NO_CONTENT)
def remove_product(pid: int, db: Session = Depends(get_session)):
    if crud.get_product(db, pid) is None:
        raise HTTPException(status_code=404, detail="Product not found")
    crud.delete_product(db, pid)
