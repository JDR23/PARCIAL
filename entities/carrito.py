from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base
from pydantic import BaseModel
from datetime import datetime

class Carrito(Base):
    __tablename__ = "carritos"

    id_carrito = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    id_cliente_creacion = Column(String, nullable=True)
    id_cliente_edicion = Column(Integer, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())



class CarritoBase(BaseModel):
    id_producto: int
    id_cliente: str


class CarritoCreate(CarritoBase):
    id_cliente_creacion: str | None = None


class CarritoUpdate(BaseModel):
    id_producto: int | None = None
    id_cliente: str | None = None
    id_cliente_edicion: str | None = None


class CarritoResponse(CarritoBase):
    id_carrito: int
    fecha_creacion: datetime

    class Config:
        orm_mode = True


class CarritoList(CarritoResponse):
    pass