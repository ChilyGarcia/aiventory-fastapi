from fastapi import APIRouter, HTTPException
from src.schemas.usuario import UsuarioIn, UsuarioLogin, UsuarioOut
from src.auth.user_auth import registrar_usuario, login_usuario

router = APIRouter(prefix="/auth", tags=["autenticación"])


@router.post("/register", response_model=UsuarioOut)
async def register(usuario: UsuarioIn):
    return await registrar_usuario(usuario)


@router.post("/login")
async def login(data: UsuarioLogin):
    resultado = await login_usuario(data)
    if not resultado:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return resultado
