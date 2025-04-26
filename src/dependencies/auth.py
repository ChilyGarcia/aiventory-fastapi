from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.auth.jwt_handler import verificar_token
from src.database import database
from src.models.user_model import usuarios
from src.auth.token_blacklist import is_blacklisted
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_usuario_actual(token: str = Depends(oauth2_scheme)):
    """
    Dependency para obtener el usuario actual basado en el token JWT.
    Verifica que el token no esté en la blacklist antes de cualquier otra validación.
    """
    logger.info("Verificando token en get_usuario_actual")

    # Primero verificar si el token está en la blacklist
    if is_blacklisted(token):
        logger.warning("Token encontrado en blacklist")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o sesión cerrada",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Luego verificar si el token es válido
    payload = verificar_token(token)
    if payload is None:
        logger.warning("Token inválido o expirado")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar las credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Finalmente, obtener el usuario
    query = usuarios.select().where(usuarios.c.email == payload.get("sub"))
    user = await database.fetch_one(query)

    if user is None:
        logger.warning(f"Usuario no encontrado para el email: {payload.get('sub')}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
