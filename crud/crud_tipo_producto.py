from sqlalchemy.orm import Session
from models.tipo_producto import TipoProducto
import uuid


def get_tipos_producto(db: Session):
    return db.query(TipoProducto).all()


def get_tipo_producto(db: Session, tipo_id: str):
    return db.query(TipoProducto).filter(TipoProducto.id == tipo_id).first()


def create_tipo_producto(db: Session, tipo_data):
    nuevo_tipo = TipoProducto(
        id=str(uuid.uuid4()), nombre=tipo_data.nombre, descripcion=tipo_data.descripcion
    )
    db.add(nuevo_tipo)
    db.commit()
    db.refresh(nuevo_tipo)
    return nuevo_tipo


def update_tipo_producto(db: Session, tipo_id: str, tipo_data):
    tipo = get_tipo_producto(db, tipo_id)
    if not tipo:
        return None
    for key, value in tipo_data.dict(exclude_unset=True).items():
        setattr(tipo, key, value)
    db.commit()
    db.refresh(tipo)
    return tipo


def delete_tipo_producto(db: Session, tipo_id: str):
    tipo = get_tipo_producto(db, tipo_id)
    if not tipo:
        return None
    db.delete(tipo)
    db.commit()
    return tipo
