from pydantic import BaseModel
from datetime import date


class ClienteBase(BaseModel):
    nombre: str
    apellido: str
    rol: str
    fecha_nacimiento: date


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(ClienteBase):
    pass


class ClienteResponse(ClienteBase):
    id: int

    class Config:
        from_attributes = True
