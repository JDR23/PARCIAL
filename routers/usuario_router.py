from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.config import get_db
from schemas import UsuarioCreate, UsuarioUpdate, UsuarioSchema
from models.usuario import Usuario
from auth.jwt_handler import get_current_active_user
from pydantic import BaseModel
import uuid

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


# Listar todos los usuarios (requiere autenticación)
@router.get("/", response_model=list[UsuarioSchema])
def listar_usuarios(
    nombre: str = None, 
    correo: str = None, 
    rol: str = None, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Lista todos los usuarios. Opcionalmente filtra por nombre, correo o rol.
    """
    from sqlalchemy import func
    query = db.query(Usuario)
    if nombre:
        query = query.filter(func.lower(Usuario.nombre).contains(func.lower(nombre)))
    if correo:
        query = query.filter(func.lower(Usuario.correo).contains(func.lower(correo)))
    if rol:
        query = query.filter(Usuario.rol == rol)
    usuarios = query.all()
    return usuarios


# Crear usuario (público - para registro inicial)
@router.post("/", response_model=UsuarioSchema)
def create_usuario(
    usuario: UsuarioCreate, 
    db: Session = Depends(get_db)
):
    nuevo_usuario = Usuario(
        id=str(uuid.uuid4()),
        nombre=usuario.nombre,
        correo=usuario.correo,
        contrasena=usuario.contrasena,
        rol=usuario.rol
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario



# Leer usuario por ID (requiere autenticación)
@router.get("/{usuario_id}", response_model=UsuarioSchema)
def read_usuario(
    usuario_id: str, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


# Actualizar usuario (requiere autenticación)
@router.put("/{usuario_id}", response_model=UsuarioSchema)
def update_usuario(
    usuario_id: str, 
    usuario_update: UsuarioUpdate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    for field, value in usuario_update.dict(exclude_unset=True).items():
        setattr(usuario, field, value)

    db.commit()
    db.refresh(usuario)
    return usuario


# Eliminar usuario (requiere autenticación)
@router.delete("/{usuario_id}")
def delete_usuario(
    usuario_id: str, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()
    return {"ok": True, "message": "Usuario eliminado"}


# Login con JWT
from datetime import timedelta
from auth.jwt_handler import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

class LoginRequest(BaseModel):
    correo: str
    contrasena: str

@router.post("/login")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Autenticación con JWT. Retorna un token de acceso.
    """
    usuario = db.query(Usuario).filter(
        Usuario.correo == login_data.correo,
        Usuario.contrasena == login_data.contrasena
    ).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    # Crear token JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": usuario.id, "rol": usuario.rol},
        expires_delta=access_token_expires
    )
    
    return {
        "ok": True,
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "correo": usuario.correo,
            "rol": usuario.rol
        },
        "message": "Login exitoso"
    }


