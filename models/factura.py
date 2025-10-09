from sqlalchemy import Column, String, Float, DateTime
from database import Base
from datetime import datetime
import uuid


class Factura(Base):
    __tablename__ = "facturas"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    cliente_id = Column(String, nullable=False)
    total = Column(Float, nullable=False)
    fecha_emision = Column(DateTime, default=datetime.utcnow)
