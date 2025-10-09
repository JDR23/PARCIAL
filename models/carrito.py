from sqlalchemy import Column, String, Integer, DateTime
from database import Base
from datetime import datetime
import uuid


class Carrito(Base):
    __tablename__ = "carritos"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    usuario_id = Column(String, nullable=False)
    producto_id = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    creado_en = Column(DateTime, default=datetime.utcnow)
