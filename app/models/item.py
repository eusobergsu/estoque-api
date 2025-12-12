from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Float
from app.database import Base

# Modelo ORM (SQLAlchemy)
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(String(250))
    price = Column(Float)
    quant = Column(Integer)

# Modelo de entrada/saída (Pydantic)
class ItemModel(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    quant: int

    class Config:
        orm_mode = True
