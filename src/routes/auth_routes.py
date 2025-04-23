from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.auth.user_auth import registrar_usuario, login_usuario
from src.schemas.usuario import UsuarioIn, UsuarioOut, UsuarioLogin
from src.dependencies.auth import get_usuario_actual
from src.auth.token_blacklist import add_to_blacklist, is_blacklisted
from src.auth.jwt_handler import SECRET_KEY, ALGORITHM
from jose import jwt
from datetime import datetime, timezone
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["autenticación"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/register", response_model=UsuarioOut)
async def register(usuario: UsuarioIn):
    return await registrar_usuario(usuario)


@router.post("/login")
async def login(data: UsuarioLogin):
    resultado = await login_usuario(data)
    if not resultado:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return resultado


@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    try:
        logger.info("Intentando cerrar sesión")
        
        # Verificar si el token ya está en la blacklist
        if is_blacklisted(token):
            logger.warning("Intento de logout con token ya en blacklist")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="La sesión ya ha sido cerrada anteriormente"
            )

        # Verificar que el token sea válido antes de agregarlo a la blacklist
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp_timestamp = payload["exp"]
        exp = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        now = datetime.now(timezone.utc)
        
        logger.info(f"Tiempo de expiración del token: {exp}")
        logger.info(f"Tiempo actual: {now}")
        
        # Si el token ya expiró, no es necesario agregarlo a la blacklist
        if exp < now:
            logger.warning(f"Token expirado. Expira en: {exp}, Hora actual: {now}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="El token ya ha expirado"
            )
        
        # Agregar el token a la blacklist
        logger.info("Agregando token a la blacklist")
        add_to_blacklist(token, exp)
        
        return {"message": "Sesión cerrada exitosamente"}
    except jwt.JWTError as e:
        logger.error(f"Error al decodificar token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    except Exception as e:
        logger.error(f"Error en logout: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al cerrar sesión: {str(e)}"
        )
