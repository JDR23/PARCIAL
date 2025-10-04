import uuid
from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


# =======================
# Usuario
# =======================
class UsuarioBase(BaseModel):
    primer_nombre_usuario: str
    segundo_nombre_usuario: Optional[str] = None
    primer_apellido_usuario: str
    segundo_apellido_usuario: Optional[str] = None
    rol_usuario: str
    fecha_nacimiento_usuario: datetime


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioUpdate(BaseModel):
    primer_nombre_usuario: Optional[str] = None
    segundo_nombre_usuario: Optional[str] = None
    primer_apellido_usuario: Optional[str] = None
    segundo_apellido_usuario: Optional[str] = None
    rol_usuario: Optional[str] = None
    fecha_nacimiento_usuario: Optional[datetime] = None


class UsuarioResponse(UsuarioBase):
    id_usuario: uuid.UUID

    class Config:
        from_attributes = True


class UsuarioList(UsuarioResponse):
    pass


# =======================
# Cliente
# =======================
class ClienteBase(BaseModel):
    nombre: str
    direccion: str
    telefono: str


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None


class ClienteResponse(ClienteBase):
    id: int

    class Config:
        from_attributes = True


# =======================
# Tipo de Producto
# =======================
class TipoProductoBase(BaseModel):
    nombre_categoria: str
    descripcion: Optional[str] = None


class TipoProductoCreate(TipoProductoBase):
    pass


class TipoProductoUpdate(BaseModel):
    nombre_categoria: Optional[str] = None
    descripcion: Optional[str] = None


class TipoProductoResponse(TipoProductoBase):
    id_tipo_producto: int

    class Config:
        from_attributes = True  # Cambiado de orm_mode a from_attributes


# =======================
# Producto
# =======================
class ProductoBase(BaseModel):
    nombre: str
    precio: float
    stock: int
    categoria_id: int  # referencia a tipo_producto


class ProductoCreate(ProductoBase):
    warranty_months: Optional[int] = None
    size: Optional[str] = None
    gender: Optional[str] = None
    expiration_date: Optional[date] = None


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None
    categoria_id: Optional[int] = None
    warranty_months: Optional[int] = None
    size: Optional[str] = None
    gender: Optional[str] = None
    expiration_date: Optional[date] = None


class ProductoResponse(ProductoBase):
    id: int
    warranty_months: Optional[int]
    size: Optional[str]
    gender: Optional[str]
    expiration_date: Optional[date]

    class Config:
        from_attributes = True


# =======================
# Carrito
# =======================
class CarritoBase(BaseModel):
    cliente_id: int
    producto_id: int
    cantidad: int


class CarritoCreate(CarritoBase):
    pass


class CarritoResponse(CarritoBase):
    id: int

    class Config:
        from_attributes = True


# =======================
# Factura
# =======================
class FacturaBase(BaseModel):
    cliente_id: int
    fecha: datetime


class FacturaCreate(FacturaBase):
    pass


class FacturaResponse(FacturaBase):
    id: int
    total: float

    class Config:
        from_attributes = True
