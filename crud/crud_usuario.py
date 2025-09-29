from sqlalchemy.orm import Session
from models.usuario import Usuario
from datetime import date
import uuid


def crear_usuario(
    db: Session,
    primer_nombre: str,
    primer_apellido: str,
    rol: str,
    fecha_nacimiento: date,
    segundo_nombre: str = None,
    segundo_apellido: str = None,
):
    nuevo_usuario = Usuario(
        primer_nombre_usuario=primer_nombre,
        segundo_nombre_usuario=segundo_nombre,
        primer_apellido_usuario=primer_apellido,
        segundo_apellido_usuario=segundo_apellido,
        rol_usuario=rol,
        fecha_nacimiento_usuario=fecha_nacimiento,
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


def obtener_usuarios(db: Session):
    return db.query(Usuario).all()


def obtener_usuario_por_id(db: Session, usuario_id: uuid.UUID):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()


def actualizar_usuario(db: Session, usuario_id: uuid.UUID, **kwargs):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario:
        for key, value in kwargs.items():
            if hasattr(usuario, key) and value is not None:
                setattr(usuario, key, value)
        db.commit()
        db.refresh(usuario)
    return usuario


def eliminar_usuario(db: Session, usuario_id: uuid.UUID):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario:
        db.delete(usuario)
        db.commit()
    return usuario
