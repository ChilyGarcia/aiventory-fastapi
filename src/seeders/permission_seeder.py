from src.models.permission_role_model import permission, permission_role
from .base_seeder import BaseSeeder


class PermissionSeeder(BaseSeeder):

    async def seed(self) -> None:
        permissions = [
            {
                "name": "create_product"
            },
            {
                "name": "read_product"
            },
            {
                "name": "update_product"
            },
            {
                "name": "delete_product"
            },
        ]

        for permission_data in permissions:
            query = permission.insert().values(**permission_data)
            await self.db.execute(query)

        roles_query = "SELECT id, name FROM roles"
        roles = await self.db.fetch_all(roles_query)
        roles_dict = {role["name"]: role["id"] for role in roles}

        permissions_query = "SELECT id, name FROM permissions"
        permissions = await self.db.fetch_all(permissions_query)
        permissions_dict = {perm["name"]: perm["id"] for perm in permissions}

        role_permissions = {
            "admin": [
                "create_product", "read_product", "update_product",
                "delete_product"
            ],
            "user": ["create_product", "read_product", "update_product"],
            "viewer": ["read_product"]
        }

        for role_name, perm_names in role_permissions.items():
            role_id = roles_dict.get(role_name)
            if role_id:
                for perm_name in perm_names:
                    perm_id = permissions_dict.get(perm_name)
                    if perm_id:
                        query = permission_role.insert().values(
                            role_id=role_id, permission_id=perm_id)
                        await self.db.execute(query)

    async def clear(self) -> None:
        await self.db.execute(permission_role.delete())
        await self.db.execute(permission.delete())
