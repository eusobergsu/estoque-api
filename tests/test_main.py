import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from app.main import app

#teste de criação de itens
@pytest.mark.asyncio
async def test_create_item():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/item_table/", json = {
            "name": "NAME test",
            "description": "item test",
            "price": 100.0,
            "quant": 5
        })
    print("Status code:", response.status_code)  # Debug
    print("Response body:", response.json())  # Debug
    assert response.status_code == 200
    assert response.json()["name"] == "NAME test"

#teste de lista de itens
@pytest.mark.asyncio
async def test_list_itens():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/item_table/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

#Teste de produto inesistente
@pytest.mark.asyncio
async def test_obter_produto_inexistente():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/item_table/999")
    assert response.status_code == 404


