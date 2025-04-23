from fastapi import HTTPException, status
from src.database import database
from src.models.user_model import usuarios
from .hashing import hash_password, verify_password
from .jwt_handler import crear_token
from datetime import datetime

async def registrar_usuario(usuario_data):

    query = usuarios.select().where(usuarios.c.email == usuario_data.email)
    existing_user = await database.fetch_one(query)
    if existing_user:
        raise HTTPException(status_code=400,
                            detail="El email ya está registrado")

    hashed_pw = hash_password(usuario_data.password)
    query = usuarios.insert().values(name=usuario_data.name,
                                     email=usuario_data.email,
                                     hashed_password=hashed_pw,
                                     role_id=2)
    user_id = await database.execute(query)
    return {
        "id": user_id,
        "name": usuario_data.name,
        "email": usuario_data.email
    }


async def login_usuario(credentials):
    query = usuarios.select().where(usuarios.c.email == credentials.email)
    user = await database.fetch_one(query)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    if not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    token, expire = crear_token({"sub": user["email"]})
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_at": expire.isoformat(),

    }
