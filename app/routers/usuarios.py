from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import insert, select
from app.database import database
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioOut
from app.core.seguranca import gerar_hash_senha, verificar_senha
from app.core.jwt import criar_token_acesso


router = APIRouter(prefix="/usuarios", tags=["Usuários"])


# ===============================
#   CADASTRO DE USUÁRIO
# ===============================
@router.post("/", response_model=UsuarioOut)
async def criar_usuario(usuario: UsuarioCreate):
    senha_hash = gerar_hash_senha(usuario.senha)

    query = insert(Usuario.__table__).values(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=senha_hash  # ← CORRIGI: senha_hsh → senha_hash
    )

    new_id = await database.execute(query)

    return UsuarioOut(
        id=new_id,
        nome=usuario.nome,
        email=usuario.email
    )


# ===============================
#   LOGIN (OAUTH2)
# ===============================
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    query = select(Usuario.__table__).where(
        Usuario.email == form_data.username
    )

    usuario = await database.fetch_one(query)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos"
        )

    if not verificar_senha(form_data.password, usuario["senha_hash"]):  # ← CORRIGI: senha_hsh → senha_hash
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos"
        )

    token = criar_token_acesso({"sub": usuario["email"]})

    return {
        "access_token": token,
        "token_type": "bearer"
    }