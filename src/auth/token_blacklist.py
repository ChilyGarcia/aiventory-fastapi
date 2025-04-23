from datetime import datetime, timezone
from typing import Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

blacklisted_tokens: Dict[str, datetime] = {}


def add_to_blacklist(token: str, expiry: datetime) -> None:
    """Añade un token a la lista negra"""
    logger.info(f"Añadiendo token a la blacklist. Expira en: {expiry}")
    blacklisted_tokens[token] = expiry
    logger.info(f"Tokens en blacklist: {len(blacklisted_tokens)}")


def is_blacklisted(token: str) -> bool:
    # Limpiar tokens expirados
    current_time = datetime.now(timezone.utc)
    logger.info(f"Verificando token. Hora actual: {current_time}")
    logger.info(
        f"Tokens en blacklist antes de limpiar: {len(blacklisted_tokens)}")

    expired_tokens = [
        t for t, expiry in blacklisted_tokens.items() if expiry < current_time
    ]

    for t in expired_tokens:
        logger.info(
            f"Eliminando token expirado que expira en: {blacklisted_tokens[t]}"
        )
        blacklisted_tokens.pop(t, None)

    logger.info(
        f"Tokens en blacklist después de limpiar: {len(blacklisted_tokens)}")
    is_token_blacklisted = token in blacklisted_tokens
    logger.info(f"¿Token está en blacklist?: {is_token_blacklisted}")

    if is_token_blacklisted:
        expiry = blacklisted_tokens[token]
        logger.info(f"Token encontrado en blacklist. Expira en: {expiry}")

    return is_token_blacklisted
