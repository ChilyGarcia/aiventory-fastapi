import asyncio
from src.database import database
from .enterprise_seeder import EnterpriseSeeder
from .role_seeder import RoleSeeder
from .permission_seeder import PermissionSeeder
from .user_seeder import UserSeeder


async def run_all_seeders():
    await database.connect()

    try:

        seeders = [
            RoleSeeder(database),
            PermissionSeeder(database),
            EnterpriseSeeder(database),
            UserSeeder(database)
        ]

        print("Limpiando datos existentes...")
        for seeder in seeders:
            await seeder.clear()

        print("Sembrando datos nuevos...")
        for seeder in seeders:
            await seeder.seed()

        print("Datos sembrados exitosamente!")

    except Exception as e:
        print(f"Error al sembrar datos: {str(e)}")

    finally:
        await database.disconnect()


if __name__ == "__main__":
    asyncio.run(run_all_seeders())
