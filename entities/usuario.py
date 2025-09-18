import uuid
from sqlalchemy import Column, String, Datetime
from sqlalchemy.dialects.postgresql import UUID
from database import Base
from pydantic import BaseModel
from datetime import datetime

class Usuario(Base):

    """
    Modelo de usuarios que representa la tabla 'usuario'
    
    Atributos:
        id: Identificador único de la categoría
        primer_nombre_usuario: Nombre del usuario
        segundo_nombre_usuario: Segundo nombre del usuario (opcional)
        primer_apellido_usuario: Primer apellido del usuario
        segundo_apellido_usuario: Segundo apellido del usuario (opcional)
        rol_usuario: Rol del usuario
        fecha_nacimiento_usuario: Fecha de nacimiento del usuario
    """
    __tablename__ = "usuarios"

    id_usuario = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    primer_nombre_usuario = Column(String, nullable=False)
    segundo_nombre_usuario = Column(String, nullable=True)
    primer_apellido_usuario = Column(String, nullable=False)
    segundo_apellido_usuario = Column(String, nullable=True)
    rol_usuario = Column(String, nullable=False)
    fecha_nacimiento_usuario = Column(Datetime, nullable=False)



# Esquema base
class UsuarioBase(BaseModel):
    primer_nombre_usuario: str
    segundo_nombre_usuario: str | None = None
    primer_apellido_usuario: str
    segundo_apellido_usuario: str | None = None
    rol_usuario: str
    fecha_nacimiento_usuario: datetime


# Esquema para crear usuario
class UsuarioCreate(UsuarioBase):
    pass


# Esquema para actualizar usuario (todos los campos opcionales)
class UsuarioUpdate(BaseModel):
    primer_nombre_usuario: str | None = None
    segundo_nombre_usuario: str | None = None
    primer_apellido_usuario: str | None = None
    segundo_apellido_usuario: str | None = None
    rol_usuario: str | None = None
    fecha_nacimiento_usuario: datetime | None = None


# Esquema de respuesta (detalle de un usuario)
class UsuarioResponse(UsuarioBase):
    id_usuario: uuid.UUID

    class Config:
        orm_mode = True


# Esquema para lista de usuarios
class UsuarioList(UsuarioResponse):
    pass
