from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid


# ==========================
# USUARIO SCHEMAS
# ==========================
class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    contrasena: str
    rol: str


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[EmailStr] = None
    contrasena: Optional[str] = None
    rol: Optional[str] = None


class UsuarioSchema(UsuarioBase):
    id: str

    class Config:
        from_attributes = True


# ==========================
# CLIENTE SCHEMAS
# ==========================
class ClienteBase(BaseModel):
    nombre: str
    correo: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None


class ClienteResponse(ClienteBase):
    id: str
    creado_en: datetime

    class Config:
        from_attributes = True


# ==========================
# TIPO PRODUCTO SCHEMAS
# ==========================
class TipoProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class TipoProductoCreate(TipoProductoBase):
    pass


class TipoProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None


class TipoProductoResponse(TipoProductoBase):
    id: str
    creado_en: datetime

    class Config:
        from_attributes = True


# ==========================
# PRODUCTO SCHEMAS
# ==========================
class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock: int = 0


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None


class ProductoResponse(ProductoBase):
    id: str
    creado_en: datetime

    class Config:
        from_attributes = True


# ==========================
# CARRITO SCHEMAS
# ==========================
class CarritoBase(BaseModel):
    usuario_id: str
    producto_id: str
    cantidad: int


class CarritoCreate(CarritoBase):
    pass


class CarritoUpdate(BaseModel):
    usuario_id: Optional[str] = None
    producto_id: Optional[str] = None
    cantidad: Optional[int] = None


class CarritoResponse(CarritoBase):
    id: str
    creado_en: datetime

    class Config:
        from_attributes = True


# ==========================
# FACTURA SCHEMAS
# ==========================
class FacturaBase(BaseModel):
    cliente_id: str
    total: float


class FacturaCreate(FacturaBase):
    pass


class FacturaUpdate(BaseModel):
    cliente_id: Optional[str] = None
    total: Optional[float] = None


class FacturaResponse(FacturaBase):
    id: str
    fecha_emision: datetime

    class Config:
        from_attributes = True
