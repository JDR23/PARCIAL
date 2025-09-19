from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import uuid
from crud import crud_usuario
from schemas import UsuarioCreate, UsuarioUpdate, UsuarioResponse

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"],
)

# Crear usuario
@router.post("/", response_model=UsuarioResponse)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return crud_usuario.create_usuario(db, usuario)

# Listar usuarios
@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud_usuario.get_usuarios(db, skip=skip, limit=limit)

# Obtener usuario por ID
@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: uuid.UUID, db: Session = Depends(get_db)):
    db_usuario = crud_usuario.get_usuario_by_id(db, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

# Actualizar usuario
@router.put("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(usuario_id: uuid.UUID, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    db_usuario = crud_usuario.update_usuario(db, usuario_id, usuario)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

# Eliminar usuario
@router.delete("/{usuario_id}", response_model=UsuarioResponse)
def eliminar_usuario(usuario_id: uuid.UUID, db: Session = Depends(get_db)):
    db_usuario = crud_usuario.delete_usuario(db, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario
