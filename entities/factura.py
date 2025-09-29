from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base
from pydantic import BaseModel
from datetime import datetime

class Factura(Base):
    __tablename__ = "facturas"

    id_factura = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_carrito = Column(Integer, ForeignKey("carritos.id_carrito"), nullable=False)
    nombre_producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    cantidad = Column(Integer, nullable=False)
    id_cliente_creacion = Column(String, nullable=False)
    id_cliente_edicion = Column(String, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())


class FacturaBase(BaseModel):
    id_carrito: int
    nombre_producto: str
    precio: float
    cantidad: int


class FacturaCreate(FacturaBase):
    id_cliente_creacion: str


class FacturaUpdate(BaseModel):
    id_cliente_edicion: str | None = None


class FacturaResponse(FacturaBase):
    id_factura: int
    fecha_creacion: datetime
    fecha_edicion: datetime | None = None

    class Config:
        orm_mode = True


class FacturaList(FacturaResponse):
    pass