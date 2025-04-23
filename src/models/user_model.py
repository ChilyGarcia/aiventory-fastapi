from sqlalchemy import Table, Column, Integer, String
from database import metadata

usuarios = Table(
    "usuarios",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("nombre", String(100)),
    Column("email", String(100)),
)
