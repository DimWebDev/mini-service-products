from sqlmodel import SQLModel, Field

class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: float = Field(gt=0, description="Unit price in EUR")
    description: str | None = Field(default=None, description="Optional description")
    neues_feld: int | None = Field(default=None, description="Beispiel-Feld")

