from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import UsuarioCreate, UsuarioUpdate, UsuarioSchema
from models.usuario import Usuario
import uuid

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


# Crear usuario
@router.post("/", response_model=UsuarioSchema)
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    nuevo_usuario = Usuario(**usuario.dict())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


# Leer usuario por ID
@router.get("/{usuario_id}", response_model=UsuarioSchema)
def read_usuario(usuario_id: uuid.UUID, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


# Actualizar usuario
@router.put("/{usuario_id}", response_model=UsuarioSchema)
def update_usuario(
    usuario_id: uuid.UUID, usuario_update: UsuarioUpdate, db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    for field, value in usuario_update.dict(exclude_unset=True).items():
        setattr(usuario, field, value)

    db.commit()
    db.refresh(usuario)
    return usuario


# Eliminar usuario
@router.delete("/{usuario_id}")
def delete_usuario(usuario_id: uuid.UUID, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()
    return {"ok": True, "message": "Usuario eliminado"}
