from sqlalchemy import Column, String, DateTime
from database import Base
from datetime import datetime
import uuid


class TipoProducto(Base):
    __tablename__ = "tipos_producto"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    creado_en = Column(DateTime, default=datetime.utcnow)
