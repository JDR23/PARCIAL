import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database import BaseModel
from datetime import datetime

class Usuario(BaseModel):
    """
    Modelo de usuarios que representa la tabla 'usuarios'
    """
    __tablename__ = "usuarios"

    id_usuario = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    primer_nombre_usuario = Column(String, nullable=False)
    segundo_nombre_usuario = Column(String, nullable=True)
    primer_apellido_usuario = Column(String, nullable=False)
    segundo_apellido_usuario = Column(String, nullable=True)
    rol_usuario = Column(String, nullable=False)
    fecha_nacimiento_usuario = Column(DateTime, nullable=False, default=datetime.utcnow)
