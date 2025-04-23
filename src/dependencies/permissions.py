from fastapi import Depends, HTTPException, status
from src.database import database
from src.models.permission_role_model import permission_role
from src.models.rol_model import rol
from src.dependencies.auth import get_usuario_actual


async def check_permission(user: dict, required_permission: str):
    """
    Verifica si un usuario tiene un permiso específico basado en su rol.
    """
    try:
        enterprise_id = getattr(user, "enterprise_id", None)
        if not enterprise_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El usuario no pertenece a ninguna empresa")

        query = """
            SELECT p.name 
            FROM permissions p 
            JOIN permissions_roles pr ON p.id = pr.permission_id 
            WHERE pr.role_id = :role_id
        """
        permissions = await database.fetch_all(
            query=query, values={"role_id": user.role_id})

        if not permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El usuario no tiene permisos asignados")

        user_permissions = [p["name"] for p in permissions]
        if required_permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=
                f"No tienes permiso para realizar esta acción ({required_permission})"
            )

        return True
    except AttributeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al verificar permisos del usuario") from e


def require_permission(permission: str):
    """
    Decorador para verificar permisos en las rutas.
    """

    async def permission_dependency(current_user=Depends(get_usuario_actual)):
        await check_permission(current_user, permission)
        return current_user

    return permission_dependency
