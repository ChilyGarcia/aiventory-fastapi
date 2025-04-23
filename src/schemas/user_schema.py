from pydantic import BaseModel


class UsuarioIn(BaseModel):
    name: str
    email: str
    password: str


class UsuarioOut(BaseModel):
    id: int
    name: str
    email: str


class UsuarioLogin(BaseModel):
    email: str
    password: str
