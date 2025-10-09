from sqlalchemy import Column, String, Float, Integer, DateTime
from database import Base
from datetime import datetime
import uuid


class Producto(Base):
    __tablename__ = "productos"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    creado_en = Column(DateTime, default=datetime.utcnow)
