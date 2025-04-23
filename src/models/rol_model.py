from sqlalchemy import Column, Integer, String, Table
from src.database import metadata

rol = Table("roles", metadata, Column("id", Integer, primary_key=True),
            Column("name", String(100), unique=True))
