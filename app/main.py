import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
from fastapi import FastAPI, HTTPException
from typing import List
from sqlalchemy import select
from app.database import Base, engine, database
from app.models.item import Item, ItemModel
from app.routers import usuarios

app = FastAPI()
app.include_router(usuarios.router)


# ✓ conectar banco
@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    app.include_router(usuarios.router)


@app.get("/")
def root():
    return {"message": "API de Estoque funcionando!"}


# ===============================
#   ROTAS — VERSÃO CORRETA
# ===============================

# Criar item
@app.post("/item/", response_model=ItemModel)
async def criar_item(item: ItemModel):
    query = Item.__table__.insert().values(
        name=item.name,
        description=item.description,
        price=item.price,
        quant=item.quant
    )
    new_id = await database.execute(query)
    return {**item.dict(), "id": new_id}


# Listar itens
@app.get("/item/", response_model=List[ItemModel])
async def listar_itens():
    query = Item.__table__.select()
    rows = await database.fetch_all(query)
    return rows


# Buscar item por ID
@app.get("/item/{item_id}", response_model=ItemModel)
async def obter_item(item_id: int):
    query = Item.__table__.select().where(Item.id == item_id)
    item = await database.fetch_one(query)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return item


# Atualizar item
@app.put("/item/{item_id}", response_model=ItemModel)
async def atualizar_item(item_id: int, item: ItemModel):
    query = (
        Item.__table__.update()
        .where(Item.id == item_id)
        .values(
            name=item.name,
            description=item.description,
            price=item.price,
            quant=item.quant,
        )
    )
    await database.execute(query)
    return {**item.dict(), "id": item_id}


# Deletar item
@app.delete("/item/{item_id}")
async def deletar_item(item_id: int):
    query = Item.__table__.delete().where(Item.id == item_id)
    await database.execute(query)
    return {"detail": f"Item {item_id} deletado"}
