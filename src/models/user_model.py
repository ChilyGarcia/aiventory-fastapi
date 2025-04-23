from sqlalchemy import Table, Column, Integer, String
from src.database import metadata

usuarios = Table("usuarios", metadata, Column("id", Integer, primary_key=True),
                 Column("nombre", String(100)),
                 Column("email", String(100), unique=True),
                 Column("hashed_password", String(200)))
