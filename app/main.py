from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Stock API up and running!"}

from fastapi import FastAPI, HTTPException
from typing import List
from app.database import Item

app = FastAPI()

# Banco de dados temporário na memória
banco_de_itens: List[Item] = []

#Criar produto
@app.post("/item/", response_model=Item)
def criar_produto(item: Item):
    item.id = len(banco_de_itens) + 1
    banco_de_itens.append(item)
    return item

#Listar produtos
@app.get("/item/", response_model=List[Item])
def listar_itens():
    return banco_de_itens

#Obter produto por um ID
@app.get("/item/{item_id}", response_model=Item)
def obter_item(item_id: int):
    for item in banco_de_itens:
        if item.id == item_id:
            return produto
    raise HTTPException(status_code=404, detail="Produto não encontrado")

#Atualizar produto

@app.put("/item/{item_id}", response_model=Item)
def atualizar_item(item_id: int, item_atualizado: Item):
    for index, item in enumerate(banco_de_itens):
        if item.id == item_id:
            item_atualizado.id = item_id
            banco_de_itens[index] = item_atualizado
            return item_atualizado
    raise HTTPException(status_code=404, detail="Produto não encontrado")

#Remover um produto
@app.delete("/item/{item_id}", response_model=Item)
def deletar_item(item_id: int):
    for index, item in enumerate(banco_de_itens):
        if item.id == item_id:
            banco_de_itens.pop(index)
            return {"detail": "Produto removido com sucesso"}
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
