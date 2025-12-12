from fastapi import APIRouter, HTTPException
from sqlalchemy import select, insert
from app.database import database
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioOut

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("/", response_model=UsuarioOut)
async def criar_usuario(usuario: UsuarioCreate):
    async with database.transaction():
        query = insert(Usuario).values(
            nome=usuario.nome,
            email=usuario.email,
            senha=usuario.senha,
            senha_hash=usuario.senha
        )
        new_id = await database.execute(query)
        return UsuarioOut(id=new_id, nome=usuario.nome, email=usuario.email)