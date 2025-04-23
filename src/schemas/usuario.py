from pydantic import BaseModel, Field
from typing import Optional


class UsuarioIn(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: str = Field(
        ..., pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    password: str = Field(..., min_length=6)


class UsuarioOut(BaseModel):
    id: int
    name: str
    email: str


class UsuarioLogin(BaseModel):
    email: str
    password: str
