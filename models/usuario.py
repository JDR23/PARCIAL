import uuid
from sqlalchemy import Column, String, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database import Base
from datetime import datetime
from pydantic import BaseModel
from datetime import date


# Modelo de la tabla en la BD (SQLAlchemy)
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    primer_nombre_usuario = Column(String, nullable=False)
    segundo_nombre_usuario = Column(String, nullable=True)
    primer_apellido_usuario = Column(String, nullable=False)
    segundo_apellido_usuario = Column(String, nullable=True)

    rol_usuario = Column(String, nullable=False)
    fecha_nacimiento_usuario = Column(Date, nullable=False)

    creado_en = Column(DateTime, default=datetime.utcnow)


# ====================
# Pydantic Schemas
# ====================


class UsuarioCreate(BaseModel):
    primer_nombre_usuario: str
    segundo_nombre_usuario: str | None = None
    primer_apellido_usuario: str
    segundo_apellido_usuario: str | None = None
    rol_usuario: str
    fecha_nacimiento_usuario: date


class UsuarioUpdate(BaseModel):
    primer_nombre_usuario: str | None = None
    segundo_nombre_usuario: str | None = None
    primer_apellido_usuario: str | None = None
    segundo_apellido_usuario: str | None = None
    rol_usuario: str | None = None
    fecha_nacimiento_usuario: date | None = None


class UsuarioSchema(BaseModel):
    id: uuid.UUID
    primer_nombre_usuario: str
    segundo_nombre_usuario: str | None
    primer_apellido_usuario: str
    segundo_apellido_usuario: str | None
    rol_usuario: str
    fecha_nacimiento_usuario: date
    creado_en: datetime

    class Config:
        from_attributes = True
