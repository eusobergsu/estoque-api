from fastapi import APIRouter, HTTPException, Depends
from app.schemas.login import LoginData
from app.core.seguranca import verificar_senha
from app.core.jwt import criar_token_acesso
from sqlalchemy import select, insert
from app.database import database
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioOut
from jose import jwt

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

@router.post("/login")
async def login(dados: LoginData):
    query = select(Usuario).where(Usuario.email == dados.email)
    usuario = await database.fetch_one(query)

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")

    # Verificar senha (depois ajustamos isso, mas fica assim por enquanto)
    if usuario.senha_hash != dados.senha:
        raise HTTPException(status_code=400, detail="Senha incorreta")

    # Criar token JWT
    token = jwt.encode(
        {"sub": usuario.email},
        "SECRET_KEY_AQUI",
        algorithm="HS256"
    )

    return {"access_token": token, "token_type": "bearer"}