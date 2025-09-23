from sqlalchemy.orm import Session
from models.usuario import Usuario
from schemas import UsuarioCreate, UsuarioUpdate
from models import Usuario


# Crear usuario
def crear_usuario(db: Session, usuario: UsuarioCreate):
    nuevo_usuario = Usuario(
        primer_nombre_usuario=usuario.primer_nombre_usuario,
        segundo_nombre_usuario=usuario.segundo_nombre_usuario,
        primer_apellido_usuario=usuario.primer_apellido_usuario,
        segundo_apellido_usuario=usuario.segundo_apellido_usuario,
        rol_usuario=usuario.rol_usuario,
        fecha_nacimiento_usuario=usuario.fecha_nacimiento_usuario,
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


# Listar usuarios
def obtener_usuarios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Usuario).offset(skip).limit(limit).all()


# Obtener usuario por ID
def obtener_usuario_por_id(db: Session, usuario_id: str):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()


# Actualizar usuario
def actualizar_usuario(db: Session, usuario_id: str, usuario: UsuarioUpdate):
    db_usuario = obtener_usuario_por_id(db, usuario_id)
    if not db_usuario:
        return None

    update_data = usuario.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_usuario, key, value)

    db.commit()
    db.refresh(db_usuario)
    return db_usuario


# Eliminar usuario
def eliminar_usuario(db: Session, usuario_id: str):
    db_usuario = obtener_usuario_por_id(db, usuario_id)
    if not db_usuario:
        return None

    db.delete(db_usuario)
    db.commit()
    return db_usuario
