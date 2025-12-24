import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import os
from fastapi import FastAPI
from app.database import database
from app.routers import usuarios, itens


app = FastAPI()


# ===============================
#   REGISTRO DE ROUTERS
# ===============================
app.include_router(usuarios.router)
app.include_router(itens.router)


# ===============================
#   EVENTOS (Apenas para produção)
# ===============================
if os.getenv("TESTING") != "1":
    @app.on_event("startup")
    async def startup():
        await database.connect()
        print("✅ Banco de dados conectado")

    @app.on_event("shutdown")
    async def shutdown():
        await database.disconnect()
        print("❌ Banco de dados desconectado")


# ===============================
#   ROTA PÚBLICA
# ===============================
@app.get("/")
def root():
    return {"message": "API de Estoque funcionando!"}