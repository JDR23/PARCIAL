import uuid
from sqlalchemy import Column, String, Date
from database import Base
from pydantic import BaseModel
from datetime import date


class Cliente(Base):
    __tablename__ = "clientes"

    # Store UUIDs as strings for SQLite compatibility
    id_cliente = Column(String, primary_key=True,
                        default=lambda: str(uuid.uuid4()), index=True)
    primer_nombre_cliente = Column(String, nullable=False)
    segundo_nombre_cliente = Column(String, nullable=True)
    primer_apellido_cliente = Column(String, nullable=False)
    segundo_apellido_cliente = Column(String, nullable=True)
    fecha_nacimiento_cliente = Column(Date, nullable=False)


class ClienteBase(BaseModel):
    primer_nombre_cliente: str
    segundo_nombre_cliente: str | None = None
    primer_apellido_cliente: str
    segundo_apellido_cliente: str | None = None
    # Use date (no time) for birth date
    fecha_nacimiento_cliente: date


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    primer_nombre_cliente: str | None = None
    segundo_nombre_cliente: str | None = None
    primer_apellido_cliente: str | None = None
    segundo_apellido_cliente: str | None = None
    fecha_nacimiento_cliente: date | None = None


class ClienteResponse(ClienteBase):
    id_cliente: str

    class Config:
        orm_mode = True


class ClienteList(ClienteResponse):
    pass
