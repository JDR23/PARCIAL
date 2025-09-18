import uuid
from sqlalchemy import Column, String, Date
from sqlalchemy.dialects.postgresql import UUID
from database import Base
from pydantic import BaseModel
from datetime import datetime

class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
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
    fecha_nacimiento_cliente: datetime


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    primer_nombre_cliente: str | None = None
    segundo_nombre_cliente: str | None = None
    primer_apellido_cliente: str | None = None
    segundo_apellido_cliente: str | None = None
    fecha_nacimiento_cliente: datetime | None = None


class ClienteResponse(ClienteBase):
    id_cliente: uuid.UUID

    class Config:
        orm_mode = True


class ClienteList(ClienteResponse):
    pass