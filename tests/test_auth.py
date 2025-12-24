import pytest


@pytest.mark.asyncio
async def test_login_valido(client):
    response = await client.post(
        "/usuarios/login",
        data={
            "username": "testedasilva@gmail.com",
            "password": "testesenha"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_invalido(client):
    response = await client.post(
        "/usuarios/login",
        data={
            "username": "testedasilva@gmail.com",
            "password": "senha_errada"
        }
    )

    assert response.status_code == 401
