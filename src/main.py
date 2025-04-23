import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from database import database, engine, metadata
from src.models.user_model import usuarios
from src.schemas.user_schema import Usuario, UsuarioIn

app = FastAPI()
metadata.create_all(engine)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/usuarios/", response_model=Usuario)
async def crear_usuario(usuario: UsuarioIn):
    query = usuarios.insert().values(nombre=usuario.nombre,
                                     email=usuario.email)
    usuario_id = await database.execute(query)
    return {**usuario.dict(), "id": usuario_id}


@app.get("/usuarios/", response_model=list[Usuario])
async def obtener_usuarios():
    query = usuarios.select()
    return await database.fetch_all(query)
