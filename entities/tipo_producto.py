from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel
import uuid

class TipoProducto(Base):
    __tablename__ = "tipos_producto"

    id_tipo_producto = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre_categoria = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)


class TipoProductoBase(BaseModel):
    nombre_categoria: str
    descripcion: str | None = None


class TipoProductoCreate(TipoProductoBase):
    pass


class TipoProductoUpdate(BaseModel):
    nombre_categoria: str | None = None
    descripcion: str | None = None


class TipoProductoResponse(TipoProductoBase):
    id_tipo_producto: int

    class Config:
        orm_mode = True


class TipoProductoList(TipoProductoResponse):
    pass


class TipoProductoSchema(BaseModel):
    id: uuid.UUID | None = None
    nombre: str
    descripcion: str | None = None

    class Config:
        from_attributes = True