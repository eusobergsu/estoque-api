import pytest


@pytest.mark.asyncio
async def test_items_sem_token(client):
    response = await client.get("/item/")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_items_com_token(client):
    login = await client.post(
        "/usuarios/login",
        data={
            "username": "testedasilva@gmail.com",
            "password": "testesenha"
        }
    )

    token = login.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = await client.get("/item/", headers=headers)
    assert response.status_code == 200
