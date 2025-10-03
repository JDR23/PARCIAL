from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import uuid


class Factura(Base):
    __tablename__ = "facturas"

    id_factura = Column(Integer, primary_key=True, autoincrement=True, index=True)
    # El UUID del cliente al que pertenece la factura
    id_cliente = Column(
        String, ForeignKey("usuarios.id_usuario"), nullable=False, index=True
    )
    total = Column(Float, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    cliente = relationship("Usuario")
    detalles = relationship("DetalleFactura", back_populates="factura")


class DetalleFactura(Base):
    __tablename__ = "detalles_factura"

    id_detalle = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_factura = Column(
        Integer, ForeignKey("facturas.id_factura"), nullable=False, index=True
    )
    id_producto = Column(
        Integer, ForeignKey("productos.id_producto"), nullable=False, index=True
    )
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(
        Float, nullable=False
    )  # Precio al momento de la compra

    # Relaciones
    factura = relationship("Factura", back_populates="detalles")
    producto = relationship("Producto")


# --- Esquemas Pydantic ---


class DetalleFacturaBase(BaseModel):
    id_producto: int
    cantidad: int
    precio_unitario: float


class DetalleFacturaCreate(DetalleFacturaBase):
    pass


class DetalleFacturaResponse(DetalleFacturaBase):
    id_detalle: int

    class Config:
        from_attributes = True


class FacturaBase(BaseModel):
    id_cliente: uuid.UUID
    total: float


class FacturaCreate(FacturaBase):
    detalles: List[DetalleFacturaCreate]


class FacturaResponse(FacturaBase):
    id_factura: int
    fecha_creacion: datetime
    detalles: List[DetalleFacturaResponse] = []

    class Config:
        from_attributes = True