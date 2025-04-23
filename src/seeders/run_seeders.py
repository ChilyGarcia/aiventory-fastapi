import asyncio
from src.database import database
from .enterprise_seeder import EnterpriseSeeder
from .role_seeder import RoleSeeder
from .user_seeder import UserSeeder


async def run_all_seeders():
    await database.connect()

    try:

        enterprise_seeder = EnterpriseSeeder()
        role_seeder = RoleSeeder()
        user_seeder = UserSeeder()

        print("Limpiando datos existentes...")
        await user_seeder.clear()
        await role_seeder.clear()
        await enterprise_seeder.clear()

        print("Sembrando datos nuevos...")
        await enterprise_seeder.seed()
        await role_seeder.seed()
        await user_seeder.seed()

        print("Datos sembrados exitosamente!")

    except Exception as e:
        print(f"Error al sembrar datos: {str(e)}")

    finally:
        await database.disconnect()


if __name__ == "__main__":
    asyncio.run(run_all_seeders())
