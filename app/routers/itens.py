from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.database import database
from app.models.item import Item, ItemModel
from app.core.deps import get_current_user

router = APIRouter(
    prefix="/item",
    tags=["items"]
)

# ===============================
#   ROTAS PROTEGIDAS — ITEMS   ||
# ===============================

@router.post("/", response_model=ItemModel)
async def criar_item(
    item: ItemModel,
    current_user=Depends(get_current_user)
):
    query = Item.__table__.insert().values(
        name=item.name,
        description=item.description,
        price=item.price,
        quant=item.quant
    )
    new_id = await database.execute(query)
    return {**item.dict(), "id": new_id}


@router.get("/", response_model=List[ItemModel])
async def listar_itens(
    current_user=Depends(get_current_user)
):
    query = Item.__table__.select()
    rows = await database.fetch_all(query)
    return rows


@router.get("/{item_id}", response_model=ItemModel)
async def obter_item(
    item_id: int,
    current_user=Depends(get_current_user)
):
    query = Item.__table__.select().where(Item.id == item_id)
    item = await database.fetch_one(query)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return item


@router.put("/{item_id}", response_model=ItemModel)
async def atualizar_item(
    item_id: int,
    item: ItemModel,
    current_user=Depends(get_current_user)
):
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


@router.delete("/{item_id}")
async def deletar_item(
    item_id: int,
    current_user=Depends(get_current_user)
):
    query = Item.__table__.delete().where(Item.id == item_id)
    await database.execute(query)
    return {"detail": f"Item {item_id} deletado"}
