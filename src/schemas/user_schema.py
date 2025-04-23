from pydantic import BaseModel


class UsuarioIn(BaseModel):
    nombre: str
    email: str
    password: str


class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: str


class UsuarioLogin(BaseModel):
    email: str
    password: str
