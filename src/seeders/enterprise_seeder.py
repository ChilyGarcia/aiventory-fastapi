from src.models.enterprise_model import enterprise
from .base_seeder import BaseSeeder

class EnterpriseSeeder(BaseSeeder):
    async def seed(self) -> None:
        enterprises = [
            {"name": "Empresa Demo 1"},
            {"name": "Empresa Demo 2"},
            {"name": "Empresa Demo 3"}
        ]
        
        for enterprise_data in enterprises:
            query = enterprise.insert().values(**enterprise_data)
            await self.db.execute(query)

    async def clear(self) -> None:
        query = enterprise.delete()
        await self.db.execute(query)
