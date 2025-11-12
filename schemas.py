from pydantic import BaseModel
from datetime import date


from pydantic import BaseModel, EmailStr
import uuid

class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    contrasena: str
    rol: str

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(UsuarioBase):
    pass

class UsuarioSchema(UsuarioBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


# schemas.py
from pydantic import BaseModel, EmailStr
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

class UsuarioUpdate(UsuarioBase):
    pass

class UsuarioSchema(UsuarioBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
