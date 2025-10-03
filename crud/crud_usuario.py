from sqlalchemy.orm import Session
from models.usuario import Usuario
from schemas import UsuarioCreate, UsuarioUpdate
import uuid
from typing import List, Optional


def crear_usuario(db: Session, usuario: UsuarioCreate) -> Usuario:
    """
    Crea un nuevo usuario en la base de datos.
    """
    # El operador ** desempaca el diccionario del modelo Pydantic
    # en argumentos clave-valor para el constructor de SQLAlchemy.
    nuevo_usuario = Usuario(**usuario.model_dump())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


def obtener_usuarios(db: Session) -> List[Usuario]:
    """
    Obtiene todos los usuarios de la base de datos.
    """
    return db.query(Usuario).all()


def obtener_usuario_por_id(db: Session, usuario_id: uuid.UUID) -> Optional[Usuario]:
    """
    Obtiene un usuario por su ID.
    """
    return db.query(Usuario).filter(Usuario.id == str(usuario_id)).first()


def actualizar_usuario(
    db: Session, usuario_db: Usuario, usuario_in: UsuarioUpdate
) -> Usuario:
    """
    Actualiza un usuario existente en la base de datos.
    """
    update_data = usuario_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(usuario_db, field, value)
    db.commit()
    db.refresh(usuario_db)
    return usuario_db


def eliminar_usuario(db: Session, usuario_id: uuid.UUID) -> Optional[Usuario]:
    usuario = obtener_usuario_por_id(db, usuario_id)
    if usuario:
        db.delete(usuario)
        db.commit()
    return usuario
