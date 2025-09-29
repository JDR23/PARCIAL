import uuid
from sqlalchemy import Column, String, Date, DateTime
from sqlalchemy.dialects.sqlite import BLOB
from database import Base
from datetime import datetime


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)

    primer_nombre_usuario = Column(String, nullable=False)
    segundo_nombre_usuario = Column(String, nullable=True)
    primer_apellido_usuario = Column(String, nullable=False)
    segundo_apellido_usuario = Column(String, nullable=True)

    rol_usuario = Column(String, nullable=False)
    fecha_nacimiento_usuario = Column(Date, nullable=False)

    creado_en = Column(DateTime, default=datetime.utcnow)
