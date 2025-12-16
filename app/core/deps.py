from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.jwt import SECRET_KEY, ALGORITHM
from app.models.usuario import Usuario
from sqlalchemy import select
from app.database import database


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Correção: usar a tabela diretamente, não o modelo
    query = select(Usuario.__table__).where(Usuario.email == email)
    usuario_record = await database.fetch_one(query)

    if usuario_record is None:
        raise credentials_exception

    # Converter o Record para dict se necessário
    return dict(usuario_record)