from pydantic import BaseModel


class UsuarioIn(BaseModel):
    nombre: str
    email: str


class Usuario(UsuarioIn):
    id: int
