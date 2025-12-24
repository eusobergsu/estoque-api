import pytest
import asyncio
from httpx import AsyncClient, ASGITransport

# Define ambiente de teste ANTES de importar a app
import os

os.environ["TESTING"] = "1"

from app.main import app
from app.database import database


# Remove o event_loop fixture customizado - deixa o pytest-asyncio gerenciar
# Isso garante que cada teste use o loop correto


@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    """
    Conecta e desconecta o banco para CADA teste.
    Isso garante que a conexão seja feita no event loop correto do teste.
    """
    # Desconecta qualquer conexão anterior
    if database.is_connected:
        await database.disconnect()

    # Conecta no event loop atual do teste
    await database.connect()
    print("✅ Banco conectado")

    yield

    # Desconecta após o teste
    if database.is_connected:
        await database.disconnect()
        print("❌ Banco desconectado")


@pytest.fixture(scope="function")
async def client():
    """Cliente HTTP para cada teste"""
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        yield ac