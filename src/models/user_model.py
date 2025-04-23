from sqlalchemy import ForeignKey, Table, Column, Integer, String
from src.database import metadata

usuarios = Table(
    "usuarios", metadata, Column("id", Integer, primary_key=True),
    Column("name", String(100)), Column("email", String(100), unique=True),
    Column("hashed_password", String(200)),
    Column("role_id", Integer, ForeignKey("roles.id"), nullable=False),
    Column("enterprise_id",
           Integer,
           ForeignKey("enterprises.id"),
           nullable=True))
