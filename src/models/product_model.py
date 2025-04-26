from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from src.database import metadata

product = Table(
    "products", metadata, Column("id", Integer, primary_key=True),
    Column("name", String(100), unique=True),
    Column("description", String(255)),
    Column("price", Float),
    Column("previous_price", Float),
    Column("discount_percentage", Float),
    Column("month", String),
    Column("initial_stock", Integer),
    Column("remaining_stock", Integer),
    Column("enterprise_id",
           Integer,
           ForeignKey("enterprises.id"),
           nullable=False))
