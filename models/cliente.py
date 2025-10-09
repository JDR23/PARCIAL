from sqlalchemy import Column, String, DateTime
from database import Base
from datetime import datetime
import uuid


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, nullable=False)
    telefono = Column(String, nullable=True)
    direccion = Column(String, nullable=True)
    creado_en = Column(DateTime, default=datetime.utcnow)
