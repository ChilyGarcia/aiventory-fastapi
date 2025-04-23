from fastapi import HTTPException
from src.models.user_model import usuarios
from src.database import database
from src.auth.hashing import hash_password, verify_password
from src.auth.jwt_handler import crear_token


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


async def login_usuario(data_login):
    query = usuarios.select().where(usuarios.c.email == data_login.email)
    user = await database.fetch_one(query)
    if user and verify_password(data_login.password, user["hashed_password"]):
        token = crear_token({"sub": user["email"], "user_id": user["id"]})
        return {"access_token": token, "token_type": "bearer"}
    return None
