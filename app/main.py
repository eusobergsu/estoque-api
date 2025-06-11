from fastapi import FastAPI, HTTPException
from typing import List
from app.database import database, engine
from app import models
from app.models import ItemModel
from sqlalchemy import select, insert, update, delete
from app.models import It
import os
from dotenv import load_dotenv

# Criação das tabelas no banco
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

if os.getenv("RAILWAY_ENVIRONMENT") is None:
    load_dotenv()


@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
def read_root():
    return {"message": "API de Estoque funcionando!"}

# Criar produto
@app.post("/item/", response_model=ItemModel)
async def criar_item(item: ItemModel):
    query = insert(Item).values(
        name=item.name,
        description=item.description,
        price=item.price,
        quant=item.quant
    )
    last_record_id = await database.execute(query)
    return {**item.dict(), "id": last_record_id}

# Listar produtos
@app.get("/item/", response_model=List[ItemModel])
async def listar_itens():
    query = select(Item)
    rows = await database.fetch_all(query)
    return rows

# Obter produto por ID
@app.get("/item/{item_id}", response_model=ItemModel)
async def obter_item(item_id: int):
    query = select(Item).where(Item.id == item_id)
    item = await database.fetch_one(query)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Atualizar produto
@app.put("/item/{item_id}", response_model=ItemModel)
async def atualizar_item(item_id: int, item: ItemModel):
    query = update(Item).where(Item.id == item_id).values(
        name=item.name,
        description=item.description,
        price=item.price,
        quant=item.quant,
    )
    await database.execute(query)
    return {**item.dict(), "id": item_id}

# Deletar produto
@app.delete("/item/{item_id}")
async def deletar_item(item_id: int):
    query = delete(Item).where(Item.id == item_id)
    await database.execute(query)
    return {"detail": f"Item {item_id} deleted"}
