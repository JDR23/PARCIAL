from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import relationship
from typing import Optional
import uuid

class Producto(Base):
    __tablename__ = "productos"

    id_producto = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_tipo_producto = Column(Integer, ForeignKey("tipos_producto.id_tipo_producto"), nullable=False)
    nombre_producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    cantidad = Column(Integer, nullable=False)
    id_usuario_creacion = Column(String, nullable=False)
    id_usuario_edicion = Column(String, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())


class ProductoBase(BaseModel):
    id_tipo_producto: int
    nombre_producto: str
    precio: float
    cantidad: int


class ProductoCreate(ProductoBase):
    id_usuario_creacion: str


class ProductoUpdate(BaseModel):
    nombre_producto: str | None = None
    precio: float | None = None
    cantidad: int | None = None
    id_usuario_edicion: str | None = None


class ProductoResponse(ProductoBase):
    id_producto: int
    fecha_creacion: datetime
    fecha_edicion: datetime | None = None

    class Config:
        orm_mode = True


class ProductoList(ProductoResponse):
    pass


class ProductoSchema(BaseModel):
    id: uuid.UUID | None = None
    nombre: str
    precio: float
    stock: int
    creado_en: datetime | None = None

    class Config:
        from_attributes = True