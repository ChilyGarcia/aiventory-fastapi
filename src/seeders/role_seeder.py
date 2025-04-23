from src.models.rol_model import rol
from .base_seeder import BaseSeeder

class RoleSeeder(BaseSeeder):
    async def seed(self) -> None:
        roles = [
            {"name": "admin"},
            {"name": "user"},
            {"name": "viewer"}
        ]
        
        for role_data in roles:
            query = rol.insert().values(**role_data)
            await self.db.execute(query)

    async def clear(self) -> None:
        query = rol.delete()
        await self.db.execute(query)
