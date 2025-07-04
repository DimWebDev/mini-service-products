from sqlmodel import select, Session
from .models import Product

def create_product(db: Session, data: Product) -> Product:
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

def list_products(db: Session) -> list[Product]:
    return db.exec(select(Product)).all()

def get_product(db: Session, pid: int) -> Product | None:
    return db.get(Product, pid)

def delete_product(db: Session, pid: int) -> None:
    if prod := db.get(Product, pid):
        db.delete(prod)
        db.commit()
