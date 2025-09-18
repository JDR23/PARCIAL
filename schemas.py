from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime


# =======================
# Usuario
# =======================
class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        orm_mode = True


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
        orm_mode = True


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
        orm_mode = True


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
        orm_mode = True


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
        orm_mode = True


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
        orm_mode = True
