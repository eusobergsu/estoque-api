import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI
from app.database import database
from app.routers import usuarios,itens


app = FastAPI()

# ===============================
#   REGISTRO DE ROUTERS
# ===============================
app.include_router(usuarios.router)
app.include_router(itens.router)


# ===============================
#   CICLO DE VIDA
# ===============================
@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# ===============================
#   ROTA PÚBLICA
# ===============================
@app.get("/")
def root():
    return {"message": "API de Estoque funcionando!"}
