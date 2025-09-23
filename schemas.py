import uuid
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from datetime import date


# =======================
# Usuario
# =======================
class UsuarioBase(BaseModel):
    primer_nombre_usuario: str
    segundo_nombre_usuario: str | None = None
    primer_apellido_usuario: str
    segundo_apellido_usuario: str | None = None
    rol_usuario: str
    fecha_nacimiento_usuario: datetime

    class Config:
        from_attributes = True  # Necesario en Pydantic v2


class UsuarioCreate(UsuarioBase):
    pass

    class Config:
        from_attributes = True


class UsuarioUpdate(BaseModel):
    primer_nombre_usuario: str | None = None
    segundo_nombre_usuario: str | None = None
    primer_apellido_usuario: str | None = None
    segundo_apellido_usuario: str | None = None
    rol_usuario: str | None = None
    fecha_nacimiento_usuario: datetime | None = None

    class Config:
        from_attributes = True


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


class ClienteResponse(ClienteBase):
    id: int

    class Config:
        from_attributes = True


# =======================
# Tipo de Producto
# =======================
class TipoProductoBase(BaseModel):
    nombre: str


class TipoProductoCreate(TipoProductoBase):
    pass


class TipoProductoResponse(TipoProductoBase):
    id: int

    class Config:
        from_attributes = True


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
