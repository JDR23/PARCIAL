import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database import Base  # Este es tu SQLAlchemy Base (de database.py)
from pydantic import BaseModel  # Este es de Pydantic, para validaciones
from datetime import datetime


class UsuarioSchema(BaseModel):
    id: uuid.UUID | None = None
    nombre: str
    correo: str
    creado_en: datetime | None = None

    class Config:
        from_attributes = True


# Modelo de SQLAlchemy (tabla en la BD)
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, index=True, nullable=False)
    creado_en = Column(DateTime, default=datetime.utcnow)


class UsuarioSchema(BaseModel):
    id: uuid.UUID | None = None
    nombre: str
    correo: str
    creado_en: datetime | None = None

    class Config:
        from_attributes = True



