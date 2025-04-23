from sqlalchemy import Column, ForeignKey, Integer, String, Table
from src.database import metadata

permission = Table("permissions", metadata,
                   Column("id", Integer, primary_key=True),
                   Column("name", String(100), unique=True))

permission_role = Table(
    "permissions_roles", metadata, Column("id", Integer, primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), nullable=False),
    Column("permission_id",
           Integer,
           ForeignKey("permissions.id"),
           nullable=False))
