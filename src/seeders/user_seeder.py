from src.models.user_model import usuarios
from src.models.rol_model import rol
from src.models.enterprise_model import enterprise
from .base_seeder import BaseSeeder
from src.auth.hashing import hash_password


class UserSeeder(BaseSeeder):

    async def seed(self) -> None:

        admin_role = await self.db.fetch_one(query=rol.select().where(
            rol.c.name == "admin"))
        user_role = await self.db.fetch_one(query=rol.select().where(
            rol.c.name == "user"))

        enterprise_1 = await self.db.fetch_one(query=enterprise.select().where(
            enterprise.c.name == "Empresa Demo 1"))

        users = [{
            "nombre": "Admin User",
            "email": "admin@example.com",
            "hashed_password": hash_password("admin123"),
            "role_id": admin_role["id"],
            "enterprise_id": enterprise_1["id"]
        }, {
            "nombre": "Normal User",
            "email": "user@example.com",
            "hashed_password": hash_password("user123"),
            "role_id": user_role["id"],
            "enterprise_id": enterprise_1["id"]
        }]

        for user_data in users:
            query = usuarios.insert().values(**user_data)
            await self.db.execute(query)

    async def clear(self) -> None:
        query = usuarios.delete()
        await self.db.execute(query)
