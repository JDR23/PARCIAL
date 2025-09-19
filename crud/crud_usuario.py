from sqlalchemy.orm import Session
from entidades.usuario import Usuario
from schemas import UsuarioCreate, UsuarioUpdate
import uuid

# Crear usuario
def create_usuario(db: Session, usuario: UsuarioCreate):
    db_usuario = Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# Obtener todos los usuarios
def get_usuarios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Usuario).offset(skip).limit(limit).all()

# Obtener un usuario por ID
def get_usuario_by_id(db: Session, usuario_id: uuid.UUID):
    return db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()

# Actualizar usuario
def update_usuario(db: Session, usuario_id: uuid.UUID, usuario: UsuarioUpdate):
    db_usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if not db_usuario:
        return None

    for key, value in usuario.dict(exclude_unset=True).items():
        setattr(db_usuario, key, value)

    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# Eliminar usuario
def delete_usuario(db: Session, usuario_id: uuid.UUID):
    db_usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if not db_usuario:
        return None
    db.delete(db_usuario)
    db.commit()
    return db_usuario
