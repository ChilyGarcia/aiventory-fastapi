from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from src.database import metadata

product = Table(
    "products", metadata, Column("id", Integer, primary_key=True),
    Column("name", String(100), unique=True),
    Column("description", String(255)),
    Column("price", Float),
    Column("stock", Integer),
    Column("enterprise_id",
           Integer,
           ForeignKey("enterprises.id"),
           nullable=False))
